import asyncio
import json
import os
from typing import Dict, Type, Any
from datetime import datetime

from aiokafka import AIOKafkaConsumer
from consumer_utils.logger import setup_logger
from consumer_utils.retry_handler import async_retry
from core.config import Settings
from core.constants import (
    KAFKA_TOPIC_SALES_EVENTS,
    OBJECT_TYPE_OPPORTUNITY,
    OBJECT_TYPE_PROJECT,
    DB_AUTO_OFFSET_RESET,
    MAX_RETRIES,
    RETRY_DELAY,
    ERROR_START_CONSUMER,
    ERROR_STOP_CONSUMER,
    ERROR_PROCESS_MESSAGE,
    ERROR_DECODE_MESSAGE,
    ERROR_CONSUME_LOOP,
    ERROR_FATAL,
    ERROR_UNKNOWN_OBJECT,
    ERROR_MISSING_OBJECT_TYPE,
    SUCCESS_START_CONSUMER,
    SUCCESS_STOP_CONSUMER,
    SUCCESS_PROCESS_MESSAGE,
    SUCCESS_CANCEL_TASK,
    UNIDENTIFIED_MESSAGES_FILE
)
from database import SessionLocal
from consumer_entities.opportunity_model import Opportunity
from consumer_entities.project_model import Project
from consumer_repository.opportunity_repository import OpportunityRepository
from consumer_repository.project_repository import ProjectRepository

logger = setup_logger(__name__)

class KafkaConsumerService:
    """Kafka consumer service for processing enterprise objects"""
    
    def __init__(self):
        self.settings = Settings()
        self.consumer: AIOKafkaConsumer = None
        self.is_running = False
        self.consume_task = None
        self.object_processors: Dict[str, Type] = {
            OBJECT_TYPE_OPPORTUNITY: Opportunity,
            OBJECT_TYPE_PROJECT: Project
        }
        self.repositories = {
            OBJECT_TYPE_OPPORTUNITY: OpportunityRepository,
            OBJECT_TYPE_PROJECT: ProjectRepository
        }
        # Ensure logs directory exists
        os.makedirs(os.path.dirname(UNIDENTIFIED_MESSAGES_FILE), exist_ok=True)
        logger.info("KafkaConsumerService initialized")

    async def start(self):
        """Start the Kafka consumer"""
        try:
            # For development, use only sales_events topic
            topics = [KAFKA_TOPIC_SALES_EVENTS]
            logger.info(f"Starting Kafka consumer with topics: {topics}")
            self.consumer = AIOKafkaConsumer(
                *topics,
                bootstrap_servers=self.settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id=self.settings.KAFKA_GROUP_ID,
                auto_offset_reset=DB_AUTO_OFFSET_RESET,
                value_deserializer=lambda m: m.decode('utf-8') if m else None
            )
            await self.consumer.start()
            self.is_running = True
            logger.info(SUCCESS_START_CONSUMER)
            
            # Start the consume task
            self.consume_task = asyncio.create_task(self.consume())
            logger.info("Consume task started")
            
        except Exception as e:
            logger.error(ERROR_START_CONSUMER.format(str(e)))
            raise

    async def stop(self):
        """Stop the Kafka consumer"""
        if self.consumer:
            logger.info("Stopping Kafka consumer")
            self.is_running = False
            if self.consume_task:
                self.consume_task.cancel()
                try:
                    await self.consume_task
                except asyncio.CancelledError:
                    pass
            await self.consumer.stop()
            logger.info(SUCCESS_STOP_CONSUMER)

    def parse_message(self, message_value: str) -> Dict[str, Any]:
        """Parse stringified JSON message"""
        try:
            if not message_value:
                raise ValueError("Empty message received")
            
            # Parse the stringified JSON
            return json.loads(message_value)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON message: {message_value}")
            raise ValueError(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing message: {str(e)}")
            raise

    def store_unidentified_message(self, message: Dict[str, Any]):
        """Store unidentified message in a separate file"""
        try:
            # Add timestamp to the message
            message_with_timestamp = {
                "timestamp": datetime.utcnow().isoformat(),
                "message": message
            }
            
            # Append the message to the unidentified messages file
            with open(UNIDENTIFIED_MESSAGES_FILE, 'a') as f:
                f.write(json.dumps(message_with_timestamp) + '\n')
                
            logger.info(f"Stored unidentified message in {UNIDENTIFIED_MESSAGES_FILE}")
        except Exception as e:
            logger.error(f"Failed to store unidentified message: {str(e)}")

    @async_retry(max_retries=MAX_RETRIES, delay=RETRY_DELAY)
    async def process_message(self, message):
        """Process a single Kafka message"""
        try:
            logger.info(f"Processing message from topic {message.topic}, partition {message.partition}, offset {message.offset}")
            
            # Parse the stringified JSON message
            data = self.parse_message(message.value)
            logger.info(f"Parsed message data: {json.dumps(data)}")
            
            if not isinstance(data, dict):
                raise ValueError(f"Expected dict, got {type(data)}")
            
            object_type = data.get("object_type")
            if not object_type:
                logger.warning(ERROR_MISSING_OBJECT_TYPE.format(json.dumps(data)))
                self.store_unidentified_message(data)
                return
            
            if object_type not in self.object_processors:
                logger.warning(ERROR_UNKNOWN_OBJECT.format(object_type))
                self.store_unidentified_message(data)
                return
            
            model_class = self.object_processors[object_type]
            repository_class = self.repositories[object_type]
            
            # Create database session
            db = SessionLocal()
            try:
                # Create repository instance with database session
                repository = repository_class(db)
                logger.info(f"Created repository instance for {object_type}")
                
                # Process the message
                await repository.process_message(data)
                
                # Commit transaction
                db.commit()
                logger.info(SUCCESS_PROCESS_MESSAGE.format(object_type))
            except Exception as e:
                db.rollback()
                logger.error(ERROR_PROCESS_MESSAGE.format(str(e)))
                raise
            finally:
                db.close()
                
        except Exception as e:
            logger.error(ERROR_DECODE_MESSAGE.format(str(e)))
            raise

    async def consume(self):
        """Consume messages from Kafka"""
        try:
            while self.is_running:
                try:
                    async for message in self.consumer:
                        if not self.is_running:
                            break
                        await self.process_message(message)
                except asyncio.CancelledError:
                    logger.info(SUCCESS_CANCEL_TASK)
                    break
                except Exception as e:
                    logger.error(ERROR_CONSUME_LOOP.format(str(e)))
                    if self.is_running:
                        await asyncio.sleep(RETRY_DELAY)  # Wait before retrying
        except Exception as e:
            logger.error(ERROR_FATAL.format(str(e)))
            raise 
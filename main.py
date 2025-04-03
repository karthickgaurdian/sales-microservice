import asyncio
import signal
import sys
from typing import Optional

from fastapi import FastAPI
from consumer_service.kafka_consumer import KafkaConsumerService
from consumer_utils.logger import setup_logger
from database import Base, engine
from consumer_entities.opportunity_model import Opportunity
from consumer_entities.project_model import Project
from consumer_utils.log_cleanup import cleanup_logs

# Create FastAPI app
app = FastAPI(title="Kafka Consumer Service")

# Setup logger
logger = setup_logger(__name__)

# Global consumer service instance
consumer_service: Optional[KafkaConsumerService] = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global consumer_service
    
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        
        # Clean up old logs on startup
        cleanup_logs()
        logger.info("Log cleanup completed")
        
        # Initialize consumer service
        consumer_service = KafkaConsumerService()
        
        # Start consumer service
        await consumer_service.start()
        
        logger.info("Kafka consumer service started successfully")
    except Exception as e:
        logger.error(f"Failed to start services: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global consumer_service
    
    if consumer_service:
        try:
            await consumer_service.stop()
            logger.info("Kafka consumer service stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping consumer service: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

async def shutdown(signal: signal.Signals, loop: asyncio.AbstractEventLoop, consumer_service: Optional[KafkaConsumerService] = None):
    """Cleanup tasks tied to the service's shutdown."""
    logger.info(f"Received exit signal {signal.name}...")
    
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    
    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    
    if consumer_service:
        await consumer_service.stop()
    
    loop.stop()

def handle_exception(loop: asyncio.AbstractEventLoop, context: dict):
    """Handle any uncaught exceptions in the event loop."""
    msg = context.get("exception", context["message"])
    logger.error(f"Caught exception: {msg}")
    logger.info("Shutting down...")
    asyncio.create_task(shutdown(signal.SIGTERM, loop))

async def main():
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

        # Clean up old logs on startup
        cleanup_logs()
        logger.info("Log cleanup completed")

        # Create event loop
        loop = asyncio.get_event_loop()
        
        # Add signal handlers
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(shutdown(s, loop))
            )
        
        # Set exception handler
        loop.set_exception_handler(handle_exception)
        
        # Initialize and start consumer service
        consumer_service = KafkaConsumerService()
        await consumer_service.start()
        
        # Keep the main loop running
        while True:
            await asyncio.sleep(1)
            
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1) 
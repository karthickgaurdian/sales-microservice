from abc import ABC, abstractmethod
from typing import List
from aiokafka import AIOKafkaConsumer
import asyncio

class IKafkaConsumer(ABC):
    @abstractmethod
    async def start(self) -> None:
        """Start the Kafka consumer"""
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        """Stop the Kafka consumer"""
        pass
    
    @abstractmethod
    async def consume(self) -> None:
        """Main consumption loop"""
        pass
    
    @abstractmethod
    async def process_message(self, message) -> None:
        """Process a single message"""
        pass 
from typing import Dict, Any

# Message Types
MESSAGE_TYPE_OPPORTUNITY = "opportunity"
MESSAGE_TYPE_PROJECT = "project"

# Event Types
EVENT_TYPE_CREATE = "create"
EVENT_TYPE_UPDATE = "update"
EVENT_TYPE_DELETE = "delete"

# Opportunity Stages
OPPORTUNITY_STAGES = [
    "Prospecting",
    "Qualification",
    "Proposal",
    "Negotiation",
    "Closed Won",
    "Closed Lost"
]

# Project Statuses
PROJECT_STATUSES = [
    "Not Started",
    "In Progress",
    "On Hold",
    "Completed",
    "Cancelled"
]

# Default Values
DEFAULT_META_DATA: Dict[str, Any] = {
    "source": "system",
    "version": "1.0",
    "environment": "development"
}

# Error Messages
ERROR_MESSAGES = {
    "invalid_message": "Invalid message format",
    "processing_failed": "Failed to process message",
    "database_error": "Database operation failed",
    "kafka_error": "Kafka operation failed",
    "validation_error": "Validation failed"
}

# Success Messages
SUCCESS_MESSAGES = {
    "message_processed": "Message processed successfully",
    "database_operation": "Database operation completed",
    "cleanup_completed": "Log cleanup completed"
}

# File Patterns
LOG_FILE_PATTERN = "*.log"
UNIDENTIFIED_MESSAGES_PATTERN = "unidentified_messages.log" 
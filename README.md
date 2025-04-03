# Kafka Consumer Service

A robust Kafka consumer service that processes enterprise events and stores them in a SQLite database. This service is designed to handle opportunity and project events with proper error handling, retries, and logging.

## Features

- Asynchronous Kafka message processing
- Structured logging with JSON formatting
- Retry mechanism with exponential backoff
- SQLite database for local development
- Docker support for containerized deployment
- Clean architecture with separation of concerns
- Comprehensive error handling and monitoring

## Author 

Karthick.M
GitHub : https://github.com/karthickgaurdian

## Project Structure

```
kafka-ms1-consumer/
├── consumer_entities/           # Data models and entities
│   ├── base_model.py           # Base SQLAlchemy model
│   ├── opportunity_model.py    # Opportunity entity model
│   └── project_model.py        # Project entity model
├── consumer_repository/        # Data access layer
│   ├── interfaces/            # Repository interfaces
│   ├── opportunity_repository.py  # Opportunity data operations
│   └── project_repository.py      # Project data operations
├── consumer_service/          # Business logic layer
│   ├── interfaces/           # Service interfaces
│   └── kafka_consumer.py     # Kafka consumer implementation
├── consumer_utils/           # Utility functions
│   ├── logger.py            # Logging configuration
│   └── retry_handler.py     # Retry mechanism
├── core/                    # Core configurations
│   └── settings.py         # Application settings
├── database/               # Database configurations
│   └── database.py        # Database connection setup
├── data/                  # SQLite database files
├── logs/                  # Application logs
├── .env.example          # Example environment variables
├── docker-compose.yml    # Docker services configuration
├── Dockerfile           # Docker build configuration
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

## Message Formats

### Opportunity Message
```json
{
    "event_id": "opp_123456789",
    "name": "Enterprise Software License Deal",
    "stage": "Negotiation",
    "amount": 50000.00,
    "probability": 75,
    "expected_close_date": "2024-06-30",
    "account_id": "acc_987654321",
    "owner_id": "usr_456789123",
    "meta_data": {
        "source": "Salesforce",
        "last_modified": "2024-03-24T20:40:35Z",
        "tags": ["enterprise", "software", "license"],
        "notes": "Key decision maker identified"
    }
}
```

### Project Message
```json
{
    "event_id": "proj_123456789",
    "name": "Cloud Migration Project",
    "status": "In Progress",
    "start_date": "2024-03-01",
    "end_date": "2024-08-15",
    "budget": 150000.00,
    "account_id": "acc_987654321",
    "owner_id": "usr_456789123",
    "meta_data": {
        "source": "HubSpot",
        "last_modified": "2024-03-24T20:45:00Z",
        "tags": ["cloud", "migration", "consulting"],
        "notes": "Technical review pending"
    }
}
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd kafka-ms1-consumer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the environment file and update settings:
```bash
cp .env.example .env
```

5. Start the services using Docker Compose:
```bash
docker-compose up -d
```

## Configuration

The service can be configured through environment variables in the `.env` file:

```env
# Application settings
APP_ENV=development

# Kafka settings
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_GROUP_ID=enterprise-consumer-group
KAFKA_TOPIC=sales_events

# Database settings (SQLite)
DATABASE_URL=sqlite:///data/enterprise.db

# Logging settings
LOG_LEVEL=INFO
LOG_FILE=logs/consumer.log
```

## Running the Service

1. Start the service:
```bash
python main.py
```

2. Monitor the logs:
```bash
tail -f logs/consumer.log
```

## Development

### Adding New Features

1. Create new models in `consumer_entities/`
2. Implement repositories in `consumer_repository/`
3. Add business logic in `consumer_service/`
4. Update the Kafka consumer to handle new message types

### Testing

Run tests using pytest:
```bash
pytest
```

## Error Handling

The service includes comprehensive error handling:
- Retries with exponential backoff for transient failures
- Structured logging for all operations
- Separate log file for unidentified messages
- Graceful shutdown handling

## Monitoring

Monitor the service through:
- Application logs in `logs/consumer.log`
- Unidentified messages in `logs/unidentified_messages.log`
- Database files in `data/enterprise.db`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
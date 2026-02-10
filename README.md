# FastAPI Core Service

This project is a FastAPI-based web service that includes a WebSocket manager and a conversation session service. It provides a structured way to handle real-time communication and manage conversation data.

## Project Structure

```
fastapi-core-service
├── src
│   ├── main.py                # Entry point of the FastAPI application
│   ├── app
│   │   ├── __init__.py        # App package initialization
│   │   ├── api
│   │   │   ├── __init__.py    # API package initialization
│   │   │   ├── routes.py      # RESTful routes
│   │   │   └── websocket_routes.py # WebSocket routes
│   │   ├── core
│   │   │   ├── __init__.py    # Core package initialization
│   │   │   ├── websocket_manager.py # WebSocket manager
│   │   │   └── conversation_service.py # Conversation service
│   │   ├── models
│   │   │   └── conversation.py # Conversation data model
│   │   ├── schemas
│   │   │   └── conversation.py # Pydantic schemas for conversation
│   │   ├── deps
│   │   │   └── __init__.py    # Dependency injection
│   │   └── config.py          # Application configuration
├── tests
│   ├── test_websocket_manager.py # Unit tests for WebSocketManager
│   └── test_conversation_service.py # Unit tests for ConversationService
├── requirements.txt            # Project dependencies
├── pyproject.toml              # Project metadata and dependencies
└── README.md                   # Project documentation
```

## Installation

To get started with the FastAPI Core Service, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fastapi-core-service
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn src.main:app --reload
   ```

## Usage

- The application exposes RESTful API endpoints defined in `src/app/api/routes.py`.
- WebSocket connections can be managed through the routes defined in `src/app/api/websocket_routes.py`.
- The conversation logic is handled by the `ConversationService` class located in `src/app/core/conversation_service.py`.

## Testing

To run the tests, use the following command:
```
pytest
```

This will execute the unit tests defined in the `tests` directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
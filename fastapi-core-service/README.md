# FastAPI Core Service

This project is a FastAPI web service that includes a WebSocket manager and a conversation session service. It is designed to handle real-time communication and manage conversation sessions effectively.

## Project Structure

```
fastapi-core-service
├── src
│   ├── main.py                # Entry point of the FastAPI application
│   ├── app
│   │   ├── __init__.py        # App package initialization
│   │   ├── api
│   │   │   ├── __init__.py    # API package initialization
│   │   │   ├── routes.py      # RESTful API routes
│   │   │   └── websocket_routes.py # WebSocket routes
│   │   ├── core
│   │   │   ├── __init__.py    # Core package initialization
│   │   │   ├── websocket_manager.py # WebSocket manager
│   │   │   └── conversation_service.py # Conversation service
│   │   ├── models
│   │   │   └── conversation.py # Conversation model
│   │   ├── schemas
│   │   │   └── conversation.py # Pydantic schemas for conversation
│   │   └── config.py          # Configuration settings
├── tests
│   ├── test_websocket_manager.py # Unit tests for WebSocketManager
│   └── test_conversation_service.py # Unit tests for ConversationService
├── requirements.txt            # Project dependencies
├── pyproject.toml             # Project metadata and dependencies
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

## Usage

To run the FastAPI application, execute the following command:

```
uvicorn src.main:app --reload
```

This will start the server in development mode, and you can access the API at `http://localhost:8000`.

## WebSocket Support

The application supports WebSocket connections for real-time communication. You can connect to the WebSocket endpoint defined in `src/app/api/websocket_routes.py`.

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
# SentraCore Backend API

A FastAPI backend for managing SentraCore robot configurations with MongoDB integration.

## Features

- **CRUD Operations**: Create, read, update, and delete SentraCore configurations
- **MongoDB Integration**: Async MongoDB operations using Motor
- **Data Models**: Pydantic models for type safety and validation
- **RESTful API**: Clean REST endpoints for all operations
- **CORS Support**: Configured for frontend integration
- **Error Handling**: Comprehensive error handling and validation

## Data Structure

### SentraCore Configuration
- **name**: Configuration name
- **description**: Optional description
- **labels**: Array of action blocks with position and parameters
- **connections**: Array of connections between labels
- **selected_option**: Currently selected action option
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

### Label Structure
- **id**: Unique identifier
- **text**: Display text/title
- **value**: Parameter value
- **x, y**: Position coordinates
- **category**: Action category (move, turn, grip, wait)

### Connection Structure
- **id**: Unique identifier
- **from_id**: Source label ID
- **to_id**: Target label ID

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB connection details
   ```

3. **MongoDB Setup**
   - Install MongoDB locally or use MongoDB Atlas
   - Update `MONGODB_URL` in `.env` file

4. **Run the Application**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Base URL: `http://localhost:8000`

- `GET /` - Health check
- `GET /health` - API status
- `GET /docs` - Interactive API documentation (Swagger UI)

### SentraCore Endpoints

- `POST /api/sentra-core/` - Create new configuration
- `GET /api/sentra-core/` - Get all configurations (with pagination)
- `GET /api/sentra-core/{id}` - Get configuration by ID
- `PUT /api/sentra-core/{id}` - Update configuration
- `DELETE /api/sentra-core/{id}` - Delete configuration
- `GET /api/sentra-core/search/` - Search by name
- `GET /api/sentra-core/count/` - Get total count
- `POST /api/sentra-core/save-state/` - Save current frontend state

## Usage Examples

### Save Current State (Frontend Integration)
```javascript
const response = await fetch('http://localhost:8000/api/sentra-core/save-state/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: "My Robot Sequence",
    description: "A sequence of robot movements",
    labels: [
      {
        id: "1",
        text: "Forward",
        value: "100",
        x: 150.0,
        y: 200.0,
        category: "move"
      }
    ],
    connections: [
      {
        id: "1-2",
        from: "1",
        to: "2"
      }
    ],
    selected_option: "move-forward"
  })
});

const result = await response.json();
```

### Get All Configurations
```bash
curl http://localhost:8000/api/sentra-core/
```

### Get Configuration by ID
```bash
curl http://localhost:8000/api/sentra-core/{id}
```

## Development

### Project Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── models/
│   └── sentra_core.py     # Pydantic data models
├── controllers/
│   └── sentra_core_controller.py  # Business logic
├── routes/
│   └── sentra_core_routes.py      # API endpoints
└── database/
    └── connection.py      # MongoDB connection management
```

### Adding New Features

1. **Models**: Add new Pydantic models in `models/`
2. **Controllers**: Add business logic in `controllers/`
3. **Routes**: Add API endpoints in `routes/`
4. **Update main.py**: Include new routers

## Testing

The API includes automatic interactive documentation at `http://localhost:8000/docs` when running.

## Error Handling

The API includes comprehensive error handling:
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side errors

All errors return JSON responses with descriptive messages. 
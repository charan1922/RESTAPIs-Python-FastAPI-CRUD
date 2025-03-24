# FastAPI Starter

Quickly get started with [FastAPI](https://fastapi.tiangolo.com/) using this starter!

- If you want to upgrade Python, you can change the image in the [Dockerfile](./.codesandbox/Dockerfile).
- Modify [requirements.txt](./requirements.txt) to add packages.

# Python RESTful API with FastAPI

This project demonstrates a simple RESTful API built using FastAPI.

## Requirements

- Python 3.7 or higher
- FastAPI
- Uvicorn (ASGI server)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd python-RESTful-fastAPI
   ```

2. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

## Running the Application

Run the application using `uvicorn`:

```bash
uvicorn main:app --reload

or

fastapi dev main.py
```

- The API will be available at: `http://127.0.0.1:8000/`

## Endpoints

- **GET /**: Returns a welcome message.
  ```json
  {
    "message": "Hello World"
  }
  ```

## License

This project is licensed under the MIT License.

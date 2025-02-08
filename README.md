# Weather App

This is a weather application built using **Flask** for the backend and **HTML**, **CSS**, and **JavaScript** for the frontend. The app fetches real-time weather data from the **OpenWeatherMap API** and displays it with friendly user interfaces. It includes caching, logging, rate limiting, and error handling for optimal performance.

## Features
- **Weather Data**: The app displays real-time weather information for any city using OpenWeatherMap API.
- **Rate Limiting**: Limits the number of requests a user can make to prevent abuse.
- **Caching**: Caches requests to improve performance and reduce API calls.
- **Logging**: Logs all requests for debugging and monitoring purposes.
- **Error Handling**: Displays user-friendly error messages while maintaining backend errors for debugging.
- **Docker Support**: The app is containerized with Docker and supports Docker Compose.

## File Structure
```
.
├── static/                # Static files (e.g., CSS, JS, images)
├── templates/             # HTML files for rendering pages
├── .gitignore             # Git ignore configuration
├── compose.yml            # Docker Compose configuration
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
└── weatherapp.py          # Main backend code
```

## Setup

### Prerequisites
1. **Python 3.x** is required.
2. **Docker** and **Docker Compose** are required if you prefer to use the Docker setup.

### Installing Dependencies
If you're setting up the app without Docker, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd weather-app
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your **OpenWeatherMap API Key** as an environment variable:
   ```bash
   export API_KEY="your_openweathermap_api_key"
   ```

4. Run the Flask application:
   ```bash
   python weatherapp.py
   ```

By default, the app will run on **port 8080**. You can change the port by setting the **PORT** environment variable.

### Docker Setup

1. **Build and Run the Application Using Docker**:
   If you prefer using Docker, you can use the Docker and Docker Compose configuration.

2. **Build the Docker Image**:
   ```bash
   docker build -t weather-app .
   ```

3. **Run with Docker Compose**:
   Docker Compose will build the image and run it in a container:
   ```bash
   docker-compose up
   ```

The app will be available at **http://localhost:8080** by default.

## How It Works

### Frontend
- The frontend consists of an **HTML** page (located in the `templates/` directory) that takes a city name from the user and displays the weather information (e.g., temperature, humidity, wind speed).
- The frontend makes an API call to the backend Flask server (`/getweather`) with the city name as a query parameter.
- The data is returned in **JSON** format and displayed in a user-friendly way with weather icons and a friendly message.

### Backend
- The backend is a **Flask** app that:
  - Retrieves the weather data from **OpenWeatherMap API** using a city name provided in the GET request.
  - Logs the request, measures request times, and applies **rate limiting** for the endpoints.
  - Caches results for quicker responses and to avoid hitting the API too frequently.
  - Handles different error scenarios (e.g., invalid city name, rate limit exceeded) and provides user-friendly error messages.

### Routes
- **`/`**: Displays the frontend weather page (caches the page for 3 seconds).
- **`/getweather`**: Retrieves weather data for a given city. Supports caching and rate-limiting.

### Rate Limiting
- **Home page**: 3 requests per 4 seconds per client IP.
- **Weather API**: 10 requests per 20 seconds per client IP.

### Error Handling
- The backend handles errors such as 400 (Bad Request), 401 (Unauthorized), 404 (City Not Found), and others with appropriate messages. These errors are logged, and user-friendly messages are shown to the frontend.

## Environment Variables
- **PORT**: Set the port for the Flask application (default: `8080`).
- **API_KEY**: Your OpenWeatherMap API key for fetching weather data.

## Contributing
Feel free to fork this repository, make improvements, and submit pull requests. If you find any bugs or have any suggestions, please create an issue.

## License
This project is licensed under the MIT License.

---
import requests
from flask import Flask, request, jsonify, render_template
from flask_caching import Cache
import time
import os
import logging
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()
PORT = os.environ.get('PORT', 8080)
API_KEY = os.environ.get('API_KEY')

if not API_KEY:
    raise ValueError("No API_KEY set for OpenWeatherMap API")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
cache = Cache(app, config={
    'CACHE_TYPE': 'SimpleCache'
})


def log_request_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(
            f"Request to 'http://{request.remote_addr}:{PORT}{request.path}' took {end_time - start_time:.2f} seconds")
        return result

    return wrapper


def rate_limit(max_requests=20, time_window=5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            client_ip_address = request.remote_addr
            cache_key = f"rate_limit_{client_ip_address}_{request.endpoint}"

            current_count = cache.get(cache_key)

            if current_count is None:
                current_count = 0

            if current_count >= max_requests:
                logger.error(f"{cache_key} exceeded. Please try again in {time_window} seconds")
                return jsonify({"error": f"Rate Limit exceeded. Please try again in {time_window} seconds"
                                }), 459
            increment_count = current_count + 1
            cache.set(cache_key, increment_count, time_window)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@app.route('/', methods=["GET"], endpoint="home_page")
@rate_limit(max_requests=3, time_window=4)
@log_request_time
@cache.cached(timeout=3)
def home():
    logger.info('Application Started')
    return render_template('weather.html')


@app.route('/getweather', methods=["GET"], endpoint="get_weather")
@rate_limit(max_requests=10, time_window=20)
@log_request_time
@cache.cached(timeout=10, query_string=True)
def get_weather():
    city = request.args.get('city', 'Miami')
    logger.info(f"Fetching weather data for city: {city}")

    if not API_KEY:
        logger.error("API KEY not found")
        return jsonify({"error": "API KEY not found"}), 401

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    logger.info(f"Request URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)
        data = response.json()

        if data.get("cod") != 200:
            error_message = data.get('message', 'Failed to fetch weather data')
            logger.error(f"Error fetching weather data: {error_message}")
            return jsonify({"error": error_message}), data.get('cod', 500)

        logger.info(f"Weather data fetched successfully: {data}")
        return jsonify(data)

    except requests.exceptions.HTTPError as e:
        status_code = response.status_code
        if status_code == 400:
            logger.error("Bad request")
            return jsonify({"error": "Bad request"}), 400
        elif status_code == 401:
            logger.error("Unauthorized request. Invalid API Key")
            return jsonify({"error": "Unauthorized request. Invalid API Key"}), 401
        elif status_code == 403:
            logger.error("Forbidden. Access Denied")
            return jsonify({"error": "Forbidden. Access Denied"}), 403
        elif status_code == 404:
            logger.error(f"City {city} NOT found")
            return jsonify({"error": f"City {city} NOT found"}), 404
        elif status_code == 500:
            logger.error("Internal Server Error. Try again later")
            return jsonify({"error": "Internal Server Error. Try again later"}), 500
        elif status_code == 502:
            logger.error("Bad Gateway")
            return jsonify({"error": "Bad Gateway"}), 502
        elif status_code == 503:
            logger.error("Service Unavailable")
            return jsonify({"error": "Service Unavailable"}), 503
        elif status_code == 504:
            logger.error("Gateway Timeout")
            return jsonify({"error": "Gateway Timeout"}), 504
        else:
            logger.error(f"HTTP error occurred: {e}")
            return jsonify({"error": f"HTTP error occurred: {e}"}), status_code

    except requests.exceptions.ConnectionError:
        logger.error("Connection Error: Failed to connect to the OpenWeatherMap API")
        return jsonify({"error": "Connection Error: Failed to connect to the OpenWeatherMap API"}), 503

    except requests.exceptions.Timeout:
        logger.error("Request Timeout: The request timed out")
        return jsonify({"error": "Request Timeout: The request timed out"}), 504

    except requests.exceptions.TooManyRedirects:
        logger.error("Too Many Redirects: The request exceeded the maximum number of redirects")
        return jsonify({"error": "Too Many Redirects: The request exceeded the maximum number of redirects"}), 508

    except requests.exceptions.RequestException as e:
        logger.error(f"Request to OpenWeatherMap API failed: {e}")
        return jsonify({"error": "Failed to fetch weather data"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=PORT)
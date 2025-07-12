import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenWeather API configuration


def get_api_key() -> Optional[str]:
    """Get OpenWeather API key from environment variable or hardcoded value."""
    # First try to get from environment variable for security
    api_key = os.getenv("OPENWEATHER_API_KEY")

    # Fallback to hardcoded value for development (replace with your key)
    if not api_key:
        # Default demo key - replace with your actual API key
        api_key = "your_api_key_here"

    return api_key


OPENWEATHER_API_KEY = get_api_key()

# API endpoints
GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
AIR_POLLUTION_URL = "https://api.openweathermap.org/data/2.5/air_pollution"

# Default settings
DEFAULT_UNITS = "metric"
DEFAULT_FORECAST_HOURS = 24
CACHE_TTL = 300  # 5 minutes cache
MAX_FORECAST_DAYS = 5

# API limits and timeouts
REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 1  # seconds between requests

# App configuration
APP_TITLE = "🌤️ Weather Forecast App"
APP_DESCRIPTION = "Get accurate weather forecasts for any location worldwide"
DEFAULT_LOCATION = "New York, USA"

# Feature flags
ENABLE_AIR_QUALITY = True
ENABLE_WEATHER_ALERTS = True
ENABLE_DETAILED_METRICS = True
ENABLE_LOCATION_SUGGESTIONS = True

# Error messages
ERROR_MESSAGES = {
    "api_key_missing": "OpenWeather API key is not configured. Please set OPENWEATHER_API_KEY environment variable.",
    "location_not_found": "Location not found. Please try a different search term.",
    "api_error": "Unable to fetch weather data. Please try again later.",
    "network_error": "Network error occurred. Please check your internet connection.",
    "rate_limit": "Too many requests. Please wait a moment and try again."
}

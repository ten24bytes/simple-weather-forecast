import streamlit as st
import requests
from typing import Optional, Tuple, Dict, Any, List
from datetime import datetime, timedelta
import time
import json
from config import (
    OPENWEATHER_API_KEY,
    GEOCODING_URL,
    CURRENT_WEATHER_URL,
    FORECAST_URL,
    REQUEST_TIMEOUT,
    CACHE_TTL
)


st.set_page_config(
    page_title="Weather Forecast",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main app header with simple styling
st.title("🌤️ Weather Forecast App")
st.markdown("*Get accurate weather forecasts for any location worldwide*")

# Sidebar for controls
with st.sidebar:
    st.header("Settings")

    # Home/Reset button
    if st.button("🏠 Reset to Home", help="Clear current location and return to home screen", use_container_width=True):
        # Clear session state
        for key in list(st.session_state.keys()):
            if key in ['selected_suggestion', 'location_input', 'location_text_input']:
                del st.session_state[key]
        # Clear any cached data
        st.cache_data.clear()
        st.rerun()

    st.divider()

    # Units selection
    units = st.radio(
        "Temperature Units",
        ["metric", "imperial"],
        format_func=lambda x: "°C (Celsius)" if x == "metric" else "°F (Fahrenheit)",
        help="Choose your preferred temperature unit"
    )

    # Forecast period selection
    forecast_hours = st.selectbox(
        "Forecast Period",
        [24, 48, 72, 120],
        format_func=lambda x: f"Next {x} hours",
        help="Select how far ahead you want to see the forecast"
    )

    # Additional settings
    show_details = st.checkbox("Show detailed metrics", value=True)

    st.divider()
    st.subheader("About")
    st.markdown("""
        This app uses the **OpenWeatherMap API** to provide accurate weather forecasts.
        
        **Features:**
        - 5-day/3-hour forecasts
        - Current weather conditions
        - Multiple temperature units
        - Beautiful, responsive design
        - Dark/light mode support
        - Free weather icons (emojis)
    """)


@st.cache_data(ttl=CACHE_TTL)
def get_coordinates(location: str) -> Tuple[Optional[float], Optional[float], Optional[str], Optional[str], Optional[str]]:
    """Get coordinates and location info from location name using OpenWeatherMap Geocoding API."""
    params = {
        "q": location,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY
    }

    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        data = response.json()
        if data:
            location_data = data[0]
            return (
                location_data["lat"],
                location_data["lon"],
                location_data.get("name"),
                location_data.get("country"),
                location_data.get("state")
            )
    except requests.RequestException as e:
        st.error(f"Error fetching location data: {e}")
    except (KeyError, IndexError) as e:
        st.error(f"Error parsing location data: {e}")

    return None, None, None, None, None


@st.cache_data(ttl=CACHE_TTL)
def get_current_weather(lat: float, lon: float, units: str) -> Optional[Dict[str, Any]]:
    """Get current weather data from OpenWeatherMap API."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": units
    }

    try:
        response = requests.get(CURRENT_WEATHER_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching current weather: {e}")

    return None


@st.cache_data(ttl=CACHE_TTL)
def get_forecast(lat: float, lon: float, units: str) -> Optional[Dict[str, Any]]:
    """Get forecast data from OpenWeatherMap API."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": units
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching forecast data: {e}")

    return None


def get_weather_emoji(weather_id: int, icon: str, is_day: bool = True) -> str:
    """Get appropriate emoji for weather condition as a free alternative to weather icons."""
    # Thunderstorm group (200-232)
    if 200 <= weather_id <= 232:
        return "⛈️"
    # Drizzle group (300-321)
    elif 300 <= weather_id <= 321:
        return "🌦️"
    # Rain group (500-531)
    elif 500 <= weather_id <= 531:
        if weather_id == 500:  # light rain
            return "🌧️"
        elif weather_id in [501, 502, 503, 504]:  # moderate to heavy rain
            return "🌧️"
        else:  # shower rain
            return "🌦️"
    # Snow group (600-622)
    elif 600 <= weather_id <= 622:
        return "❄️"
    # Atmosphere group (701-781)
    elif 701 <= weather_id <= 781:
        if weather_id == 701:  # mist
            return "🌫️"
        elif weather_id == 711:  # smoke
            return "💨"
        elif weather_id == 721:  # haze
            return "🌫️"
        elif weather_id in [731, 751, 761]:  # dust/sand
            return "💨"
        elif weather_id == 741:  # fog
            return "🌫️"
        elif weather_id == 771:  # squalls
            return "💨"
        elif weather_id == 781:  # tornado
            return "🌪️"
        else:
            return "🌫️"
    # Clear group (800)
    elif weather_id == 800:
        return "☀️" if is_day else "🌙"
    # Clouds group (801-804)
    elif 801 <= weather_id <= 804:
        if weather_id == 801:  # few clouds
            return "🌤️" if is_day else "🌙"
        elif weather_id == 802:  # scattered clouds
            return "⛅"
        elif weather_id in [803, 804]:  # broken/overcast clouds
            return "☁️"
    # Default fallback
    return "🌤️"


def get_weather_gradient(weather_id: int, is_day: bool = True) -> str:
    """Get CSS gradient based on weather condition for enhanced visual appeal."""
    if 200 <= weather_id <= 232:  # Thunderstorm
        return "linear-gradient(135deg, #2c3e50, #3498db)"
    elif 300 <= weather_id <= 531:  # Rain/Drizzle
        return "linear-gradient(135deg, #3498db, #2980b9)"
    elif 600 <= weather_id <= 622:  # Snow
        return "linear-gradient(135deg, #ecf0f1, #bdc3c7)"
    elif 701 <= weather_id <= 781:  # Atmosphere
        return "linear-gradient(135deg, #95a5a6, #7f8c8d)"
    elif weather_id == 800:  # Clear
        if is_day:
            return "linear-gradient(135deg, #f39c12, #e67e22)"
        else:
            return "linear-gradient(135deg, #2c3e50, #34495e)"
    elif 801 <= weather_id <= 804:  # Clouds
        return "linear-gradient(135deg, #bdc3c7, #95a5a6)"
    else:
        return "linear-gradient(135deg, #1e90ff, #4dabf7)"


def format_datetime(dt_txt: str) -> Tuple[str, str]:
    """Format datetime string to a more readable format."""
    try:
        dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
        date_str = dt.strftime("%a, %b %d")
        time_str = dt.strftime("%I:%M %p")
        return date_str, time_str
    except ValueError:
        return dt_txt, ""


def get_wind_direction(deg: float) -> str:
    """Convert wind degree to compass direction."""
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    index = round(deg / 22.5) % 16
    return directions[index]


def display_current_weather(weather_data: Dict[str, Any], units: str, city: Optional[str], country: Optional[str], state: Optional[str] = None):
    """Display current weather in a beautiful card format."""
    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    description = weather_data["weather"][0]["description"]
    weather_id = weather_data["weather"][0]["id"]
    icon = weather_data["weather"][0]["icon"]

    # Weather icon system
    is_day = "d" in icon
    weather_emoji = get_weather_emoji(weather_id, icon, is_day)
    weather_gradient = get_weather_gradient(weather_id, is_day)

    # Location string with fallbacks
    location_parts = []
    if city:
        location_parts.append(city)
    if state and state != city:
        location_parts.append(state)
    if country:
        location_parts.append(country)
    location_str = ", ".join(location_parts) if location_parts else "Unknown Location"

    unit_symbol = "°C" if units == "metric" else "°F"

    # Get all the weather data
    humidity = weather_data["main"]["humidity"]
    pressure = weather_data["main"]["pressure"]

    # Get wind data if available
    wind_html = ""
    if "wind" in weather_data:
        wind_speed = weather_data["wind"]["speed"]
        wind_deg = weather_data["wind"].get("deg", 0)
        wind_dir = get_wind_direction(wind_deg)
        wind_unit = "m/s" if units == "metric" else "mph"
        wind_html = f"""<div class='condition-card' style='border-left: 4px solid #27ae60;'>
                    <div class='condition-label'>💨 Wind {wind_dir}</div>
                    <div class='condition-value'>{wind_speed:.1f} {wind_unit}</div>
                </div>"""

    # Get visibility data if available
    visibility_html = ""
    if "visibility" in weather_data:
        visibility = weather_data["visibility"] / 1000  # Convert to km
        vis_unit = "km" if units == "metric" else "mi"
        if units == "imperial":
            visibility = visibility * 0.621371  # Convert to miles
        visibility_html = f"""<div class='condition-card' style='border-left: 4px solid #f39c12;'>
                    <div class='condition-label'>👁️ Visibility</div>
                    <div class='condition-value'>{visibility:.1f} {vis_unit}</div>
                </div>"""

    # Create a container with equal height columns using flex
    st.markdown(f"""
        <style>
        .weather-card {{
            background: {weather_gradient};
            color: white;
            border-radius: 15px;
            padding: 2.5rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .conditions-title {{
            margin: 0 0 1rem 0;
            font-size: 1.3rem;
            color: var(--text-color);
        }}
        
        .condition-card {{
            background: var(--background-color);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border: 1px solid var(--border-color);
        }}
        
        .condition-label {{
            font-size: 0.9rem;
            color: var(--secondary-text-color);
            margin-bottom: 0.3rem;
        }}
        
        .condition-value {{
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--text-color);
        }}
        
        /* Light theme variables */
        :root {{
            --background-color: white;
            --text-color: #2c3e50;
            --secondary-text-color: #666;
            --border-color: rgba(0,0,0,0.1);
        }}
        
        /* Dark theme variables */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --background-color: #262730;
                --text-color: #ffffff;
                --secondary-text-color: #a6a6a6;
                --border-color: rgba(255,255,255,0.1);
            }}
        }}
        
        /* Override for Streamlit dark theme */
        .stApp[data-theme="dark"] {{
            --background-color: #262730;
            --text-color: #ffffff;
            --secondary-text-color: #a6a6a6;
            --border-color: rgba(255,255,255,0.1);
        }}
        </style>
        
        <div style='display: flex; gap: 2rem; align-items: stretch; margin-bottom: 2rem;'>
            <div style='flex: 1;' class='weather-card'>
                <h3 style='margin: 0; color: white; font-size: 1.8rem; font-weight: 600;'>{location_str}</h3>
                <div style='font-size: 6rem; margin: 1.5rem 0; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));'>
                    {weather_emoji}
                </div>
                <div style='font-size: 3.5rem; font-weight: 300; margin: 0.8rem 0; color: white;'>{temp:.1f}{unit_symbol}</div>
                <div style='font-size: 1.4rem; color: white; text-transform: capitalize; font-weight: 500; margin: 0.5rem 0;'>{description.title()}</div>
                <div style='margin-top: 0.8rem; color: white; font-size: 1.1rem; opacity: 0.9;'>
                    Feels like {feels_like:.0f}{unit_symbol}
                </div>
            </div>
            <div style='flex: 1; display: flex; flex-direction: column;'>
                <h3 class='conditions-title'>📊 Current Conditions</h3>
                <div class='condition-card' style='border-left: 4px solid #3498db;'>
                    <div class='condition-label'>💧 Humidity</div>
                    <div class='condition-value'>{humidity}%</div>
                </div>
                <div class='condition-card' style='border-left: 4px solid #e74c3c;'>
                    <div class='condition-label'>🌡️ Pressure</div>
                    <div class='condition-value'>{pressure} hPa</div>
                </div>
                {wind_html}
                {visibility_html}
            </div>
        </div>
    """, unsafe_allow_html=True)


def display_forecast(forecast_data: Dict[str, Any], units: str, hours: int):
    """Display forecast data with clean styling."""
    entries_to_show = min(hours // 3, len(forecast_data["list"]))
    unit_symbol = "°C" if units == "metric" else "°F"

    st.subheader(f"📅 {hours}-Hour Detailed Forecast")

    # Group forecasts by day for better organization
    forecasts_by_day = {}
    for i, entry in enumerate(forecast_data["list"][:entries_to_show]):
        dt = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
        day_key = dt.strftime("%Y-%m-%d")

        if day_key not in forecasts_by_day:
            forecasts_by_day[day_key] = []
        forecasts_by_day[day_key].append(entry)

    for day_key, day_forecasts in forecasts_by_day.items():
        day_date = datetime.strptime(day_key, "%Y-%m-%d")
        st.markdown(f"#### {day_date.strftime('%A, %B %d')}")

        for entry in day_forecasts:
            dt_txt = entry["dt_txt"]
            temp = entry["main"]["temp"]
            temp_min = entry["main"]["temp_min"]
            temp_max = entry["main"]["temp_max"]
            weather = entry["weather"][0]["description"]
            weather_id = entry["weather"][0]["id"]
            icon = entry["weather"][0]["icon"]
            humidity = entry["main"]["humidity"]

            # Weather details
            wind_speed = entry.get("wind", {}).get("speed", 0)
            clouds = entry.get("clouds", {}).get("all", 0)
            pop = entry.get("pop", 0) * 100  # Probability of precipitation

            is_day = "d" in icon
            weather_emoji = get_weather_emoji(weather_id, icon, is_day)

            date_str, time_str = format_datetime(dt_txt)

            # Create forecast card
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <div style='font-size: 2.5rem;'>{weather_emoji}</div>
                    <div style='font-size: 0.8rem;'>{time_str}</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"**{temp:.1f}{unit_symbol}** - {weather.title()}")
                st.markdown(f"H: {temp_max:.0f}° L: {temp_min:.0f}° | 💧 {humidity}%")

            with col3:
                st.markdown(f"💨 {wind_speed:.1f} {'m/s' if units == 'metric' else 'mph'}")
                st.markdown(f"☁️ {clouds}%")
                if pop > 0:
                    st.markdown(f"☔ {pop:.0f}%")

            st.divider()


# Handle suggestion button clicks and reset functionality
suggestion_value = ""
if 'selected_suggestion' in st.session_state and st.session_state.selected_suggestion:
    suggestion_value = st.session_state.selected_suggestion
    st.session_state.selected_suggestion = None  # Clear the suggestion

# Main app content with location input
st.subheader("🔍 Enter a location")
location = st.text_input(
    "Location",
    value=suggestion_value,
    placeholder="e.g., New York, London, Tokyo, 10001, etc.",
    help="Enter a city name, zip code, or any location. You can also include country for better results (e.g., 'Paris, France')",
    key="location_text_input"
)

# Search suggestions
if not location or location.strip() == "":
    st.info("""
    👆 **Enter a location above to get started**
    
    You can search using:
    - **City names:** New York, London, Tokyo
    - **City with country:** Paris, France
    - **ZIP codes:** 10001, 90210
    - **Airport codes:** JFK, LAX
    - **Coordinates:** 40.7128,-74.0060
    """)

    # Location suggestions
    st.subheader("🌍 Popular Destinations")

    suggestions = [
        ("🗽", "New York", "New York, USA"),
        ("🏛️", "London", "London, GB"),
        ("🗼", "Tokyo", "Tokyo, Japan"),
        ("🥖", "Paris", "Paris, France"),
        ("🕌", "Istanbul", "Istanbul, Turkey"),
        ("🏖️", "Sydney", "Sydney, Australia"),
        ("🏔️", "Denver", "Denver, USA"),
        ("🌴", "Miami", "Miami, USA"),
        ("🍁", "Toronto", "Toronto, Canada"),
        ("🗻", "Zurich", "Zurich, Switzerland"),
        ("🏜️", "Dubai", "Dubai, UAE"),
        ("🎭", "Rio de Janeiro", "Rio de Janeiro, Brazil")
    ]

    # Create suggestion buttons in a grid
    cols = st.columns(4)
    for i, (emoji, city, full_name) in enumerate(suggestions):
        with cols[i % 4]:
            if st.button(f"{emoji} {city}", key=f"suggestion_{i}", help=f"Search for {full_name}"):
                st.session_state.selected_suggestion = full_name
                st.rerun()

    # Add some tips
    st.info("""
    💡 **Pro Tips:**
    - Include country names for better accuracy (e.g., "Birmingham, UK" vs "Birmingham, AL")
    - Use major landmarks or airports for quick access
    - ZIP codes work great for US locations
    - Weather data updates every 10 minutes
    """)

else:
    with st.spinner("🌐 Fetching weather data..."):
        # Get coordinates
        lat, lon, city, country, state = get_coordinates(location)

        if lat is not None and lon is not None:
            # Display current weather and forecast in tabs for better organization
            tab1, tab2, tab3 = st.tabs(["🌤️ Current Weather", "📅 Forecast", "📊 Details"])

            with tab1:
                # Get and display current weather
                current_weather = get_current_weather(lat, lon, units)
                if current_weather:
                    display_current_weather(current_weather, units, city, country, state)
                else:
                    st.error("❌ Could not retrieve current weather data. Please try again.")

            with tab2:
                # Get and display forecast
                forecast = get_forecast(lat, lon, units)
                if forecast:
                    display_forecast(forecast, units, forecast_hours)
                else:
                    st.error("❌ Could not retrieve forecast data. Please try again.")

            with tab3:
                if show_details and current_weather:
                    st.subheader("📊 Additional Information")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**🌅 Sun & Moon**")
                        if "sys" in current_weather:
                            sunrise = datetime.fromtimestamp(current_weather["sys"]["sunrise"])
                            sunset = datetime.fromtimestamp(current_weather["sys"]["sunset"])

                            st.write(f"🌅 Sunrise: **{sunrise.strftime('%I:%M %p')}**")
                            st.write(f"🌇 Sunset: **{sunset.strftime('%I:%M %p')}**")

                            # Check if it's currently day or night
                            now = datetime.now()
                            current_time = now.time()
                            sunrise_time = sunrise.time()
                            sunset_time = sunset.time()

                            if sunrise_time <= current_time <= sunset_time:
                                st.write("🌞 Currently: **Daytime**")
                            else:
                                st.write("🌙 Currently: **Nighttime**")

                    with col2:
                        st.markdown("**📍 Location Details**")
                        st.write(f"📍 Coordinates: **{lat:.4f}, {lon:.4f}**")
                        if "timezone" in current_weather:
                            timezone_offset = current_weather["timezone"]
                            offset_hours = timezone_offset // 3600
                            st.write(f"🕐 Timezone: **UTC{offset_hours:+d}**")

                else:
                    st.info("Enable 'Show detailed metrics' in the sidebar to see more information.")
        else:
            st.error("🔍 **Location not found.** Please try a different search term.")

            # Error help
            st.info("""
            ❓ **Need help finding your location?**
            
            Try these search formats:
            - **City names:** "Paris", "New York", "Tokyo"
            - **City with country:** "Paris, France" or "London, GB"
            - **US ZIP codes:** "10001", "90210", "60601"  
            - **Airport codes:** "JFK", "LAX", "LHR"
            - **State abbreviations:** "Miami, FL" or "Denver, CO"
            """)

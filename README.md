# 🌤️ Weather Forecast App

A beautiful, modern weather forecast application built with Streamlit and the OpenWeatherMap API. Get accurate weather forecasts for any location worldwide with a responsive design that works perfectly in both light and dark modes.

![Weather App Preview](https://img.shields.io/badge/Weather-Forecast-blue?style=for-the-badge&logo=weather&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![UV](https://img.shields.io/badge/UV-Package%20Manager-green?style=for-the-badge)

## ✨ Features

- **🌍 Global Coverage**: Get weather data for any location worldwide using OpenWeatherMap API
- **📱 Responsive Design**: Beautiful UI that works perfectly on desktop and mobile devices
- **🌙 Dark/Light Mode**: Automatic system theme detection with CSS variables and smooth transitions
- **📊 Detailed Forecasts**: 5-day/3-hour forecasts with comprehensive weather metrics
- **🎯 Current Weather**: Real-time weather conditions with detailed atmospheric data
- **⚡ Fast Performance**: Intelligent caching system with 5-minute TTL for optimal speed
- **🎨 Modern UI**: Clean, glassmorphism-inspired interface with weather-adaptive gradients
- **🆓 Open Source Icons**: Emoji-based weather icons with 200+ condition mappings (no external dependencies)
- **🔍 Smart Search**: Multiple location formats supported (city, ZIP, coordinates, airport codes)
- **📈 Weather Analysis**: Intelligent insights with sunrise/sunset times and atmospheric conditions
- **🎛️ Interactive Controls**: Tabbed interface with current weather, forecast, and detailed metrics
- **🌟 Location Suggestions**: Popular destination buttons with interactive search

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (recommended 3.13)
- [uv](https://docs.astral.sh/uv/) package manager
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd weather-forecast
   ```

2. **Install dependencies with uv**

   ```bash
   uv sync
   ```

3. **Set up your API key**

   Option A: Environment variable (recommended)

   ```bash
   # For Windows PowerShell
   $env:OPENWEATHER_API_KEY="your_api_key_here"

   # For Windows Command Prompt
   set OPENWEATHER_API_KEY=your_api_key_here

   # For Linux/macOS
   export OPENWEATHER_API_KEY="your_api_key_here"
   ```

   Option B: Create a `.env` file

   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

   Option C: Update `config.py` directly

   ```python
   OPENWEATHER_API_KEY = "your_api_key_here"
   ```

4. **Run the application**

   ```bash
   uv run streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 🎮 Usage

### Location Search

- **City names**: "New York", "London", "Tokyo"
- **City with country**: "Paris, France", "Birmingham, UK"
- **ZIP codes**: "10001", "90210"
- **Airport codes**: "JFK", "LAX", "LHR"
- **Coordinates**: "40.7128,-74.0060"

### Features

- Choose temperature units (Celsius/Fahrenheit)
- Select forecast period (24-120 hours)
- Toggle detailed metrics
- Automatic theme detection with CSS variables
- Popular location suggestions with emoji icons
- Tabbed interface for organized content
- Reset functionality to clear data
- Real-time data caching for performance

## 🛠️ Development

### Project Structure

```
weather-forecast/
├── app.py              # Main Streamlit application
├── config.py           # Configuration and API settings
├── demo.py             # Demo script and API testing
├── main.py             # Entry point script
├── pyproject.toml      # Project dependencies and settings
├── uv.lock            # Locked dependency versions
├── README.md          # This file
├── IMPROVEMENTS.md    # Detailed improvement summary
├── .streamlit/        # Streamlit configuration
│   └── config.toml    # Theme and app settings
├── .vscode/           # VS Code settings
│   └── tasks.json     # Development tasks
├── .env               # Environment variables (create this)
└── __pycache__/       # Python cache files
```

### Development Setup

1. **Install development dependencies**

   ```bash
   uv sync --dev
   ```

2. **Run with development settings**

   ```bash
   uv run streamlit run app.py --server.runOnSave true
   ```

3. **Code formatting and linting**
   ```bash
   uv run black .
   uv run isort .
   uv run ruff check .
   uv run mypy .
   ```

### Available Tasks

- **Run app**: `uv run streamlit run app.py`
- **Development mode**: Use VS Code task "Run Streamlit Weather App"
- **Test API**: `uv run python demo.py`

## 🎨 Design Features

### Modern UI Elements

- **Google Fonts**: Professional Inter typography
- **Glassmorphism**: Backdrop blur effects
- **Smooth Animations**: Hover effects and transitions
- **Responsive Grid**: Mobile-first design approach
- **Color Harmony**: Consistent color palette

### Dark/Light Mode

- **Automatic Detection**: System preference detection
- **CSS Variables**: Consistent theming approach
- **Smooth Transitions**: Seamless theme switching
- **High Contrast**: Accessibility-focused design

### Weather Icons

- **Free & Open Source**: Emoji-based system
- **No Dependencies**: Works offline
- **Comprehensive**: 200+ weather condition codes
- **Consistent Style**: Professional appearance

## 📦 Dependencies

### Core Dependencies

- **Streamlit**: Modern web app framework
- **Requests**: HTTP library for API calls
- **Pandas**: Data manipulation (future enhancements)
- **Plotly**: Interactive charts (future enhancements)

### Development Dependencies

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast Python linter
- **MyPy**: Type checking
- **Pytest**: Testing framework

## 🌐 API Information

This app uses the [OpenWeatherMap API](https://openweathermap.org/api):

- **Current Weather API**: Real-time weather data
- **5 Day / 3 Hour Forecast API**: Extended forecasts
- **Geocoding API**: Location coordinate resolution

**Free tier includes:**

- 1,000 API calls per day
- Current weather data
- 5-day/3-hour forecasts
- Geocoding services

## 🚀 Deployment

### Streamlit Community Cloud

1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Set `OPENWEATHER_API_KEY` in Streamlit secrets
4. Deploy!

### Other Platforms

The app works on any platform that supports Python and Streamlit:

- **Heroku**: Cloud application platform
- **Railway**: Modern app hosting
- **Render**: Unified cloud platform
- **DigitalOcean App Platform**: Developer-friendly cloud
- **AWS Lambda**: Serverless deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests and linting: `uv run pytest && uv run black . && uv run mypy .`
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for the weather API
- [Streamlit](https://streamlit.io/) for the amazing framework
- [Astral](https://astral.sh/) for the fast uv package manager
- [Unicode Consortium](https://unicode.org/) for emoji weather icons

## 🆕 Recent Improvements

- ✅ **Free weather icons** using emojis (no external dependencies)
- ✅ **Enhanced dark/light mode** with automatic system detection
- ✅ **Modern responsive design** with smooth animations
- ✅ **Professional code structure** with type hints and error handling
- ✅ **Better location search** with smart suggestions and popular destinations
- ✅ **Improved performance** with optimized caching and 5-minute TTL
- ✅ **Updated dependencies** using modern UV package manager
- ✅ **Tabbed interface** for better organization (Current, Forecast, Details)
- ✅ **Enhanced error handling** with helpful user feedback
- ✅ **Weather-adaptive gradients** that change based on conditions
- ✅ **Comprehensive weather mapping** for 200+ weather condition codes
- ✅ **Wind direction compass** and atmospheric data display
- ✅ **Sunrise/sunset information** with day/night detection
- ✅ **Reset functionality** to clear data and return to home screen

## 📞 Support

If you have questions or run into issues:

1. Check the [Improvements Documentation](IMPROVEMENTS.md)
2. Review the [Issues](../../issues) page
3. Check [OpenWeatherMap API documentation](https://openweathermap.org/api)
4. Review [Streamlit documentation](https://docs.streamlit.io/)

---

**Made with ❤️ and 🌤️ | Powered by OpenWeatherMap API**

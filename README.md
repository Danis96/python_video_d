# Facebook Video Scraper

Advanced Facebook video scraper with enhanced title extraction and flexible scrolling options.

## ✨ Features

- 🎯 **Enhanced Title Extraction**: Extracts proper episode titles like "Draga mama 218. 'Oni što ostaju i oni što odlaze'"
- 🔄 **Flexible Scrolling**: Choose number of scrolls or scroll to bottom for ALL videos
- 🤖 **Stealth Mode**: Undetected Chrome browsing with advanced evasion techniques
- 📊 **Comprehensive Data**: Extracts titles, dates, likes, comments, and video URLs
- 💾 **JSON Output**: Clean, structured data export
- 🎮 **Multiple Interfaces**: Command line, interactive runner, or direct Python usage

## 🚀 Quick Start

### Method 1: Interactive Runner (Recommended)
```bash
python run_scraper.py
```
Follow the prompts to choose scroll mode and target URL.

### Method 2: Command Line
```bash
# Scroll to bottom (get ALL videos)
python facebook_video_scraper.py --scrolls MAX

# Limited scrolls (faster)
python facebook_video_scraper.py --scrolls 10

# Custom URL with 20 scrolls
python facebook_video_scraper.py --scrolls 20 --url "https://www.facebook.com/ANOTHER_PAGE/videos"
```

### Method 3: Python Script
```python
from facebook_video_scraper import FacebookVideoScraper

scraper = FacebookVideoScraper()

# Scroll to bottom (get ALL videos)
scraper.run_scraper(scroll_count="MAX")

# Limited scrolls
scraper.run_scraper(scroll_count="15")
```

## 📜 Scroll Options

| Option | Description | Speed | Coverage |
|--------|-------------|-------|----------|
| `MAX` | Scroll to absolute bottom | Slower | ALL videos |
| `5` | 5 scrolls | Fast | ~20-30 videos |
| `10` | 10 scrolls | Medium | ~40-60 videos |
| `20` | 20 scrolls | Medium-Slow | ~80-120 videos |

## ⚙️ Configuration

Edit `facebook_config.env`:

```env
# Facebook Login Credentials
FACEBOOK_EMAIL=your_email@gmail.com
FACEBOOK_PASSWORD=your_password

# Chrome Driver Configuration
CHROME_DRIVER_PATH=

# Scrolling Configuration
SCROLL_PAUSE_TIME=3
MAX_SCROLL_ATTEMPTS=50
DEFAULT_SCROLL_MODE=MAX

# Output Configuration
OUTPUT_FILE=facebook_videos.json
```

## 📊 Output Format

The scraper generates `facebook_videos.json` with this structure:

```json
{
  "total_videos": 99,
  "scraping_timestamp": "1750241314",
  "videos": [
    {
      "id": "595328265177242",
      "title": "Draga mama 218. \"Oni što ostaju i oni što odlaze\"",
      "url": "https://www.facebook.com/watch/?v=595328265177242",
      "date": "3 years ago",
      "likes": 0,
      "comments": 0,
      "shares": 0,
      "views": "",
      "description": "",
      "timestamp": "1750241314"
    }
  ]
}
```

## 🎯 Usage Examples

### Get ALL videos (thorough scraping)
```bash
python run_scraper.py
# Choose option 1 (MAX scrolls)
```

### Quick sampling (first few videos)
```bash
python facebook_video_scraper.py --scrolls 5
```

### Specific page with custom scrolls
```bash
python facebook_video_scraper.py --scrolls 15 --url "https://www.facebook.com/SOME_PAGE/videos"
```

## 🛠️ Requirements

- Python 3.7+
- Chrome browser
- Required packages: `selenium`, `beautifulsoup4`, `webdriver-manager`, `python-dotenv`

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure credentials
cp facebook_config.env.example facebook_config.env
# Edit facebook_config.env with your credentials

# Run scraper
python run_scraper.py
```

## ⚠️ Disclaimer

This tool is for educational purposes only. Use only on content you own or have permission to access. Respect Facebook's Terms of Service and rate limits.

## 🎮 Lord Danis Edition

Enhanced with advanced title extraction specifically optimized for "Draga mama" episode series with proper Serbian/Croatian character support. 
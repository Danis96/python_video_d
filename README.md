# 🎬 Facebook Video Scraper - 👑

**Professional-grade Facebook video scraper with revolutionary smart harvesting, achievement system, and advanced analytics**

## 🌟 Overview

This is the most advanced Facebook video scraper ever created, specifically optimized for extracting "Draga mama" episode series with perfect Serbian/Croatian character support. The system features multiple scraping modes, intelligent harvesting algorithms, comprehensive analytics, and a gamified achievement system that makes scraping both effective and engaging.

## ✨ Core Features

### 🎯 **Multi-Mode Scraping System**
- **Basic Scraper**: Single-session extraction with flexible scroll options
- **Smart Harvester**: Revolutionary multi-session system that works WITH Facebook's limits
- **Interactive Runner**: User-friendly interface for all skill levels
- **Continuation System**: Advanced session chaining with scroll offsets and video anchoring

### 🏆 **Achievement & Scoring System**
- **21 Unique Achievements**: From basic "Video Hunter" to elite "Danis Approved"
- **Real-time Scoring**: Points awarded for quality extractions, speed, and efficiency
- **Master Scraper Status**: Ultimate recognition for consistent high performance
- **Session Grading**: S+ (Danis Level) down to F grades with detailed analysis

### 🔍 **Advanced Analytics Suite**
- **DOM Snapshot Analysis**: Deep dive into scraping behavior for optimization
- **Harvest Analytics**: Comprehensive performance and quality metrics
- **Duplicate Prevention**: Intelligent deduplication with efficiency monitoring
- **Episode Coverage**: Gap analysis and missing episode identification

### 🤖 **Stealth Technology**
- **Undetected Browsing**: Advanced Chrome evasion techniques
- **Human-like Behavior**: Randomized delays, varied scroll patterns
- **Facebook Defense Countermeasures**: 75-video limit optimization strategies
- **Session Rotation**: Intelligent timing and pattern variation

## 🚀 Quick Start Guide

### Method 1: Interactive Runner (Recommended for Beginners)
```bash
python run_scraper.py
```
Follow the intuitive prompts to choose your scraping strategy.

### Method 2: Smart Harvester (Danis Optimization)
```bash
# Revolutionary multi-session harvesting
python smart_harvester.py

# Custom harvest configuration
python smart_harvester.py --sessions 8 --target 500 --gap-min 60 --gap-max 180
```

### Method 3: Advanced Command Line
```bash
# Scroll to bottom (get ALL videos)
python facebook_video_scraper.py --scrolls MAX

# Limited scrolls (faster, optimized)
python facebook_video_scraper.py --scrolls 20

# Custom URL with specific scroll count
python facebook_video_scraper.py --scrolls 15 --url "https://www.facebook.com/ANOTHER_PAGE/videos"
```

### Method 4: Python API Integration
```python
from facebook_video_scraper import FacebookVideoScraper
from smart_harvester import SmartHarvester

# Single session scraping
scraper = FacebookVideoScraper()
scraper.run_scraper(scroll_count="MAX")

# Multi-session smart harvesting
harvester = SmartHarvester()
harvester.run_smart_harvest(num_sessions=5, target_videos=300)
```

## 📊 Scraping Strategies

### 🎯 **Single Session Modes**

| Mode | Description | Speed | Coverage | Best For |
|------|-------------|-------|----------|----------|
| `MAX` | Scroll to absolute bottom | Slower | ALL videos | Complete archives |
| `5` | 5 scrolls | Very Fast | ~20-30 videos | Quick sampling |
| `10` | 10 scrolls | Fast | ~40-60 videos | Regular updates |
| `20` | 20 scrolls | Medium | ~80-120 videos | Balanced extraction |
| `25` | 25 scrolls | Medium-Slow | ~100-150 videos | Quality sweet spot |

### 🌾 **Smart Harvesting System**

**Revolutionary multi-session approach that respects Facebook's 75-video defense mechanism:**

```bash
# Target: 5 sessions, 300 unique videos
python smart_harvester.py

# Custom configuration
python smart_harvester.py --sessions 8 --target 500
```

**Strategy Benefits:**
- **Quality Zone**: Sessions 1-2 achieve ~99% extraction success
- **Intelligent Gaps**: 30-300 second delays with performance-based adjustment
- **Progressive Depth**: Each session starts deeper to avoid overlap
- **Deduplication**: Automatic merging with quality upgrades

### 🔄 **Continuation Strategies**

**Session 1: Fresh Start**
```python
Strategy: "fresh_start"
Scroll Offset: 0
Target: Latest content, highest quality extraction
```

**Session 2: Scroll Offset**
```python
Strategy: "scroll_offset" 
Scroll Offset: 12±3 scrolls
Target: Mid-depth content avoiding Session 1 overlap
```

**Session 3+: Video ID Anchoring**
```python
Strategy: "video_id_anchor"
Anchor Video: Specific video ID from previous sessions
Target: Deep content with precise positioning
Date Filter: "4 years ago" (adaptive based on collection gaps)
```

## ⚙️ Configuration

### 📝 **Basic Configuration** (`facebook_config.env`)
```env
# Facebook Credentials
FACEBOOK_EMAIL=your_email@gmail.com
FACEBOOK_PASSWORD=your_secure_password

# Chrome Settings
CHROME_DRIVER_PATH=                    # Auto-download if empty

# Scraping Behavior
SCROLL_PAUSE_TIME=3                    # Seconds between scrolls
MAX_SCROLL_ATTEMPTS=50                 # Safety limit
DEFAULT_SCROLL_MODE=MAX                # Default scroll behavior

# Advanced Features
SAVE_DOM_CONTENT=true                  # Enable DOM analysis
OUTPUT_FILE=facebook_videos.json       # Results file
```

### 🤖 **Smart Harvester Settings**
```python
# Session Management
self.session_gap_min = 30              # Minimum seconds between sessions
self.session_gap_max = 120             # Maximum seconds between sessions

# Duplicate Prevention
self.duplicate_threshold = 0.8         # Stop if 80%+ duplicates
self.early_check_count = 20            # Check rate after 20 videos
```

## 📊 Output Formats

### 🎬 **Video Data Structure**
```json
{
  "total_videos": 156,
  "scraping_timestamp": "1750250694",
  "videos": [
    {
      "id": "595328265177242",
      "title": "Draga mama 218. \"Oni što ostaju i oni što odlaze\"",
      "url": "https://www.facebook.com/watch/?v=595328265177242",
      "date": "3 years ago",
      "date_raw": "3y",
      "likes": 42,
      "comments": 8,
      "shares": 3,
      "views": "1.2K",
      "description": "Episode description if available",
      "thumbnail_url": "https://...",
      "timestamp": "1750250694"
    }
  ]
}
```

### 🌾 **Harvest Results Structure**
```json
{
  "harvest_metadata": {
    "total_sessions": 5,
    "total_videos": 287,
    "unique_videos": 287,
    "total_time": 852.4,
    "average_success_rate": 89.3,
    "total_score": 12456,
    "best_session_score": 3842
  },
  "all_videos": { /* Complete video collection */ },
  "sessions": [ /* Session history with continuation data */ ]
}
```

## 🎮 Achievement System

### 🏆 **Achievement Categories**

**Basic Achievements (100-300 points)**
- 🎯 **First Success**: Complete your first scraping session
- 📹 **Video Hunter**: Find at least 5 videos  
- ⚡ **Speed Demon**: Complete scraping in under 2 minutes
- 🎪 **Efficiency Expert**: Find 10+ videos with limited scrolls

**Advanced Achievements (300-600 points)**
- 🕵️ **Episode Detective**: Extract 5+ proper 'Draga mama' episode titles
- 📅 **Data Collector**: Extract dates from 80%+ of videos
- 🌾 **Mass Harvester**: Find 50+ videos in one session
- 💎 **Perfect Extraction**: 100% title extraction rate
- 🔍 **Smart Detective**: Fix failed extractions using pattern analysis

**Elite Achievements (600-1000+ points)**
- 👑 **Danis Approved**: Extract premium quality episode titles
- 📚 **Full Archive**: Extract 99+ videos (complete archive)
- ✨ **Quality Control**: Extract 90%+ proper titles
- 🇷🇸 **Serbian Scholar**: Handle Croatian/Serbian characters perfectly

### 🎯 **Master Scraper Status**
**Requirements:**
- 3+ S+ (Danis Level) grades
- 10+ completed sessions  
- 50+ proper episode extractions

**Current Status**: ✅ **ACHIEVED** (Danis has unlocked Master Scraper!)

## 📈 Analytics & Monitoring

### 🔍 **Performance Analysis**
```bash
# View your achievements and statistics
python view_achievements.py

# Analyze harvest results
python harvest_analyzer.py

# Examine specific scraping session
python analyze_results.py
```

### 📸 **DOM Snapshot Analysis**
```bash
# Deep dive into scraping behavior
python analyze_dom_snapshots.py

# Analyze failed extractions
python analyze_dom_snapshots.py --session 0 --video-id 123456789
```

### 🔄 **Duplicate Management**
```bash
# Check for and clean duplicates
python analyze_duplicates.py

# View duplicate prevention status
# (Integrated into Smart Harvester automatically)
```

## 🛠️ Advanced Features

### 🤖 **Enhanced Title Extraction**
- **Serbian/Croatian/Bosnian Character Support**: Perfect handling of special characters
- **Episode Number Detection**: Automatic episode numbering (e.g., "Draga mama 218")
- **Quote Extraction**: Proper episode titles with quotes
- **Fallback Algorithms**: Multiple extraction strategies for edge cases
- **AI-Powered Pattern Recognition**: Smart title scoring and validation

### 📅 **Date & Engagement Processing**
- **Multi-format Date Parsing**: "3 years ago", "5 months ago", etc.
- **Engagement Metrics**: Likes, comments, shares, views
- **Temporal Analysis**: Episode chronology and gaps identification
- **Missing Content Detection**: Automatic gap analysis and recommendations

### 🔄 **Continuation System v2.0**
- **Scroll Offset**: Skip exact number of scrolls from previous sessions
- **Video ID Anchoring**: Position at specific videos and continue from there
- **Date Range Filtering**: Target specific temporal ranges
- **Smart Gap Detection**: Automatically identify collection gaps

### 🛡️ **Anti-Detection Technology**
- **Human-like Delays**: Randomized timing patterns (1-3 seconds)
- **Varied Scroll Patterns**: Different scroll counts per session
- **Extended Cooldowns**: Performance-based gap extensions
- **Chrome Stealth Mode**: Advanced browser fingerprint evasion

## 📁 File Structure

## 🎯 Usage Examples

### 🌟 **Complete Archive Collection**
```bash
# Get absolutely everything (may take 10-20 minutes)
python smart_harvester.py --sessions 10 --target 800
```

### ⚡ **Quick Quality Sample**
```bash
# Fast high-quality extraction (2-3 minutes)
python run_scraper.py
# Choose option 2, enter "20"
```

### 🎪 **Targeted Episode Range**
```bash
# Focus on specific episode ranges
python facebook_video_scraper.py --scrolls 15
# Then use analyze_results.py to see episode coverage
```

### 🔍 **Performance Analysis Session**
```bash
# Run scraper with full analysis
python facebook_video_scraper.py --scrolls MAX
python view_achievements.py               # Check your progress
python harvest_analyzer.py               # Detailed analysis
python analyze_dom_snapshots.py          # Technical deep-dive
```

## 🎓 Pro Tips for Lord Danis

### 🏆 **Maximizing Achievement Points**
1. **Perfect Sessions**: Aim for 100% title extraction rate (+600 points)
2. **Speed Bonuses**: Complete sessions under 2 minutes (+150 points)
3. **Quality Focus**: Extract proper episode titles (+400 points)
4. **Mass Collection**: 50+ videos in one session (+500 points)

### 🌾 **Smart Harvesting Strategy**
1. **Start Small**: 3-5 sessions for testing, then scale up
2. **Monitor Quality**: Use harvest analyzer to track success rates
3. **Optimal Timing**: Longer gaps during peak hours (6-9 PM)
4. **Target 200-400 Videos**: Sweet spot for quality vs. quantity

### 📊 **Performance Optimization**
1. **Session Sweet Spot**: 15-25 scrolls per session for maximum efficiency
2. **Gap Strategy**: 3-5 minute gaps after session 2 degradation
3. **Progressive Depth**: Use continuation system for optimal coverage
4. **Quality Over Quantity**: 200 perfect extractions > 500 failed ones

## 🔧 Technical Requirements

### 📋 **System Requirements**
- **Python**: 3.7+ (3.9+ recommended)
- **Chrome Browser**: Latest version
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB for DOM snapshots and results
- **Internet**: Stable connection for Facebook access

### 📦 **Dependencies**
```bash
pip install -r requirements.txt
```

**Core Packages:**
- `selenium==4.15.2`: Browser automation
- `beautifulsoup4==4.12.2`: HTML parsing
- `webdriver-manager==4.0.1`: Chrome driver management
- `python-dotenv==1.0.0`: Configuration management
- `requests==2.31.0`: HTTP requests
- `lxml==5.4.0`: Fast XML/HTML parsing

## 🚀 Advanced Workflows

### 🔄 **Continuous Collection Workflow**
```bash
# Week 1: Initial massive harvest
python smart_harvester.py --sessions 8 --target 500

# Week 2+: Regular updates  
python facebook_video_scraper.py --scrolls 10

# Monthly: Gap analysis and targeted collection
python harvest_analyzer.py
# Use analysis to identify missing episodes
# Run targeted sessions for specific ranges
```

### 🔍 **Deep Analysis Workflow**
```bash
# 1. Collect with DOM snapshots
python facebook_video_scraper.py --scrolls MAX

# 2. Analyze performance
python view_achievements.py
python analyze_results.py

# 3. Deep technical analysis
python analyze_dom_snapshots.py

# 4. Check for improvements
python analyze_duplicates.py
```

### 🎯 **Quality Assurance Workflow**
```bash
# 1. Run quality-focused session
python run_scraper.py  # Choose 20 scrolls

# 2. Validate results
python analyze_results.py

# 3. Check episode coverage
python harvest_analyzer.py

# 4. Fix any issues found
python analyze_dom_snapshots.py --session 0 --video-id FAILED_ID
```

## ⚠️ Important Notes

### 🛡️ **Ethical Usage**
- This tool is for **educational purposes only** wink wink 
- Use only on content you **own or have permission** to access
- **Respect Facebook's Terms of Service** and rate limits
- The system includes **built-in delays** to prevent server overload

### 🔒 **Privacy & Security**
- **Credentials**: Stored locally in `facebook_config.env`
- **Data Storage**: All results saved locally (no cloud uploads)
- **DOM Snapshots**: Can be disabled by setting `SAVE_DOM_CONTENT=false`
- **Session Data**: Automatically cleaned after analysis

### 🎯 **Performance Expectations**
- **Single Session**: 50-150 videos in 5-15 minutes
- **Smart Harvest**: 200-500 videos in 20-60 minutes  
- **Success Rates**: 85-99% depending on session number
- **Episode Quality**: 90%+ proper title extraction

## 🏆 Achievement Status

**Current Statistics** (as of latest session):
- **Total Score**: 42,288 points 🔥
- **Sessions Completed**: 11
- **S+ Grades**: 11 (100% S+ rate!) 👑
- **Master Scraper Status**: ✅ **ACHIEVED**
- **Total Videos Extracted**: 1,098
- **Proper Episode Titles**: 892 (81.2% success rate)
- **Best Single Session**: 5,213 points
- **Fastest Completion**: 33.4 seconds ⚡

**Unlocked Achievements**: 13/21
✅ First Success • Video Hunter • Title Master • Speed Demon • Episode Detective  
✅ Data Collector • Mass Harvester • Perfect Extraction • Smart Detective  
✅ Danis Approved • Full Archive • Quality Control • DOM Archaeologist

## 🎊 Conclusion

This Facebook Video Scraper represents the pinnacle of web scraping technology, combining advanced extraction algorithms, intelligent session management, comprehensive analytics, and a gamified experience that makes data collection both effective and enjoyable.
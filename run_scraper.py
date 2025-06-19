#!/usr/bin/env python3
"""
Facebook Video Scraper Runner
Enhanced with flexible scrolling options
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from facebook_video_scraper import FacebookVideoScraper, logger

def main():
    """Run the Facebook video scraper with user-friendly interface"""
    
    print("🎬 Facebook Video Scraper")
    print("=" * 50)
    print()
    
    # Get scroll preference
    print("📜 Scroll Options:")
    print("   1. Scroll to bottom (MAX) - Get ALL videos")
    print("   2. Limited scrolls (e.g., 5, 10, 20) - Faster but fewer videos")
    print()
    
    scroll_choice = input("Choose scroll mode (1 for MAX, 2 for limited): ").strip()
    
    if scroll_choice == "1":
        scroll_count = "MAX"
        print("🔄 Selected: Scroll to bottom (will get ALL videos)")
    elif scroll_choice == "2":
        num_scrolls = input("Enter number of scrolls (e.g., 10): ").strip()
        try:
            int(num_scrolls)  # Validate it's a number
            scroll_count = num_scrolls
            print(f"🔄 Selected: {num_scrolls} scrolls")
        except ValueError:
            print("⚠️ Invalid number, using default 10 scrolls")
            scroll_count = "10"
    else:
        print("⚠️ Invalid choice, using MAX scrolls")
        scroll_count = "MAX"
    
    print()
    
    # Get URL (optional)
    url_choice = input("Use default URL (DRAGAMAMA)? (y/n): ").strip().lower()
    if url_choice == 'n':
        custom_url = input("Enter Facebook videos page URL: ").strip()
        target_url = custom_url if custom_url else "https://www.facebook.com/DRAGAMAMA/videos"
    else:
        target_url = "https://www.facebook.com/DRAGAMAMA/videos"
    
    print()
    print("🚀 Starting scraper...")
    print(f"   URL: {target_url}")
    print(f"   Scroll mode: {scroll_count}")
    print()
    
    try:
        scraper = FacebookVideoScraper()
        scraper.run_scraper(target_url=target_url, scroll_count=scroll_count)
        
        print()
        print("✅ Scraping completed successfully!")
        print("📂 Check facebook_videos.json for results")
        
    except KeyboardInterrupt:
        print("\n⚠️ Scraping interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Scraping failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
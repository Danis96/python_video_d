#!/usr/bin/env python3
"""
Analyze Facebook Video Scraper Results
"""
import json

def analyze_results():
    # Load the scraped data
    with open('facebook_videos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    videos = data['videos']
    print(f'🎬 FACEBOOK VIDEO SCRAPER RESULTS')
    print(f'=' * 50)
    print(f'Total Videos Found: {len(videos)}')
    print(f'Scraping Timestamp: {data["scraping_timestamp"]}')
    print()

    # Count videos with proper titles vs default titles
    proper_titles = [v for v in videos if not v['title'].startswith('DRAGAMAMA_Video_')]
    default_titles = [v for v in videos if v['title'].startswith('DRAGAMAMA_Video_')]

    print(f'📝 TITLE ANALYSIS:')
    print(f'   Videos with proper titles: {len(proper_titles)}')
    print(f'   Videos with default titles: {len(default_titles)}')
    print()

    if proper_titles:
        print(f'🏆 VIDEOS WITH EXTRACTED TITLES:')
        for i, video in enumerate(proper_titles[:10]):
            print(f'   {i+1}. {video["title"]}')
            print(f'      ID: {video["id"]}')
            print(f'      URL: {video["url"]}')
            print()

    print(f'🔢 SAMPLE VIDEO IDS (first 10):')
    for i, video in enumerate(videos[:10]):
        status = '✅ TITLE' if not video['title'].startswith('DRAGAMAMA_Video_') else '⚠️  DEFAULT'
        print(f'   {i+1}. {video["id"]} - {status}')
    print()

    print(f'📊 ENGAGEMENT DATA:')
    videos_with_likes = [v for v in videos if v['likes'] > 0]
    videos_with_dates = [v for v in videos if v['date']]
    print(f'   Videos with likes: {len(videos_with_likes)}')
    print(f'   Videos with dates: {len(videos_with_dates)}')
    print()

    # Show last 5 video IDs to see the range
    print(f'🔚 LAST 5 VIDEO IDS:')
    for i, video in enumerate(videos[-5:], len(videos)-4):
        status = '✅ TITLE' if not video['title'].startswith('DRAGAMAMA_Video_') else '⚠️  DEFAULT'
        print(f'   {i}. {video["id"]} - {status}')

if __name__ == "__main__":
    analyze_results() 
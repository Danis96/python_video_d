#!/usr/bin/env python3
"""
Harvest Results Duplicate Analyzer and Cleaner
Analyzes and removes duplicates from harvest_results.json
Author: Lord Danis Assistant
"""

import json
import os
from typing import Dict, List
from datetime import datetime

def analyze_harvest_duplicates(file_path: str = "harvest_results.json") -> Dict:
    """Analyze duplicates in harvest results"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    analysis = {
        'total_videos': len(data.get('all_videos', {})),
        'sessions': len(data.get('sessions', [])),
        'metadata_unique_count': data.get('harvest_metadata', {}).get('unique_videos', 0),
        'metadata_total_count': data.get('harvest_metadata', {}).get('total_videos', 0),
        'video_ids': list(data.get('all_videos', {}).keys()),
        'potential_duplicates': []
    }
    
    # Check for potential issues
    videos = data.get('all_videos', {})
    
    # Since all_videos is a dictionary with video_id as keys, 
    # duplicates would be impossible at this level
    print("📊 HARVEST RESULTS DUPLICATE ANALYSIS")
    print("=" * 50)
    print(f"📹 Total videos in all_videos: {analysis['total_videos']}")
    print(f"📊 Sessions recorded: {analysis['sessions']}")
    print(f"🔢 Metadata unique count: {analysis['metadata_unique_count']}")
    print(f"🔢 Metadata total count: {analysis['metadata_total_count']}")
    print("")
    
    # Check for discrepancies
    if analysis['total_videos'] != analysis['metadata_unique_count']:
        print("⚠️ DISCREPANCY DETECTED:")
        print(f"   all_videos count ({analysis['total_videos']}) != metadata unique_videos ({analysis['metadata_unique_count']})")
        print("")
    
    # Look for videos with similar titles (potential content duplicates)
    title_groups = {}
    for video_id, video_data in videos.items():
        title = video_data.get('title', '').strip()
        if title not in title_groups:
            title_groups[title] = []
        title_groups[title].append(video_id)
    
    # Find titles with multiple videos
    duplicate_titles = {title: ids for title, ids in title_groups.items() if len(ids) > 1}
    
    if duplicate_titles:
        print("🔍 VIDEOS WITH IDENTICAL TITLES:")
        for title, video_ids in duplicate_titles.items():
            print(f"   '{title}' → {len(video_ids)} videos: {video_ids}")
            analysis['potential_duplicates'].extend(video_ids[1:])  # Keep first, mark others as duplicates
        print("")
    else:
        print("✅ No videos with identical titles found")
        print("")
    
    return analysis

def clean_harvest_duplicates(file_path: str = "harvest_results.json", backup: bool = True) -> bool:
    """Clean duplicates from harvest results"""
    
    if backup:
        backup_file = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with open(file_path, 'r', encoding='utf-8') as src:
            with open(backup_file, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        print(f"💾 Backup created: {backup_file}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    original_count = len(data.get('all_videos', {}))
    videos = data.get('all_videos', {})
    
    # Find videos with identical titles
    title_to_video = {}
    duplicates_to_remove = []
    
    for video_id, video_data in videos.items():
        title = video_data.get('title', '').strip()
        
        if title in title_to_video:
            # This title already exists, decide which one to keep
            existing_id = title_to_video[title]
            existing_video = videos[existing_id]
            
            # Keep the one with better data (more engagement, better date, etc.)
            keep_current = False
            
            # Prefer video with engagement data
            if video_data.get('likes', 0) > existing_video.get('likes', 0):
                keep_current = True
            elif video_data.get('date') and not existing_video.get('date'):
                keep_current = True
            elif len(video_data.get('title', '')) > len(existing_video.get('title', '')):
                keep_current = True
            
            if keep_current:
                duplicates_to_remove.append(existing_id)
                title_to_video[title] = video_id
            else:
                duplicates_to_remove.append(video_id)
        else:
            title_to_video[title] = video_id
    
    # Remove duplicates
    for video_id in duplicates_to_remove:
        del videos[video_id]
    
    # Update metadata
    new_count = len(videos)
    data['harvest_metadata']['unique_videos'] = new_count
    data['harvest_metadata']['total_videos'] = new_count
    data['harvest_metadata']['last_cleanup'] = datetime.now().isoformat()
    
    # Save cleaned data
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"🧹 CLEANUP COMPLETE:")
    print(f"   Original videos: {original_count}")
    print(f"   Duplicates removed: {len(duplicates_to_remove)}")
    print(f"   Final unique videos: {new_count}")
    
    if duplicates_to_remove:
        print(f"   Removed video IDs: {duplicates_to_remove[:5]}{'...' if len(duplicates_to_remove) > 5 else ''}")
    
    return len(duplicates_to_remove) > 0

if __name__ == "__main__":
    print("🔍 Analyzing harvest results for duplicates...")
    analysis = analyze_harvest_duplicates()
    
    if analysis.get('potential_duplicates'):
        print(f"\n🧹 Found {len(analysis['potential_duplicates'])} potential duplicates")
        response = input("Would you like to clean duplicates? (y/n): ").lower().strip()
        
        if response == 'y':
            success = clean_harvest_duplicates()
            if success:
                print("✅ Duplicates cleaned successfully!")
            else:
                print("ℹ️ No duplicates were removed")
        else:
            print("❌ Cleanup cancelled")
    else:
        print("✅ No duplicates found!") 
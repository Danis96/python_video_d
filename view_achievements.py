#!/usr/bin/env python3
"""
Achievement Viewer for Lord Danis
View your scraping achievements, statistics, and progress
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

def load_achievements() -> Dict[str, Any]:
    """Load achievements from file"""
    achievements_file = "achievements.json"
    
    if not os.path.exists(achievements_file):
        print("❌ No achievements file found. Run the scraper first!")
        return {}
    
    try:
        with open(achievements_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading achievements: {e}")
        return {}

def display_lord_danis_status(data: Dict[str, Any]) -> None:
    """Display Lord Danis special status and recognition"""
    lord_danis = data.get('lord_danis_achievements', {})
    
    print("\n" + "="*60)
    print("👑 === LORD DANIS ACHIEVEMENT STATUS ===")
    print("="*60)
    
    # Master Scraper Status
    if lord_danis.get('master_scraper_status', False):
        print("🏆 STATUS: MASTER SCRAPER ACHIEVED! 🏆")
        print("   You have proven yourself worthy of the title!")
    else:
        print("📈 STATUS: Working towards Master Scraper")
        print("   Requirements: 3+ S+ grades, 10+ sessions, 50+ proper episodes")
    
    print(f"📊 S+ (Lord Danis Level) Grades: {lord_danis.get('s_plus_grades', 0)}")
    print(f"💎 Perfect Sessions: {lord_danis.get('perfect_sessions', 0)}")
    print(f"🔥 Consecutive Quality Runs: {lord_danis.get('consecutive_quality_runs', 0)}")

def display_achievements_gallery(data: Dict[str, Any]) -> None:
    """Display all achievements in a beautiful gallery format"""
    print("\n" + "="*60)
    print("🏆 === ACHIEVEMENTS GALLERY ===")
    print("="*60)
    
    # Define all possible achievements (from the scraper)
    all_achievements = [
        ("🎯", "First Success", "Complete your first scraping session", 100),
        ("📹", "Video Hunter", "Find at least 5 videos", 50),
        ("📝", "Title Master", "Extract proper episode titles", 200),
        ("⚡", "Speed Demon", "Complete scraping in under 2 minutes", 150),
        ("🎪", "Efficiency Expert", "Find 10+ videos with limited scrolls", 300),
        ("🕵️", "Episode Detective", "Extract 5+ proper 'Draga mama' episode titles", 400),
        ("📅", "Data Collector", "Extract dates from 80%+ of videos", 250),
        ("👍", "Engagement Finder", "Find likes/engagement data", 300),
        ("🌾", "Mass Harvester", "Find 50+ videos in one session", 500),
        ("💎", "Perfect Extraction", "100% title extraction rate", 600),
        ("🔍", "Smart Detective", "Fix failed extractions using pattern analysis", 350),
        ("👑", "Lord Danis Approved", "Extract premium quality episode titles", 1000),
        ("📜", "Scroll Master", "Efficiently use different scroll modes", 350),
        ("🥷", "Stealth Ninja", "Complete without detection", 200),
        ("📚", "Full Archive", "Extract 99+ videos (complete archive)", 800),
        ("✨", "Quality Control", "Extract 90%+ proper titles", 700),
        ("🇷🇸", "Serbian Scholar", "Handle Croatian/Serbian characters perfectly", 300),
        ("⏰", "Time Saver", "Use limited scrolls effectively", 150),
        ("🗃️", "JSON Master", "Generate perfect JSON output", 100),
        ("🔄", "Consistent Performer", "Maintain high quality across runs", 400),
        ("🚀", "Innovation Award", "Use advanced scraping techniques", 500)
    ]
    
    unlocked_achievements = data.get('unlocked_achievements', [])
    
    unlocked_count = 0
    total_points_from_achievements = 0
    
    for icon, name, description, points in all_achievements:
        if name in unlocked_achievements:
            print(f"✅ {icon} {name} (+{points} pts)")
            print(f"   {description}")
            unlocked_count += 1
            total_points_from_achievements += points
        else:
            print(f"⬜ {icon} {name} (+{points} pts)")
            print(f"   {description} [LOCKED]")
        print()
    
    print(f"📊 Achievement Progress: {unlocked_count}/{len(all_achievements)} ({unlocked_count/len(all_achievements)*100:.1f}%)")
    print(f"🏆 Points from Achievements: {total_points_from_achievements}")

def display_statistics(data: Dict[str, Any]) -> None:
    """Display comprehensive statistics"""
    print("\n" + "="*60)
    print("📊 === SCRAPING STATISTICS ===")
    print("="*60)
    
    # Overall stats
    print(f"🎯 Total Score: {data.get('total_score', 0):,} points")
    print(f"📈 Sessions Completed: {data.get('sessions_completed', 0)}")
    print(f"🏆 Best Session Score: {data.get('best_session_score', 0):,} points")
    
    # Performance stats
    stats = data.get('statistics', {})
    print(f"\n🎬 Total Videos Scraped: {stats.get('total_videos_scraped', 0):,}")
    print(f"📝 Total Titles Extracted: {stats.get('total_titles_extracted', 0):,}")
    print(f"🎭 Proper Episode Titles: {stats.get('total_proper_episodes', 0):,}")
    print(f"📅 Dates Found: {stats.get('total_dates_found', 0):,}")
    print(f"👍 Engagement Data Found: {stats.get('total_engagement_found', 0):,}")
    
    # Records
    if stats.get('fastest_completion', 0) > 0:
        print(f"⚡ Fastest Completion: {stats['fastest_completion']:.1f} seconds")
    if stats.get('highest_efficiency', 0) > 0:
        print(f"🎪 Highest Efficiency: {stats['highest_efficiency']:.2f} videos/scroll")

def display_session_history(data: Dict[str, Any]) -> None:
    """Display recent session history"""
    history = data.get('session_history', [])
    
    if not history:
        print("\n📜 No session history available yet.")
        return
    
    print("\n" + "="*60)
    print("📜 === RECENT SESSION HISTORY ===")
    print("="*60)
    
    for i, session in enumerate(reversed(history[-5:]), 1):  # Show last 5 sessions
        timestamp = datetime.fromtimestamp(session['timestamp']).strftime('%Y-%m-%d %H:%M')
        print(f"{i}. {timestamp}")
        print(f"   Score: {session['score']:,} pts | Videos: {session['videos_found']} | Grade: {session['grade']}")
        print(f"   Proper Titles: {session['proper_titles']} | Time: {session['completion_time']:.1f}s")
        print()

def calculate_next_milestone(data: Dict[str, Any]) -> None:
    """Calculate and display next milestone"""
    print("\n" + "="*60)
    print("🎯 === NEXT MILESTONES ===")
    print("="*60)
    
    stats = data.get('statistics', {})
    lord_danis = data.get('lord_danis_achievements', {})
    
    # Master Scraper requirements
    if not lord_danis.get('master_scraper_status', False):
        s_plus_needed = max(0, 3 - lord_danis.get('s_plus_grades', 0))
        sessions_needed = max(0, 10 - data.get('sessions_completed', 0))
        episodes_needed = max(0, 50 - stats.get('total_proper_episodes', 0))
        
        print("🏆 Master Scraper Requirements:")
        if s_plus_needed > 0:
            print(f"   • {s_plus_needed} more S+ grades needed")
        if sessions_needed > 0:
            print(f"   • {sessions_needed} more sessions needed")
        if episodes_needed > 0:
            print(f"   • {episodes_needed} more proper episodes needed")
        
        if s_plus_needed == 0 and sessions_needed == 0 and episodes_needed == 0:
            print("   ✅ All requirements met! Status will be updated next session.")
    else:
        print("🏆 Master Scraper Status: ACHIEVED!")
    
    # Point milestones
    current_points = data.get('total_score', 0)
    next_milestones = [1000, 5000, 10000, 25000, 50000, 100000]
    
    for milestone in next_milestones:
        if current_points < milestone:
            needed = milestone - current_points
            print(f"💎 Next Point Milestone: {milestone:,} points ({needed:,} more needed)")
            break

def main():
    """Main function to display Lord Danis's achievements"""
    print("👑 Welcome to Lord Danis's Achievement Viewer!")
    print("🏆 Let's see how your scraping prowess has evolved...")
    
    data = load_achievements()
    if not data:
        return
    
    # Display all sections
    display_lord_danis_status(data)
    display_statistics(data)
    display_achievements_gallery(data)
    display_session_history(data)
    calculate_next_milestone(data)
    
    print("\n" + "="*60)
    print("🎊 Thank you for using Lord Danis's Achievement System!")
    print("🚀 Keep scraping to unlock more achievements!")
    print("="*60)

if __name__ == "__main__":
    main() 
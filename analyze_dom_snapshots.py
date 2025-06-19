#!/usr/bin/env python3
"""
DOM Snapshot Analysis Tool
Analyze saved DOM content to improve extraction algorithms
Author: Lord Danis Assistant
🔍 Deep dive into scraping behavior through DOM archaeology!
"""

import os
import json
import gzip
import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from datetime import datetime
import argparse

class DOMAnalyzer:
    """Advanced DOM snapshot analyzer for improving extraction patterns"""
    
    def __init__(self, dom_storage_dir: str = "dom_snapshots"):
        self.dom_storage_dir: str = dom_storage_dir
        self.sessions: List[Dict] = []
        self.load_sessions()
    
    def load_sessions(self) -> None:
        """Load all session summaries"""
        if not os.path.exists(self.dom_storage_dir):
            print(f"❌ DOM storage directory not found: {self.dom_storage_dir}")
            return
        
        for filename in os.listdir(self.dom_storage_dir):
            if filename.endswith("_session_summary.json"):
                try:
                    with open(os.path.join(self.dom_storage_dir, filename), 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                        self.sessions.append(session_data)
                except Exception as e:
                    print(f"⚠️ Error loading session {filename}: {e}")
        
        self.sessions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        print(f"📊 Loaded {len(self.sessions)} scraping sessions")
    
    def list_sessions(self) -> None:
        """Display all available sessions"""
        print("\n🗂️  === AVAILABLE SESSIONS ===")
        print("-" * 60)
        
        for i, session in enumerate(self.sessions):
            session_id = session['session_id']
            timestamp = session['timestamp'][:19].replace('T', ' ')
            videos_found = session['videos_found']
            success_rate = session['extraction_success_rate']
            failed_count = len(session.get('failed_extractions', []))
            
            print(f"{i+1:2d}. {session_id}")
            print(f"    📅 {timestamp}")
            print(f"    📹 Videos: {videos_found} | Success: {success_rate:.1f}% | Failed: {failed_count}")
            print(f"    📸 Snapshots: {len(session.get('dom_snapshots', []))}")
            print()
    
    def analyze_session(self, session_index: int) -> None:
        """Analyze a specific session in detail"""
        if not 0 <= session_index < len(self.sessions):
            print(f"❌ Invalid session index. Use 0-{len(self.sessions)-1}")
            return
        
        session = self.sessions[session_index]
        session_id = session['session_id']
        
        print(f"\n🔍 === ANALYZING SESSION: {session_id} ===")
        print("=" * 60)
        
        # Session overview
        print(f"📊 SESSION OVERVIEW:")
        print(f"   📹 Videos Found: {session['videos_found']}")
        print(f"   ✅ Success Rate: {session['extraction_success_rate']:.1f}%")
        print(f"   ❌ Failed Extractions: {len(session.get('failed_extractions', []))}")
        print(f"   📸 DOM Snapshots: {len(session.get('dom_snapshots', []))}")
        
        # Failed extractions analysis
        failed_extractions = session.get('failed_extractions', [])
        if failed_extractions:
            print(f"\n❌ FAILED EXTRACTIONS:")
            for i, failed in enumerate(failed_extractions):
                print(f"   {i+1}. ID: {failed['video_id']}")
                print(f"      Title: {failed['title']}")
                print(f"      Date: {failed['date']}")
        
        # DOM snapshots timeline
        print(f"\n📸 DOM SNAPSHOTS TIMELINE:")
        snapshots = session.get('dom_snapshots', [])
        for i, snapshot in enumerate(snapshots):
            stage = snapshot['stage']
            timestamp = snapshot['timestamp'][11:19]  # Extract time only
            description = snapshot.get('description', '')
            videos_found = snapshot.get('metadata', {}).get('videos_found_so_far', 0)
            
            print(f"   {i+1:2d}. [{timestamp}] {stage.upper()}")
            print(f"       📝 {description}")
            print(f"       📹 Videos so far: {videos_found}")
    
    def analyze_failed_extraction(self, session_index: int, video_id: str) -> None:
        """Deep analysis of a specific failed video extraction"""
        if not 0 <= session_index < len(self.sessions):
            print(f"❌ Invalid session index")
            return
        
        session = self.sessions[session_index]
        session_id = session['session_id']
        
        # Find extraction snapshot
        extraction_snapshot = None
        for snapshot in session.get('dom_snapshots', []):
            if snapshot['stage'] == 'before_extraction':
                extraction_snapshot = snapshot['snapshot_id']
                break
        
        if not extraction_snapshot:
            print(f"❌ No extraction snapshot found for session {session_id}")
            return
        
        # Look for existing analysis
        analysis_file = f"{self.dom_storage_dir}/{extraction_snapshot}_analysis_{video_id}.json"
        
        if os.path.exists(analysis_file):
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
            
            print(f"\n🔍 === ANALYSIS FOR VIDEO {video_id} ===")
            print("=" * 50)
            
            # Basic info
            print(f"📹 Video ID: {video_id}")
            print(f"📸 Snapshot: {extraction_snapshot}")
            print(f"🔗 Video Links Found: {analysis['video_links_found']}")
            
            # Potential titles found
            potential_titles = analysis.get('potential_titles', [])
            if potential_titles:
                print(f"\n🎯 POTENTIAL TITLES FOUND ({len(potential_titles)}):")
                # Sort by score
                potential_titles.sort(key=lambda x: x['score'], reverse=True)
                
                for i, title_data in enumerate(potential_titles[:5]):  # Show top 5
                    text = title_data['text']
                    score = title_data['score']
                    level = title_data['parent_level']
                    
                    print(f"   {i+1}. (Score: {score:3d}) {text[:80]}...")
                    print(f"      Parent Level: {level}")
            
            # DOM statistics
            dom_stats = analysis.get('dom_statistics', {})
            if dom_stats:
                print(f"\n📊 DOM STATISTICS:")
                print(f"   Total Links: {dom_stats.get('total_links', 0):,}")
                print(f"   Video Links: {dom_stats.get('video_links', 0):,}")
                print(f"   Heading Elements: {dom_stats.get('heading_elements', 0):,}")
                print(f"   Span Elements: {dom_stats.get('span_elements', 0):,}")
                print(f"   Aria-label Elements: {dom_stats.get('elements_with_aria_label', 0):,}")
            
            # Link patterns
            patterns = analysis.get('patterns_found', [])
            if patterns:
                print(f"\n🔗 LINK PATTERNS:")
                for i, pattern in enumerate(patterns[:2]):  # Show first 2 patterns
                    print(f"   Link {i+1}:")
                    print(f"     Text: {pattern.get('text', 'N/A')}")
                    print(f"     Aria-label: {pattern.get('aria_label', 'N/A')}")
                    print(f"     Surrounding levels: {len(pattern.get('surrounding_text', []))}")
        else:
            print(f"❌ No analysis file found: {analysis_file}")
            print(f"🔄 Run the scraper again to generate analysis for this video")
    
    def extract_raw_dom(self, session_index: int, stage: str) -> Optional[str]:
        """Extract and display raw DOM content for a specific stage"""
        if not 0 <= session_index < len(self.sessions):
            print(f"❌ Invalid session index")
            return None
        
        session = self.sessions[session_index]
        session_id = session['session_id']
        
        # Find the requested snapshot
        target_snapshot = None
        for snapshot in session.get('dom_snapshots', []):
            if snapshot['stage'] == stage:
                target_snapshot = snapshot['snapshot_id']
                break
        
        if not target_snapshot:
            print(f"❌ No snapshot found for stage '{stage}' in session {session_id}")
            available_stages = [s['stage'] for s in session.get('dom_snapshots', [])]
            print(f"Available stages: {', '.join(available_stages)}")
            return None
        
        # Load the HTML content
        html_file = f"{self.dom_storage_dir}/{target_snapshot}.html.gz"
        if not os.path.exists(html_file):
            print(f"❌ HTML file not found: {html_file}")
            return None
        
        try:
            with gzip.open(html_file, 'rt', encoding='utf-8') as f:
                content = f.read()
            
            print(f"✅ Loaded DOM content: {len(content):,} characters")
            return content
            
        except Exception as e:
            print(f"❌ Error loading DOM content: {e}")
            return None
    
    def search_dom_patterns(self, session_index: int, pattern: str, stage: str = "before_extraction") -> None:
        """Search for specific patterns in DOM content"""
        content = self.extract_raw_dom(session_index, stage)
        if not content:
            return
        
        soup = BeautifulSoup(content, 'html.parser')
        
        print(f"\n🔍 === SEARCHING FOR PATTERN: '{pattern}' ===")
        print("=" * 50)
        
        # Search in different ways
        searches = [
            ("Text Content", soup.find_all(string=re.compile(pattern, re.IGNORECASE))),
            ("Link Text", [a for a in soup.find_all('a') if pattern.lower() in a.get_text().lower()]),
            ("Aria Labels", [elem for elem in soup.find_all(attrs={"aria-label": True}) 
                           if pattern.lower() in (elem.get('aria-label') or '').lower()]),
            ("Element Text", [elem for elem in soup.find_all() 
                            if pattern.lower() in elem.get_text()[:200].lower()])
        ]
        
        for search_type, results in searches:
            if results:
                print(f"\n📍 {search_type.upper()} ({len(results)} matches):")
                for i, result in enumerate(results[:3]):  # Show first 3
                    if hasattr(result, 'get_text'):
                        text = result.get_text(strip=True)[:100]
                        print(f"   {i+1}. {text}...")
                    else:
                        print(f"   {i+1}. {str(result)[:100]}...")
    
    def compare_sessions(self, session1_idx: int, session2_idx: int) -> None:
        """Compare two sessions to identify improvement patterns"""
        if not (0 <= session1_idx < len(self.sessions) and 0 <= session2_idx < len(self.sessions)):
            print(f"❌ Invalid session indices")
            return
        
        s1 = self.sessions[session1_idx]
        s2 = self.sessions[session2_idx]
        
        print(f"\n⚖️  === SESSION COMPARISON ===")
        print("=" * 40)
        print(f"Session 1: {s1['session_id']}")
        print(f"Session 2: {s2['session_id']}")
        print("-" * 40)
        
        # Compare key metrics
        metrics = [
            ("Videos Found", "videos_found"),
            ("Success Rate", "extraction_success_rate"),
            ("Failed Extractions", lambda s: len(s.get('failed_extractions', []))),
            ("DOM Snapshots", lambda s: len(s.get('dom_snapshots', [])))
        ]
        
        for label, key in metrics:
            if callable(key):
                val1, val2 = key(s1), key(s2)
            else:
                val1, val2 = s1.get(key, 0), s2.get(key, 0)
            
            diff = val2 - val1
            direction = "📈" if diff > 0 else "📉" if diff < 0 else "➡️"
            
            print(f"{label:18s}: {val1:6.1f} → {val2:6.1f} {direction}")
    
    def generate_improvement_report(self) -> None:
        """Generate recommendations for improving extraction algorithms"""
        if len(self.sessions) < 2:
            print("❌ Need at least 2 sessions for improvement analysis")
            return
        
        print(f"\n💡 === IMPROVEMENT RECOMMENDATIONS ===")
        print("=" * 50)
        
        # Analyze trends
        recent_sessions = self.sessions[:5]  # Last 5 sessions
        
        # Success rate trend
        success_rates = [s['extraction_success_rate'] for s in recent_sessions]
        avg_success = sum(success_rates) / len(success_rates)
        
        print(f"📊 CURRENT PERFORMANCE:")
        print(f"   Average Success Rate: {avg_success:.1f}%")
        print(f"   Best Session: {max(success_rates):.1f}%")
        print(f"   Worst Session: {min(success_rates):.1f}%")
        
        # Common failure patterns
        all_failed = []
        for session in recent_sessions:
            all_failed.extend(session.get('failed_extractions', []))
        
        if all_failed:
            print(f"\n❌ COMMON FAILURE PATTERNS:")
            failure_ids = [f['video_id'] for f in all_failed]
            print(f"   Total Failed Videos: {len(failure_ids)}")
            print(f"   Unique Failed Videos: {len(set(failure_ids))}")
            
            # Look for patterns in failed video IDs
            if len(failure_ids) > 1:
                id_lengths = [len(vid_id) for vid_id in failure_ids]
                avg_id_length = sum(id_lengths) / len(id_lengths)
                print(f"   Average Failed Video ID Length: {avg_id_length:.1f}")
        
        print(f"\n🎯 RECOMMENDATIONS:")
        print(f"   1. Focus on videos that consistently fail")
        print(f"   2. Analyze DOM patterns at 'before_extraction' stage")
        print(f"   3. Test new extraction selectors on saved snapshots")
        print(f"   4. Compare successful vs failed extraction contexts")

def main():
    """Main function for DOM analysis tool"""
    parser = argparse.ArgumentParser(description="Analyze DOM snapshots to improve scraping")
    parser.add_argument("--list", "-l", action="store_true", help="List all sessions")
    parser.add_argument("--analyze", "-a", type=int, help="Analyze specific session (index)")
    parser.add_argument("--failed", "-f", nargs=2, metavar=("SESSION_IDX", "VIDEO_ID"),
                       help="Analyze failed extraction for specific video")
    parser.add_argument("--search", "-s", nargs=3, metavar=("SESSION_IDX", "PATTERN", "STAGE"),
                       help="Search for pattern in DOM content")
    parser.add_argument("--compare", "-c", nargs=2, type=int, metavar=("IDX1", "IDX2"),
                       help="Compare two sessions")
    parser.add_argument("--improve", "-i", action="store_true", help="Generate improvement report")
    
    args = parser.parse_args()
    
    analyzer = DOMAnalyzer()
    
    if args.list:
        analyzer.list_sessions()
    elif args.analyze is not None:
        analyzer.analyze_session(args.analyze)
    elif args.failed:
        session_idx, video_id = int(args.failed[0]), args.failed[1]
        analyzer.analyze_failed_extraction(session_idx, video_id)
    elif args.search:
        session_idx, pattern, stage = int(args.search[0]), args.search[1], args.search[2]
        analyzer.search_dom_patterns(session_idx, pattern, stage)
    elif args.compare:
        analyzer.compare_sessions(args.compare[0], args.compare[1])
    elif args.improve:
        analyzer.generate_improvement_report()
    else:
        # Interactive mode
        print("🔍 DOM Snapshot Analyzer - Interactive Mode")
        print("=" * 50)
        analyzer.list_sessions()
        
        print("\nCommands:")
        print("  python analyze_dom_snapshots.py --list")
        print("  python analyze_dom_snapshots.py --analyze 0")
        print("  python analyze_dom_snapshots.py --failed 0 394517285283903")
        print("  python analyze_dom_snapshots.py --search 0 'draga mama' before_extraction")
        print("  python analyze_dom_snapshots.py --compare 0 1")
        print("  python analyze_dom_snapshots.py --improve")

if __name__ == "__main__":
    main() 
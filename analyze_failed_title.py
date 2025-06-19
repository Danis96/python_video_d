#!/usr/bin/env python3
"""
DOM Analysis Tool for Failed Title Extractions
Analyzes specific video IDs in DOM snapshots to understand why title extraction failed
Author: Lord Danis Assistant
"""

import os
import gzip
import json
import re
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

def analyze_video_in_dom(video_id: str, html_content: str) -> Dict:
    """Analyze DOM content for a specific video ID"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    analysis = {
        "video_id": video_id,
        "links_found": [],
        "potential_titles": [],
        "dom_context": [],
        "text_patterns": []
    }
    
    # Find all links containing the video ID
    video_links = soup.find_all('a', href=re.compile(f'watch.*v={video_id}'))
    analysis["links_found"] = len(video_links)
    
    print(f"\n🔍 === ANALYZING VIDEO {video_id[-8:]}... ===")
    print(f"Found {len(video_links)} links for this video")
    
    for i, link in enumerate(video_links[:3]):  # Analyze first 3 links
        print(f"\n📋 LINK {i+1} ANALYSIS:")
        print(f"   Href: {link.get('href', '')[:60]}...")
        print(f"   Text: '{link.get_text(strip=True)}'")
        print(f"   Aria-label: '{link.get('aria-label', '')}'")
        
        # Analyze parent containers for title content
        current = link
        for level in range(1, 8):  # Check up to 7 parent levels
            try:
                parent = current.parent
                if parent is None:
                    break
                
                parent_text = parent.get_text(separator='\n', strip=True)
                lines = [line.strip() for line in parent_text.split('\n') if line.strip()]
                
                # Look for potential episode titles
                for line_num, line in enumerate(lines[:15]):  # Check first 15 lines
                    if is_potential_title(line, video_id):
                        title_info = {
                            "text": line,
                            "parent_level": level,
                            "line_position": line_num,
                            "score": score_potential_title(line),
                            "link_index": i
                        }
                        analysis["potential_titles"].append(title_info)
                        print(f"   📝 Level {level}, Line {line_num}: '{line}' (score: {title_info['score']})")
                
                # Store context for debugging
                if level <= 3 and len(parent_text) > 20:
                    context = {
                        "level": level,
                        "tag": parent.name,
                        "classes": parent.get('class', []),
                        "text_preview": parent_text[:200] + "..." if len(parent_text) > 200 else parent_text,
                        "children_count": len(parent.find_all())
                    }
                    analysis["dom_context"].append(context)
                
                current = parent
                
            except Exception as e:
                print(f"   ⚠️ Error at level {level}: {e}")
                break
    
    # Look for the video ID in the raw text and surrounding content
    text_content = soup.get_text()
    if video_id in text_content:
        # Find the position and extract surrounding text
        positions = []
        start = 0
        while True:
            pos = text_content.find(video_id, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        
        print(f"\n📍 Found video ID {len(positions)} times in raw text")
        
        for pos in positions[:3]:  # Check first 3 occurrences
            # Extract 200 characters before and after
            start_pos = max(0, pos - 200)
            end_pos = min(len(text_content), pos + len(video_id) + 200)
            context = text_content[start_pos:end_pos]
            
            # Split into lines and look for titles
            context_lines = context.split('\n')
            for line in context_lines:
                line = line.strip()
                if line and is_potential_title(line, video_id):
                    pattern_info = {
                        "text": line,
                        "context": "raw_text_search",
                        "score": score_potential_title(line)
                    }
                    analysis["text_patterns"].append(pattern_info)
                    print(f"   📄 Raw text match: '{line}' (score: {pattern_info['score']})")
    
    # Sort potential titles by score
    analysis["potential_titles"].sort(key=lambda x: x["score"], reverse=True)
    analysis["text_patterns"].sort(key=lambda x: x["score"], reverse=True)
    
    return analysis

def is_potential_title(text: str, video_id: str) -> bool:
    """Check if text could be a video title"""
    if not text or len(text) < 4 or len(text) > 300:
        return False
    
    text_lower = text.lower()
    
    # Skip UI elements
    ui_terms = ['like', 'comment', 'share', 'see more', 'see less', 'follow', 'unfollow',
               'watch', 'play', 'pause', 'ago', 'yesterday', 'views', 'subscribers',
               'facebook', 'loading', 'error', 'cookies', 'privacy', 'settings']
    
    if any(term in text_lower for term in ui_terms) and len(text) < 30:
        return False
    
    # Strong indicators
    good_indicators = [
        'draga mama', 'mama', 'epizod', 'izdanj', 'rubrika', 'podnaziv',
        'nastavlja', 'bhr1', 'nakon', 'letnje', 'ljetne', 'pauze', 'pecanje',
        'oni što ostaju', 'ostaju i odlaze'
    ]
    
    if any(indicator in text_lower for indicator in good_indicators):
        return True
    
    # Episode numbers
    if re.search(r'\b\d{2,4}\.\s*[A-Za-zšđčćžŠĐČĆŽ]', text):
        return True
    
    # Quoted content
    if '"' in text and len(text) > 10:
        return True
    
    # Reasonable title length with letters
    if 8 <= len(text) <= 150:
        letter_count = sum(1 for c in text if c.isalpha())
        if letter_count >= len(text) * 0.5:
            return True
    
    return False

def score_potential_title(text: str) -> int:
    """Score potential title candidates"""
    score = 0
    text_lower = text.lower()
    
    # Base length score
    if 15 <= len(text) <= 80:
        score += 20
    elif 8 <= len(text) <= 150:
        score += 10
    
    # Content scoring
    if 'draga mama' in text_lower:
        score += 100
    
    # Specific episode indicators
    known_titles = ['pecanje', 'oni što ostaju i oni što odlaze', 'oni što ostaju', 'ostaju i odlaze']
    for title in known_titles:
        if title in text_lower:
            score += 150
    
    # Episode numbers
    if re.search(r'\b(77|218|219|220)\b', text):
        score += 80
    
    if re.search(r'\b\d{2,4}\.\s*[A-Za-z]', text):
        score += 50
    
    # Quoted content
    if '"' in text:
        score += 30
    
    # Serbian characters
    if re.search(r'[šđčćžŠĐČĆŽ]', text):
        score += 20
    
    # Penalties
    ui_terms = ['like', 'comment', 'share', 'ago', 'views']
    ui_count = sum(1 for term in ui_terms if term in text_lower)
    score -= ui_count * 30
    
    return score

def main():
    """Main analysis function"""
    # Specific videos to analyze
    target_videos = {
        "10201500151657676": "Should be: Draga Mama 77. Pecanje",
        "595328265177242": "Should be: Draga mama 218. Oni što ostaju i oni što odlaze"
    }
    
    print("🔍 === DOM SNAPSHOT ANALYSIS FOR FAILED TITLES ===")
    print(f"Analyzing {len(target_videos)} specific video extraction failures...")
    
    # Find DOM snapshots directory
    dom_dir = "dom_snapshots"
    if not os.path.exists(dom_dir):
        print("❌ DOM snapshots directory not found!")
        return
    
    # Get list of compressed HTML files
    html_files = [f for f in os.listdir(dom_dir) if f.endswith('.html.gz')]
    print(f"Found {len(html_files)} DOM snapshot files")
    
    results = {}
    
    for video_id, expected_title in target_videos.items():
        print(f"\n{'='*80}")
        print(f"🎯 SEARCHING FOR VIDEO {video_id[-8:]}...")
        print(f"Expected title: {expected_title}")
        print(f"{'='*80}")
        
        found_in_files = []
        
        # Check each DOM snapshot
        for html_file in html_files:
            try:
                file_path = os.path.join(dom_dir, html_file)
                
                # Load compressed HTML
                with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Quick check if video ID is in this file
                if video_id in html_content:
                    print(f"✅ Found in {html_file}")
                    found_in_files.append(html_file)
                    
                    # Perform detailed analysis
                    analysis = analyze_video_in_dom(video_id, html_content)
                    results[f"{video_id}_{html_file}"] = analysis
                    
                    # Show top candidates
                    if analysis["potential_titles"]:
                        print(f"\n🏆 TOP TITLE CANDIDATES:")
                        for i, title_info in enumerate(analysis["potential_titles"][:5]):
                            print(f"   {i+1}. Score {title_info['score']}: '{title_info['text']}'")
                            print(f"      (Level {title_info['parent_level']}, Line {title_info['line_position']})")
                    else:
                        print("❌ No potential titles found in structured analysis")
                    
                    if analysis["text_patterns"]:
                        print(f"\n📄 TEXT PATTERN MATCHES:")
                        for i, pattern in enumerate(analysis["text_patterns"][:3]):
                            print(f"   {i+1}. Score {pattern['score']}: '{pattern['text']}'")
                    
            except Exception as e:
                print(f"⚠️ Error processing {html_file}: {e}")
        
        if not found_in_files:
            print(f"❌ Video {video_id[-8:]}... not found in any DOM snapshots!")
        
        results[video_id] = {
            "expected_title": expected_title,
            "found_in_files": found_in_files,
            "video_id": video_id
        }
    
    # Save analysis results
    output_file = "title_extraction_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"📊 ANALYSIS COMPLETE")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main() 
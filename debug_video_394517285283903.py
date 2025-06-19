#!/usr/bin/env python3
"""
Debug Script for Enhanced Title Extraction
Tests the new JSON-based title extraction on specific failed videos
Author: Lord Danis Assistant
"""

import gzip
import json
import re
import logging
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_json_title_extraction(video_id: str, dom_content: str) -> dict:
    """Test the enhanced JSON-based title extraction"""
    results = {
        "video_id": video_id,
        "json_patterns_found": [],
        "aria_patterns_found": [],
        "extracted_titles": []
    }
    
    # Pattern 1: Look for video_title JSON structure
    video_title_patterns = [
        r'"video_title"\s*:\s*\{\s*"text"\s*:\s*"([^"]+)"',
        r'"title"\s*:\s*"([^"]*Draga\s*mama[^"]*)"',
        r'"name"\s*:\s*"([^"]*Draga\s*mama[^"]*)"',
        r'"text"\s*:\s*"([^"]*Draga\s*mama[^"]*)"'
    ]
    
    for i, pattern in enumerate(video_title_patterns):
        matches = re.findall(pattern, dom_content, re.IGNORECASE | re.DOTALL)
        if matches:
            results["json_patterns_found"].append(f"Pattern {i+1}: {len(matches)} matches")
            for match in matches:
                if match and len(match.strip()) > 5:
                    # Decode unicode escapes
                    try:
                        decoded_title = match.encode().decode('unicode_escape')
                        results["extracted_titles"].append(decoded_title.strip())
                        logger.info(f"📋 Found title via JSON pattern {i+1}: {decoded_title}")
                    except:
                        results["extracted_titles"].append(match.strip())
                        logger.info(f"📋 Found title via JSON pattern {i+1}: {match}")
    
    # Pattern 2: Look for aria-label patterns
    aria_patterns = [
        r'aria-label="[^"]*([^"]*Draga\s*mama[^"]*)"',
        r'title="([^"]*Draga\s*mama[^"]*)"',
        r'alt="([^"]*Draga\s*mama[^"]*)"'
    ]
    
    for i, pattern in enumerate(aria_patterns):
        matches = re.findall(pattern, dom_content, re.IGNORECASE)
        if matches:
            results["aria_patterns_found"].append(f"Aria pattern {i+1}: {len(matches)} matches")
            for match in matches:
                if match and len(match.strip()) > 5:
                    results["extracted_titles"].append(match.strip())
                    logger.info(f"🏷️ Found title via aria pattern {i+1}: {match}")
    
    # Pattern 3: Search for video ID context
    if video_id in dom_content:
        # Look for titles near the video ID
        video_context_pattern = rf'({re.escape(video_id)}.*?)"video_title"\s*:\s*\{{\s*"text"\s*:\s*"([^"]+)"'
        context_matches = re.findall(video_context_pattern, dom_content, re.IGNORECASE | re.DOTALL)
        
        if context_matches:
            results["json_patterns_found"].append(f"Context pattern: {len(context_matches)} matches")
            for match in context_matches:
                if len(match) >= 2:
                    title_text = match[1]
                    if title_text and len(title_text.strip()) > 5:
                        try:
                            decoded_title = title_text.encode().decode('unicode_escape')
                            results["extracted_titles"].append(decoded_title.strip())
                            logger.info(f"🎯 Found title via context pattern: {decoded_title}")
                        except:
                            results["extracted_titles"].append(title_text.strip())
                            logger.info(f"🎯 Found title via context pattern: {title_text}")
    
    return results

def analyze_specific_videos():
    """Analyze the specific videos mentioned by Lord Danis"""
    target_videos = {
        "10201500151657676": "Expected: Draga Mama 77. Pecanje",
        "595328265177242": "Expected: Draga mama 218. Oni što ostaju i oni što odlaze"
    }
    
    logger.info("🔍 === ENHANCED TITLE EXTRACTION DEBUG TEST ===")
    logger.info("🎯 Testing specific videos with known title extraction issues")
    
    # Find DOM snapshots containing these videos
    dom_files = [
        "dom_snapshots/20250618_131141_before_extraction_131521.html.gz",
        "dom_snapshots/20250618_143336_before_extraction_143605.html.gz",
        "dom_snapshots/20250618_134002_before_extraction_134218.html.gz"
    ]
    
    total_results = {}
    
    for dom_file in dom_files:
        try:
            logger.info(f"\n📂 Analyzing DOM file: {dom_file}")
            
            # Read compressed DOM content
            with gzip.open(dom_file, 'rt', encoding='utf-8') as f:
                dom_content = f.read()
            
            logger.info(f"📊 DOM file size: {len(dom_content):,} characters")
            
            # Test each target video
            for video_id, expected_title in target_videos.items():
                if video_id in dom_content:
                    logger.info(f"\n🎬 Testing video {video_id}")
                    logger.info(f"   Expected: {expected_title}")
                    
                    results = test_json_title_extraction(video_id, dom_content)
                    
                    if video_id not in total_results:
                        total_results[video_id] = []
                    
                    total_results[video_id].append({
                        "dom_file": dom_file,
                        "results": results
                    })
                    
                    logger.info(f"   📋 JSON patterns found: {len(results['json_patterns_found'])}")
                    logger.info(f"   🏷️ Aria patterns found: {len(results['aria_patterns_found'])}")
                    logger.info(f"   🎯 Total titles extracted: {len(results['extracted_titles'])}")
                    
                    if results['extracted_titles']:
                        logger.info("   ✅ Extracted titles:")
                        for i, title in enumerate(results['extracted_titles']):
                            logger.info(f"      {i+1}. {title}")
                    else:
                        logger.warning("   ❌ No titles extracted with enhanced method")
                        
        except FileNotFoundError:
            logger.warning(f"⚠️ DOM file not found: {dom_file}")
        except Exception as e:
            logger.error(f"❌ Error analyzing {dom_file}: {e}")
    
    # Summary
    logger.info("\n🏆 === EXTRACTION TEST SUMMARY ===")
    for video_id, expected_title in target_videos.items():
        logger.info(f"\n🎬 Video {video_id}")
        logger.info(f"   Expected: {expected_title}")
        
        if video_id in total_results:
            all_extracted_titles = []
            for result_data in total_results[video_id]:
                all_extracted_titles.extend(result_data["results"]["extracted_titles"])
            
            # Remove duplicates while preserving order
            unique_titles = []
            for title in all_extracted_titles:
                if title not in unique_titles:
                    unique_titles.append(title)
            
            if unique_titles:
                logger.info(f"   ✅ Successfully extracted {len(unique_titles)} unique titles:")
                for i, title in enumerate(unique_titles):
                    logger.info(f"      {i+1}. {title}")
                    
                    # Check if we found the expected title
                    if "77" in title and "Pecanje" in title and video_id == "10201500151657676":
                        logger.info(f"      🎉 PERFECT MATCH for Draga Mama 77!")
                    elif "218" in title and ("Oni što ostaju" in title or "oni što odlaze" in title) and video_id == "595328265177242":
                        logger.info(f"      🎉 PERFECT MATCH for Draga mama 218!")
            else:
                logger.warning(f"   ❌ No titles extracted across all DOM files")
        else:
            logger.warning(f"   ❌ Video not found in any DOM snapshots")

if __name__ == "__main__":
    analyze_specific_videos() 
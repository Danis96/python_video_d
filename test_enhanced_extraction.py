#!/usr/bin/env python3
"""
Simple test to validate enhanced title extraction
Author: Lord Danis Assistant
"""

import re

def simulate_page_source_extraction(video_ids, mock_page_source):
    """Simulate the enhanced page source extraction"""
    extracted_titles = {}
    
    for video_id in video_ids:
        # Pattern 1: Look for video_title JSON structure near the video ID
        video_context_pattern = rf'({re.escape(video_id)}.*?)"video_title"\s*:\s*\{{\s*"text"\s*:\s*"([^"]+)"'
        matches = re.findall(video_context_pattern, mock_page_source, re.IGNORECASE | re.DOTALL)
        
        if matches:
            for match in matches:
                title_text = match[1]
                if title_text and len(title_text.strip()) > 5:
                    # Decode unicode escapes
                    try:
                        decoded_title = title_text.encode().decode('unicode_escape')
                        extracted_titles[video_id] = decoded_title.strip()
                        print(f"✅ Found title for {video_id}: {decoded_title}")
                        break
                    except:
                        extracted_titles[video_id] = title_text.strip()
                        print(f"✅ Found title for {video_id}: {title_text}")
                        break
        
        # Pattern 2: Reverse search - find video_title first, then look for nearby video ID
        if video_id not in extracted_titles:
            title_pattern = r'"video_title"\s*:\s*\{\s*"text"\s*:\s*"([^"]+)"'
            title_matches = re.findall(title_pattern, mock_page_source)
            
            for title_match in title_matches:
                # Look for video ID within 2000 characters before or after the title
                title_pos = mock_page_source.find(f'"text":"{title_match}"')
                if title_pos > 0:
                    context_start = max(0, title_pos - 1000)
                    context_end = min(len(mock_page_source), title_pos + 1000)
                    context = mock_page_source[context_start:context_end]
                    
                    if video_id in context and title_match:
                        decoded_title = title_match.encode().decode('unicode_escape')
                        extracted_titles[video_id] = decoded_title.strip()
                        print(f"🎯 Found title via context for {video_id}: {decoded_title}")
                        break
    
    return extracted_titles

def test_title_extraction():
    """Test our enhanced extraction logic"""
    print("🧪 Testing Enhanced Title Extraction Logic")
    
    # Test videos from Lord Danis's examples
    test_video_ids = ["10201500151657676", "595328265177242"]
    
    # Mock page source simulating Facebook's JSON structure (based on DOM analysis)
    mock_page_source = '''
    ... some facebook content ...
    {"video_id":"595328265177242","video_title":{"text":"Draga mama 218. Oni što ostaju i oni što odlaze"}}
    ... more content ...
    {"video_id":"10201500151657676","video_title":{"text":"Draga mama 77. Pecanje"}}
    ... more facebook content ...
    "video_title":{"text":"Draga mama 218. Oni što ostaju i oni što odlaze"} near 595328265177242
    "video_title":{"text":"Draga mama 77. Pecanje"} context with 10201500151657676
    '''
    
    results = simulate_page_source_extraction(test_video_ids, mock_page_source)
    
    print(f"\n📊 Results:")
    for video_id, title in results.items():
        print(f"   {video_id}: {title}")
    
    # Check if we found the expected titles
    expected_results = {
        "595328265177242": "Draga mama 218. Oni što ostaju i oni što odlaze",
        "10201500151657676": "Draga mama 77. Pecanje"
    }
    
    print(f"\n🎯 Validation:")
    all_correct = True
    for video_id, expected_title in expected_results.items():
        if video_id in results:
            if expected_title in results[video_id]:
                print(f"   ✅ {video_id}: CORRECT ({expected_title})")
            else:
                print(f"   ❌ {video_id}: Expected '{expected_title}', got '{results[video_id]}'")
                all_correct = False
        else:
            print(f"   ❌ {video_id}: NOT FOUND")
            all_correct = False
    
    if all_correct:
        print(f"\n🏆 ALL TESTS PASSED! Enhanced extraction is working correctly!")
    else:
        print(f"\n⚠️ Some tests failed - need to investigate further")

if __name__ == "__main__":
    test_title_extraction() 
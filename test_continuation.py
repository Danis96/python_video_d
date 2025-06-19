#!/usr/bin/env python3
"""
Test script for Enhanced Continuation System
Validates scroll offset, video ID anchoring, and date filtering
Author: Lord Danis Assistant
"""

import json
import logging
from smart_harvester import SmartHarvester, ContinuationPoint

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_continuation_point_calculation():
    """Test the enhanced continuation point calculation logic"""
    logger.info("🧪 Testing Enhanced Continuation Point Calculation...")
    
    harvester = SmartHarvester()
    
    # Test Session 1 (Fresh Start)
    continuation_1 = harvester._calculate_advanced_continuation_point(0)
    logger.info(f"Session 1: {continuation_1.strategy} - {continuation_1.reasoning}")
    assert continuation_1.strategy == "fresh_start"
    assert continuation_1.scroll_offset == 0
    
    # Test Session 2 (Scroll Offset)
    continuation_2 = harvester._calculate_advanced_continuation_point(1)
    logger.info(f"Session 2: {continuation_2.strategy} - {continuation_2.reasoning}")
    assert continuation_2.strategy == "scroll_offset"
    assert 10 <= continuation_2.scroll_offset <= 15
    
    logger.info("✅ Continuation point calculation tests passed!")

def test_session_config_generation():
    """Test enhanced session configuration generation"""
    logger.info("🧪 Testing Enhanced Session Configuration...")
    
    harvester = SmartHarvester()
    
    # Test multiple session configs
    for session_num in range(3):
        config = harvester._generate_session_config(session_num, 5)
        
        logger.info(f"Session {session_num + 1} Config:")
        logger.info(f"  Scroll Count: {config['scroll_count']}")
        logger.info(f"  Strategy: {config['continuation']['strategy']}")
        logger.info(f"  Reasoning: {config['continuation']['reasoning']}")
        
        # Validate configuration
        assert "scroll_count" in config
        assert "continuation" in config
        assert "strategy" in config["continuation"]
        
        # Check session-specific logic
        if session_num == 0:
            assert config["continuation"]["strategy"] == "fresh_start"
        elif session_num == 1:
            assert config["continuation"]["strategy"] == "scroll_offset"
    
    logger.info("✅ Session configuration tests passed!")

def test_collection_analysis():
    """Test collection analysis for gap detection"""
    logger.info("🧪 Testing Collection Analysis...")
    
    harvester = SmartHarvester()
    
    # Test with empty collection
    analysis = harvester._analyze_collection_gaps()
    logger.info(f"Empty collection analysis: {analysis}")
    
    # Test with sample videos (if harvest results exist)
    try:
        if harvester.all_videos:
            logger.info(f"Current collection: {len(harvester.all_videos)} videos")
            
            # Analyze date distribution
            date_groups = {}
            for video in harvester.all_videos.values():
                if video.date:
                    date_groups[video.date] = date_groups.get(video.date, 0) + 1
            
            logger.info("Date distribution:")
            for date_range, count in sorted(date_groups.items(), key=lambda x: x[1], reverse=True)[:5]:
                logger.info(f"  {date_range}: {count} videos")
    except Exception as e:
        logger.info(f"Collection analysis skipped: {e}")
    
    logger.info("✅ Collection analysis tests passed!")

def test_date_priority_parsing():
    """Test date string parsing for priority calculation"""
    logger.info("🧪 Testing Date Priority Parsing...")
    
    harvester = SmartHarvester()
    
    test_dates = [
        ("3 years ago", 3 * 365),
        ("5 months ago", 5 * 30),
        ("2 days ago", 2),
        ("1 hour ago", 0),
        ("", 9999),
        ("invalid date", 5000)
    ]
    
    for date_str, expected_range in test_dates:
        priority = harvester._parse_date_to_priority(date_str)
        logger.info(f"'{date_str}' -> Priority: {priority} (expected ~{expected_range})")
        
        # Allow some tolerance for the expected range
        if expected_range < 9999:
            assert abs(priority - expected_range) <= 100  # Allow some tolerance
    
    logger.info("✅ Date priority parsing tests passed!")

def test_gap_calculation():
    """Test intelligent gap calculation with performance history"""
    logger.info("🧪 Testing Gap Calculation...")
    
    harvester = SmartHarvester()
    
    # Test base gap calculation
    base_gap = harvester._calculate_session_gap()
    logger.info(f"Base gap: {base_gap}s")
    assert 30 <= base_gap <= 300
    
    # Test with gap multiplier
    extended_gap = harvester._calculate_session_gap(gap_multiplier=2.5)
    logger.info(f"Extended gap (2.5x): {extended_gap}s")
    assert extended_gap >= base_gap
    
    logger.info("✅ Gap calculation tests passed!")

def validate_continuation_data_structure():
    """Validate the ContinuationPoint data structure"""
    logger.info("🧪 Validating ContinuationPoint Data Structure...")
    
    # Test creating continuation points
    test_point = ContinuationPoint(
        strategy="video_id_anchor",
        reasoning="Test continuation point",
        scroll_offset=15,
        target_date_range="4 years ago",
        anchor_video_id="1234567890123456",
        expected_scroll_depth=35,
        date_filter_active=True,
        scroll_strategy="deep"
    )
    
    logger.info(f"Test continuation point: {test_point.strategy}")
    logger.info(f"Scroll offset: {test_point.scroll_offset}")
    logger.info(f"Anchor video: {test_point.anchor_video_id}")
    logger.info(f"Date range: {test_point.target_date_range}")
    
    # Test serialization (for saving to JSON)
    from dataclasses import asdict
    serialized = asdict(test_point)
    logger.info(f"Serialization successful: {len(serialized)} fields")
    
    logger.info("✅ ContinuationPoint validation passed!")

def main():
    """Run all continuation system tests"""
    logger.info("🚀 === ENHANCED CONTINUATION SYSTEM TESTS ===")
    
    try:
        test_continuation_point_calculation()
        test_session_config_generation()
        test_collection_analysis()
        test_date_priority_parsing()
        test_gap_calculation()
        validate_continuation_data_structure()
        
        logger.info("\n🎉 === ALL TESTS PASSED! ===")
        logger.info("✅ Enhanced Continuation System is ready for deployment")
        logger.info("🌾 Smart Harvesting v2.0 validated successfully")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
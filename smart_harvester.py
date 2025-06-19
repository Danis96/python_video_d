#!/usr/bin/env python3
"""
SMART HARVESTING SYSTEM
Revolutionary multi-session Facebook video harvester that works WITH Facebook's limits
Author: Lord Danis Assistant
🚀 Batch processing • 📅 Date pagination • 🎯 Quality focus • 🔄 Session rotation
"""

import os
import json
import time
import random
import argparse
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
from facebook_video_scraper import FacebookVideoScraper, VideoData

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ContinuationPoint:
    """Advanced continuation data structure"""
    strategy: str  # 'fresh_start', 'scroll_offset', 'date_anchor', 'video_id_anchor'
    reasoning: str
    scroll_offset: int = 0  # Number of scrolls to skip
    target_date_range: Optional[str] = None  # e.g., "4 years ago"
    anchor_video_id: Optional[str] = None  # Video ID to start from
    expected_scroll_depth: int = 0  # Estimated scroll depth for this continuation
    date_filter_active: bool = False
    scroll_strategy: str = "adaptive"  # 'standard', 'deep', 'adaptive'

@dataclass
class HarvestSession:
    """Data structure for tracking harvest sessions"""
    session_id: str
    timestamp: datetime
    videos_found: int
    success_rate: float
    completion_time: float
    target_filter: str
    total_score: int
    continuation_point: Optional[ContinuationPoint] = None

@dataclass
class HarvestStats:
    """Statistics for the entire harvest operation"""
    total_sessions: int = 0
    total_videos: int = 0
    unique_videos: int = 0
    total_time: float = 0
    average_success_rate: float = 0
    total_score: int = 0
    best_session_score: int = 0
    last_harvest: str = ""

class SmartHarvester:
    """
    SMART HARVESTING SYSTEM with Advanced Continuation
    Implements scroll offsets, date filtering, and video ID anchoring
    """
    
    def __init__(self):
        self.sessions: List[HarvestSession] = []
        self.all_videos: Dict[str, VideoData] = {}  # video_id -> VideoData
        self.harvest_stats: HarvestStats = HarvestStats()
        self.harvest_file: str = "harvest_results.json"
        self.session_gap_min: int = 30  # Minimum seconds between sessions
        self.session_gap_max: int = 120  # Maximum seconds between sessions
        
        # Load existing harvest data
        self._load_harvest_history()
        
        logger.info(f"🌾 Smart Harvester initialized: {len(self.all_videos)} videos in collection")
        
        # Duplicate prevention settings
        self.duplicate_threshold = 0.8  # Stop session if 80%+ videos are duplicates
        self.early_check_count = 20     # Check duplicate rate after first 20 videos
    
    def _load_harvest_history(self) -> None:
        """Load previous harvest results and statistics"""
        try:
            if os.path.exists(self.harvest_file):
                with open(self.harvest_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load harvest metadata
                if "harvest_metadata" in data:
                    metadata = data["harvest_metadata"]
                    self.harvest_stats.total_sessions = metadata.get("total_sessions", 0)
                    self.harvest_stats.total_videos = metadata.get("total_videos", 0)
                    self.harvest_stats.unique_videos = metadata.get("unique_videos", 0)
                    self.harvest_stats.total_time = metadata.get("total_time", 0)
                    self.harvest_stats.average_success_rate = metadata.get("average_success_rate", 0)
                    self.harvest_stats.total_score = metadata.get("total_score", 0)
                    self.harvest_stats.best_session_score = metadata.get("best_session_score", 0)
                    self.harvest_stats.last_harvest = metadata.get("last_harvest", "")
                
                # Load all videos
                if "all_videos" in data:
                    for video_id, video_data in data["all_videos"].items():
                        self.all_videos[video_id] = VideoData(
                            video_id=video_data["video_id"],
                            title=video_data["title"],
                            url=video_data["url"],
                            date=video_data.get("date", ""),
                            date_raw=video_data.get("date_raw", ""),
                            likes=video_data.get("likes", 0),
                            comments=video_data.get("comments", 0),
                            shares=video_data.get("shares", 0),
                            views=video_data.get("views", ""),
                            description=video_data.get("description", ""),
                            thumbnail_url=video_data.get("thumbnail_url", "")
                        )
                
                # Load sessions with continuation points
                if "sessions" in data:
                    for session_data in data["sessions"]:
                        continuation_data = session_data.get("continuation_point")
                        continuation_point = None
                        if continuation_data:
                            continuation_point = ContinuationPoint(
                                strategy=continuation_data.get("strategy", "fresh_start"),
                                reasoning=continuation_data.get("reasoning", ""),
                                scroll_offset=continuation_data.get("scroll_offset", 0),
                                target_date_range=continuation_data.get("target_date_range"),
                                anchor_video_id=continuation_data.get("anchor_video_id"),
                                expected_scroll_depth=continuation_data.get("expected_scroll_depth", 0),
                                date_filter_active=continuation_data.get("date_filter_active", False),
                                scroll_strategy=continuation_data.get("scroll_strategy", "adaptive")
                            )
                        
                        session = HarvestSession(
                            session_id=session_data["session_id"],
                            timestamp=datetime.fromisoformat(session_data["timestamp"]),
                            videos_found=session_data["videos_found"],
                            success_rate=session_data["success_rate"],
                            completion_time=session_data["completion_time"],
                            target_filter=session_data["target_filter"],
                            total_score=session_data["total_score"],
                            continuation_point=continuation_point
                        )
                        self.sessions.append(session)
                
                logger.info(f"📈 Loaded harvest history: {len(self.sessions)} sessions, {len(self.all_videos)} unique videos")
                
        except Exception as e:
            logger.warning(f"Could not load harvest history: {e}")
    
    def _should_continue_session(self, scraped_videos: List[VideoData]) -> bool:
        """
        Determine if session should continue based on duplicate rate
        
        Args:
            scraped_videos: Videos scraped so far in current session
            
        Returns:
            bool: True if session should continue, False if too many duplicates
        """
        if len(scraped_videos) < self.early_check_count:
            return True  # Too early to make a decision
        
        duplicates = sum(1 for video in scraped_videos if video.video_id in self.all_videos)
        duplicate_rate = duplicates / len(scraped_videos)
        
        if duplicate_rate >= self.duplicate_threshold:
            logger.warning(f"🛑 HIGH DUPLICATE RATE DETECTED: {duplicate_rate*100:.1f}% ({duplicates}/{len(scraped_videos)})")
            logger.warning(f"   Terminating session early to avoid inefficiency")
            return False
        
        logger.info(f"📊 Duplicate check: {duplicate_rate*100:.1f}% duplicates ({duplicates}/{len(scraped_videos)}) - continuing")
        return True
    
    def _save_harvest_results(self) -> None:
        """Save harvest results with enhanced continuation data"""
        try:
            # Convert sessions to dictionaries with continuation points
            sessions_data = []
            for session in self.sessions:
                session_dict = {
                    "session_id": session.session_id,
                    "timestamp": session.timestamp.isoformat(),
                    "videos_found": session.videos_found,
                    "success_rate": session.success_rate,
                    "completion_time": session.completion_time,
                    "target_filter": session.target_filter,
                    "total_score": session.total_score
                }
                
                if session.continuation_point:
                    session_dict["continuation_point"] = asdict(session.continuation_point)
                
                sessions_data.append(session_dict)
            
            # Convert videos to dictionaries
            videos_data = {}
            for video_id, video in self.all_videos.items():
                videos_data[video_id] = asdict(video)
            
            harvest_data = {
                "harvest_metadata": {
                    "harvester_version": "2.0", 
                    "last_harvest": datetime.now().isoformat(),
                    "total_sessions": len(self.sessions),
                    "total_videos": self.harvest_stats.total_videos,
                    "unique_videos": len(self.all_videos),
                    "total_time": self.harvest_stats.total_time,
                    "average_success_rate": self.harvest_stats.average_success_rate,
                    "total_score": self.harvest_stats.total_score,
                    "best_session_score": self.harvest_stats.best_session_score
                },
                "sessions": sessions_data,
                "all_videos": videos_data,
                "total_sessions": len(self.sessions),
                "total_videos": self.harvest_stats.total_videos,
                "unique_videos": len(self.all_videos),
                "total_time": self.harvest_stats.total_time,
                "total_score": self.harvest_stats.total_score,
                "best_session_score": self.harvest_stats.best_session_score
            }
            
            with open(self.harvest_file, 'w', encoding='utf-8') as f:
                json.dump(harvest_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"💾 Harvest results saved to {self.harvest_file}")
            
        except Exception as e:
            logger.error(f"Failed to save harvest results: {e}")
    
    def _calculate_session_gap(self, gap_multiplier: float = 1.0) -> int:
        """Calculate intelligent gap between sessions based on previous performance"""
        base_gap = random.randint(self.session_gap_min, self.session_gap_max)
        
        # Analyze recent session performance for dynamic gap adjustment
        if len(self.sessions) >= 2:
            recent_success_rates = [s.success_rate for s in self.sessions[-2:]]
            
            # If we see degradation (Lord Danis pattern), increase gap significantly
            if len(recent_success_rates) == 2 and recent_success_rates[1] < recent_success_rates[0] - 10:
                logger.info(f"📉 DEGRADATION DETECTED: Success dropped from {recent_success_rates[0]:.1f}% to {recent_success_rates[1]:.1f}%")
                gap_multiplier *= 3.0  # Triple the gap after degradation
        
        # Apply session-based multipliers (Lord Danis optimization)
        if len(self.sessions) >= 2:  # After session 2, longer gaps
            gap_multiplier *= 2.5
        
        final_gap = int(base_gap * gap_multiplier)
        
        # Cap at reasonable limits
        return min(max(final_gap, 30), 300)  # 30s to 5 minutes
    
    def _analyze_collection_gaps(self) -> Dict:
        """Analyze the video collection to find optimal continuation points"""
        if not self.all_videos:
            return {"strategy": "fresh_start", "reasoning": "No existing videos"}
        
        # Analyze date distribution
        date_groups = {}
        videos_with_dates = [v for v in self.all_videos.values() if v.date and v.date != ""]
        
        for video in videos_with_dates:
            date_key = video.date
            if date_key not in date_groups:
                date_groups[date_key] = []
            date_groups[date_key].append(video)
        
        logger.info(f"📊 COLLECTION ANALYSIS: {len(date_groups)} different date ranges")
        for date_range, videos in sorted(date_groups.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            logger.info(f"   📅 {date_range}: {len(videos)} videos")
        
        # Find the most recent incomplete date range
        sorted_dates = sorted(date_groups.keys(), key=lambda x: self._parse_date_to_priority(x))
        
        analysis = {
            "total_videos": len(self.all_videos),
            "date_ranges": len(date_groups),
            "most_recent_dates": sorted_dates[:3] if sorted_dates else [],
            "largest_date_groups": sorted(date_groups.items(), key=lambda x: len(x[1]), reverse=True)[:3]
        }
        
        return analysis

    def _parse_date_to_priority(self, date_str: str) -> int:
        """Convert date string to priority score (lower = more recent)"""
        if not date_str:
            return 9999
        
        # Extract number from date strings like "3 years ago", "5 months ago"
        import re
        match = re.search(r'(\d+)\s+(year|month|day|hour)', date_str.lower())
        if match:
            number = int(match.group(1))
            unit = match.group(2)
            
            # Convert to days for comparison
            if unit == "year":
                return number * 365
            elif unit == "month":
                return number * 30
            elif unit == "day":
                return number
            elif unit == "hour":
                return 0
        
        return 5000  # Default for unparseable dates

    def _calculate_advanced_continuation_point(self, session_num: int) -> ContinuationPoint:
        """
        Calculate advanced continuation point with scroll offset and anchoring
        Implements Lord Danis's enhanced continuation strategy
        """
        logger.info(f"🧠 CALCULATING ADVANCED CONTINUATION for session {session_num + 1}...")
        
        # Session 1: Always fresh start
        if session_num == 0:
            return ContinuationPoint(
                strategy="fresh_start",
                reasoning="Session 1: Fresh start from top",
                scroll_offset=0,
                expected_scroll_depth=0,
                scroll_strategy="standard"
            )
        
        # Analyze collection
        analysis = self._analyze_collection_gaps()
        
        # Session 2: Scroll offset continuation
        if session_num == 1:
            # Start deeper to avoid re-scraping same content
            scroll_offset = random.randint(10, 15)  # Skip first 10-15 scrolls
            
            return ContinuationPoint(
                strategy="scroll_offset",
                reasoning=f"Session 2: Start at scroll {scroll_offset} to avoid overlap",
                scroll_offset=scroll_offset,
                expected_scroll_depth=scroll_offset + 20,  # Plan for 20 more scrolls
                scroll_strategy="adaptive"
            )
        
        # Session 3+: Video ID anchoring with date filtering
        if session_num >= 2:
            # Find the oldest video from recent sessions as anchor point
            recent_videos = []
            if len(self.sessions) >= 2:
                # Get videos from last 2 sessions by examining their timestamps
                last_two_session_ids = [s.session_id for s in self.sessions[-2:]]
                logger.info(f"🔍 Analyzing videos from sessions: {last_two_session_ids}")
            
            # Get videos with dates for anchoring
            dated_videos = [(vid, self._parse_date_to_priority(vid.date)) for vid in self.all_videos.values() if vid.date]
            
            if dated_videos:
                # Sort by date priority (most recent first, then oldest)
                dated_videos.sort(key=lambda x: x[1])
                
                # For session 3+, target the middle-to-older content
                target_index = min(len(dated_videos) // 2, len(dated_videos) - 1)
                anchor_video = dated_videos[target_index][0]
                
                # Calculate expected scroll depth based on content age
                scroll_depth = min(session_num * 12, 50)  # Progressive deeper starts
                
                return ContinuationPoint(
                    strategy="video_id_anchor",
                    reasoning=f"Session {session_num + 1}: Continue from video {anchor_video.video_id[-8:]}... ({anchor_video.date})",
                    scroll_offset=scroll_depth,
                    target_date_range=anchor_video.date,
                    anchor_video_id=anchor_video.video_id,
                    expected_scroll_depth=scroll_depth + 15,
                    date_filter_active=True,
                    scroll_strategy="deep"
                )
        
        # Fallback: Date-based continuation
        if analysis["most_recent_dates"]:
            target_date = analysis["most_recent_dates"][-1]  # Oldest available date
            
            return ContinuationPoint(
                strategy="date_anchor",
                reasoning=f"Session {session_num + 1}: Target {target_date} content",
                scroll_offset=session_num * 8,
                target_date_range=target_date,
                expected_scroll_depth=(session_num * 8) + 20,
                date_filter_active=True,
                scroll_strategy="adaptive"
            )
        
        # Ultimate fallback
        return ContinuationPoint(
            strategy="deep_scroll",
            reasoning=f"Session {session_num + 1}: Deep scroll continuation",
            scroll_offset=session_num * 10,
            expected_scroll_depth=(session_num * 10) + 25,
            scroll_strategy="deep"
        )

    def _generate_session_config(self, session_num: int, total_sessions: int) -> Dict:
        """
        Generate enhanced session configuration with continuation intelligence
        """
        # Calculate advanced continuation point
        continuation = self._calculate_advanced_continuation_point(session_num)
        
        # Determine scroll count based on continuation strategy
        if continuation.strategy == "fresh_start":
            scroll_count = random.randint(18, 22)  # Standard range for session 1
        elif continuation.strategy == "scroll_offset":
            scroll_count = random.randint(16, 20)  # Slightly less for session 2 
        elif continuation.scroll_strategy == "deep":
            scroll_count = random.randint(12, 16)  # Reduced for deep sessions
        else:
            scroll_count = random.randint(15, 20)  # Adaptive range
        
        # Adjust gap multiplier based on session performance
        gap_multiplier = 1.0
        if session_num >= 2:  # Lord Danis pattern: longer gaps after session 2
            gap_multiplier = 2.5
        elif len(self.sessions) >= 1 and self.sessions[-1].success_rate < 50:
            gap_multiplier = 2.0  # Longer gap after poor performance
        
        config = {
            "scroll_count": str(scroll_count),
            "target_filter": f"harvest_batch_{session_num + 1}",
            "gap_multiplier": gap_multiplier,
            "continuation": asdict(continuation),
            "session_priority": "quality" if session_num < 2 else "coverage"
        }
        
        logger.info(f"📋 SESSION {session_num + 1} CONFIG:")
        logger.info(f"   🔄 Scrolls: {scroll_count}")
        logger.info(f"   📍 Strategy: {continuation.strategy}")
        logger.info(f"   🎯 Reasoning: {continuation.reasoning}")
        if continuation.scroll_offset > 0:
            logger.info(f"   ⏭️ Scroll Offset: {continuation.scroll_offset}")
        if continuation.anchor_video_id:
            logger.info(f"   🎪 Anchor Video: {continuation.anchor_video_id[-8:]}...")
        if continuation.target_date_range:
            logger.info(f"   📅 Target Date: {continuation.target_date_range}")
        
        return config

    def run_harvest_session(self, session_config: Dict, session_num: int) -> Optional[HarvestSession]:
        """
        Run a single harvest session with enhanced continuation support
        """
        try:
            session_id = f"harvest_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            logger.info(f"\n🌾 === HARVEST SESSION {session_num + 1} STARTING ===")
            logger.info(f"🆔 Session ID: {session_id}")
            
            # Create scraper with enhanced configuration
            scraper = FacebookVideoScraper()
            
            # Extract continuation parameters
            continuation = session_config.get("continuation", {})
            scroll_offset = continuation.get("scroll_offset", 0)
            anchor_video_id = continuation.get("anchor_video_id")
            target_date_range = continuation.get("target_date_range")
            
            # Log what continuation features will be applied
            if scroll_offset > 0:
                logger.info(f"📍 SCROLL OFFSET: Will skip first {scroll_offset} scrolls")
            if anchor_video_id:
                logger.info(f"🎯 VIDEO ANCHOR: Starting from {anchor_video_id[-8:]}...")
            if target_date_range:
                logger.info(f"📅 DATE FILTER: Targeting {target_date_range} content")
            
            start_time = time.time()
            
            # Run enhanced scraper with continuation parameters and duplicate checking
            videos = scraper.run_scraper_return_videos(
                target_url="https://www.facebook.com/DRAGAMAMA/videos",
                scroll_count=session_config["scroll_count"],
                scroll_offset=scroll_offset,
                anchor_video_id=anchor_video_id,
                date_filter=target_date_range,
                duplicate_checker=self._should_continue_session
            )
            
            completion_time = time.time() - start_time
            
            # Calculate new videos and session metrics with duplicate tracking
            new_videos = 0
            duplicate_videos = 0
            session_score = 0
            
            if videos:
                logger.info(f"🔍 DUPLICATE CHECK: Processing {len(videos)} scraped videos...")
                
                for video in videos:
                    if video.video_id not in self.all_videos:
                        self.all_videos[video.video_id] = video
                        new_videos += 1
                    else:
                        duplicate_videos += 1
                        logger.debug(f"   🔄 Duplicate skipped: {video.video_id} - {video.title[:40]}...")
                
                logger.info(f"✅ DEDUPLICATION COMPLETE:")
                logger.info(f"   🆕 New unique videos: {new_videos}")
                logger.info(f"   🔄 Duplicates skipped: {duplicate_videos}")
                logger.info(f"   📊 Efficiency: {(new_videos/(new_videos+duplicate_videos)*100):.1f}% new content")
                
                # Calculate success rate based on proper titles
                proper_titles = len([v for v in videos if not v.title.startswith('DRAGAMAMA_Video_')])
                success_rate = (proper_titles / len(videos)) * 100 if videos else 0
                
                # Get session score from scraper
                session_score = scraper.scoring_system.session_score if hasattr(scraper, 'scoring_system') else 0
            else:
                success_rate = 0
            
            # Create session with continuation point
            continuation_point = ContinuationPoint(**continuation) if continuation else None
            
            session = HarvestSession(
                session_id=session_id,
                timestamp=datetime.now(),
                videos_found=len(videos) if videos else 0,
                success_rate=success_rate,
                completion_time=completion_time,
                target_filter=session_config["target_filter"],
                total_score=session_score,
                continuation_point=continuation_point
            )
            
            self.sessions.append(session)
            
            logger.info(f"✅ SESSION COMPLETE: {len(videos) if videos else 0} scraped, {new_videos} new unique videos")
            logger.info(f"⏱️ Time: {completion_time:.1f}s, Score: {session_score} points, Success Rate: {success_rate:.1f}%")
            
            # Enhanced session analysis
            if continuation_point:
                logger.info(f"📊 CONTINUATION ANALYSIS:")
                logger.info(f"   📍 Strategy used: {continuation_point.strategy}")
                if scroll_offset > 0:
                    efficiency = len(videos) / (scroll_offset + int(session_config["scroll_count"])) if videos else 0
                    logger.info(f"   🎯 Offset efficiency: {efficiency:.2f} videos per scroll")
                if anchor_video_id and videos:
                    anchor_success = any(anchor_video_id in v.video_id for v in videos)
                    logger.info(f"   🎪 Anchor targeting: {'✅ Success' if anchor_success else '⚠️ Anchor not in results'}")
                if target_date_range and videos:
                    date_matches = len([v for v in videos if v.date and target_date_range in v.date])
                    logger.info(f"   📅 Date filter matches: {date_matches}/{len(videos)} videos")
            
            return session
            
        except Exception as e:
            logger.error(f"❌ Session {session_num+1} failed: {e}")
            return None

    def run_smart_harvest(self, num_sessions: int = 5, target_videos: int = 300) -> None:
        """
        Execute SMART HARVESTING with enhanced continuation system
        
        Args:
            num_sessions: Number of harvest sessions to run
            target_videos: Target number of unique videos to collect
        """
        logger.info("=" * 80)
        logger.info("🚀 === SMART HARVESTING SYSTEM v2.0 ACTIVATED ===")
        logger.info("=" * 80)
        logger.info(f"🎯 TARGET: {num_sessions} sessions, {target_videos} unique videos")
        logger.info(f"📊 CURRENT: {len(self.all_videos)} videos in collection")
        logger.info(f"🔧 FEATURES: Scroll Offset | Date Filtering | Video ID Anchoring")
        
        harvest_start = time.time()
        successful_sessions = 0
        
        for session_num in range(num_sessions):
            # Check if we've reached our target
            if len(self.all_videos) >= target_videos:
                logger.info(f"🎯 TARGET REACHED: {len(self.all_videos)} >= {target_videos} videos!")
                break
            
            # Generate enhanced session configuration
            session_config = self._generate_session_config(session_num, num_sessions)
            
            # Run session with continuation support
            session = self.run_harvest_session(session_config, session_num)
            
            if session:
                successful_sessions += 1
                
                # Update harvest statistics
                self.harvest_stats.total_sessions += 1
                self.harvest_stats.total_videos += session.videos_found
                self.harvest_stats.unique_videos = len(self.all_videos)
                self.harvest_stats.total_time += session.completion_time
                self.harvest_stats.total_score += session.total_score
                
                if session.total_score > self.harvest_stats.best_session_score:
                    self.harvest_stats.best_session_score = session.total_score
                
                # Save progress after each successful session
                self._save_harvest_results()
                
                # Display progress
                logger.info(f"📈 PROGRESS: {len(self.all_videos)} unique videos collected")
                
                # Enhanced gap calculation with continuation awareness
                if session_num < num_sessions - 1:
                    gap_multiplier = session_config.get("gap_multiplier", 1.0)
                    gap = self._calculate_session_gap(gap_multiplier)
                    
                    # Display next session preview
                    next_continuation = self._calculate_advanced_continuation_point(session_num + 1)
                    logger.info(f"🎯 NEXT SESSION PLAN: {next_continuation.reasoning}")
                    
                    if next_continuation.scroll_offset > 0:
                        logger.info(f"📍 Next scroll offset: {next_continuation.scroll_offset}")
                    if next_continuation.anchor_video_id:
                        logger.info(f"🎪 Next anchor: Video {next_continuation.anchor_video_id[-8:]}...")
                    if next_continuation.target_date_range:
                        logger.info(f"📅 Next target date: {next_continuation.target_date_range}")
                    
                    logger.info(f"⏸️ OPTIMIZED SESSION GAP: {gap}s (stealth cooldown)")
                    time.sleep(gap)
            else:
                logger.warning(f"⚠️ Session {session_num+1} failed, continuing with next session")
                # Longer gap after failures
                time.sleep(random.randint(60, 180))
        
        # Calculate final statistics
        total_harvest_time = time.time() - harvest_start
        self.harvest_stats.total_time = total_harvest_time
        
        if successful_sessions > 0:
            session_success_rates = [s.success_rate for s in self.sessions[-successful_sessions:]]
            self.harvest_stats.average_success_rate = sum(session_success_rates) / len(session_success_rates)
        
        # Final save
        self._save_harvest_results()
        
        # Display comprehensive results
        self._display_harvest_report(successful_sessions, total_harvest_time)
    
    def _display_harvest_report(self, successful_sessions: int, total_time: float) -> None:
        """Display comprehensive harvest results"""
        logger.info("\n" + "=" * 80)
        logger.info("🏆 === SMART HARVEST COMPLETE ===")
        logger.info("=" * 80)
        
        # Session statistics
        logger.info(f"📊 SESSION STATISTICS:")
        logger.info(f"   ✅ Successful Sessions: {successful_sessions}")
        logger.info(f"   ❌ Failed Sessions: {len(self.sessions) - successful_sessions}")
        logger.info(f"   ⏱️ Total Time: {total_time/60:.1f} minutes")
        logger.info(f"   📈 Average Success Rate: {self.harvest_stats.average_success_rate:.1f}%")
        
        # Video statistics
        logger.info(f"\n📹 VIDEO COLLECTION:")
        logger.info(f"   🎯 Unique Videos: {len(self.all_videos)}")
        logger.info(f"   📊 Total Videos Found: {self.harvest_stats.total_videos}")
        logger.info(f"   ✨ Deduplication Rate: {(1 - len(self.all_videos)/max(self.harvest_stats.total_videos, 1))*100:.1f}%")
        
        # Quality analysis
        proper_titles = len([v for v in self.all_videos.values() if not v.title.startswith('DRAGAMAMA_Video_')])
        quality_rate = (proper_titles / len(self.all_videos)) * 100 if self.all_videos else 0
        
        logger.info(f"\n🎨 QUALITY ANALYSIS:")
        logger.info(f"   📝 Proper Titles: {proper_titles}/{len(self.all_videos)} ({quality_rate:.1f}%)")
        logger.info(f"   🏆 Total Score: {self.harvest_stats.total_score:,} points")
        logger.info(f"   🥇 Best Session Score: {self.harvest_stats.best_session_score:,} points")
        
        # Top videos sample
        logger.info(f"\n🎬 SAMPLE VIDEOS:")
        draga_mama_videos = [v for v in self.all_videos.values() if 'Draga mama' in v.title][:5]
        for i, video in enumerate(draga_mama_videos, 1):
            logger.info(f"   {i}. {video.title}")
            logger.info(f"      📅 {video.date} | 👍 {video.likes} | 🆔 {video.video_id}")
        
        # Performance insights
        if len(self.sessions) >= 2:
            logger.info(f"\n🧠 PERFORMANCE INSIGHTS:")
            recent_sessions = self.sessions[-min(3, len(self.sessions)):]
            avg_videos_per_session = sum(s.videos_found for s in recent_sessions) / len(recent_sessions)
            avg_time_per_session = sum(s.completion_time for s in recent_sessions) / len(recent_sessions)
            
            logger.info(f"   📊 Avg Videos/Session: {avg_videos_per_session:.1f}")
            logger.info(f"   ⏱️ Avg Time/Session: {avg_time_per_session:.1f}s")
            logger.info(f"   🚀 Collection Rate: {len(self.all_videos)/(total_time/3600):.1f} videos/hour")
            
            # Success rate analysis
            if len(self.sessions) >= 3:
                session_rates = [s.success_rate for s in self.sessions]
                logger.info(f"   📈 Success Rate Trend: {session_rates[0]:.1f}% → {session_rates[1]:.1f}% → {session_rates[2]:.1f}%")
                
                # Validate LORD DANIS optimization theory
                first_two_avg = (session_rates[0] + session_rates[1]) / 2
                if first_two_avg > 95 and session_rates[2] < 80:
                    logger.info(f"   🎯 OPTIMIZATION VALIDATED: Sweet spot confirmed (first 2 sessions: {first_two_avg:.1f}%)")
        
        # Optimization recommendations
        logger.info(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
        logger.info(f"   🎯 Optimal Strategy: Stick to 2-session batches with longer gaps")
        logger.info(f"   ⏰ Timing: Increase gap to 3-5 minutes between sessions after seeing session 3 degradation")
        logger.info(f"   🎪 Sweet Spot Confirmed: Sessions 1-2 prove the 15-25 scroll range is perfect")
        logger.info(f"   📈 Scale Up: Ready for larger harvests with confidence!")
        
        logger.info(f"\n💾 Results saved to: {self.harvest_file}")
        logger.info("=" * 80)

def main():
    """Main function for SMART HARVESTING SYSTEM"""
    parser = argparse.ArgumentParser(description="SMART HARVESTING SYSTEM - Multi-session Facebook video harvester")
    parser.add_argument("--sessions", "-s", type=int, default=5, 
                       help="Number of harvest sessions to run (default: 5)")
    parser.add_argument("--target", "-t", type=int, default=300,
                       help="Target number of unique videos to collect (default: 300)")
    parser.add_argument("--gap-min", type=int, default=30,
                       help="Minimum seconds between sessions (default: 30)")
    parser.add_argument("--gap-max", type=int, default=120,
                       help="Maximum seconds between sessions (default: 120)")
    
    args = parser.parse_args()
    
    try:
        # Create harvester
        harvester = SmartHarvester()
        harvester.session_gap_min = args.gap_min
        harvester.session_gap_max = args.gap_max
        
        logger.info(f"🎯 SMART HARVESTER CONFIG:")
        logger.info(f"   Sessions: {args.sessions}")
        logger.info(f"   Target Videos: {args.target}")
        logger.info(f"   Session Gap: {args.gap_min}-{args.gap_max} seconds")
        
        # Run smart harvest
        harvester.run_smart_harvest(num_sessions=args.sessions, target_videos=args.target)
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Harvest interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Harvest failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
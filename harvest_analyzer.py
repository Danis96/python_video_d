#!/usr/bin/env python3
"""
SMART HARVEST ANALYZER
Comprehensive analysis tool for harvest results with insights and recommendations
Author: Lord Danis Assistant
📊 Statistics • 📈 Trends • 🎯 Insights • 📋 Reports
"""

import os
import json
import argparse
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class AnalysisReport:
    """Comprehensive analysis report"""
    total_videos: int
    unique_videos: int
    duplicate_rate: float
    quality_scores: Dict
    session_performance: Dict
    recommendations: List[str]
    trend_analysis: Dict

class HarvestAnalyzer:
    """
    SMART HARVEST ANALYZER
    
    📊 Analyze harvest performance and quality
    📈 Identify trends and patterns
    🎯 Generate actionable insights
    📋 Create comprehensive reports
    """
    
    def __init__(self, harvest_file: str = "harvest_results.json"):
        self.harvest_file = harvest_file
        self.harvest_data = {}
        self.load_harvest_data()
    
    def load_harvest_data(self) -> None:
        """Load harvest data from file"""
        try:
            if os.path.exists(self.harvest_file):
                with open(self.harvest_file, 'r', encoding='utf-8') as f:
                    self.harvest_data = json.load(f)
                logger.info(f"📊 Loaded harvest data: {len(self.harvest_data.get('all_videos', {}))} videos")
            else:
                logger.error(f"❌ Harvest file not found: {self.harvest_file}")
                
        except Exception as e:
            logger.error(f"Failed to load harvest data: {e}")
    
    def analyze_video_quality(self) -> Dict:
        """Analyze video title quality and extraction success"""
        videos = self.harvest_data.get('all_videos', {})
        if not videos:
            return {}
        
        quality_analysis = {
            'total_videos': len(videos),
            'proper_titles': 0,
            'failed_extractions': 0,
            'draga_mama_episodes': 0,
            'with_dates': 0,
            'with_engagement': 0,
            'episode_numbers': [],
            'quality_breakdown': {
                'excellent': 0,  # Perfect episode titles
                'good': 0,       # Good titles but not perfect
                'fair': 0,       # Basic titles
                'poor': 0        # Failed extractions
            }
        }
        
        for video_id, video_data in videos.items():
            title = video_data.get('title', '')
            date = video_data.get('date', '')
            likes = video_data.get('likes', 0)
            
            # Count dates and engagement
            if date:
                quality_analysis['with_dates'] += 1
            if likes > 0:
                quality_analysis['with_engagement'] += 1
            
            # Analyze title quality
            if title.startswith('DRAGAMAMA_Video_'):
                quality_analysis['failed_extractions'] += 1
                quality_analysis['quality_breakdown']['poor'] += 1
            else:
                quality_analysis['proper_titles'] += 1
                
                # Check for Draga mama episodes
                if 'Draga mama' in title:
                    quality_analysis['draga_mama_episodes'] += 1
                    
                    # Extract episode number
                    import re
                    episode_match = re.search(r'Draga mama (\d{3,4})', title)
                    if episode_match:
                        episode_num = int(episode_match.group(1))
                        quality_analysis['episode_numbers'].append(episode_num)
                    
                    # Quality classification
                    if 'Draga mama' in title and '"' in title:
                        quality_analysis['quality_breakdown']['excellent'] += 1
                    elif 'Draga mama' in title:
                        quality_analysis['quality_breakdown']['good'] += 1
                    else:
                        quality_analysis['quality_breakdown']['fair'] += 1
                else:
                    quality_analysis['quality_breakdown']['fair'] += 1
        
        # Calculate percentages
        total = quality_analysis['total_videos']
        quality_analysis['success_rate'] = (quality_analysis['proper_titles'] / total * 100) if total > 0 else 0
        quality_analysis['episode_rate'] = (quality_analysis['draga_mama_episodes'] / total * 100) if total > 0 else 0
        quality_analysis['date_rate'] = (quality_analysis['with_dates'] / total * 100) if total > 0 else 0
        quality_analysis['engagement_rate'] = (quality_analysis['with_engagement'] / total * 100) if total > 0 else 0
        
        return quality_analysis
    
    def analyze_episode_coverage(self) -> Dict:
        """Analyze episode number coverage and find gaps"""
        videos = self.harvest_data.get('all_videos', {})
        episode_analysis = {
            'episode_numbers': [],
            'episode_range': {},
            'gaps': [],
            'coverage_stats': {}
        }
        
        import re
        for video_data in videos.values():
            title = video_data.get('title', '')
            episode_match = re.search(r'Draga mama (\d{3,4})', title)
            if episode_match:
                episode_num = int(episode_match.group(1))
                episode_analysis['episode_numbers'].append(episode_num)
        
        if episode_analysis['episode_numbers']:
            episodes = sorted(episode_analysis['episode_numbers'])
            episode_analysis['episode_range'] = {
                'min': min(episodes),
                'max': max(episodes),
                'span': max(episodes) - min(episodes) + 1
            }
            
            # Find gaps
            full_range = set(range(min(episodes), max(episodes) + 1))
            found_episodes = set(episodes)
            gaps = sorted(list(full_range - found_episodes))
            episode_analysis['gaps'] = gaps
            
            episode_analysis['coverage_stats'] = {
                'episodes_found': len(episodes),
                'total_possible': len(full_range),
                'coverage_rate': len(found_episodes) / len(full_range) * 100,
                'missing_count': len(gaps)
            }
        
        return episode_analysis
    
    def run_complete_analysis(self) -> AnalysisReport:
        """Run complete analysis and generate comprehensive report"""
        if not self.harvest_data:
            logger.error("❌ No harvest data available for analysis")
            return None
        
        logger.info("🔍 Running comprehensive harvest analysis...")
        
        # Perform analyses
        quality_analysis = self.analyze_video_quality()
        episode_analysis = self.analyze_episode_coverage()
        
        # Generate visual report
        self._display_visual_report(quality_analysis, episode_analysis)
        
        return AnalysisReport(
            total_videos=quality_analysis.get('total_videos', 0),
            unique_videos=len(self.harvest_data.get('all_videos', {})),
            duplicate_rate=0,
            quality_scores=quality_analysis,
            session_performance={},
            recommendations=[],
            trend_analysis=episode_analysis
        )
    
    def _display_visual_report(self, quality_analysis: Dict, episode_analysis: Dict) -> None:
        """Display comprehensive visual report"""
        print("=" * 80)
        print("📊 === SMART HARVEST ANALYSIS REPORT ===")
        print("=" * 80)
        print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        
        # Quality Analysis
        print("🎨 QUALITY ANALYSIS:")
        print(f"   📹 Total Videos: {quality_analysis.get('total_videos', 0):,}")
        print(f"   ✅ Proper Titles: {quality_analysis.get('proper_titles', 0):,} ({quality_analysis.get('success_rate', 0):.1f}%)")
        print(f"   📺 Draga Mama Episodes: {quality_analysis.get('draga_mama_episodes', 0):,} ({quality_analysis.get('episode_rate', 0):.1f}%)")
        print(f"   📅 With Dates: {quality_analysis.get('with_dates', 0):,} ({quality_analysis.get('date_rate', 0):.1f}%)")
        print(f"   👍 With Engagement: {quality_analysis.get('with_engagement', 0):,} ({quality_analysis.get('engagement_rate', 0):.1f}%)")
        print("")
        
        # Episode Analysis
        if episode_analysis.get('episode_range'):
            print("📺 EPISODE COVERAGE:")
            episode_range = episode_analysis['episode_range']
            print(f"   📊 Episode Range: {episode_range['min']} - {episode_range['max']}")
            print(f"   🎯 Episodes Found: {episode_analysis['coverage_stats']['episodes_found']}")
            print(f"   📈 Coverage Rate: {episode_analysis['coverage_stats']['coverage_rate']:.1f}%")
            print(f"   🔍 Missing Episodes: {episode_analysis['coverage_stats']['missing_count']}")
            print("")
        
        print("=" * 80)

def main():
    """Main function for harvest analysis"""
    parser = argparse.ArgumentParser(description="SMART HARVEST ANALYZER")
    parser.add_argument("--file", "-f", default="harvest_results.json",
                       help="Harvest results file to analyze")
    
    args = parser.parse_args()
    
    try:
        analyzer = HarvestAnalyzer(args.file)
        report = analyzer.run_complete_analysis()
        
        if report:
            logger.info("✅ Analysis complete!")
        else:
            return 1
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
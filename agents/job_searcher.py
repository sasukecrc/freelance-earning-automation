"""
Job Searcher Agent - Finds high-paying freelance web development jobs
"""
import json
import time
import logging
from datetime import datetime
from typing import List, Dict

from core.composio_client import search_jobs

logger = logging.getLogger(__name__)

# High-value search queries - targeting the best paying opportunities
JOB_SEARCH_QUERIES = [
    # Highest paying
    "urgent web developer needed build website $1000 $5000 budget freelance 2026",
    "freelance full stack developer react node website build project $2000+ 2026",
    "hire web developer Shopify WooCommerce e-commerce store $1000+ 2026",
    "WordPress developer needed rebuild redesign site performance optimization $1000+",
    "webflow developer freelance project product showcase website $1000+ 2026",
    
    # Mid-range
    "freelance web developer build landing page business website $500-$2000 2026",
    "looking for web developer small business website redesign 2026 remote",
    "contract web developer WordPress Elementor custom site build 2026",
    "frontend developer freelance react nextjs website 2026 budget $800+",
    
    # Hourly rate focused
    "freelance web developer hourly rate $50-$150 remote 2026",
    "part time web developer contract $50-$100 per hour remote 2026",
]

# High-value platforms to check
PLATFORM_QUERIES = [
    "site:upwork.com web developer freelance project budget $1000+ 2026",
    "site:fiverr.com web developer gig website build 2026",
    "site:freelancer.com web development project 2026",
    "site:peopleperhour.com web developer job 2026",
    "site:toptal.com web developer opportunity 2026",
]

# LinkedIn-specific searches
LINKEDIN_QUERIES = [
    "site:linkedin.com/jobs web developer freelance contract 2026",
    "site:linkedin.com \"need a website\" OR \"looking for web developer\" 2026",
    "site:linkedin.com \"hire web developer\" OR \"web developer needed\" 2026",
]


def estimate_job_value(job: Dict) -> int:
    """Estimate potential value of a job based on its description/title"""
    title = (job.get("title", "") or "").lower()
    text_for_analysis = title
    
    # Keywords indicating high value
    high_value = ["$1000", "$2000", "$5000", "$10000", "e-commerce", "ecommerce", 
                  "shopify", "full stack", "react", "enterprise", "urgent"]
    mid_value = ["wordpress", "webflow", "landing page", "redesign", "business website"]
    
    score = 0
    for kw in high_value:
        if kw in text_for_analysis:
            score += 3
    for kw in mid_value:
        if kw in text_for_analysis:
            score += 1
    
    # Newer jobs get higher priority
    if job.get("published_date"):
        try:
            # Simple recency scoring
            score += 1
        except:
            pass
    
    return score


def rank_jobs_by_value(jobs: List[Dict]) -> List[Dict]:
    """Sort jobs by estimated value (highest first)"""
    for job in jobs:
        job["_value_score"] = estimate_job_value(job)
    
    return sorted(jobs, key=lambda j: j["_value_score"], reverse=True)


def deduplicate_jobs(jobs: List[Dict]) -> List[Dict]:
    """Remove duplicate job listings"""
    seen_urls = set()
    unique_jobs = []
    for job in jobs:
        url = job.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_jobs.append(job)
    return unique_jobs


def find_high_value_jobs(max_jobs: int = 20) -> List[Dict]:
    """
    Main function to find the best paying web development jobs
    
    Args:
        max_jobs: Maximum number of jobs to return
        
    Returns:
        List of high-value job listings, ranked by value
    """
    logger.info("ðŸ” Job Searcher: Starting high-value job search...")
    all_jobs = []
    
    # Search using all query strategies
    all_queries = JOB_SEARCH_QUERIES + PLATFORM_QUERIES + LINKEDIN_QUERIES
    
    for query in all_queries:
        try:
            logger.info(f"  Searching: {query[:60]}...")
            jobs = search_jobs(query)
            if jobs:
                all_jobs.extend(jobs)
                logger.info(f"  âœ“ Found {len(jobs)} results")
            # Rate limiting - be respectful
            time.sleep(0.5)
        except Exception as e:
            logger.warning(f"  âœ— Search failed: {e}")
    
    # Deduplicate and rank
    unique_jobs = deduplicate_jobs(all_jobs)
    ranked_jobs = rank_jobs_by_value(unique_jobs)
    
    # Return top N
    top_jobs = ranked_jobs[:max_jobs]
    
    logger.info(f"\nðŸ“Š Job Search Complete:")
    logger.info(f"   Total found: {len(all_jobs)}")
    logger.info(f"   Unique: {len(unique_jobs)}")
    logger.info(f"   Top {len(top_jobs)} ranked by value")
    
    # Print top 10
    for i, job in enumerate(top_jobs[:10]):
        logger.info(f"   {i+1}. ðŸ’° {job.get('title', 'Unknown')[:80]} - {job.get('source', 'Unknown')}")
    
    return top_jobs


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    jobs = find_high_value_jobs()
    print(json.dumps(jobs, indent=2))

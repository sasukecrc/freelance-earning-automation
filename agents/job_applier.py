"""
Job Applier Agent - Applies to high-paying freelance web development jobs
"""
import json
import logging
import time
from typing import List, Dict
from datetime import datetime

from core.composio_client import send_application_email, search_jobs
from core.config import APPLICATION_TEMPLATES, GMAIL_FROM

logger = logging.getLogger(__name__)


# Tracking file for applications
TRACKING_FILE = "data/applications_tracker.json"


def load_tracking() -> Dict:
    """Load application tracking data"""
    try:
        with open(TRACKING_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"applications": [], "total_sent": 0, "responses": [], "earnings": 0}


def save_tracking(tracking: Dict):
    """Save application tracking data"""
    with open(TRACKING_FILE, "w") as f:
        json.dump(tracking, f, indent=2)


def classify_job_type(title: str) -> str:
    """Classify job type to pick the right application template"""
    title_lower = (title or "").lower()
    
    if any(kw in title_lower for kw in ["webflow", "webflow developer"]):
        return "webflow"
    elif any(kw in title_lower for kw in ["wordpress", "woocommerce", "elementor"]):
        return "wordpress"
    elif any(kw in title_lower for kw in ["shopify", "e-commerce", "ecommerce"]):
        return "shopify"
    else:
        return "general_webdev"


def apply_to_job(job: Dict) -> Dict:
    """
    Apply to a single job opportunity
    
    Args:
        job: Job listing dictionary with title, url, etc.
        
    Returns:
        Application result
    """
    title = job.get("title", "Web Developer Position")
    job_type = classify_job_type(title)
    template = APPLICATION_TEMPLATES.get(job_type, APPLICATION_TEMPLATES["general_webdev"])
    
    # For now, send to self as tracking - in production you'd extract 
    # the actual employer email from the job listing
    subject = f"Application: {title[:80]}"
    body = template
    
    logger.info(f"  ðŸ“§ Applying to: {title[:60]}...")
    
    try:
        result = send_application_email(GMAIL_FROM, subject, body)
        if result.get("success"):
            logger.info(f"  âœ“ Application sent successfully!")
            return {
                "job_title": title,
                "job_url": job.get("url", ""),
                "job_source": job.get("source", ""),
                "applied_at": datetime.utcnow().isoformat(),
                "status": "sent",
                "template_used": job_type,
                "result": "success"
            }
        else:
            logger.warning(f"  âœ— Application failed: {result.get('error')}")
            return {
                "job_title": title,
                "job_url": job.get("url", ""),
                "applied_at": datetime.utcnow().isoformat(),
                "status": "failed",
                "error": str(result.get("error", "Unknown"))
            }
    except Exception as e:
        logger.error(f"  âœ— Error applying: {e}")
        return {
            "job_title": title,
            "applied_at": datetime.utcnow().isoformat(),
            "status": "error",
            "error": str(e)
        }


def run_job_application_cycle(max_applications: int = 15) -> Dict:
    """
    Run a full job application cycle: find best jobs, apply to top ones
    
    Args:
        max_applications: Maximum number to apply to
        
    Returns:
        Summary of what was done
    """
    logger.info("ðŸ¤– Job Applier Agent: Starting application cycle...")
    
    tracking = load_tracking()
    
    # Find high-value jobs
    from agents.job_searcher import find_high_value_jobs
    jobs = find_high_value_jobs(max_jobs=max_applications * 2)
    
    # Filter out already applied jobs
    already_applied = {a.get("job_url", "") for a in tracking["applications"] 
                      if a.get("job_url")}
    
    new_jobs = [j for j in jobs if j.get("url") not in already_applied]
    
    if not new_jobs:
        logger.info("  No new jobs to apply to. All already processed.")
        return {"applications_sent": 0, "total_to_date": tracking["total_sent"]}
    
    # Apply to top N new jobs
    jobs_to_apply = new_jobs[:max_applications]
    
    logger.info(f"\n  ðŸŽ¯ Applying to {len(jobs_to_apply)} high-value jobs...")
    
    results = []
    for job in jobs_to_apply:
        result = apply_to_job(job)
        results.append(result)
        tracking["applications"].append(result)
        tracking["total_sent"] += 1
        save_tracking(tracking)
        # Small delay between applications
        time.sleep(1)
    
    # Summary
    sent = sum(1 for r in results if r.get("status") == "sent")
    failed = sum(1 for r in results if r.get("status") in ("failed", "error"))
    
    summary = {
        "run_timestamp": datetime.utcnow().isoformat(),
        "jobs_found": len(jobs),
        "new_jobs": len(new_jobs),
        "applications_attempted": len(jobs_to_apply),
        "applications_sent": sent,
        "applications_failed": failed,
        "total_applications_to_date": tracking["total_sent"]
    }
    
    logger.info(f"\nðŸ“Š Application Cycle Complete:")
    logger.info(f"   Found: {summary['jobs_found']} jobs")
    logger.info(f"   Applied: {summary['applications_sent']} successfully")
    logger.info(f"   Failed: {summary['applications_failed']}")
    logger.info(f"   Total to date: {summary['total_applications_to_date']}")
    
    return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_job_application_cycle()
    print(json.dumps(result, indent=2))

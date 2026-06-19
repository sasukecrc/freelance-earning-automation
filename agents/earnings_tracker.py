"""
Earnings Tracker - Tracks all applications, responses, and earnings
"""
import json
import logging
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)

TRACKING_FILE = "data/applications_tracker.json"


def get_earnings_dashboard() -> Dict:
    """
    Generate a comprehensive earnings dashboard
    
    Returns:
        Dictionary with all tracking data
    """
    try:
        with open(TRACKING_FILE, "r") as f:
            tracking = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tracking = {"applications": [], "total_sent": 0, "responses": [], "earnings": 0}
    
    applications = tracking.get("applications", [])
    responses = tracking.get("responses", [])
    
    # Count by status
    sent_count = sum(1 for a in applications if a.get("status") == "sent")
    failed_count = sum(1 for a in applications if a.get("status") in ("failed", "error"))
    
    # Applications by day
    today = datetime.utcnow().strftime("%Y-%m-%d")
    today_apps = sum(1 for a in applications if a.get("applied_at", "").startswith(today))
    
    # Most recent applications
    recent_apps = sorted(applications, key=lambda a: a.get("applied_at", ""), reverse=True)[:5]
    
    dashboard = {
        "total_applications_sent": tracking.get("total_sent", 0),
        "today_applications": today_apps,
        "successful": sent_count,
        "failed": failed_count,
        "responses_received": len(responses),
        "total_earnings": tracking.get("earnings", 0),
        "target": 1000,
        "remaining": max(0, 1000 - tracking.get("earnings", 0)),
        "recent_applications": recent_apps,
        "recent_responses": responses[-5:] if responses else [],
        "last_updated": datetime.utcnow().isoformat()
    }
    
    return dashboard


def log_response(job_title: str, response_text: str, response_type: str = "email"):
    """Log a response from a potential client"""
    try:
        with open(TRACKING_FILE, "r") as f:
            tracking = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tracking = {"applications": [], "total_sent": 0, "responses": [], "earnings": 0}
    
    response_entry = {
        "job_title": job_title,
        "response": response_text,
        "response_type": response_type,
        "received_at": datetime.utcnow().isoformat()
    }
    
    tracking.setdefault("responses", []).append(response_entry)
    
    with open(TRACKING_FILE, "w") as f:
        json.dump(tracking, f, indent=2)
    
    logger.info(f"ðŸ“¬ Response logged for: {job_title}")


def log_earnings(amount: float, source: str, job_title: str = ""):
    """Log earnings from a successful project"""
    try:
        with open(TRACKING_FILE, "r") as f:
            tracking = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tracking = {"applications": [], "total_sent": 0, "responses": [], "earnings": 0}
    
    tracking["earnings"] = tracking.get("earnings", 0) + amount
    
    earnings_entry = {
        "amount": amount,
        "source": source,
        "job_title": job_title,
        "date": datetime.utcnow().isoformat()
    }
    
    tracking.setdefault("earnings_history", []).append(earnings_entry)
    
    with open(TRACKING_FILE, "w") as f:
        json.dump(tracking, f, indent=2)
    
    logger.info(f"ðŸ’° Earnings logged: ${amount} from {source}")
    logger.info(f"   Total earnings: ${tracking['earnings']}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dashboard = get_earnings_dashboard()
    print(json.dumps(dashboard, indent=2))

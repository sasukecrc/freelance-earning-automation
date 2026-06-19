"""
Main Orchestrator - Coordinates all AI agents for maximum earning
"""
import json
import logging
import time
import sys
from datetime import datetime
from typing import Dict

# Add parent directory to path
sys.path.insert(0, ".")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("Orchestrator")


def print_banner():
    """Print startup banner"""
    print("""
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘     ðŸš€ FREELANCE EARNING AUTOMATION SYSTEM v2.0             â•‘
â•‘     Multi-Agent AI Workforce - 24/7 Operation                â•‘
â•‘     Target: $1,000 in 1-2 Days                               â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    """)


def log_separator(title: str):
    """Print a section separator"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def run_full_automation_cycle() -> Dict:
    """
    Run a complete automation cycle with all agents working in sequence
    
    Cycle includes:
    1. Job Searching (find best paying opportunities)
    2. Job Applying (apply to top jobs)
    3. LinkedIn Marketing (post services)
    4. Earnings Tracking (report progress)
    
    Returns:
        Summary of everything done in this cycle
    """
    cycle_start = datetime.utcnow()
    logger.info(f"ðŸ”„ Starting automation cycle at {cycle_start.isoformat()}")
    
    results = {
        "cycle_start": cycle_start.isoformat(),
        "cycle_end": None,
        "jobs_found": 0,
        "applications_sent": 0,
        "linkedin_posts": 0,
        "total_applications_to_date": 0,
        "errors": []
    }
    
    # === STEP 1: JOB SEARCHING ===
    log_separator("PHASE 1: JOB SEARCHING - Finding Best Paying Opportunities")
    try:
        from agents.job_searcher import find_high_value_jobs
        jobs = find_high_value_jobs(max_jobs=30)
        results["jobs_found"] = len(jobs)
        logger.info(f"âœ… Phase 1 Complete: Found {len(jobs)} high-value jobs")
    except Exception as e:
        logger.error(f"âŒ Phase 1 Failed: {e}")
        results["errors"].append(f"Job search error: {e}")
    
    # === STEP 2: JOB APPLYING ===
    log_separator("PHASE 2: JOB APPLYING - Sending Applications to Best Jobs")
    try:
        from agents.job_applier import run_job_application_cycle
        app_result = run_job_application_cycle(max_applications=15)
        results["applications_sent"] = app_result.get("applications_sent", 0)
        results["total_applications_to_date"] = app_result.get("total_applications_to_date", 0)
        logger.info(f"âœ… Phase 2 Complete: Sent {results['applications_sent']} applications")
    except Exception as e:
        logger.error(f"âŒ Phase 2 Failed: {e}")
        results["errors"].append(f"Job apply error: {e}")
    
    # === STEP 3: LINKEDIN MARKETING ===
    log_separator("PHASE 3: LINKEDIN MARKETING - Promoting Services")
    try:
        from agents.linkedin_marketer import run_linkedin_cycle
        li_result = run_linkedin_cycle()
        results["linkedin_posts"] = 1 if li_result.get("post_published") else 0
        logger.info(f"âœ… Phase 3 Complete: LinkedIn post published")
    except Exception as e:
        logger.error(f"âŒ Phase 3 Failed: {e}")
        results["errors"].append(f"LinkedIn post error: {e}")
    
    # === STEP 4: EARNINGS TRACKING ===
    log_separator("PHASE 4: EARNINGS TRACKING - Progress Report")
    try:
        from agents.earnings_tracker import get_earnings_dashboard
        dashboard = get_earnings_dashboard()
        
        total_apps = dashboard.get("total_applications_sent", 0)
        earnings = dashboard.get("total_earnings", 0)
        remaining = dashboard.get("remaining", 1000)
        
        logger.info(f"ðŸ“Š EARNINGS DASHBOARD:")
        logger.info(f"   Total Applications Sent: {total_apps}")
        logger.info(f"   Current Earnings: ${earnings}")
        logger.info(f"   Remaining to Target: ${remaining}")
        logger.info(f"   Target: $1,000")
        
        results["total_applications_to_date"] = total_apps
        results["earnings"] = earnings
        results["remaining"] = remaining
        
    except Exception as e:
        logger.error(f"âŒ Phase 4 Failed: {e}")
        results["errors"].append(f"Tracking error: {e}")
    
    # === CYCLE COMPLETE ===
    cycle_end = datetime.utcnow()
    results["cycle_end"] = cycle_end.isoformat()
    cycle_duration = (cycle_end - cycle_start).total_seconds()
    results["cycle_duration_seconds"] = cycle_duration
    
    log_separator(f"CYCLE COMPLETE ({cycle_duration:.1f} seconds)")
    logger.info(f"ðŸ“Š CYCLE SUMMARY:")
    logger.info(f"   Jobs Found: {results['jobs_found']}")
    logger.info(f"   Applications Sent: {results['applications_sent']}")
    logger.info(f"   LinkedIn Posts: {results['linkedin_posts']}")
    logger.info(f"   Total Apps to Date: {results['total_applications_to_date']}")
    logger.info(f"   Errors: {len(results['errors'])}")
    
    if results["errors"]:
        for err in results["errors"]:
            logger.warning(f"   âš  {err}")
    
    # Calculate earning potential estimate
    applications_per_day = total_apps if total_apps > 0 else 15
    conversion_rate = 0.05  # 5% of applications lead to projects
    avg_project_value = 500  # average project value
    
    estimated_conversions = applications_per_day * conversion_rate
    estimated_daily_earnings = estimated_conversions * avg_project_value
    
    logger.info(f"\nðŸ’° EARNING POTENTIAL ESTIMATE:")
    logger.info(f"   Applications/day: ~{applications_per_day}")
    logger.info(f"   Est. Conversion Rate: {conversion_rate*100}%")
    logger.info(f"   Est. Conversions/day: ~{estimated_conversions:.1f}")
    logger.info(f"   Est. Daily Earnings: ~${estimated_daily_earnings:.0f}")
    logger.info(f"   Est. Time to $1,000: ~{1000/max(estimated_daily_earnings, 1):.1f} days")
    
    return results


def run_continuous_operation(interval_hours: int = 4, max_cycles: int = None):
    """
    Run the automation system continuously
    
    Args:
        interval_hours: Hours between cycles
        max_cycles: Maximum number of cycles (None = infinite)
    """
    print_banner()
    logger.info(f"ðŸš€ Starting continuous operation (every {interval_hours}h)")
    logger.info(f"   Target: $1,000 in freelance earnings")
    logger.info(f"   Press Ctrl+C to stop\n")
    
    cycle_count = 0
    
    try:
        while max_cycles is None or cycle_count < max_cycles:
            cycle_count += 1
            logger.info(f"\n{'#'*60}")
            logger.info(f"  CYCLE #{cycle_count}")
            logger.info(f"{'#'*60}\n")
            
            results = run_full_automation_cycle()
            
            # Save cycle results
            cycle_results_file = f"data/cycle_{cycle_count}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            with open(cycle_results_file, "w") as f:
                json.dump(results, f, indent=2)
            logger.info(f"ðŸ“ Cycle results saved to {cycle_results_file}")
            
            # Check if target reached
            if results.get("earnings", 0) >= 1000:
                logger.info(f"\nðŸŽ‰ðŸŽ‰ðŸŽ‰ TARGET REACHED! $1,000 EARNED! ðŸŽ‰ðŸŽ‰ðŸŽ‰")
                return results
            
            if max_cycles is None or cycle_count < max_cycles:
                next_run = datetime.utcnow().timestamp() + (interval_hours * 3600)
                next_run_str = datetime.utcfromtimestamp(next_run).strftime("%Y-%m-%d %H:%M:%S UTC")
                logger.info(f"\nâ° Next cycle at {next_run_str}")
                logger.info(f"   Sleeping for {interval_hours} hours...\n")
                time.sleep(interval_hours * 3600)
                
    except KeyboardInterrupt:
        logger.info("\n\nâ¹ Operation stopped by user")
    
    logger.info(f"\nðŸ“Š Final Summary after {cycle_count} cycles:")
    return run_full_automation_cycle()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Freelance Earning Automation System")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")
    parser.add_argument("--interval", type=int, default=4, help="Hours between cycles")
    parser.add_argument("--cycles", type=int, default=None, help="Max number of cycles")
    parser.add_argument("--once", action="store_true", help="Run a single cycle")
    
    args = parser.parse_args()
    
    if args.continuous:
        run_continuous_operation(interval_hours=args.interval, max_cycles=args.cycles)
    else:
        # Default: run once
        results = run_full_automation_cycle()
        print("\n\nFinal Results:")
        print(json.dumps(results, indent=2))

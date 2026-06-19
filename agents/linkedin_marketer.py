"""
LinkedIn Marketer Agent - Posts marketing content and manages LinkedIn presence
"""
import json
import logging
import time
from typing import Dict, List
from datetime import datetime

from core.composio_client import post_linkedin_update, call_composio, extract_tool_result

logger = logging.getLogger(__name__)

# Posting schedule - different content types to rotate through
MARKETING_POSTS = [
    # Service promotion posts
    {
        "type": "service",
        "content": """I build websites that grow businesses. ðŸ’»

Whether you need:
â€¢ A landing page that converts
â€¢ A full e-commerce store
â€¢ A WordPress site that actually performs
â€¢ A Webflow site that looks premium

I deliver fast, mobile-optimized, SEO-friendly results.

DM me or email sasukecrcr@gmail.com for a free consultation.

#WebDeveloper #Freelance #WebDesign #BusinessGrowth"""
    },
    {
        "type": "social_proof",
        "content": """Just finished building another high-converting website for a client! ðŸš€

The result? Clean design, lightning-fast load times, and a mobile experience that actually works.

I have capacity for 2 more projects this week at a special rate.

Let's talk about your project: sasukecrcr@gmail.com

#WebDevelopment #ClientWork #FreelanceLife #WebDesign"""
    },
    {
        "type": "tip",
        "content": """3 things every small business website MUST have in 2026: ðŸ‘‡

1. Mobile-first design (70%+ of traffic is mobile)
2. Speed optimization (3s load time = 53% bounce rate)
3. Clear call-to-action (tell visitors what to do)

Need help with your site? I build all of this in. Let's chat!

sasukecrcr@gmail.com | github.com/sasukecrc

#WebDevTips #SmallBusiness #WebsiteTips #DigitalMarketing"""
    },
    {
        "type": "offer",
        "content": """ðŸ”¥ SPECIAL OFFER - 30% OFF for first 5 clients!

I'm a professional web developer offering:
âœ… Landing Pages - $299 (was $429)
âœ… Business Websites - $599 (was $857)
âœ… E-commerce Stores - $999 (was $1429)
âœ… Website Redesign - From $399

Limited spots available! DM me or email sasukecrcr@gmail.com

#WebDeveloper #SpecialOffer #Freelance #WebsiteDesign #SmallBusiness"""
    },
    {
        "type": "value",
        "content": """Your website is your 24/7 salesperson. ðŸª

Is it working for you or against you?

A well-designed website can:
ðŸ“ˆ Increase conversions by 200%+
âš¡ Load in under 2 seconds
ðŸ“± Work perfectly on all devices
ðŸ” Rank higher on Google

I build websites that actually generate results.

Let's talk: sasukecrcr@gmail.com

#WebDesign #Business #Marketing #Growth #DigitalTransformation"""
    }
]


def post_marketing_content(post_index: int = None) -> Dict:
    """
    Post marketing content to LinkedIn
    
    Args:
        post_index: Specific post to use, or None for next in rotation
        
    Returns:
        Result of the post
    """
    # Load tracking to know which post to use next
    tracking_file = "data/marketing_tracker.json"
    try:
        with open(tracking_file, "r") as f:
            tracking = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tracking = {"last_post_index": -1, "posts_sent": 0}
    
    if post_index is None:
        post_index = (tracking["last_post_index"] + 1) % len(MARKETING_POSTS)
    
    post = MARKETING_POSTS[post_index]
    
    logger.info(f"  ðŸ“ Posting LinkedIn content (type: {post['type']})...")
    
    try:
        result = post_linkedin_update(post["content"])
        
        if result.get("success"):
            tracking["last_post_index"] = post_index
            tracking["posts_sent"] = tracking.get("posts_sent", 0) + 1
            tracking["last_post_time"] = datetime.utcnow().isoformat()
            
            with open(tracking_file, "w") as f:
                json.dump(tracking, f, indent=2)
            
            logger.info(f"  âœ“ LinkedIn post published successfully!")
            return {"success": True, "post_type": post["type"], "post_index": post_index}
        else:
            logger.warning(f"  âœ— LinkedIn post failed: {result.get('error')}")
            return {"success": False, "error": result.get("error")}
            
    except Exception as e:
        logger.error(f"  âœ— LinkedIn post error: {e}")
        return {"success": False, "error": str(e)}


def run_linkedin_cycle() -> Dict:
    """
    Run a complete LinkedIn marketing cycle
    
    Returns:
        Summary of actions taken
    """
    logger.info("ðŸ¤– LinkedIn Marketer Agent: Starting marketing cycle...")
    
    # Post marketing content
    post_result = post_marketing_content()
    
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "post_published": post_result.get("success", False),
        "post_type": post_result.get("post_type", "none"),
        "total_posts_to_date": 0
    }
    
    # Get total count from tracking
    try:
        with open("data/marketing_tracker.json", "r") as f:
            tracking = json.load(f)
        summary["total_posts_to_date"] = tracking.get("posts_sent", 0)
    except:
        pass
    
    logger.info(f"\nðŸ“Š LinkedIn Marketing Complete:")
    logger.info(f"   Posted: {summary['post_published']}")
    logger.info(f"   Type: {summary['post_type']}")
    logger.info(f"   Total posts: {summary['total_posts_to_date']}")
    
    return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_linkedin_cycle()
    print(json.dumps(result, indent=2))

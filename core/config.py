"""
Configuration for Freelance Earning Automation System
"""
import os

# Composio MCP Configuration
COMPOSIO_MCP_URL = "https://connect.composio.dev/mcp"
COMPOSIO_API_KEY = os.environ.get("COMPOSIO_API_KEY", "")

# LinkedIn User Info
LINKEDIN_PERSON_ID = "BpfA29-PM3"
LINKEDIN_AUTHOR_URN = "urn:li:person:BpfA29-PM3"

# Gmail
GMAIL_FROM = "sasukecrcr@gmail.com"

# GitHub
GITHUB_USERNAME = "sasukecrc"

# Earnings Target
TARGET_EARNINGS = 1000  # USD
TARGET_DAYS = 2

# Job Search Configuration
MIN_JOB_BUDGET = 300  # Minimum budget to consider
MAX_APPLICATIONS_PER_RUN = 15
SEARCH_INTERVAL_HOURS = 4  # How often to search for new jobs

# Application Templates
APPLICATION_TEMPLATES = {
    "webflow": """Hi there,

I am applying for the Webflow Developer position. I have extensive experience building production Webflow sites from Figma designs using CMS collections, custom code, and responsive layouts.

I can complete your product showcase website quickly and to a high standard.

Portfolio: https://github.com/sasukecrc
Email: sasukecrcr@gmail.com

Looking forward to discussing this project!

Best regards,
CR7 SASUKE CR7""",

    "wordpress": """Hi,

I am writing to apply for the WordPress Developer opportunity. I specialize in WordPress development including custom themes, plugins, WooCommerce, Elementor, and performance optimization.

I can rebuild and optimize your site for better performance and modern design.

Portfolio: https://github.com/sasukecrc
Email: sasukecrcr@gmail.com

Let me know if you'd like to see examples of my work.

Best regards,
CR7 SASUKE CR7""",

    "shopify": """Hi,

I am applying for the Shopify Developer position. I have strong experience with Shopify store setup, theme customization, app integration, and e-commerce optimization.

I can set up and optimize your e-commerce store for maximum conversions.

Portfolio: https://github.com/sasukecrc
Email: sasukecrcr@gmail.com

Looking forward to hearing from you!

Best regards,
CR7 SASUKE CR7""",

    "general_webdev": """Hi,

I am applying for the Web Developer position. I build fast, mobile-optimized, SEO-friendly websites that drive results. My services include:

- Landing Pages & Business Websites
- E-commerce Stores (Shopify, WooCommerce)
- WordPress & Webflow Development
- Custom HTML/CSS/JS Sites
- Website Redesigns & Performance Optimization

I offer affordable rates and fast turnaround.

Portfolio: https://github.com/sasukecrc
Email: sasukecrcr@gmail.com

Let's build something great together!

Best regards,
CR7 SASUKE CR7"""
}

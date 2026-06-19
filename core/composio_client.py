"""
Composio MCP Client - Makes HTTP requests to the Composio MCP endpoint
"""
import json
import time
import urllib.request
import urllib.error
import logging

from core.config import COMPOSIO_MCP_URL, COMPOSIO_API_KEY

logger = logging.getLogger(__name__)


class ComposioMCPError(Exception):
    """Custom exception for Composio MCP errors"""
    pass


def call_composio(method_name: str, arguments: dict = None, timeout: int = 60) -> dict:
    """
    Call a Composio MCP tool via HTTP POST
    
    Args:
        method_name: The tool name (e.g. COMPOSIO_SEARCH_WEB, GMAIL_SEND_EMAIL)
        arguments: The tool arguments
        timeout: Request timeout in seconds
        
    Returns:
        Parsed response dictionary
    """
    if arguments is None:
        arguments = {}
    
    # Generate unique request ID
    request_id = int(time.time() * 1000) % 100000
    
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": method_name,
            "arguments": arguments
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-consumer-api-key": COMPOSIO_API_KEY
    }
    
    data = json.dumps(payload).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            COMPOSIO_MCP_URL,
            data=data,
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw_response = response.read().decode("utf-8")
            
        # Parse SSE-style response
        if raw_response.startswith("event: message"):
            # Extract the JSON data part
            lines = raw_response.split("\n")
            json_line = None
            for line in lines:
                if line.startswith("data: "):
                    json_line = line[6:]
                    break
            
            if json_line:
                result = json.loads(json_line)
                return result
            else:
                raise ComposioMCPError("No data found in SSE response")
        else:
            result = json.loads(raw_response)
            return result
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        logger.error(f"HTTP Error {e.code}: {error_body}")
        raise ComposioMCPError(f"HTTP Error {e.code}: {error_body}")
    except urllib.error.URLError as e:
        logger.error(f"URL Error: {e.reason}")
        raise ComposioMCPError(f"URL Error: {e.reason}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON Parse Error: {e}")
        raise ComposioMCPError(f"JSON Parse Error: {e}")


def extract_tool_result(response: dict) -> dict:
    """
    Extract the actual tool result from a Composio MCP response
    
    Args:
        response: Full response from call_composio
        
    Returns:
        Dictionary with success, data, and error fields
    """
    try:
        content = response.get("result", {}).get("content", [])
        if not content:
            return {"success": False, "data": None, "error": "No content in response"}
        
        text_content = content[0].get("text", "{}")
        result_data = json.loads(text_content)
        
        is_error = response.get("result", {}).get("isError", False)
        data = result_data.get("data", {})
        
        if is_error:
            error_msg = data.get("error", "Unknown error")
            return {"success": False, "data": data, "error": error_msg}
        
        return {"success": True, "data": data, "error": None}
        
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        return {"success": False, "data": None, "error": str(e)}


def search_jobs(query: str) -> list:
    """
    Search for freelance web development jobs
    
    Args:
        query: Search query string
        
    Returns:
        List of job listings found
    """
    try:
        # Execute web search via Composio
        response = call_composio("COMPOSIO_MULTI_EXECUTE_TOOL", {
            "tools": [
                {
                    "tool_slug": "COMPOSIO_SEARCH_WEB",
                    "arguments": {"query": query}
                }
            ],
            "sync_response_to_workbench": False,
            "thought": f"Searching for: {query}",
            "current_step": "SEARCHING_JOBS"
        })
        
        result = extract_tool_result(response)
        if not result["success"]:
            logger.warning(f"Search failed: {result['error']}")
            return []
        
        # Extract job listings from result
        jobs = []
        results_list = result["data"].get("results", [])
        for r in results_list:
            job_data = r.get("response", {}).get("data", {})
            citations = job_data.get("citations", [])
            for citation in citations:
                jobs.append({
                    "title": citation.get("title", "Unknown"),
                    "url": citation.get("url", ""),
                    "published_date": citation.get("publishedDate", ""),
                    "source": citation.get("author", "Unknown")
                })
        
        return jobs
        
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        return []


def send_application_email(to_email: str, subject: str, body: str) -> dict:
    """
    Send a job application email
    
    Args:
        to_email: Recipient email
        subject: Email subject
        body: Email body
        
    Returns:
        Result dictionary with success status
    """
    try:
        # Send to myself first - in production you'd send to actual job posters
        response = call_composio("COMPOSIO_MULTI_EXECUTE_TOOL", {
            "tools": [
                {
                    "tool_slug": "GMAIL_SEND_EMAIL",
                    "arguments": {
                        "to": to_email,
                        "subject": subject,
                        "body": body,
                        "is_html": False
                    }
                }
            ],
            "sync_response_to_workbench": False,
            "thought": f"Sending application: {subject}",
            "current_step": "APPLYING_TO_JOB"
        })
        
        result = extract_tool_result(response)
        return result
        
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return {"success": False, "error": str(e)}


def post_linkedin_update(text: str) -> dict:
    """
    Post an update on LinkedIn
    
    Args:
        text: Post content
        
    Returns:
        Result dictionary
    """
    try:
        response = call_composio("COMPOSIO_MULTI_EXECUTE_TOOL", {
            "tools": [
                {
                    "tool_slug": "LINKEDIN_CREATE_LINKED_IN_POST",
                    "arguments": {
                        "author": "urn:li:person:BpfA29-PM3",
                        "commentary": text,
                        "visibility": "PUBLIC",
                        "feedDistribution": "MAIN_FEED",
                        "lifecycleState": "PUBLISHED"
                    }
                }
            ],
            "sync_response_to_workbench": False,
            "thought": "Posting LinkedIn update",
            "current_step": "POSTING_LINKEDIN"
        })
        
        result = extract_tool_result(response)
        return result
        
    except Exception as e:
        logger.error(f"Error posting to LinkedIn: {e}")
        return {"success": False, "error": str(e)}


def discover_app_tools(use_case: str) -> dict:
    """
    Discover what tools are available via Composio for a use case
    
    Args:
        use_case: Description of what you want to do
        
    Returns:
        Tool information
    """
    try:
        response = call_composio("COMPOSIO_MULTI_EXECUTE_TOOL", {
            "tools": [
                {
                    "tool_slug": "COMPOSIO_SEARCH_TOOLS",
                    "arguments": {
                        "queries": [{"use_case": use_case}]
                    }
                }
            ],
            "sync_response_to_workbench": False,
            "thought": f"Discovering tools for: {use_case}",
            "current_step": "DISCOVERING_TOOLS"
        })
        
        result = extract_tool_result(response)
        return result
        
    except Exception as e:
        logger.error(f"Error discovering tools: {e}")
        return {"success": False, "error": str(e)}

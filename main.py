import os
import json
import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
FLASHY_API_KEY = os.environ.get("FLASHY_API_KEY", "")
BASE_URL = "https://api.flashy.app"

mcp = FastMCP("flashy-mcp")
def req(method: str, endpoint: str, params=None, body=None):
        headers = {"x-api-key": FLASHY_API_KEY, "Content-Type": "application/json", "Accept": "application/json"}
        with httpx.Client(timeout=30) as client:
            r = client.request(method, f"{BASE_URL}{endpoint}", headers=headers, params=params, json=body)
            try:
                return r.json()
            except Exception:
                return {"status_code": r.status_code, "text": r.text}

@mcp.tool()
def flashy_get_account() -> str:
    """Get Flashy account information"""
    return json.dumps(req("GET", "/account"))

@mcp.tool()
def flashy_list_contacts(limit: int = 50, page: int = 1) -> str:
    """List contacts in Flashy"""
    return json.dumps(req("GET", "/contacts", params={"limit": limit, "page": page}))

@mcp.tool()
def flashy_get_contact(contact_id: str) -> str:
    """Get a specific contact by ID"""
    return json.dumps(req("GET", f"/contacts/{contact_id}"))

@mcp.tool()
def flashy_create_contact(email: str, first_name: str = "", last_name: str = "", phone: str = "") -> str:
    """Create a new contact in Flashy"""
    body = {"email": email}
    if first_name:
        body["first_name"] = first_name
    if last_name:
        body["last_name"] = last_name
    if phone:
        body["phone"] = phone
    return json.dumps(req("POST", "/contacts", body=body))

@mcp.tool()
def flashy_update_contact(contact_id: str, first_name: str = "", last_name: str = "", phone: str = "") -> str:
    """Update an existing contact in Flashy"""
    body = {}
    if first_name:
        body["first_name"] = first_name
    if last_name:
        body["last_name"] = last_name
    if phone:
        body["phone"] = phone
    return json.dumps(req("PUT", f"/contacts/{contact_id}", body=body))

@mcp.tool()
def flashy_search_contacts(query: str, limit: int = 50) -> str:
    """Search contacts in Flashy"""
    return json.dumps(req("GET", "/contacts", params={"search": query, "limit": limit}))

@mcp.tool()
def flashy_list_lists() -> str:
    """List all contact lists in Flashy"""
    return json.dumps(req("GET", "/lists"))

@mcp.tool()
def flashy_get_list(list_id: str) -> str:
    """Get a specific list by ID"""
    return json.dumps(req("GET", f"/lists/{list_id}"))

@mcp.tool()
def flashy_add_contact_to_list(list_id: str, email: str) -> str:
    """Add a contact to a list"""
    return json.dumps(req("POST", f"/lists/{list_id}/contacts", body={"email": email}))

@mcp.tool()
def flashy_remove_contact_from_list(list_id: str, contact_id: str) -> str:
    """Remove a contact from a list"""
    return json.dumps(req("DELETE", f"/lists/{list_id}/contacts/{contact_id}"))

@mcp.tool()
def flashy_list_messages(limit: int = 50) -> str:
    """List messages/campaigns in Flashy"""
    return json.dumps(req("GET", "/messages", params={"limit": limit}))

@mcp.tool()
def flashy_get_message(message_id: str) -> str:
    """Get a specific message by ID"""
    return json.dumps(req("GET", f"/messages/{message_id}"))

@mcp.tool()
def flashy_track_event(email: str, event_name: str) -> str:
    """Track a custom event for a contact"""
    return json.dumps(req("POST", "/events", body={"email": email, "event": event_name}))

@mcp.tool()
def flashy_get_reports(limit: int = 20) -> str:
    """Get campaign reports from Flashy"""
    return json.dumps(req("GET", "/reports", params={"limit": limit}))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = port
    mcp.settings.transport_security = TransportSecuritySettings(enable_dns_rebinding_protection=False)
    mcp.run(transport="streamable-http")

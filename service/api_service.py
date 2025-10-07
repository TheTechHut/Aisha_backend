import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


async def call_api(url, method="POST", headers=None, params=None, json=None, data=None, files=None, timeout=15):
    """Universal function to call any external API asynchronously using httpx."""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method=method, url=url, headers=headers, params=params, json=json, data=data, files=files
            )
        response.raise_for_status()
        try:
            return {"success": True, "data": response.json()}
        except Exception:
            return {"success": True, "data": response.text}
    except httpx.HTTPStatusError as exc:
        return {"success": False, "error": f"Status {exc.response.status_code}", "details": exc.response.text}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


# Example function to call Gemini API  











        




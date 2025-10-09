import httpx
import requests

async def call_api(
    url: str,
    method: str,
    headers: dict = None,
    params: dict = None,
    json: dict = None,
    data: dict = None,
    files: dict = None,
    timeout: int = 15
) -> dict:
    """
    Universal async function to call any external API using httpx.AsyncClient.

    Args:
        url (str): API endpoint URL.
        method (str): HTTP method ('GET', 'POST', etc.).
        headers (dict, optional): HTTP headers.
        params (dict, optional): URL query parameters.
        json (dict, optional): JSON payload.
        data (dict, optional): Form payload.
        files (dict, optional): File uploads.
        timeout (int, optional): Request timeout in seconds.

    Returns:
        dict: {
            "success": bool,
            "data": dict or str if successful,
            "error": str if error,
            "details": str if error details
        }
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
                data=data,
                files=files
            )
        response.raise_for_status()
        try:
            return {"success": True, "data": response.json()}
        except Exception:
            return {"success": True, "data": response.text}
    except httpx.HTTPStatusError as exc:
        return {
            "success": False,
            "error": f"HTTP Status {exc.response.status_code}",
            "details": exc.response.text
        }
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc)
        }
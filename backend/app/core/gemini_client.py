"""Helper to create a Gemini client with optional proxy support."""
from google import genai
from google.genai import types
from app.core.config import settings


def get_genai_client():
    """Create a genai.Client, using HTTPS_PROXY / HTTP_PROXY if configured."""
    api_key = settings.GEMINI_API_KEY
    proxy = settings.HTTPS_PROXY or settings.HTTP_PROXY

    if proxy:
        http_options = types.HttpOptions(
            client_args={"proxy": proxy},
            async_client_args={"proxy": proxy},
        )
        return genai.Client(api_key=api_key, http_options=http_options)

    return genai.Client(api_key=api_key)

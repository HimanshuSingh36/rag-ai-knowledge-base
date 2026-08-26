from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()


# def _build_client(api_key_name: str, base_url_name: str):
#     api_key = os.getenv(api_key_name)
#     base_url = os.getenv(base_url_name)
#     if not api_key or not base_url:
#         raise SystemExit(
#             f"Missing {api_key_name} or {base_url_name} in your .env file. "
#             "Please check .env and try again."
#         )
#     client = OpenAI(api_key=api_key, base_url=base_url)
#     return client

def gemini_client():
    api_key=os.getenv("google_api_key")
    base_url=os.getenv("google_base_url")
    if not api_key or not base_url:
        raise SystemExit(
            "Missing google_api_key or google_base_url in your .env file. "
            "Please check .env and try again."
        )
    client = OpenAI(api_key=api_key, base_url=base_url)
    return client

def groq_client():
    api_key=os.getenv("groq_api_key")
    base_url=os.getenv("groq_base_url")
    if not api_key or not base_url:
        raise SystemExit(
            "Missing groq_api_key or groq_base_url in your .env file. "
                "Please check .env and try again."
        )
    client = OpenAI(api_key=api_key, base_url=base_url)
    return client

def openrouter_client():
    api_key=os.getenv("openrouter_api_key")
    base_url=os.getenv("openrouter_base_url")
    if not api_key or not base_url:
        raise SystemExit(
            "Missing openrouter_api_key or openrouter_base_url in your .env file. "
                "Please check .env and try again."
        )
    client = OpenAI(api_key=api_key, base_url=base_url)
    return client
# gemini_client = _build_client("google_api_key", "google_base_url")
# groq_client = _build_client("groq_api_key", "groq_base_url")
# openrouter_client = _build_client("openrouter_api_key", "openrouter_base_url")
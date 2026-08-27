
import os
import subprocess
import requests

from bs4 import BeautifulSoup
from tavily import TavilyClient
from retriever import search_documents
from logger import logger


# ============================================================
# CLIENTS
# ============================================================

tavily_client = TavilyClient(
    api_key=os.getenv("tavily_api_key")
)


# ============================================================
# WEB SEARCH
# ============================================================

def web_search(query: str) -> str:
    """
    Search the web using Tavily.

    Returns search results containing:
    - title
    - content
    - URL

    The agent can then decide whether it wants to
    inspect any of the returned URLs using read_url().
    """

    try:
        logger.info(f"🔎 Web search started: {query}")

        response = tavily_client.search(
            query,
            search_depth="advanced"
        )

        results = response.get("results", [])

        if not results:
            logger.warning(
                f"🔎 No web search results found: {query}"
            )

            return f"No results found for '{query}'."

        formatted_results = []

        for index, result in enumerate(results, start=1):

            title = result.get(
                "title",
                "Untitled"
            )

            content = result.get(
                "content",
                ""
            )

            url = result.get(
                "url",
                ""
            )

            formatted_results.append(
                f"""
Result {index}

Title:
{title}

Content:
{content}

URL:
{url}
""".strip()
            )

        logger.info(
            f"🔎 Web search completed: "
            f"{query} | {len(results)} results"
        )

        return "\n\n".join(formatted_results)

    except Exception as e:

        logger.error(
            f"❌ Web search for '{query}' failed: {e}",
            exc_info=True
        )

        return (
            f"Web search for '{query}' failed: {e}"
        )


# ============================================================
# READ URL
# ============================================================

def read_url(url: str) -> str:
    """
    Fetch a webpage and extract readable text.

    The function:
    1. Sends HTTP request
    2. Validates response
    3. Parses HTML
    4. Removes unnecessary elements
    5. Extracts title
    6. Extracts readable text
    7. Cleans whitespace
    8. Limits output size
    """

    try:

        logger.info(
            f"🌐 Reading URL: {url}"
        )

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(compatible; AI-Agent/1.0)"
                )
            }
        )

        response.raise_for_status()

        # ----------------------------------------------------
        # Check content type
        # ----------------------------------------------------

        content_type = response.headers.get(
            "Content-Type",
            ""
        )

        if "text/html" not in content_type.lower():

            logger.warning(
                f"⚠️ URL is not HTML: "
                f"{url} | {content_type}"
            )

            return (
                f"The URL does not contain an HTML webpage.\n"
                f"Content-Type: {content_type}"
            )

        # ----------------------------------------------------
        # Parse HTML
        # ----------------------------------------------------

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # ----------------------------------------------------
        # Remove unnecessary elements
        # ----------------------------------------------------

        for element in soup.find_all(
            [
                "script",
                "style",
                "noscript",
                "svg"
            ]
        ):
            element.decompose()

        # ----------------------------------------------------
        # Extract title
        # ----------------------------------------------------

        title = ""

        if soup.title:
            title = soup.title.get_text(
                strip=True
            )

        # ----------------------------------------------------
        # Extract readable text
        # ----------------------------------------------------

        text = soup.get_text(
            separator="\n",
            strip=True
        )

        # ----------------------------------------------------
        # Clean whitespace
        # ----------------------------------------------------

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:
                lines.append(line)

        clean_text = "\n".join(lines)

        # ----------------------------------------------------
        # Check if content exists
        # ----------------------------------------------------

        if not clean_text:

            logger.warning(
                f"⚠️ No readable content found: {url}"
            )

            return (
                "No readable content could be "
                "extracted from this webpage."
            )

        # ----------------------------------------------------
        # Limit output size
        # ----------------------------------------------------

        max_chars = 30000

        was_truncated = False

        if len(clean_text) > max_chars:

            clean_text = clean_text[:max_chars]

            was_truncated = True

            logger.warning(
                f"⚠️ URL content truncated: {url}"
            )

        # ----------------------------------------------------
        # Build final result
        # ----------------------------------------------------

        result = (
            f"Title: {title}\n\n"
            f"URL: {url}\n\n"
            f"Content:\n{clean_text}"
        )

        if was_truncated:

            result += (
                "\n\n[Content truncated because "
                "it exceeded the maximum size.]"
            )

        logger.info(
            f"✅ URL read successfully: "
            f"{url} | {len(clean_text)} characters"
        )

        return result

    # --------------------------------------------------------
    # Timeout
    # --------------------------------------------------------

    except requests.exceptions.Timeout:

        logger.error(
            f"⏱️ URL request timed out: {url}"
        )

        return (
            f"Reading URL timed out: {url}"
        )

    # --------------------------------------------------------
    # HTTP errors
    # --------------------------------------------------------

    except requests.exceptions.HTTPError as e:

        logger.error(
            f"❌ HTTP error while reading URL "
            f"{url}: {e}"
        )

        return (
            f"HTTP error while reading URL: {e}"
        )

    # --------------------------------------------------------
    # Request errors
    # --------------------------------------------------------

    except requests.exceptions.RequestException as e:

        logger.error(
            f"❌ Request failed for URL "
            f"{url}: {e}"
        )

        return (
            f"Request failed while reading URL: {e}"
        )

    # --------------------------------------------------------
    # Unexpected errors
    # --------------------------------------------------------

    except Exception as e:

        logger.error(
            f"❌ Unexpected error while reading "
            f"URL {url}: {e}",
            exc_info=True
        )

        return (
            f"Unexpected error while reading URL: {e}"
        )


# ============================================================
# WEATHER
# ============================================================

def get_weather(city: str) -> str:
    """
    Get current weather information for a city.
    """

    url = (
        f"https://wttr.in/"
        f"{city.lower()}"
        f"?format=%C+%t"
    )

    try:

        logger.info(
            f"🌤️ Weather lookup started: {city}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        weather = response.text.strip()

        logger.info(
            f"🌤️ Weather lookup completed: {city}"
        )

        return (
            f"The weather of {city} is {weather}"
        )

    except requests.exceptions.Timeout:

        logger.error(
            f"⏱️ Weather lookup timed out: {city}"
        )

        return (
            f"Weather lookup for {city} timed out."
        )

    except requests.exceptions.RequestException as e:

        logger.error(
            f"❌ Weather lookup failed for "
            f"{city}: {e}"
        )

        return (
            f"Weather lookup for {city} failed: {e}"
        )


# ============================================================
# RUN COMMAND
# ============================================================

def run_command(cmd: str) -> str:
    """
    Execute a shell command and return stdout/stderr.

    NOTE:
    This tool is potentially dangerous when exposed
    to an unrestricted LLM.
    """

    logger.warning(
        f"💻 Executing shell command: {cmd}"
    )

    try:

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        logger.info(
            f"💻 Command completed: "
            f"return_code={result.returncode}"
        )

        return (
            f"Return code: {result.returncode}\n\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )

    except subprocess.TimeoutExpired:

        logger.error(
            f"⏱️ Command timed out: {cmd}"
        )

        return "Command execution timed out."

    except Exception as e:

        logger.error(
            f"❌ Command execution failed: "
            f"{cmd}: {e}",
            exc_info=True
        )

        return (
            f"Command execution failed: {e}"
        )


# ============================================================
# TOOL REGISTRY
# ============================================================

available_tools = {
    "search_documents": search_documents,
    "web_search": web_search,
    "read_url": read_url,
    "get_weather": get_weather,
    "run_command": run_command,
}

AVAILABLE_TOOL_NAMES = list(
    available_tools.keys()
)
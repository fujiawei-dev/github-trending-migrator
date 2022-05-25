"""
Github-Trending-API

API serving data about trending GitHub repositories/developers.
"""

from enum import Enum
from typing import Any, Dict, List, Union

import fastapi

from .scraping import GITHUB_TRENDING_URL, get_github_trending
from .version import __version__


class AllowedDateRanges(str, Enum):
    """Optional query parameter, default date range: daily"""

    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class AllowedSpokenLanguages(str, Enum):
    """Optional query parameter, default language: any
    identifier (language name) = 2-char-string (abbrev. for urlParam)
    """

    Chinese = "zh"
    English = "en"


class AllowedProgrammingLanguages(str, Enum):
    """Path Parameter
    identifier (language name) = string (urlParam)
    """

    c__ = "c++"
    javascript = "javascript"
    python = "python"
    shell = "shell"
    typescript = "typescript"
    c = "c"
    cython = "cython"
    dart = "dart"
    go = "go"
    rust = "rust"


app = fastapi.FastAPI(
    title="Github Trending API",
    description="API serving data about trending GitHub repositories/developers.",
    version=__version__,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


DOMAIN_NAME = "http://127.0.0.1:12351"


@app.get("/")
def help_routes() -> Dict[str, str]:
    """API endpoints and documentation."""
    return {
        "repositories": f"{DOMAIN_NAME}/repositories",
        "developers": f"{DOMAIN_NAME}/developers",
        "docs": f"{DOMAIN_NAME}/docs",
        "redoc": f"{DOMAIN_NAME}/redoc",
    }


@app.get("/repositories")
async def trending_repositories(
    since: AllowedDateRanges = None,
    spoken_language_code: AllowedSpokenLanguages = None,
) -> Union[List[Any], str]:
    """Returns data about trending repositories (all programming
    languages, cannot be specified on this endpoint).
    """
    payload = {"since": "daily"}

    if since:
        payload["since"] = since.value
    if spoken_language_code:
        payload["spoken_language_code"] = spoken_language_code.value

    return await get_github_trending(payload)


@app.get("/repositories/{prog_lang}")
async def trending_repositories_by_progr_language(
    prog_lang: AllowedProgrammingLanguages,
    since: AllowedDateRanges = None,
    spoken_language_code: AllowedSpokenLanguages = None,
) -> Union[List[Any], str]:
    """Returns data about trending repositories. A specific programming
    language can be added as path parameter to specify search.
    """
    payload = {"since": "daily"}

    if since:
        payload["since"] = since.value
    if spoken_language_code:
        payload["spoken_language_code"] = spoken_language_code.value

    url = GITHUB_TRENDING_URL + "/" + prog_lang
    return await get_github_trending(payload, url)


@app.get("/developers")
async def trending_developers(
    since: AllowedDateRanges = None,
) -> Union[List[Any], str]:
    """Returns data about trending developers (all programming languages,
    cannot be specified on this endpoint).
    """
    payload = {"since": "daily"}

    if since:
        payload["since"] = since.value

    url = GITHUB_TRENDING_URL + "/developers"
    return await get_github_trending(payload, url, False)


@app.get("/developers/{prog_lang}")
async def trending_developers_by_progr_language(
    prog_lang: AllowedProgrammingLanguages,
    since: AllowedDateRanges = None,
) -> Union[List[Any], str]:
    """Returns data about trending developers. A specific programming
    language can be added as path parameter to specify search.
    """
    payload = {"since": "daily"}

    if since:
        payload["since"] = since.value

    url = GITHUB_TRENDING_URL + "/developers/" + prog_lang
    return await get_github_trending(payload, url, False)

"""
Date: 2022.05.09 20:20
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.26 08:05:06
"""
import asyncio
from itertools import chain
from typing import List

import aiohttp

from .blacklist import repos as repos_blacklist
from .logger import log
from .scraping import GITHUB_TRENDING_URL, get_github_trending


async def get_all_organizations_list(
    session: aiohttp.ClientSession,
    base_url: str,
    auth: aiohttp.BasicAuth,
) -> List[str]:
    response: aiohttp.ClientResponse = await session.get(
        url=base_url + "/api/v1/admin/orgs",
        auth=auth,
    )

    organizations = await response.json()

    log.debug(f"Response [{response.status}]")

    if response.status != 200:
        log.error(f"Body {organizations}")
        return []

    log.error(f"Organizations {len(organizations)}")

    return [organization["username"] for organization in organizations]


async def get_all_repositories_list(
    session: aiohttp.ClientSession,
    base_url: str,
    auth: aiohttp.BasicAuth,
    organization: str,
):
    repositories_list = []
    page = 1

    while True:
        response: aiohttp.ClientResponse = await session.get(
            url=base_url + "/api/v1/orgs/" + organization + "/repos?page=%d" % page,
            auth=auth,
        )

        repositories = await response.json()

        log.debug(f"Response [{response.status}]")

        if response.status != 200:
            log.error(f"Body {repositories}")
            continue

        if len(repositories) == 0:
            break

        log.info(f"{organization} {len(repositories)}")

        repositories_list.extend(
            [
                repository["original_url"].removesuffix(".git")
                for repository in repositories
            ]
        )

        page += 1

    return repositories_list


async def migrate_to_gitea(
    session: aiohttp.ClientSession,
    clone_addr: str,
    repo_name: str,
    description: str,
    base_url: str,
    auth: aiohttp.BasicAuth,
) -> List[str]:
    log.debug("Origin " + clone_addr)

    response: aiohttp.ClientResponse = await session.post(
        url=base_url + "/api/v1/repos/migrate",
        auth=auth,
        json={
            "clone_addr": clone_addr,
            "repo_name": repo_name,
            "description": description,
            "mirror": True,
            "private": False,
            "repo_owner": "mirror",
            "service": "git",
            "labels": True,
        },
    )

    log.debug(f"Response [{response.status}]")
    log.debug(f"Body {await response.json()}")


async def get_repos_blacklist():
    async with aiohttp.ClientSession() as session:
        base_urls = ["http://192.168.0.10:13000", "http://192.168.0.18:13000"]
        auths = [aiohttp.BasicAuth("root", "123456"), aiohttp.BasicAuth("root", "root")]

        for base_url, auth in zip(base_urls, auths):
            organizations = await get_all_organizations_list(session, base_url, auth)
            for organization in organizations:
                repos_blacklist.update(
                    await get_all_repositories_list(
                        session, base_url, auth, organization
                    )
                )


async def migrate_to_gitea_from_github_trending():
    await get_repos_blacklist()

    repositories = chain(
        await get_github_trending({"since": "daily"}),
        await get_github_trending({"since": "daily"}, GITHUB_TRENDING_URL + "/go"),
        await get_github_trending({"since": "daily"}, GITHUB_TRENDING_URL + "/python"),
        await get_github_trending({"since": "daily"}, GITHUB_TRENDING_URL + "/rust"),
    )

    async with aiohttp.ClientSession() as session:
        for repository in repositories:
            try:
                if repository["total_stars"] < 1500 or repository["forks"] < 500:
                    continue
            except TypeError:
                log.error(repository)
                continue

            if repository["url"] in repos_blacklist:
                continue

            try:
                await migrate_to_gitea(
                    session,
                    repository["url"],
                    repository["repository"],
                    repository["description"],
                    "http://192.168.0.10:13000",
                    aiohttp.BasicAuth("root", "123456"),
                )
            except asyncio.exceptions.TimeoutError:
                continue

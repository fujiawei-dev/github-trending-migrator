"""
Date: 2022.05.09 20:20
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.09 20:20
"""
import asyncio
from itertools import chain

import aiohttp

from .logger import log
from .scraping import GITHUB_TRENDING_URL as base_url, get_github_trending


async def migrate_to_gitea(session, clone_addr, repo_name, description):
    log.debug(clone_addr)

    response = await session.post(
        url="http://127.0.0.1:13000/api/v1/repos/migrate",
        # url="http://192.168.0.118:13000/api/v1/repos/migrate",
        auth=aiohttp.BasicAuth("root", "root"),
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


async def migrate_to_gitea_from_github_trending():
    repositories = chain(
        await get_github_trending({"since": "daily"}),
        await get_github_trending({"since": "weekly"}),
        await get_github_trending({"since": "monthly"}),
        await get_github_trending({"since": "daily"}, base_url + "/go"),
        await get_github_trending({"since": "weekly"}, base_url + "/go"),
        await get_github_trending({"since": "monthly"}, base_url + "/go"),
        await get_github_trending({"since": "daily"}, base_url + "/python"),
        await get_github_trending({"since": "weekly"}, base_url + "/python"),
        await get_github_trending({"since": "monthly"}, base_url + "/python"),
        await get_github_trending({"since": "daily"}, base_url + "/kotlin"),
        await get_github_trending({"since": "weekly"}, base_url + "/kotlin"),
        await get_github_trending({"since": "monthly"}, base_url + "/kotlin"),
        await get_github_trending({"since": "daily"}, base_url + "/java"),
        await get_github_trending({"since": "weekly"}, base_url + "/java"),
        await get_github_trending({"since": "monthly"}, base_url + "/java"),
        await get_github_trending({"since": "daily"}, base_url + "/dart"),
        await get_github_trending({"since": "weekly"}, base_url + "/dart"),
        await get_github_trending({"since": "monthly"}, base_url + "/dart"),
        await get_github_trending({"since": "daily"}, base_url + "/c++"),
        await get_github_trending({"since": "weekly"}, base_url + "/c++"),
        await get_github_trending({"since": "monthly"}, base_url + "/c++"),
    )

    async with aiohttp.ClientSession() as session:
        tasks = []

        for repository in repositories:
            if repository["total_stars"] < 1500 or repository["forks"] < 500:
                continue

            tasks.append(
                asyncio.create_task(
                    migrate_to_gitea(
                        session,
                        repository["url"],
                        repository["repository"],
                        repository["description"],
                    )
                )
            )

        await asyncio.wait(tasks)

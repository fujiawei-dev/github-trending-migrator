"""
Date: 2022.05.09 20:20
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.09 20:20
"""
import asyncio

import aiohttp

from .logger import log
from .scraping import get_github_trending


async def migrate_to_gitea(session, clone_addr, repo_name, description):
    log.debug(clone_addr)

    await session.post(
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


async def migrate_to_gitea_from_github_trending():
    repositories = await get_github_trending()
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

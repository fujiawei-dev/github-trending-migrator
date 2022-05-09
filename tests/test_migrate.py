"""
Date: 2022.05.09 21:32
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.09 21:32
"""
import asyncio

from github_trending_migrator.migrate import migrate_to_gitea_from_github_trending


def test_migrate_to_gitea_from_github_trending():
    asyncio.run(migrate_to_gitea_from_github_trending())

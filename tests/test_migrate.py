"""
Date: 2022.05.09 21:32
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.25 10:23:11
"""
import asyncio

from github_trending_migrator.migrate import (
    migrate_to_gitea_from_github_trending,
    get_repos_blacklist,
)


# pytest tests/test_migrate.py::test_get_repos_blacklist -v -s
def test_get_repos_blacklist():
    assert len(get_repos_blacklist()) > 600


# pytest tests/test_migrate.py::test_migrate_to_gitea_from_github_trending -v -s
def test_migrate_to_gitea_from_github_trending():
    asyncio.run(migrate_to_gitea_from_github_trending())

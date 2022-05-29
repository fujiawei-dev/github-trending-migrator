"""
Date: 2022.05.09 21:32
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.29 17:02:57
"""
import asyncio

from github_trending_migrator.migrate import (
    migrate_to_gitea_from_github_trending,
    migrate_to_gitea_from_gitea,
    get_repos_blacklist,
    repos_blacklist,
)


# pytest tests/test_migrate.py::test_get_repos_blacklist -v -s
def test_get_repos_blacklist():
    asyncio.run(get_repos_blacklist())
    assert len(repos_blacklist) > 600


# pytest tests/test_migrate.py::test_migrate_to_gitea_from_github_trending -v -s
def test_migrate_to_gitea_from_github_trending():
    asyncio.run(migrate_to_gitea_from_github_trending())


# pytest tests/test_migrate.py::test_migrate_to_gitea_from_gitea -v -s
def test_migrate_to_gitea_from_gitea():
    asyncio.run(migrate_to_gitea_from_gitea())

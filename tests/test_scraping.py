"""Functions for web scraping are tested
"""
import json

import pytest

from github_trending_migrator.scraping import (
    filter_articles,
    make_soup,
    scraping_developers,
    scraping_repositories,
)


@pytest.mark.parametrize(
    "input_html,expected_json",
    [
        pytest.param(
            "tests/data/repodata1.html",
            "tests/data/repodata1.json",
            id="25 typescript repositories, normal data",
        ),
        pytest.param(
            "tests/data/repodata2.html",
            "tests/data/repodata2.json",
            id="4 repositories instead of 25",
        ),
        pytest.param(
            "tests/data/repodata3.html",
            "tests/data/repodata3.json",
            id="Missing description of one repository",
        ),
        pytest.param(
            "tests/data/repodata4.html",
            "tests/data/repodata4.json",
            id="""1 repo which contains neither total_stars nor forks and a repo which has no since_stars""",
        ),
    ],
)
def test_repository_scraping(input_html: str, expected_json: str):
    """Tests functions which scrape data about repositories from HTML."""
    with open(expected_json) as file:
        correct_repo_json = json.loads(file.read())
    with open(input_html) as file:
        raw_html = file.read()

    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    repo_json = scraping_repositories(soup, since="daily")

    assert len(repo_json) == len(correct_repo_json)

    for i in range(len(repo_json)):
        assert repo_json[i] == correct_repo_json[i]


@pytest.mark.parametrize(
    "input_html,expected_json",
    [
        pytest.param(
            "tests/data/devdata1.html",
            "tests/data/devdata1.json",
            id="25 developers, normal data.",
        ),
        pytest.param(
            "tests/data/devdata2.html",
            "tests/data/devdata2.json",
            id="1 missing popular repository of developer.",
        ),
        pytest.param(
            "tests/data/devdata3.html",
            "tests/data/devdata3.json",
            id="15 developers, description of 1 repo is missing.",
        ),
    ],
)
def test_developer_scraping(input_html: str, expected_json: str):
    """Tests functions which scrape data about developers from HTML."""
    with open(expected_json) as file:
        correct_repo_json = json.loads(file.read())
    with open(input_html) as file:
        raw_html = file.read()

    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    repo_json = scraping_developers(soup, since="daily")

    assert len(repo_json) == len(correct_repo_json)
    for i in range(len(repo_json)):
        assert repo_json[i] == correct_repo_json[i]

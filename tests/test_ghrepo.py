from ghtesting.ghrepo import GHRepo
from ghtesting.ghdatabase import GHDatabase
import json
import os
import logging as log

# Testcase is mixed from multiple repos
jsontest = {
    "_id": "angular/angular.js",
    "createdAt": "2010-01-06T00:34:37Z",
    "description": "AngularJS - HTML enhanced for web apps!",
    "isFork": False,
    "isMirror": False,
    "primaryLanguage": {"name": "Python"},
    "languages": {
        "edges": [
            {"node": {"name": "JavaScript"}, "size": 6810485},
            {"node": {"name": "HTML"}, "size": 84393},
            {"node": {"name": "Shell"}, "size": 31578},
            {"node": {"name": "CSS"}, "size": 3638},
            {"node": {"name": "PHP"}, "size": 7222},
        ],
        "totalSize": 6937316,
    },
    "nameWithOwner": "angular/angular.js",
    "parent": None,
    "queriedAt": "2021-10-18T00:30:05Z",
    "repositoryTopics": {
        "edges": [
            {"node": {"topic": {"name": "ajenti"}}},
            {"node": {"topic": {"name": "python"}}},
            {"node": {"topic": {"name": "javascript"}}},
            {"node": {"topic": {"name": "administration"}}},
            {"node": {"topic": {"name": "linux"}}},
            {"node": {"topic": {"name": "panel"}}},
            {"node": {"topic": {"name": "angular"}}},
        ]
    },
    "rootdir": {
        "entries": [
            {"name": ".circleci", "type": "tree"},
            {"name": ".editorconfig", "type": "blob"},
            {"name": ".eslintignore", "type": "blob"},
            {"name": ".eslintrc-base.json", "type": "blob"},
            {"name": ".eslintrc-browser.json", "type": "blob"},
            {"name": ".eslintrc-node.json", "type": "blob"},
            {"name": ".eslintrc-todo.json", "type": "blob"},
            {"name": ".eslintrc.json", "type": "blob"},
            {"name": ".gitattributes", "type": "blob"},
            {"name": ".github", "type": "tree"},
            {"name": ".gitignore", "type": "blob"},
            {"name": ".mailmap", "type": "blob"},
            {"name": ".nvmrc", "type": "blob"},
            {"name": "CHANGELOG.md", "type": "blob"},
            {"name": "CODE_OF_CONDUCT.md", "type": "blob"},
            {"name": "CONTRIBUTING.md", "type": "blob"},
            {"name": "DEVELOPERS.md", "type": "blob"},
            {"name": "Gruntfile.js", "type": "blob"},
            {"name": "LICENSE", "type": "blob"},
            {"name": "README.closure.md", "type": "blob"},
            {"name": "README.md", "type": "blob"},
            {"name": "RELEASE.md", "type": "blob"},
            {"name": "SECURITY.md", "type": "blob"},
            {"name": "TRIAGING.md", "type": "blob"},
            {"name": "angularFiles.js", "type": "blob"},
            {"name": "benchmarks", "type": "tree"},
            {"name": "css", "type": "tree"},
            {"name": "docs", "type": "tree"},
            {"name": "i18n", "type": "tree"},
            {"name": "images", "type": "tree"},
            {"name": "karma-docs.conf.js", "type": "blob"},
            {"name": "karma-jqlite.conf.js", "type": "blob"},
            {"name": "karma-jquery-2.1.conf.js", "type": "blob"},
            {"name": "karma-jquery-2.2.conf.js", "type": "blob"},
            {"name": "karma-jquery.conf-factory.js", "type": "blob"},
            {"name": "karma-jquery.conf.js", "type": "blob"},
            {"name": "karma-modules-ngAnimate.conf.js", "type": "blob"},
            {"name": "karma-modules-ngMock.conf.js", "type": "blob"},
            {"name": "karma-modules.conf.js", "type": "blob"},
            {"name": "karma-shared.conf.js", "type": "blob"},
            {"name": "lib", "type": "tree"},
            {"name": "logs", "type": "tree"},
            {"name": "package.json", "type": "blob"},
            {"name": "protractor-circleci-conf.js", "type": "blob"},
            {"name": "protractor-conf.js", "type": "blob"},
            {"name": "protractor-shared-conf.js", "type": "blob"},
            {"name": "scripts", "type": "tree"},
            {"name": "src", "type": "tree"},
            {"name": "test", "type": "tree"},
            {"name": "vendor", "type": "tree"},
            {"name": "yarn.lock", "type": "blob"},
        ]
    },
    "stargazers": {"totalCount": 59596},
    "updatedAt": "2021-10-18T07:22:36Z",
    "url": "https://github.com/angular/angular.js",
    "workflowdir": None,
}


def test_repo_name():
    ## basically test that the repo is accessible
    # db = GHDatabase("github", "webframework_repos")
    # repojson = next(db.get_repos())
    # print(repojson)
    repo = GHRepo(jsontest)
    log.warning(f"Name: {repo.name}")
    assert repo.name == "angular/angular.js"


def test_repo_stars():
    repo = GHRepo(jsontest)
    log.warning(f"Stars: {repo.stars}")
    assert repo.stars == 59596

def test_repo_primarylanguage():
    repo = GHRepo(jsontest)
    log.warning(f"Primarylanguage: {repo.primarylanguage}")
    assert repo.primarylanguage == 'Python'

def test_repo_languages():
    repo = GHRepo(jsontest)

    log.warning(f"Languages: {repo.languages}")
    assert repo.languages == ["JavaScript", "HTML", "Shell", "CSS", "PHP"]


def test_repo_topics():
    repo = GHRepo(jsontest)

    log.warning(f"Topics: {repo.topics}")
    assert "angular" in repo.topics
    assert "linux" in repo.topics


def test_repo_rootdir():
    repo = GHRepo(jsontest)
    log.warning(f"Rootdir: {repo.rootdir}")
    assert (".circleci", "tree") in repo.rootdir
    assert ("package.json", "blob") in repo.rootdir


def test_repo_url():
    repo = GHRepo(jsontest)
    log.warning(f"Url: {repo.url}")
    assert "https://github.com/angular/angular.js" == repo.url

import logging as log
import re

class GHRepo:
    def __init__(self, json):
        self.json = json
        self._name = None
        self._isfork = None
        self._stars = None
        self._primarylanguage = None
        self._languages = None
        self._topics = None
        self._rootdir = None
        self._url = None
        self._badge_urls = None
        self._issue_count = None
        self._fork_count = None
        self._commit_count = None
        self._created_at = None
        self._pushed_at = None
        self._auto_merge_allowed = None
        self._funding_links = None
        self._is_archived = None

    @property
    def name(self):
        if self._name is None:
                self._name = self.json['_id']
        return self._name

    @property
    def isfork(self):
        if self._isfork is None:
                self._isfork = self.json['isFork']
        return self._isfork

    @property
    def stars(self):
        if self._stars is None:
            try:
                self._stars = self.json['stargazers']['totalCount']
            except:
                self._stars = None
        return self._stars

    @property
    def primarylanguage(self):
        if self._primarylanguage is None:
            try:
                self._primarylanguage = self.json['primaryLanguage']['name']
            except:
                self._primarylanguage = 'n/a'
        return self._primarylanguage

    @property
    def languages(self):
        if self._languages is None:
            self._languages = []
            for langobj in self.json['languages']['edges']:
                self._languages.append(langobj['node']['name'])
        return self._languages

    @property
    def topics(self):
        if self._topics is None:
            self._topics = []
            for topicobj in self.json['repositoryTopics']['edges']:
                self._topics.append(topicobj['node']['topic']['name'])
        return self._topics

    @property
    def rootdir(self):
        if self._rootdir is None:
            self._rootdir = []
            for fileobj in self.json['rootdir']['entries']:
                self._rootdir.append((fileobj['name'], fileobj['type']))
        return self._rootdir

    @property
    def url(self):
        if self._url is None:
            self._url = self.json['url']
        return self._url

    @property
    def badge_urls(self):
        if self._badge_urls is None:
            try:
                self._badge_urls = self.json['badges']
            except:
                self._badge_urls = None
        return self._badge_urls

    def _match_url_to_service(self, url):
        service_urls = {
            r'.*travis-ci.(?:org|com).*': 'travisci',
            r'.*img.shields.io/travis.*': 'travisci',


            r'.*circleci.com.*': 'circleci',
            r'.*img.shields.io/circleci.*': 'circleci',

            r'.*github.com/.*/workflows/.*': 'github',
            r'.*img.shields.io/github/workflow.*': 'github',

            r'.*ci.appveyor.com.*': 'appveyorci',
            r'.*img.shields.io/appveyor/ci/.*': 'appveyorci',

            r'.*saucelabs.com.*': 'saucelabs',

            r'.*dev.azure.com.*': 'azure_pipelines',
            r'.*visualstudio.com/.*/build.*': 'azure_pipelines',

            r'.*app.bitrise.io.*': 'bitrise',

            r'.*badge.buildkite.com.*': 'buildkite',

            r'.*codeship.com.*': 'codeship',
            r'.*img.shields.io/codeship/.*': 'codeship',

            r'.*gitlab.com/.*/badges/.*/pipeline.svg': 'gitlab',
            r'.*gitlab.com/.*/badges/.*/build.svg': 'gitlab',

            r'.*semaphoreci.com.*': 'semaphoreci',

            r'.*api.shippable.com.*': 'shippable',
            r'.*img.shields.io/shippable/.*': 'shippable',

            r'.*teamcity.jetbrains.com/.*/build.*': 'teamcity',

            r'.*app.wercker.com.*': 'wercker',

            #coverage
            # r'.*codecov.io.*': 'codecov',
            # r'.*img.shields.io/codecov/.*': 'codecov',

            # r'.*coveralls.io.*': 'coveralls',
            # r'.*img.shields.io/coveralls/.*': 'coverall',
        }
        for regex, service in service_urls.items():
            if re.match(regex, url):
                return service
        return None

    @property
    def badges(self):

        matched_services = list()
        unmatched_urls = list()

        if self.badge_urls is None:
            return None

        for url in self.badge_urls:
            service = self._match_url_to_service(url)
            if service is None:
                unmatched_urls.append(url)
            else:
                matched_services.append(service)

        return sorted(set(matched_services)), unmatched_urls

    @property
    def issue_count(self):
        try:
            self._issue_count = self.json['issues']['totalCount']
        except:
            self._issue_count = None
        return self._issue_count

    @property
    def fork_count(self):
        try:
            self._fork_count = self.json['forkCount']
        except:
            self._fork_count = None
        return self._fork_count

    @property
    def commit_count(self):
        try:
            self._commit_count = self.json['defaultBranchRef']['target']['history']['totalCount']
        except:
            self._commit_count = None
        return self._commit_count


    @property
    def auto_merge_allowed(self):
        try:
            self._auto_merge_allowed = self.json['autoMergeAllowed']
        except:
            self._auto_merge_allowed = None
        return self._auto_merge_allowed

    @property
    def created_at(self):
        try:
            self._created_at = self.json['createdAt']
        except:
            self._created_at = None
        return self._created_at

    @property
    def pushed_at(self):
        try:
            self._pushed_at = self.json['pushedAt']
        except:
            self._pushed_at = None
        return self._pushed_at

    @property
    def funding_links(self):
        try:
            self._funding_links = list()
            for link in self.json['fundingLinks']:
                self._funding_links.append(link['url'])
        except:
            self._funding_links = None
        return self._funding_links

import logging as log
import re

class GHRepo:
    def __init__(self, json):
        self.json = json
        self._name = None
        self._stars = None
        self._primarylanguage = None
        self._languages = None
        self._topics = None
        self._rootdir = None
        self._url = None
        self._badge_urls = None

    @property
    def name(self):
        if self._name is None:
            self._name = self.json['_id']
        return self._name

    @property
    def stars(self):
        if self._stars is None:
            self._stars = self.json['stargazers']['totalCount']
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


        for url in self.badge_urls:
            service = self._match_url_to_service(url)
            if service is None:
                unmatched_urls.append(url)
            else:
                matched_services.append(service)

        return sorted(set(matched_services)), unmatched_urls

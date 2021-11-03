import logging as log

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

#!/usr/bin/env python3

import requests
import re
from bs4 import BeautifulSoup

from ghdatabase import GHDatabase
from ghrepo import GHRepo

URL = "https://www.github.com/vim/vim"

def extract_readme(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    readmediv = soup.find('div', {'data-target': "readme-toc.content"})
    print(readmediv)

def extract_readme_badges(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify())
    readmediv = soup.find('div', {'data-target': "readme-toc.content"})
    if readmediv is None:
        return list()
    # ps = soup.find_all('p')
    # for p in ps:
    #     print(p)

    # convert to list of strings
    badge_htmls = list(map(str, readmediv.find_all('img')))

    badge_urls = list()
    for badge_html in badge_htmls:
        for badge_url in re.findall('"(https?://(?:.*?))"', badge_html):
            if 'githubusercontent' in badge_url:
                continue
            if f'{url}/raw' in badge_url:
                # pointing to file in repo
                continue
            if 'opencollective.com' in badge_url:
                continue
            if 'imgur.com' in badge_url:
                continue
            badge_urls.append(badge_url)
    return badge_urls
    # imgs = readmediv.find_all('img')
    # for i in imgs:
    #     print(i)

# print(extract_readme_badges('https://github.com/vdel26/tinychart'))
# print(extract_readme('https://github.com/angular-ui/ui-grid'))
# for i in extract_readme_badges('https://github.com/angular-ui/ui-grid'):
#     print(i)
# exit(0)

db = GHDatabase('github', 'webframework_repos')

count = 1
for repojson in db.get_repos():
    repo = GHRepo(repojson)

    print(f'{count}: {repo.name}')
    count = count + 1

    if repo.badge_urls is None:
        print(f'  getting badges for {repo.name}...')
        badges = extract_readme_badges(repo.url)
        # print(badges)
        db.append_to_repo(repo.name, {'badges': badges})

    # print(repo.url)
    # servs, unmatched = repo.badges
    # for u in unmatched:
    #     print(u)

    # exit()

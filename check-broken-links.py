import requests
from bs4 import BeautifulSoup
import urllib.parse
from collections import deque


def check_link(url, base_url):
  if url.startswith('http'):
    try:
      r = requests.get(url)
      if r.status_code == 200:
        return True
      else:
        return False
    except:
      return False
  elif '#' in url:
    try:
      r = requests.get(base_url)
      if r.status_code == 200:
        return True
      else:
        return False
    except:
      return False
  else:
    try:
      r = requests.get(urllib.parse.urljoin(base_url, url))
      if r.status_code == 200:
        return True
      else:
        return False
    except:
      return False

def find_dead_links(url, base_url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  links = soup.find_all('a')
  dead_links = []
  for link in links:
    href = link.get('href')
    if not check_link(href, base_url):
      dead_links.append((href, url))
  return dead_links

def crawl_site(url):
  queue = deque([url])
  visited = set()
  dead_links = []
  while queue:
    current_url = queue.popleft()
    r = requests.get(current_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
      href = link.get('href')
      if not check_link(href, url):
        dead_links.append((href, current_url))
    for link in links:
      href = link.get('href')
      if href.startswith(url) and href not in visited:
        queue.append(href)
        visited.add(href)
  if not dead_links:
    print('No dead links found!')
  else:
    for link, page in dead_links:
      print(f'Dead link {link} found on page {page}')

url = 'https://docs.kanaries.net'
crawl_site(url)

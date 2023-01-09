import requests
from bs4 import BeautifulSoup

def check_link(url):
  try:
    r = requests.get(url)
    if r.status_code == 200:
      return True
    else:
      return False
  except:
    return False

def find_dead_links(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  links = soup.find_all('a')
  dead_links = []
  for link in links:
    href = link.get('href')
    if not check_link(href):
      dead_links.append(href)
  return dead_links

def crawl_site(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  links = soup.find_all('a')
  for link in links:
    href = link.get('href')
    if href.startswith(url):
      dead_links = find_dead_links(href)
      print(f'Dead links on {href}: {dead_links}')

url = 'https://docs.kanaries.net'
crawl_site(url)

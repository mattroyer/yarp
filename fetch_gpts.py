import requests
from bs4 import BeautifulSoup
from time import sleep

def fetch_open_graph_data(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  og_data = {}
  for meta in soup.find_all('meta'):
    if meta.get('property', '').startswith('og:'):
      og_data[meta.get('property')] = meta.get('content')
  return format_html(og_data)

def strip_chatgpt(title):
  return title.replace('ChatGPT - ', '')

def format_html(og_data):
  return f"""
    <a href='https://chat.openai.com{og_data['og:url']}' class='gpt' target='_blank'>
      <img src='{og_data['og:image']}' alt='{strip_chatgpt(og_data['og:title'])}' width='{og_data['og:image:width']}' height='{og_data['og:image:height']}'>
      <h2>{strip_chatgpt(og_data['og:title'])}</h2>
      <p>{og_data['og:description']}</p>
    </a>
  """

def update_index_html(gpts_content):
  with open('index.html', 'r') as file:
    soup = BeautifulSoup(file, 'html.parser')

  gpts_div = soup.find('div', class_='gpts')
  gpts_div.clear()
  gpts_div.append(BeautifulSoup(gpts_content, 'html.parser'))

  formatted_html = soup.prettify()

  with open('index.html', 'w') as file:
    file.write(formatted_html)

gpts_content = ''
with open('GPTs.txt') as f:
  gpts = [line.rstrip() for line in f]
  for gpt in gpts:
    gpts_content += fetch_open_graph_data(gpt)
    sleep(0.5)

update_index_html(gpts_content)

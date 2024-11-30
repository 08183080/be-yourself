import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


def get_one(url):
    response = requests.get(url, headers)
    if response.status_code == 200:
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')
        title = soup.find('h1', class_='entry-title').text
        content = soup.find('div', class_='single-content').text

        return title, content

def write_one(title, content, path):
    with open(path + '\\'+ title + '.txt', 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    url = 'https://www.jiexy.com/42614.html'
    title, content = get_one(url)
    print(title)
    print(content)
    write_one(title, content, 'D:\\be-yourself\\data')
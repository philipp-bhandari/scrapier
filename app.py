from bs4 import BeautifulSoup
import requests
from pprint import pprint
import urllib
from urllib.request import urlretrieve

query_url = 'http://joyreactor.cc/tag/%D0%A5%D0%B5%D0%BD%D1%82%D0%B0%D0%B9'


def pagination(url):
    soup = make_soup(url)
    pag = soup.find('div', {'class': 'pagination_expanded'}).find('span', {'class': 'current'}).text
    return int(pag)


def make_soup(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    response = response.text
    return BeautifulSoup(response, 'lxml')


def get_images(url, counter):

    soup = make_soup(url)

    images = [img for img in soup.find_all('img')]
    print('Downloading images to current working directory.')

    image_links = [each.get('src') for each in images]
    for each in image_links:
        if ('/static/' or 'comment') in each:
            continue  # -------------------------------------------------------------------------------------------гифы
        filename = each.split('/')[-1]
        full_size_url = 'http://img0.reactor.cc/pics/post/full/' + filename
        try:
            if(filename[-5:-1] == '.jpe') & (filename != 'default_avatar.jpeg'):
                try:
                    name = f'{counter}-{image_links.index(each)}.jpeg'
                    print(name)
                    print(each)
                    urllib.request.urlretrieve(full_size_url, name)
                    print('***')
                except ValueError:
                    continue
                except OSError:
                    continue
        except IndexError:
            pass
    return image_links


count_pages = pagination(query_url)
# count_pages = 10
link_list = []

while count_pages != 0:
    link_list.append(f'{query_url}/{count_pages}')
    count_pages -= 1

for link in link_list:
    print(f'Забираем из {link}')
    counter_for_names = link_list.index(link)
    get_images(link, counter_for_names)

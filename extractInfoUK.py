from bs4 import BeautifulSoup
from datetime import date


def read_xml(file):
    with open(file) as fp:
        xml = BeautifulSoup(fp, 'lxml-xml')
    return xml


def get_date(sitting):
    return date.fromisoformat(sitting.date['format'])


def get_sittings(xml):
    return xml.find_all('housecommons')


def get_debates(sittings):
    sections = sittings.debates.find_all('section', recursive=True)
    for section in sections:
        titles = section.find_all('title')
        print(titles)


soup = read_xml('S6CV0005P0.xml')
sittings = get_sittings(soup)
for sitting in sittings:
    get_debates(sitting)
print(len(sittings))

# some = soup.find_all("housecommons")
# for a in some:
#     print(get_date(a))

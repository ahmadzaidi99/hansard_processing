from bs4 import BeautifulSoup
import requests
import os


def committee_meeting_pages(sessions):
    page = requests.get('https://www.ourcommons.ca/Committees/en/Home')
    committees_soup = BeautifulSoup(page.content, 'html5lib')
    committee_pages = committees_soup.find_all('a', class_='list-group-linked-item')
    committee_meeting_pages = []
    for link in committee_pages:
        link = link.get('href')
        for session in sessions:
            items = session.split('-')
            parliament = items[0]
            session = items[1]
            to_append = 'https://www.ourcommons.ca/' + str(link) + '/Meetings?parl=' + parliament + '&session=' + session
            committee_meeting_pages.append(to_append)
    return committee_meeting_pages


def get_evidence_links(meetings_page):
    page = requests.get(meetings_page)
    meeting_soup = BeautifulSoup(page.content, 'html5lib')
    meeting_evidence = meeting_soup.find_all('a', class_='btn btn-default btn-meeting-evidence')
    evidence_links = []
    for link in meeting_evidence:
        evidence_links.append('https:' + link.get('href'))
    return evidence_links


def get_xml(evidence_link):
    page = requests.get(evidence_link)
    evidence_soup = BeautifulSoup(page.content, 'html5lib')
    download_link = evidence_soup.find('a', class_='btn btn-export-xml hidden-xs')
    address_part = download_link.get('href')
    full_link = 'https://www.ourcommons.ca' + address_part
    split_link = full_link.split('/')
    file_name = split_link[-2] + '_' + split_link[-1]
    meeting_xml = requests.get(full_link)
    path = 'xml' + '/'

    if not os.path.exists(path):
        os.makedirs(path)

    with open(os.path.join(path, file_name), 'wb') as xml_file:
        xml_file.write(meeting_xml.content)
        xml_file.close()

def populate_xmls(sessions):
    meeting_pages = committee_meeting_pages(sessions)
    for meeting_page in meeting_pages:
        evidence_links = get_evidence_links(meeting_page)
        for evidence_link in evidence_links:
            get_xml(evidence_link)

populate_xmls(['42-1', '43-1', '42-2'])
import xml.etree.ElementTree as ET
import json
import os


meeting = dict()
meeting['metadata'] = dict()
meeting['turns'] = []
numturns = 0


def read_file(xml):
    xml_tree = ET.parse(xml)
    return xml_tree


def get_info(xml_tree):
    info = xml_tree.find('ExtractedInformation')
    for child in info:
        field = child.get('Name')
        meeting['metadata'][field] = child.text


def get_turns(xml_tree):
    global numturns
    global meeting
    for intervention in xml_tree.getroot().iter('Intervention'):
        numturns += 1
        speaker_id = intervention[0][0].get('DbId')
        speaker_name = intervention[0][0].text
        contribution: str = ''
        for child in intervention[1]:
            contribution += child.text.strip() + ' '
        meeting['turns'].append({
            'turn': numturns,
            'speakerID': speaker_id,
            'name': speaker_name,
            'contribution': contribution
        })


def xml_to_json(input_file):
    tree = read_file(input_file)
    get_info(tree)
    get_turns(tree)

    acronym = meeting['metadata'].get('Acronyme')
    parliament = meeting['metadata'].get('ParliamentNumber')
    session = meeting['metadata'].get('SessionNumber')
    meeting_number = meeting['metadata'].get('Number')

    filename = acronym + '_' + parliament + '_' + session + + meeting_number + '.json'

    path = 'json' + '/' + acronym + '/'

    if not os.path.exists(path):
        os.makedirs(path)

    with open(os.path.join(path, filename), 'w+') as outfile:
        json.dump(meeting, outfile)
        outfile.close()
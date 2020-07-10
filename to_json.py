import xml.etree.ElementTree as ET
import json
import os
from os import listdir
from os.path import isfile, join

class get_json:


    def read_file(self, xml):
        xml_tree = ET.parse(xml)
        return xml_tree



    def get_info(self, xml_tree):
        info = xml_tree.find('ExtractedInformation')
        for child in info:
            field = child.get('Name')
            self.meeting['metadata'][field] = child.text


    def get_turns(self, xml_tree):
        for intervention in xml_tree.getroot().iter('Intervention'):
            self.numturns += 1
            speaker_id = intervention[0][0].get('DbId')
            speaker_name = intervention[0][0].text
            # print(speaker_name)
            contribution = ''
            for child in intervention[1]:
                if type(child.text) == str:
                    contribution += child.text.strip() + ' '
            self.meeting['turns'].append({
                'turn': self.numturns,
                'speakerID': speaker_id,
                'name': speaker_name,
                'contribution': contribution
            })


    def __init__(self, input_file):
        self.meeting = dict()
        self.meeting['metadata'] = dict()
        self.meeting['turns'] = []
        self.numturns = 0

        tree = self.read_file(input_file)
        self.get_info(tree)
        self.get_turns(tree)

        acronym = self.meeting['metadata'].get('Acronyme')
        parliament = self.meeting['metadata'].get('ParliamentNumber')
        session = self.meeting['metadata'].get('SessionNumber')
        meeting_number = self.meeting['metadata'].get('Number')

        filename = acronym + '_' + parliament + '_' + session + '_' + meeting_number + '.json'

        path = 'json'

        if not os.path.exists(path):
            os.makedirs(path)

        with open(os.path.join(path, filename), 'w+') as outfile:
            json.dump(self.meeting, outfile)
            outfile.close()


def run():
    onlyfiles = [f for f in listdir('xml') if isfile(join('xml', f))]
    for file in onlyfiles:
        get_json(os.path.join('xml', file))

run()
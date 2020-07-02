import xml.etree.ElementTree as ET


def read_file(xml):
    tree = ET.parse(xml)
    return tree


def get_info(tree):
    info = tree.find('ExtractedInformation')
    for child in info:
        field = child.get('Name')
        print(field, ':', child.text)

def speaker_names(id, title):
    global speaker_dict
    if id in speaker_dict:
        return
    speaker_dict[id] = title


def get_turns(tree):
    global numturns
    numturns = 0
    text = ''
    for intervention in tree.getroot().iter('Intervention'):
        numturns += 1
        text += 'Turn ' + str(numturns) + '\n'
        speaker_names(intervention[0][0].get('DbId'), intervention[0][0].text)
        text += intervention[0][0].text + ':' + '\n'
        for child in intervention[1]:
            text += child.text.strip() + ' '
        text += '\n\n'
    return text


def output_file():
    with open('output.txt', 'w+') as file:
        tree = read_file('CAsample.XML')
        file.write(get_turns(tree))
        file.close()
        get_info(tree)

speaker_dict = dict()

output_file()

file = open('output.txt', 'rt')
data = file.read()
words = data.split()

print(len(words))
print(numturns)
print(speaker_dict)
print(len(speaker_dict))

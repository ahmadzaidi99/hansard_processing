import json
import matplotlib.pyplot as plt
import numpy as np

meeting = dict()
speakers = dict()


def load_file(file_name):
    global meeting
    with open(file_name) as json_file:
        meeting = json.load(json_file)
        json_file.close()


def num_turns():
    return len(meeting['turns'])


def meeting_contrib_wordcount():
    total = 0
    for i in range(1, num_turns() + 1):
        total += turn_word_count(get_turn(i))
    return total


def test_totals():
    total = 0
    for id in speaker_list().keys():
        total += speaker_total_words(id)
    print(total, meeting_contrib_wordcount())
    if meeting_contrib_wordcount() == total:
        return "it works"
    else:
        return "not equal"


def get_turn(turn_number):
    return meeting['turns'][turn_number - 1]


def turn_word_count(turn):
    contribution = turn.get('contribution')
    return len(contribution.split())


def speaker_all_contrib(speaker_id):
    turns = dict()
    for i in range(num_turns() - 1):
        if meeting['turns'][i].get('speakerID') == str(speaker_id):
            turns[meeting['turns'][i].get('turn')] = meeting['turns'][i].get('contribution')
    return turns


def all_turns_word_dist():
    word_count_list = []
    for i in range(1, num_turns()+1):
        word_count = turn_word_count(get_turn(i))
        word_count_list.append(word_count)
    return word_count_list


def all_turn_stats():
    word_dist = np.array(all_turns_word_dist())
    stats = dict()
    common_percentiles = [0.1, 0.25, 0.5, 0.75, 0.9]
    for percentile in common_percentiles:
        stats[percentile] = np.quantile(word_dist, percentile)
    stats['std'] = np.std(word_dist, dtype=np.float64)
    return stats


def turn_percentiles(percentile):
    word_dist = np.array(all_turns_word_dist())
    return np.quantile(word_dist, percentile)



def speaker_total_words(speaker_id):
    all_turns = speaker_all_contrib(speaker_id)
    total = 0
    for value in all_turns.values():
        total += len(value.split())
    return total


def speaker_list():
    global speakers
    for i in range(num_turns() - 1):
        if meeting['turns'][i].get('speakerID') in speakers:
            continue
        speakers[meeting['turns'][i].get('speakerID')] = meeting['turns'][i].get('name')
    return speakers


def speaker_contrib_share(speaker_id):
    total_contrib = meeting_contrib_wordcount()
    speaker_contrib = speaker_total_words(speaker_id)
    return speaker_contrib / total_contrib


def speaker_shares():
    shares_list = dict()
    speakers_list = speaker_list()
    for key in speakers_list.keys():
        shares_list[key] = speaker_contrib_share(key)
    return shares_list


def speaker_shares_test():
    shares_list = speaker_shares()
    total = 0
    for value in shares_list.values():
        total += value
    return total


def find_speaker_id(speaker):
    for key, value in speaker_list().items():
        if speaker.lower() in value.lower():
            return key
    return "speaker does not exist, try typing a different query"

def plt_turn_histogram():
    plt.hist(all_turns_word_dist(), density=True, bins = 30)
    plt.title('Turn Histogram for Meeting')
    plt.xlabel('Words in turn')
    plt.ylabel('Percent of turns')
    plt.show()


load_file('INAN_43_1.json')
print(num_turns())
print(get_turn(5))
# print(speaker_all_contrib(258653))
print(find_speaker_id('Kirt Ejesiak'))
print(meeting['turns'][0].get('contribution'))
print(turn_word_count(meeting['turns'][0]))
print(speaker_total_words(258653))
print(meeting_contrib_wordcount())
print(speaker_contrib_share(258653))
print(speaker_shares())
print(speaker_shares_test())
print(all_turns_word_dist())
print(all_turn_stats())
print(test_totals())
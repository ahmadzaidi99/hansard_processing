import json
import matplotlib.pyplot as plt
import numpy as np
import os
from os import listdir
from os.path import isfile, join


def turn_word_count(turn):
    contribution = turn.get('contribution')
    return len(contribution.split())

def get_percentiles(list):
    stats = dict()
    percentiles = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95]
    for percentile in percentiles:
        stats[percentile] = np.quantile(list, percentile)
    return stats


class MeetingData:

    def __init__(self, file_name):
        with open(file_name) as json_file:
            self.speakers = dict()
            self.meeting = json.load(json_file)
            self.speaker_list()
            json_file.close()

    def num_turns(self):
        return len(self.meeting['turns'])

    def meeting_contrib_wordcount(self):
        total = 0
        for i in range(1, self.num_turns() + 1):
            total += turn_word_count(self.get_turn(i))
        return total

    def get_turn(self, turn_number):
        return self.meeting['turns'][turn_number - 1]

    def speaker_all_contrib(self, speaker_id):
        turns = dict()
        for i in range(self.num_turns() - 1):
            if self.meeting['turns'][i].get('speakerID') == str(speaker_id):
                turns[self.meeting['turns'][i].get('turn')] = self.meeting['turns'][i].get('contribution')
        return turns

    def all_turns_word_dist(self):
        word_count_list = []
        for i in range(1, self.num_turns() + 1):
            word_count = turn_word_count(self.get_turn(i))
            word_count_list.append(word_count)
        return word_count_list

    def all_turn_stats(self):
        word_dist = np.array(self.all_turns_word_dist())
        stats = dict()
        common_percentiles = [0.1, 0.25, 0.5, 0.75, 0.9]
        for percentile in common_percentiles:
            stats[percentile] = np.quantile(word_dist, percentile)
        stats['std'] = np.std(word_dist, dtype=np.float64)
        return stats

    def turn_percentiles(self, percentile):
        word_dist = np.array(self.all_turns_word_dist())
        return np.quantile(word_dist, percentile)

    def speaker_total_words(self, speaker_id):
        all_turns = self.speaker_all_contrib(speaker_id)
        total = 0
        for value in all_turns.values():
            total += len(value.split())
        return total

    def speaker_list(self):
        for i in range(self.num_turns() - 1):
            if self.meeting['turns'][i].get('speakerID') in self.speakers.keys():
                continue
            self.speakers[self.meeting['turns'][i].get('speakerID')] = self.meeting['turns'][i].get('name')

    def speaker_contrib_share(self, speaker_id):
        total_contrib = self.meeting_contrib_wordcount()
        speaker_contrib = self.speaker_total_words(speaker_id)
        if total_contrib <= 0:
            return
        return speaker_contrib / total_contrib

    def speaker_shares(self):
        shares_list = dict()
        for key in self.speakers.keys():
            shares_list[key] = self.speaker_contrib_share(key)
        return shares_list

    def super_speakers(self):
        shares = self.speaker_shares()
        count = 0
        for value in shares.values():
            if value >= .1:
                count += 1
        return count

    def speaker_shares_test(self):
        shares_list = self.speaker_shares()
        total = 0
        for value in shares_list.values():
            total += value
        return total

    def find_speaker_id(self, speaker):
        for key, value in self.speakers.items():
            if speaker.lower() in value.lower():
                return key
        return "speaker does not exist, try typing a different query"

    def plt_turn_histogram(self):
        plt.hist(self.all_turns_word_dist(), density=True, bins=30)
        plt.title('Turn Histogram for Meeting')
        plt.xlabel('Words in turn')
        plt.ylabel('Percent of turns')
        plt.show()


def run():
    all_turn_word_lengths = []
    all_num_speakers = []
    all_num_turns = []
    all_super_speakers = []
    all_meetings_words = []

    onlyfiles = [f for f in listdir('json') if isfile(join('json', f))]
    count_them = 0
    for file in onlyfiles:
        the_meeting = MeetingData(os.path.join('json', file))
        all_turn_word_lengths.extend(the_meeting.all_turns_word_dist())
        all_num_speakers.append(len(the_meeting.speakers.keys()))
        all_num_turns.append(the_meeting.num_turns())
        all_super_speakers.append(the_meeting.super_speakers())
        all_meetings_words.append(the_meeting.meeting_contrib_wordcount())
        count_them += 1

    plt.hist(all_turn_word_lengths, density=True, bins=20, range=(0, 350))
    plt.title('Turn Histogram for Meeting')
    plt.xlabel('Words in turn')
    plt.ylabel('Percent of turns')
    plt.show()

    print('Number of meetings in sample: ' + str(count_them))
    print('Turn word lengths: ' + str(get_percentiles(all_turn_word_lengths)))
    print('Number of speakers in meeting: ' + str(get_percentiles(all_num_speakers)))
    print('Number of super speakers (speak for at least 10% of meeting) :' + str(get_percentiles(all_super_speakers)))
    print('Number of turns in meeting: ' + str(get_percentiles(all_num_turns)))
    print('Total words from contributions in meeting: ' + str(get_percentiles(all_meetings_words)))


run()

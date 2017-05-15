'''This module turnes json requests for tests into PDFs'''

import json
import string

class JsonDecoder(object):
    '''This class\' purpose is to provide a simple way to process a test file from any module'''

    def __init__(self, json_path):
        with open(json_path, 'r') as json_opened:
            self.raw_data = json.load(json_opened)
        self.event_names = set()
        self.division_names = set()
        self.type_names = set()
        #Top level: event names
        for event_name in self.raw_data.keys():
            self.event_names.add(event_name)
            #Just under top level: division names
            for division_name in self.raw_data[event_name].keys():
                self.division_names.add(division_name)
                for year in self.raw_data[event_name][division_name].keys():
                    for test_block in self.raw_data[event_name][division_name][year]:
                        #Two levels under division names: test info
                        type_names.add(test_block['type'])

    def generate(self, decoded_years, decoded_events, decoded_divisions, decoded_types, solutions = True):
        tests_and_labels = list()
        for event in decoded_events:
            subdata_event = self.raw_data[event]
            for division in decoded_divisions:
                if division not in subdata_event.keys():
                    continue
                subdata_division = subdata_event[division]
                for year in decoded_years:
                    if str(year) not in subdata_division.keys():
                        continue
                    subdata_year = subdata_division[str(year)]
                    for test_block in subdata_year:
                        for test_type in decoded_types:
                            if test_block['type'] == test_type:
                                tests_and_labels.append((test_block['test'], '{}@{}@{}@{}'.format(event, year, division, test_type)))
                                if solutions:
                                    tests_and_labels.append((test_block['solutions'], '{}@{}@{}@{}'.format(event, year, division, test_type)))

    def string_similarity(self, string_a, string_b):
        '''
        Computes the similarity of two strings. Returns a value in the range [0,1]
        http://www.catalysoft.com/articles/StrikeAMatch.html
        '''

        pair_list = lambda input_string: ['{}{}'.format(input_string[ind], input_string[ind + 1]) \
            for ind in range(len(input_string) - 1)]

        intersection = pair_list(string_a) & pair_list(string_b)

        return 2 * len(intersection) / (len(string_a) + len(string_b) - 2)

    def decode_years(self, year_str: str):
        '''Decodes the "years" string of a TestRequest JSON object'''
        years = set()
        year_str = ''.join(a for a in year_str if a in string.digits or a in [',', '-'])
        year_list = year_str.split(',')
        for segment in year_list:
            if '-' in segment:
                if segment.count('-') > 1:
                    #Something went wrong. Make no assumptions. Omit it altogether.
                    continue
                bottom, top = segment.split('-')
                bottom, top = int(bottom), int(top)
                bottom, top = min(bottom, top), max(bottom, top)
                for temp_year in range(bottom, top + 1):
                    years.add(temp_year)
            else:
                years.add(int(segment))
        return sorted(years)

    def decode_events(self, event_str):
        '''Decodes the "events" string of the TestRequest object'''
        events = set()
        event_str = event_str.strip().split(',')
        for event in event_str:
            #For every event, compare it to each known event and that event's aliases. Choose the one with maximum similarity
            max_event = ''
            max_similarity = 0.0
            for known_event in self.event_names:
                similarity = max(self.string_similarity(prob, event) for prob in known_event.lower().strip().split('|'))
                #0.75 is an estimation. This value MUST be tuned later
                if similarity > 0.75 and similarity > max_similarity:
                    max_similarity = similarity
                    max_event = known_event
            if max_event != '':
                events.add(max_event)
        return sorted(events)

    def decode_divisions(self, division_str):
        '''Literally just a copy-paste of decode_events with variable names changed'''
        divisions = set()
        division_str = division_str.strip().split(',')
        for division in division_str:
            #For every division, compare it to each known division and that division's aliases. Choose the one with maximum similarity
            max_division = ''
            max_similarity = 0.0
            for known_division in self.division_names:
                similarity = max(self.string_similarity(prob, division) for prob in known_division.lower().strip().split('|'))
                #0.75 is an estimation. This value MUST be tuned later
                if similarity > 0.75 and similarity > max_similarity:
                    max_similarity = similarity
                    max_division = known_division
            if max_division != '':
                divisions.add(max_division)
        return sorted(divisions)

    def decode_type(self, type_str):
        '''Literally just a copy-paste of decode_divisions with variable names changed'''
        test_types = set()
        test_type_str = test_type_str.strip().split(',')
        for test_type in test_type_str:
            #For every test_type, compare it to each known test_type and that test_type's aliases. Choose the one with maximum similarity
            max_test_type = ''
            max_similarity = 0.0
            for known_test_type in self.test_type_names:
                similarity = max(self.string_similarity(prob, test_type) for prob in known_test_type.lower().strip().split('|'))
                #0.75 is an estimation. This value MUST be tuned later
                if similarity > 0.75 and similarity > max_similarity:
                    max_similarity = similarity
                    max_test_type = known_test_type
            if max_test_type != '':
                test_types.add(max_test_type)
        return sorted(test_types)

from csv import DictReader
import json


def replace(dict, name, newName):
    dict[newName] = dict[name]
    del dict[name]


with open('C:/Users/lbcdn/Documents/Processing/shift/res/Cards.csv', newline='') as csv_file:
    dict_reader = DictReader(csv_file)
    for row in dict_reader:
        if row['Deck'] != 'White':
            break
        del row['Deck']
        del row['Desc']

        replace(row, 'Rules', 'desc')
        replace(row, 'Ticks Required [7, 9]', 'ticks')
        replace(row, 'Name', 'name')
        replace(row, 'Type', 'type')

        if not row['ticks']:
            row['ticks'] = 0

        row['type'] = 'Types.' + row['type']

        s = json.dumps(row)
        sub = '\"' + row['type'] + '\"'
        s = s.replace(sub, row['type'])
        print(s + ',')

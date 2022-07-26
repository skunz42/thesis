import csv
import sys

CRIME = 0
SAFE = 1
NYC_CRIME_SIZE = 134
NYC_SAFE_SIZE = 1063

def read_csv(filename, subreddits):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)

        for row in csv_reader:
            name = row[0]
            hits = int(row[1])
            karma = int(row[2])
            subscribers = int(row[3])
            jaccard = 0.0
            subreddits.append([name, hits, karma, subscribers, jaccard])

def jaccard(subreddits, input_type):
    for s in subreddits:
        if input_type == CRIME:
            s[4] = (s[1] + s[2]) / (NYC_CRIME_SIZE + s[3])
        elif input_type == SAFE:
            s[4] = (s[1] + s[2]) / (NYC_SAFE_SIZE + s[3])

def print_subs(subreddits):
    for k in subreddits:
        if k[3] > 10000:
            print(f'{k[0]}: {k[4]}')

def main():
    if len(sys.argv) != 3:
        print("wrong input format: jaccard.py <csv_filename> <input_type>")
        return

    filename = sys.argv[1]
    input_type = int(sys.argv[2])
    subreddits = []
    read_csv(filename, subreddits)
    jaccard(subreddits, input_type)
    print_subs(subreddits)

main()

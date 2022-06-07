import matplotlib.pyplot as plt
import sys
import csv

MAX_CLASSES = 5
PCRIME_INDEX = 12
POP_CLASS = 10
POL_CLASS = 11
PCRIME = 7
TEXT_COLOR = 'black'

def read_csv(filename, input_type, input_size, raw_csv_results):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)

        for row in csv_reader:
            parsed_value = int(row[input_type])
            raw_csv_results[parsed_value].append(float(row[PCRIME]))

def make_graph(x_axis, y_axis, input_type):
    plt.style.use('ggplot')
    plt.bar(x_axis, y_axis, width=0.6)
    if input_type == 0:
        plt.xlabel('Metro Size', color=TEXT_COLOR)
        plt.ylabel('Crime Posts as % of Total', color=TEXT_COLOR)
        plt.xticks(rotation=315, color=TEXT_COLOR)
        plt.yticks(color=TEXT_COLOR)
    elif input_type == 1:
        plt.xlabel('Metro Political Affiliation', color=TEXT_COLOR)
        plt.ylabel('Crime Posts as % of Total', color=TEXT_COLOR)
        plt.xticks(rotation=315, color=TEXT_COLOR)
        plt.yticks(color=TEXT_COLOR)

    plt.tight_layout()
    plt.show()

def main():
    if len(sys.argv) != 3:
        print("wrong input format: bar-graph.py <csv_filename> <input-type>")
        return

    raw_input_type = int(sys.argv[2])
    input_type = POP_CLASS
    input_size = 4
    if raw_input_type == 1:
        input_type = POL_CLASS
        input_size = 5

    raw_csv_results = []
    for i in range(input_size):
        raw_csv_results.append([])

    read_csv(sys.argv[1], input_type, input_size, raw_csv_results)
    results = []
    labels = []

    if raw_input_type == 0:
        labels = ['Very small', 'Small', 'Medium', 'Large']
    elif raw_input_type == 1:
        labels = ['Very Conservative', 'Conservative', 'Moderate', 'Liberal', 'Very Liberal']

    for i in range(input_size):
        results.append(sum(raw_csv_results[i]) / len(raw_csv_results[i]))

    make_graph(labels, results, raw_input_type)

main()

import matplotlib.pyplot as plt
import sys
import csv

MAX_CLASSES = 5
PCRIME_INDEX = 12
CRIME_INDEX = 13
POP_CLASS = 3
POL_CLASS = 11
PCRIME = 7
TEXT_COLOR = 'black'

def read_csv(filename, x_axis, y_axis, colors):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)

        for row in csv_reader:
            y_axis.append(float(row[PCRIME]))
            pop_class = int(row[POP_CLASS])
            
            p_dem = 100.0 * int(row[4]) / (int(row[4])+int(row[5]))
            if pop_class >= 500000:
                x_axis.append(p_dem)
                if p_dem >= 62.5:
                    colors.append((0.02, 0.443, 0.69))
                elif p_dem >= 52.5:
                    colors.append((0.573, 0.773, 0.871))
                elif p_dem >= 47.5:
                    colors.append((0.969, 0.969, 0.969))
                elif p_dem >= 37.5:
                    colors.append((0.957, 0.647, 0.51))
                else:
                    colors.append((0.792, 0, 0.125))
            else:
                y_axis.pop()

def make_graph(x_axis, y_axis, colors):
    plt.style.use('ggplot')
    plt.scatter(x_axis, y_axis, c=colors)
    plt.xlabel('Percent Voting Democrat', color=TEXT_COLOR)
    plt.ylabel('Normalized Crime Post Score', color=TEXT_COLOR)
    plt.xticks(rotation=315, color=TEXT_COLOR)
    plt.yticks(color=TEXT_COLOR)

    plt.tight_layout()
    plt.show()

def main():
    if len(sys.argv) != 2:
        print("wrong input format: scatter-graph.py <csv_filename>")
        return

    x_axis = []
    y_axis = []
    colors = []
    read_csv(sys.argv[1], x_axis, y_axis, colors)

    make_graph(x_axis, y_axis, colors)

main()

FILE_PATH = "../data/keywords.txt"
NUM_COLS = 4

def read_file(output):
    with open(FILE_PATH) as txt_file:
        for line in txt_file:
            output.append(line.rstrip())

def write_file(output):
    for i in range(len(output)//NUM_COLS):
        print(f"    {output[i]} & {output[i+len(output)//NUM_COLS]} & {output[i+2*len(output)//NUM_COLS]} & {output[i+3*len(output)//NUM_COLS]} \\\\ \\hline")

    leftover = len(output)%NUM_COLS
    leftover_string = "    "

    for l in range(leftover):
        leftover_string += output[len(output)-leftover+l]
        if l != leftover-1:
            leftover_string += " & "
        else:
            leftover_string += " \\\\ \\hline"
    print(leftover_string)

def main():
    output = []
    read_file(output)
    output.sort()
    write_file(output)

main()

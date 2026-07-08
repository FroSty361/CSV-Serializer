import sys
from src.core.core import CSVSerializer
from tests.classes.test_class import Test

def main():
    if len(sys.argv) - 1 < 1:
        sys.exit("Must Have An Argument For The CSV File")

    file_arg = sys.argv[1]

    input_class = Test()

    print(f"First = {input_class}")

    with open(file_arg, "r") as file:
        for line in file:
            tokens = line.split("|")

            length = len(tokens)

            if length < 1:
                continue
            elif length < 2:
                continue

            name = tokens[0]
            value = tokens[1]

            CSVSerializer.deserialize_kvp(input_class, name, value)

    print(input_class)

if __name__ == '__main__':
    main()
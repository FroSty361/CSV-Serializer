import sys
from src.core.core import CSVSerializer, CSVSerializerOptions
from tests.classes.test_class import Test


def main():
    if len(sys.argv) - 1 < 1:
        sys.exit("Must Have An Argument For The CSV File")

    file_arg = sys.argv[1]

    input_class = Test()

    print(f"First = {input_class}")

    options = CSVSerializerOptions(overwrite_copies=True, delimiter=",", raise_field_errors=True)

    CSVSerializer.deserialize_from_path(input_class, file_arg, options)

    print(input_class)


if __name__ == '__main__':
    main()
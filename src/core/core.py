from dataclasses import dataclass


@dataclass
class CSVSerializerOptions:
    overwrite_copies: bool = False
    raise_field_errors: bool = False

    delimiter: str = ','

class CSVSerializer:
    @staticmethod
    def deserialize_from_path(input_class: object, path: str, options: CSVSerializerOptions):
        content = ""

        try:
            with open(path, "r") as file:
                content = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"{path} Does Not Exist")

        CSVSerializer.deserialize(input_class, content, options)

    @staticmethod
    def deserialize(input_class: object, content: str, options: CSVSerializerOptions):
        lines = content.splitlines()

        used_names = []

        for i in range(len(lines)):
            line = lines[i]
            line = line.rstrip('\r\n')

            if len(line) == 0:
                continue

            if line.split(options.delimiter)[0] == "|name|":
                continue # For Heading

            name, value = CSVSerializer.deserialize_line(line, options)

            used_names.append(name)

            if len(used_names) > len(set(used_names)):
                used_names = list(set(used_names))

                if not options.overwrite_copies:
                    continue

            CSVSerializer.deserialize_kvp(input_class, name, value, options.raise_field_errors)

        return input_class

    @staticmethod
    def deserialize_line(line: str, options: CSVSerializerOptions):
        name = ""
        value = ""
        got_name = False
        in_quotes = False

        for char in line:
            if char == '"':
                if not got_name:
                    raise Exception("Can not have '\"' in csv field for name")

                in_quotes = not in_quotes
            elif char == options.delimiter:
                if in_quotes:
                    if got_name:
                        value += char
                    else:
                        raise Exception(f"Can not have '{options.delimiter}' in csv field for name")
                else:
                    if got_name:
                        raise Exception(
                            f"Already used '{options.delimiter}' as the delimiter. If making a string containing '{options.delimiter}', wrap string in quotes")
                    else:
                        got_name = True
            else:
                if got_name:
                    value += char
                else:
                    name += char

        return (name, value)

    @staticmethod
    def deserialize_kvp(input_class, name: str, value: str, raise_field_errors: bool = False):
        try:
            current_value = getattr(input_class, name)
        except AttributeError:
            if raise_field_errors:
                raise AttributeError(f"{type(input_class)} Has No Attribute Named {name}")

            print(f"{type(input_class)} Has No Attribute Named {name}")
            return

        try:
            new_value = type(current_value)(value)
        except TypeError:
            if raise_field_errors:
                raise TypeError(f"TypeError when setting property named {name} when its type is {type(current_value)}")

            print(f"TypeError when setting property named {name} when it has type {type(current_value)}")
        else:
            setattr(input_class, name, new_value)
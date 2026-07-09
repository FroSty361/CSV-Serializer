class CSVSerializer:
    @staticmethod
    def deserialize_from_path(input_class: object, path: str, overwrite_copies: bool):
        content = ""

        with open(path, "r") as file:
            content = file.read()

        CSVSerializer.deserialize(input_class, content, overwrite_copies)

    @staticmethod
    def deserialize(input_class: object, content: str, overwrite_copies: bool):
        lines = content.splitlines()

        used_names = []

        for i in range(len(lines)):
            line = lines[i]
            tokens = line.split(',')

            length = len(tokens)

            if length < 2:
                continue

            name = tokens[0]
            value = tokens[1]

            used_names.append(name)

            if len(used_names) > len(set(used_names)):
                used_names = list(set(used_names))

                if overwrite_copies == False:
                    continue

            CSVSerializer.deserialize_kvp(input_class, name, value)

        return input_class

    @staticmethod
    def deserialize_kvp(input_class, name: str, value: str):
        try:
            current_value = getattr(input_class, name)
        except AttributeError:
            print(f"{type(input_class)} Has No Attribute Named {name}")
            return

        try:
            new_value = type(current_value)(value)
        except TypeError:
            raise TypeError(f"TypeError when setting property named {name} when its type is {type(current_value)}")
        else:
            setattr(input_class, name, new_value)
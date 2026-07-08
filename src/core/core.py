class CSVSerializer:
    @staticmethod
    def deserialize(input_class: object, path: str):
        content = ""

        with open(path, "r") as file:
            content = file.read()

        CSVSerializer.deserialize(content, input_class)

    @staticmethod
    def deserialize(input_class: object, content: str):
        ...

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
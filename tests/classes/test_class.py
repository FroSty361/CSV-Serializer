class Test:
    def __init__(self):
        self.string: str = ""

        self.integer: int = 0
        self.floating_point_number: float = 0.0

    def __str__(self):
        result = f"{self.string}\n"

        result += f"{self.integer}\n"
        result += f"{self.floating_point_number}"

        return result
class Index(object):

    @staticmethod
    def from_one_based(num: int):
        """Create index based on one based integer"""
        return Index(num - 1)

    @staticmethod
    def from_zero_based(num: int):
        """Create index based on zero based integer"""
        return Index(num)

    def __init__(self, number: int):
        """Index Object"""
        self.zero_index = number

    @property
    def one_based_index(self):
        return self.zero_index + 1

    @property
    def zero_based_index(self):
        return self.zero_index

    def __repr__(self) -> str:
        return f"{self.one_based_index}"

    def __eq__(self, other):
        """Check for equality between 2 indices"""

        # Check if the type is the same
        if type(other) != Index:
            return False

        # Check if the zero index value is the same
        if other.zero_index == self.zero_index:
            return True

        # Otherwise it is not equal
        return False

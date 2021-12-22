import unittest

from Core.Index import Index


class IndexTest(unittest.TestCase):

    def setUp(self) -> None:
        self.valid_index_value_1 = Index.from_zero_based(1)
        self.valid_index_value_1_copy = Index.from_zero_based(1)
        self.valid_index_value_0 = Index.from_zero_based(0)
        self.valid_index_value_0_copy = Index.from_zero_based(0)
        self.valid_index_value_3 = Index.from_zero_based(3)
        self.invalid_index_none_type = None
        self.invalid_index_other_type = type

    def test_index_equality(self):
        """Check if 2 index with same values are equal"""

        # Same object
        self.assertEqual(self.valid_index_value_1, self.valid_index_value_1)
        self.assertEqual(self.valid_index_value_0, self.valid_index_value_0)

        # Same value different object
        self.assertEqual(self.valid_index_value_1, self.valid_index_value_1_copy)
        self.assertEqual(self.valid_index_value_0, self.valid_index_value_0_copy)

    def test_index_inequality(self):
        """Check of 2 different index are not equal"""

        # Different types
        self.assertNotEqual(self.valid_index_value_0, self.invalid_index_none_type)
        self.assertNotEqual(self.valid_index_value_0, self.invalid_index_other_type)

        # Same type different value
        self.assertNotEqual(self.valid_index_value_0, self.valid_index_value_1)
        self.assertNotEqual(self.valid_index_value_1, self.valid_index_value_3)
        self.assertNotEqual(self.valid_index_value_0, self.valid_index_value_3)


if __name__ == "__main__":
    unittest.main()

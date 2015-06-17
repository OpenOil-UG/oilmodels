from django.test import TestCase

from pdftables import interpret_range

# Create your tests here.

class TestRangeParser(TestCase):

    def test_ranges(self):
        inputs = ["1", "2-4", "1,3,5", "1,6-8, 4"]
        outputs = [
            [1], [2,3,4], [1,3,5], [1,6,7,8,4]]
        for inp, expected_out in zip(inputs, outputs):
            actual_out = interpret_range(inp)
            self.assertEqual(actual_out, expected_out)

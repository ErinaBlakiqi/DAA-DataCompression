import unittest
import Logic

class TestRLECompression(unittest.TestCase):

    def test_rle_compress_normal_case(self):
        """Test RLE compression with a normal binary string."""
        binary_string = "0001111000"
        expected_output = "3:0,4:1,3:0"
        self.assertEqual(Logic.rle_compress(binary_string), expected_output)

    def test_rle_compress_edge_case_single_bit(self):
        """Test RLE compression with the smallest possible input (1 character)."""
        binary_string = "0"
        expected_output = "1:0"
        self.assertEqual(Logic.rle_compress(binary_string), expected_output)

    def test_rle_compress_edge_case_one_type(self):
        """Test RLE compression with a string that contains only one type of character."""
        binary_string = "11111"
        expected_output = "5:1"
        self.assertEqual(Logic.rle_compress(binary_string), expected_output)

    def test_rle_compress_error_case_empty_string(self):
        """Test RLE compression with an empty string (should return an empty result)."""
        binary_string = ""
        expected_output = ""
        self.assertEqual(Logic.rle_compress(binary_string), expected_output)

    def test_rle_compress_error_case_invalid_characters(self):
        """Test RLE compression with a string containing non-binary characters (should raise an exception)."""
        binary_string = "00112AB00"
        with self.assertRaises(ValueError):
            Logic.rle_compress(binary_string)

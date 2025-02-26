import unittest
import Logic

class TestRLECompression(unittest.TestCase):
    
    def test_rle_decompress_normal_case(self):
        """Test RLE decompression with a normal encoded string."""
        rle_string = "3:0,2:1,4:0"
        expected_output = "000110000"
        self.assertEqual(Logic.rle_decompress(rle_string), expected_output)

    def test_rle_decompress_edge_case_single_character(self):
        """Test RLE decompression with the smallest possible input (1 character)."""
        rle_string = "5:1"
        expected_output = "11111"
        self.assertEqual(Logic.rle_decompress(rle_string), expected_output)

    def test_rle_decompress_edge_case_alternating_pattern(self):
        """Test RLE decompression with a string that alternates between characters."""
        rle_string = "1:0,1:1,1:0,1:1"
        expected_output = "0101"
        self.assertEqual(Logic.rle_decompress(rle_string), expected_output)

    def test_rle_decompress_error_case_empty_string(self):
        """Test RLE decompression with an empty string (should return an empty result)."""
        rle_string = ""
        expected_output = ""
        self.assertEqual(Logic.rle_decompress(rle_string), expected_output)

    def test_rle_decompress_error_case_invalid_format(self):
        """Test RLE decompression with an incorrectly formatted string (should raise an exception)."""
        rle_string = "3:0,2:1,invalid,4:0"
        with self.assertRaises(ValueError):
            Logic.rle_decompress(rle_string)
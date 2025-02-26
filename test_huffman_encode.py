import unittest
import Logic

class TestHuffmanEncoding(unittest.TestCase):
    def test_normal_case(self):
        """Test Huffman encoding with a standard sentence."""
        text = "hello world"
        root = Logic.build_huffman_tree(text)
        huffman_codes = Logic.generate_huffman_codes(root)
        encoded_text = Logic.huffman_encode(text, huffman_codes)
        # Expected output: A non-empty binary string
        self.assertIsInstance(encoded_text, str)
        self.assertGreater(len(encoded_text), 0)

    def test_edge_case_single_char(self):
        """Test Huffman encoding with a string consisting of a single repeated character."""
        text = "aaaaaa"
        root = Logic.build_huffman_tree(text)
        huffman_codes = Logic.generate_huffman_codes(root)
        encoded_text = Logic.huffman_encode(text, huffman_codes)
        # Expected output: All bits should be the same
        self.assertEqual(encoded_text, "000000")

    def test_edge_case_empty_string(self):
        """Test Huffman encoding with an empty string."""
        text = ""
        root = Logic.build_huffman_tree(text)
        huffman_codes = Logic.generate_huffman_codes(root)
        encoded_text = Logic.huffman_encode(text, huffman_codes)
        # Expected output: An empty string
        self.assertEqual(encoded_text, "")

    def test_error_case_invalid_character(self):
        """Test Huffman encoding with a character not present in the generated codes."""
        text = "hello world"
        root = Logic.build_huffman_tree(text)
        huffman_codes = Logic.generate_huffman_codes(root)
        # Expected output: A KeyError should be raised
        with self.assertRaises(KeyError):
            Logic.huffman_encode("unknown_char", huffman_codes)

    def test_huffman_decode(self):
        """Test Huffman decoding by ensuring encoding and decoding return the original text."""
        text = "test case"
        root = Logic.build_huffman_tree(text)
        huffman_codes = Logic.generate_huffman_codes(root)
        encoded_text = Logic.huffman_encode(text, huffman_codes)
        decoded_text = Logic.huffman_decode(encoded_text, root)
        # Expected output: Decoded text should match the original input
        self.assertEqual(decoded_text, text)
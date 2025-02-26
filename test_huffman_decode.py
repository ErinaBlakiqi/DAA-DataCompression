import unittest
import Logic

class TestHuffmanDecoding(unittest.TestCase):
    
    def test_normal_case_standard(self):
        """Test Huffman decoding with a standard input string."""
        text = "hello"
        root = Logic.build_huffman_tree(text)
        huffman_codes = Logic.generate_huffman_codes(root)
        encoded_text = Logic.huffman_encode(text, huffman_codes)
        decoded_text = Logic.huffman_decode(encoded_text, root)
        self.assertEqual(decoded_text, text)
    
    def test_normal_case_repeated_characters(self):
        """Test Huffman decoding with a string consisting of repeated characters."""
        text = "aaaaaa"
        root = Logic.build_huffman_tree(text)
        huffman_codes = Logic.generate_huffman_codes(root)
        encoded_text = Logic.huffman_encode(text, huffman_codes)
        decoded_text = Logic.huffman_decode(encoded_text, root)
        self.assertEqual(decoded_text, text)
    
    def test_edge_case_empty_string(self):
        """Test Huffman decoding with an empty string."""
        text = ""
        root = Logic.build_huffman_tree(text)
        huffman_codes = Logic.generate_huffman_codes(root)
        encoded_text = Logic.huffman_encode(text, huffman_codes)
        decoded_text = Logic.huffman_decode(encoded_text, root)
        self.assertEqual(decoded_text, text)
    
    def test_edge_case_single_char(self):
        """Test Huffman decoding with a string consisting of a single repeated character."""
        text = "x"
        root = Logic.build_huffman_tree(text)
        huffman_codes = Logic.generate_huffman_codes(root)
        encoded_text = Logic.huffman_encode(text, huffman_codes)
        decoded_text = Logic.huffman_decode(encoded_text, root)
        self.assertEqual(decoded_text, text)
    
    def test_error_case_invalid_encoded_text(self):
        """Test Huffman decoding with an invalid encoded string."""
        text = "hello"
        root = Logic.build_huffman_tree(text)
        huffman_codes = Logic.generate_huffman_codes(root)
        encoded_text = "110a101010"  # Invalid character 'a'
        
        with self.assertRaises(ValueError):
            Logic.huffman_decode(encoded_text, root)
    
    def test_error_case_invalid_tree(self):
        """Test Huffman decoding with an invalid Huffman tree (None)."""
        invalid_tree = None  # Invalid Huffman Tree
        
        with self.assertRaises(AttributeError):
            Logic.huffman_decode("101010", invalid_tree)

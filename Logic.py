import heapq
from collections import Counter
import math

# Define the Huffman Node class
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Step 1: Build Huffman Tree
def build_huffman_tree(text):
    freq = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

# Step 2: Generate Huffman Codes
def generate_huffman_codes(root, code='', huffman_codes={}):
    if root is None:
        return
    if root.char is not None:
        huffman_codes[root.char] = code
    generate_huffman_codes(root.left, code + '0', huffman_codes)
    generate_huffman_codes(root.right, code + '1', huffman_codes)
    return huffman_codes

# Step 3: Encode Text with Huffman Codes
def huffman_encode(text, huffman_codes):
    return ''.join(huffman_codes[char] for char in text)


# Example Usage
if __name__ == "__main__":
    # Compress
    compress_file('input.txt', 'compressed.txt', 'huffman_tree.txt')

    # Decompress
    decompress_file('compressed.txt', 'huffman_tree.txt', 'decompressed.txt')
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

# Step 4: Apply RLE Compression
def rle_compress(binary_string):
    compressed = []
    count = 1
    for i in range(1, len(binary_string)):
        if binary_string[i] == binary_string[i - 1]:
            count += 1
        else:
            compressed.append(f"{count}:{binary_string[i-1]}")
            count = 1
    compressed.append(f"{count}:{binary_string[-1]}")
    return ','.join(compressed)

# Compression Function
def compress_file(input_file, output_file, tree_file):
    with open(input_file, 'r') as f:
        text = f.read()

    # Huffman Coding
    root = build_huffman_tree(text)
    huffman_codes = generate_huffman_codes(root)
    encoded_text = huffman_encode(text, huffman_codes)

    # Run-Length Encoding
    rle_output = rle_compress(encoded_text)

    # Write Outputs
    with open(output_file, 'w') as f:
        f.write(rle_output)
    with open(tree_file, 'w') as f:
        f.write(str(huffman_codes))

    # Compression Ratio
    original_size = len(text) * 8  # Original in bits

    # Estimate compressed size in bits
    rle_pairs = rle_output.split(',')
    compressed_size = sum(math.ceil(math.log2(int(pair.split(':')[0]) + 1)) + 1 for pair in rle_pairs)

    compression_ratio = (original_size - compressed_size) / original_size * 100

    # Output the results
    print(f"Original Size (bits): {original_size}")
    print(f"Compressed Size (bits): {compressed_size}")
    print(f"Compression Ratio: {compression_ratio:.2f}%")




# Example Usage
if __name__ == "__main__":
    # Compress
    compress_file('input.txt', 'compressed.txt', 'huffman_tree.txt')

    # Decompress
    decompress_file('compressed.txt', 'huffman_tree.txt', 'decompressed.txt')
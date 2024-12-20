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

# Step 5: Decode RLE
def rle_decompress(rle_data):
    decompressed = []
    rle_pairs = rle_data.split(',')
    for pair in rle_pairs:
        count, bit = pair.split(':')
        decompressed.append(bit * int(count))
    return ''.join(decompressed)

# Step 6: Decode Huffman Encoding
def huffman_decode(encoded_text, huffman_tree):
    decoded_text = []
    current_node = huffman_tree
    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:  # Leaf node
            decoded_text.append(current_node.char)
            current_node = huffman_tree  # Reset to the root
    return ''.join(decoded_text)

# Step 7: Rebuild Huffman Tree from Codes
def rebuild_huffman_tree(huffman_codes):
    root = HuffmanNode(None, 0)
    for char, code in huffman_codes.items():
        current_node = root
        for bit in code:
            if bit == '0':
                if current_node.left is None:
                    current_node.left = HuffmanNode(None, 0)
                current_node = current_node.left
            else:
                if current_node.right is None:
                    current_node.right = HuffmanNode(None, 0)
                current_node = current_node.right
        current_node.char = char  # Assign character at the leaf
    return root

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

# Decompression Function
def decompress_file(compressed_file, tree_file, output_file):
    # Read the compressed file
    with open(compressed_file, 'r') as f:
        rle_data = f.read()

    # Read the Huffman tree
    with open(tree_file, 'r') as f:
        huffman_codes = eval(f.read())  # Convert string back to dictionary (use with trusted input only)

    # Rebuild the Huffman tree
    huffman_tree = rebuild_huffman_tree(huffman_codes)

    # Step 1: Decode RLE
    binary_string = rle_decompress(rle_data)

    # Step 2: Decode Huffman
    original_text = huffman_decode(binary_string, huffman_tree)

    # Write the decompressed data to the output file
    with open(output_file, 'w') as f:
        f.write(original_text)

    print(f"Decompression complete. Output saved to {output_file}.")

# Example Usage
if __name__ == "__main__":
    # Compress
    compress_file('input.txt', 'compressed.txt', 'huffman_tree.txt')

    # Decompress
    decompress_file('compressed.txt', 'huffman_tree.txt', 'decompressed.txt')
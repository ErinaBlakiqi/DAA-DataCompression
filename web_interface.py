import streamlit as st
import time
import heapq
from collections import Counter
import math
import matplotlib.pyplot as plt
import networkx as nx
import os

# Define the Huffman Node class
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Huffman Tree and Encoding Logic
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

def generate_huffman_codes(root, code='', huffman_codes={}):
    if root is None:
        return
    if root.char is not None:
        huffman_codes[root.char] = code
    generate_huffman_codes(root.left, code + '0', huffman_codes)
    generate_huffman_codes(root.right, code + '1', huffman_codes)
    return huffman_codes

def huffman_encode(text, huffman_codes):
    return ''.join(huffman_codes[char] for char in text)


# Run-Length Encoding Logic
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

def rle_decompress(rle_data):
    decompressed = []
    rle_pairs = rle_data.split(',')
    for pair in rle_pairs:
        count, bit = pair.split(':')
        decompressed.append(bit * int(count))
    return ''.join(decompressed)

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
        current_node.char = char
    return root

def huffman_decode(encoded_text, huffman_tree):
    decoded_text = []
    current_node = huffman_tree
    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.char is not None:
            decoded_text.append(current_node.char)
            current_node = huffman_tree
    return ''.join(decoded_text)

def compress_text(text):
    start_time = time.time()

    # Huffman Encoding
    root = build_huffman_tree(text)
    huffman_codes = generate_huffman_codes(root)
    encoded_text = huffman_encode(text, huffman_codes)

    # Run-Length Encoding
    compressed_data = rle_compress(encoded_text)

    original_size = len(text) * 8  # Original in bits
    rle_pairs = compressed_data.split(',')
    compressed_size = sum(math.ceil(math.log2(int(pair.split(':')[0]) + 1)) + 1 for pair in rle_pairs)

    compression_ratio = (original_size - compressed_size) / original_size * 100
    end_time = time.time()

    compression_time = end_time - start_time

    return compressed_data, huffman_codes, root, compression_ratio, original_size, compressed_size, compression_time

def decompress_text(compressed_data, huffman_codes):
    start_time = time.time()

    # Rebuild Huffman Tree
    huffman_tree = rebuild_huffman_tree(huffman_codes)

    # Decode RLE
    binary_string = rle_decompress(compressed_data)

    # Decode Huffman
    original_text = huffman_decode(binary_string, huffman_tree)

    end_time = time.time()
    return original_text, end_time - start_time


def plot_compression_stats(original_size, compressed_size, compression_ratio):
    fig, ax = plt.subplots()
    labels = ['Original Size', 'Compressed Size']
    sizes = [original_size, compressed_size]

    ax.bar(labels, sizes, color=['blue', 'green'])
    ax.set_title(f'Compression Ratio: {compression_ratio:.2f}%')
    ax.set_ylabel('Size (bits)')

    st.pyplot(fig)

def plot_compression_stats(original_size, compressed_size, compression_ratio):
    fig, ax = plt.subplots()
    labels = ['Original Size', 'Compressed Size']
    sizes = [original_size, compressed_size]

    ax.bar(labels, sizes, color=['blue', 'green'])
    ax.set_title(f'Compression Ratio: {compression_ratio:.2f}%')
    ax.set_ylabel('Size (bits)')

    st.pyplot(fig)

# Huffman Tree Visualization
def add_edges(graph, node, pos, x=0, y=0, layer=1, parent=None):
    if node is not None:
        pos[node] = (x, -y)
        if parent:
            graph.add_edge(parent, node)

        next_y = y + 1
        next_x = 2 ** (-layer)
        add_edges(graph, node.left, pos, x - next_x, next_y, layer + 1, node)
        add_edges(graph, node.right, pos, x + next_x, next_y, layer + 1, node)

def visualize_huffman_tree(root):
    graph = nx.DiGraph()
    pos = {}

    add_edges(graph, root, pos)

    labels = {node: node.char if node.char else '' for node in pos}

    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, labels=labels, with_labels=True, node_size=500, node_color="black", font_color="white")
    plt.title("Huffman Tree Visualization")
    st.pyplot(plt)


# Streamlit GUI
st.title("Data Compression Tool")

uploaded_file = st.file_uploader("Upload a text file for compression", type=["txt"])
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    st.text_area("Original Text", text, height=200)

    if st.button("Compress"):
        compressed_data, huffman_codes, root, compression_ratio, original_size, compressed_size, compression_time = compress_text(text)

        st.success("Compression Complete")
        st.text_area("Compressed Data", compressed_data, height=200)

        # Displaying Compression Stats
        st.write(f"**Original Size (bits):** {original_size}")
        st.write(f"**Compressed Size (bits):** {compressed_size}")
        st.write(f"**Compression Ratio:** {compression_ratio:.2f}%")
        st.write(f"**Compression Time:** {compression_time:.8f} seconds")

        plot_compression_stats(original_size, compressed_size, compression_ratio)

        st.write("### Huffman Tree Visualization")
        visualize_huffman_tree(root)

        # Save button now directly uses Streamlit's download_button
        st.download_button(
            label="Download Compressed File",
            data=compressed_data,
            file_name="compressed.txt",
            mime="text/plain"
        )

        if st.button("Decompress"):
            decompressed_text, decompression_time = decompress_text(compressed_data, huffman_codes)
            st.text_area("Decompressed Text", decompressed_text, height=200)
            st.write(f"Decompression Time: {decompression_time:.2f} seconds")



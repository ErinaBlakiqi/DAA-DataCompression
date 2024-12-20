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

    original_size = len(text) * 8  # Original in bits
    compressed_size_huffman = len(encoded_text)  # Size after Huffman in bits

    compression_ratio_huffman = (original_size - compressed_size_huffman) / original_size * 100
    end_time = time.time()

    return encoded_text, huffman_codes, root, compression_ratio_huffman, original_size, compressed_size_huffman, end_time - start_time

def apply_rle_to_huffman(encoded_text):
    compressed_data = rle_compress(encoded_text)

    rle_pairs = compressed_data.split(',')
    compressed_size_rle = sum(math.ceil(math.log2(int(pair.split(':')[0]) + 1)) + 1 for pair in rle_pairs)

    return compressed_data, compressed_size_rle

def visualize_huffman_tree(root):
    def add_edges(graph, node, pos, x=0, y=0, layer=1, parent=None):
        if node is not None:
            pos[node] = (x, -y)
            if parent:
                graph.add_edge(parent, node)

            next_y = y + 1
            next_x = 2 ** (-layer)
            add_edges(graph, node.left, pos, x - next_x, next_y, layer + 1, node)
            add_edges(graph, node.right, pos, x + next_x, next_y, layer + 1, node)

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
huffman_encoded_text = st.session_state.get('huffman_encoded_text', None)
huffman_codes = st.session_state.get('huffman_codes', None)
huffman_tree = st.session_state.get('huffman_tree', None)
rle_compressed_data = st.session_state.get('rle_compressed_data', None)
original_size = st.session_state.get('original_size', 0)
compressed_size_huffman = st.session_state.get('compressed_size_huffman', 0)
compressed_size_rle = st.session_state.get('compressed_size_rle', 0)
compression_ratio_huffman = st.session_state.get('compression_ratio_huffman', 0)
compression_ratio_rle = st.session_state.get('compression_ratio_rle', 0)

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    st.text_area("Original Text", text, height=200)

    if st.button("Apply Huffman Coding"):
        huffman_encoded_text, huffman_codes, huffman_tree, compression_ratio_huffman, original_size, compressed_size_huffman, compression_time = compress_text(text)

        st.session_state['huffman_encoded_text'] = huffman_encoded_text
        st.session_state['huffman_codes'] = huffman_codes
        st.session_state['huffman_tree'] = huffman_tree
        st.session_state['compression_ratio_huffman'] = compression_ratio_huffman
        st.session_state['original_size'] = original_size
        st.session_state['compressed_size_huffman'] = compressed_size_huffman

        st.success("Huffman Coding Applied")
        st.text_area("Huffman Binary Output", huffman_encoded_text, height=200, key="huffman_output")

        st.write(f"Huffman Compression Ratio: {compression_ratio_huffman:.2f}%")
        st.write(f"Original Size: {original_size} bits")
        st.write(f"Compressed Size (Huffman): {compressed_size_huffman} bits")

    if huffman_tree and st.button("Show Huffman Tree"):
        visualize_huffman_tree(huffman_tree)

    if huffman_encoded_text and st.button("Apply RLE"):
        rle_compressed_data, compressed_size_rle = apply_rle_to_huffman(huffman_encoded_text)

        compression_ratio_rle = (original_size - compressed_size_rle) / original_size * 100

        st.session_state['rle_compressed_data'] = rle_compressed_data
        st.session_state['compressed_size_rle'] = compressed_size_rle
        st.session_state['compression_ratio_rle'] = compression_ratio_rle

        st.success("RLE Compression Applied")
        st.text_area("RLE Compressed Data", rle_compressed_data, height=200, key="rle_output")

        st.write(f"RLE Compression Ratio: {compression_ratio_rle:.2f}%")
        st.write(f"Compressed Size (RLE): {compressed_size_rle} bits")

        if st.button("Save Compressed File"):
            compressed_file = 'compressed_rle.txt'
            with open(compressed_file, 'w') as f:
                f.write(rle_compressed_data)
            st.download_button(label="Download RLE Compressed File", data=rle_compressed_data, file_name=compressed_file)

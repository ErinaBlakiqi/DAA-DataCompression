import tkinter as tk
from tkinter import filedialog, messagebox
import time
import heapq
from collections import Counter
import math
import matplotlib.pyplot as plt
import networkx as nx
import os


# Define the Huffman Node class
class HuffmanNode:
    def _init_(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def _lt_(self, other):
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
            compressed.append(f"{count}:{binary_string[i - 1]}")
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
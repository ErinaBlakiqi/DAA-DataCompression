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

    return compressed_data, huffman_codes, root, compression_ratio, original_size, compressed_size, end_time - start_time


def plot_compression_stats(original_size, compressed_size, compression_ratio):
    fig, ax = plt.subplots()
    labels = ['Original Size', 'Compressed Size']
    sizes = [original_size, compressed_size]

    ax.bar(labels, sizes, color=['blue', 'green'])
    ax.set_title(f'Compression Ratio: {compression_ratio:.2f}%')
    ax.set_ylabel('Size (bits)')

    plt.show()


def visualize_huffman_tree(root):
    graph = nx.DiGraph()
    pos = {}

    add_edges(graph, root, pos)

    labels = {node: node.char if node.char else '' for node in pos}

    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, labels=labels, with_labels=True, node_size=500, node_color="black", font_color="white")
    plt.title("Huffman Tree Visualization")
    plt.show()

# Tkinter GUI
class CompressionApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Data Compression Tool")
        self.root.state('zoomed')  # Make the window full-screen

        self.upload_button = tk.Button(self.root, text="Upload Text File", command=self.upload_file)
        self.upload_button.pack(pady=10)

        self.compress_button = tk.Button(self.root, text="Compress", state=tk.DISABLED, command=self.compress)
        self.compress_button.pack(pady=10)

        self.text_display = tk.Text(self.root, height=10, width=100)
        self.text_display.pack(pady=10)

        self.compressed_display = tk.Text(self.root, height=10, width=100)
        self.compressed_display.pack(pady=10)

        self.stats_label = tk.Label(self.root, text="Compression Stats", font=("Helvetica", 14))
        self.stats_label.pack(pady=10)

        self.stats_text = tk.Text(self.root, height=5, width=100)
        self.stats_text.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Compressed File", state=tk.DISABLED, command=self.save_file)
        self.save_button.pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_display.delete(1.0, tk.END)
                text = file.read()
                self.text_display.insert(tk.END, text)
                self.compress_button.config(state=tk.NORMAL)

    def compress(self):
        text = self.text_display.get(1.0, tk.END).strip()
        compressed_data, huffman_codes, root, compression_ratio, original_size, compressed_size, compression_time = compress_text(
            text)

        self.compressed_display.delete(1.0, tk.END)
        self.compressed_display.insert(tk.END, compressed_data)

        self.stats_text.delete(1.0, tk.END)
        stats = f"Original Size: {original_size} bits\n"
        stats += f"Compressed Size: {compressed_size} bits\n"
        stats += f"Compression Ratio: {compression_ratio:.4f}%\n"
        stats += f"Compression Time: {compression_time:.6f} seconds"
        self.stats_text.insert(tk.END, stats)

        messagebox.showinfo("Compression Complete",
                            f"Compression completed successfully!\nTime: {compression_time:.6f} seconds")

        self.save_button.config(state=tk.NORMAL)

    def save_file(self):
        compressed_data = self.compressed_display.get(1.0, tk.END).strip()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(compressed_data)
            messagebox.showinfo("File Saved", f"Compressed file saved as {file_path}")


if _name_ == "_main_":
    root = tk.Tk()
    app = CompressionApp(root)
    root.mainloop()
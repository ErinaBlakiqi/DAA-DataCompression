# DAA-DataCompression
Using Huffman Coding and Run-Length Encoding
# Data Compression Tool: Huffman Coding and Run-Length Encoding

This project implements a data compression tool that uses a combination of **Huffman Coding** and **Run-Length Encoding (RLE)** to compress and decompress text data. The tool is implemented as a Python-based command-line application, a Streamlit web app, and a Tkinter desktop application, providing flexibility in how users can interact with it.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Usage](#command-line-usage)
  - [Web Interface](#web-interface)
  - [Desktop Interface](#desktop-interface)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The tool leverages two popular compression algorithms:

1. **Huffman Coding**: A lossless data compression algorithm that uses variable-length codes for encoding characters, based on their frequency of occurrence in the input data.
2. **Run-Length Encoding (RLE)**: A simple form of compression where consecutive data elements (runs) of the same value are stored as a single data value and its count.

The combination of these two techniques enables efficient text compression with high potential for reducing data size.

## Installation

### Requirements

- Python 3.x
- `tkinter` (for desktop app)
- `streamlit` (for web interface)

## Dependencies

Ensure you have the following dependencies installed:

- `heapq` (for implementing the priority queue used in Huffman coding)
- `collections` (for efficient counting of characters)

## Usage

### Command-Line Usage

To run the program on the command line:

#### Compress a file:

```bash
python main.py

### This will:

- Compress the input text file using Huffman Coding and RLE.
- Save the compressed data to a file (`compressed.txt`).
- Store the Huffman tree used for compression to a separate file (`huffman_tree.txt`).
- Print the compression ratio in the console.

### Decompress a file:

```bash
python main.py

### This will:

- Decompress the given compressed file using RLE and Huffman decoding.
- Save the decompressed data to an output file (`decompressed.txt`).

### Web Interface

To use the **Streamlit** web interface, simply run:

```bash
streamlit run web_interface.py






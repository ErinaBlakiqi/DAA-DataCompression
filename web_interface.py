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
#!/usr/bin/env python3

import os
import re
from collections import deque,defaultdict

def main(marker_type="packet"):
    input_path = (__file__).replace(".py","_input.txt")
    
    with open(input_path,"r") as f:
        input_stream = f.readline().strip("\n")
    
    last_seq = deque()
    lookup = defaultdict(int)
    
    print(f"Input stream has length of: {len(input_stream)}")   
    
    if marker_type=="packet":
        seq_len=4
    elif marker_type=="message":
        seq_len=14
    else:
        raise ValueError("Marker types can be only one of 'message' or 'packet'")

    for i,val in enumerate(input_stream):
        if lookup[val] > 0:
            left_most = None
            while left_most != val:
                left_most = last_seq.popleft()
                lookup[left_most] -= 1
        
        last_seq.append(val)
        lookup[val] += 1
        
        if len(last_seq)==seq_len:
            print(f"Start sequence found at index {i} with value {val}")
            print(f"Last sequence is {input_stream[i-seq_len+1:i+1]}, same as {last_seq}\n")
            break
if __name__ == "__main__":
    main("packet")
    main("message")

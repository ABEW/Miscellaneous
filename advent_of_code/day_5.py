#!/usr/bin/env python3

import os
import re
from collections import deque

def main():
    input_path = (__file__).replace(".py","_input.txt")
    
    stacks = None
    
    with open(input_path,"r") as f:
        for line in f:
            if line.strip()=="":
                continue
            elif not line.startswith("move"):
                parsed_line = re.sub(r"[\[\|\]]","",line).replace("    "," _ ").split()
                if stacks is None:
                    stacks = [deque() for i in range(len(parsed_line))]
                _ = [stacks[i].appendleft(val) for i,val in enumerate(parsed_line) if val != "_"] 
            else:
                _, count, _, st_deck, _, end_deck = line.split()
                count, st_deck, end_deck = list(map(int,[count, st_deck, end_deck]))
                temp_buff = []
                for _ in range(count):
                    temp_buff.append(stacks[st_deck-1].pop())
#                    stacks[end_deck-1].append(stacks[st_deck-1].pop())
                for _ in range(count):
                    stacks[end_deck-1].append(temp_buff.pop())
    print(stacks)
    print("".join([val.pop() for val in stacks]))
if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
import re

def main():
	input_path = (__file__).replace(".py","_input.txt")

	task_pairs = []

	with open(input_path,"r") as f:
		for line in f:
			task_pairs.append(list(map(int,re.split(",|-",line))))

	overlap_all_ct = 0

	for task in task_pairs:
		st1,end1,st2,end2 = task
		
		if (st1 <= st2) and (end2 <= end1):
			overlap_all_ct += 1
		elif (st2 <= st1) and (end1 <= end2):
			overlap_all_ct += 1

	print(f"\nThere are {overlap_all_ct} fully overlapping tasks.\n")

	overlap_some_ct = 0

	for task in task_pairs:
		st1,end1,st2,end2 = task
		
		if (st1>end2) or (st2>end1):
			continue
		else:
			overlap_some_ct += 1

	print(f"There are {overlap_some_ct} partial/fully overlapping tasks.\n")

if __name__ == "__main__":
	main()

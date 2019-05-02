#!/usr/bin/env python3

# Kaushal Kishore (bithack)
# 111601008
# Question No. 2a

# Here we are again. This time no bunny is floating in the middle of the ocean.
# And no agent want to find the dirt. This time we will write a script to count the 
# number of the words in a file.

import sys
import os.path

def main(argv):
    if len(argv) != 2:
        print("Usage: python3 counting_words.py filepath")
        sys.exit()
    else:
        try:
            word_count = 0
            current_state = 0

            filepath = sys.argv[1]
            if os.path.isfile(filepath):
                # if the filepath exists and is a file
                with open(filepath) as f:
                    while True:
                        ch = f.read(1)
                        print(ch)
                        if not ch:
                            break

                        if current_state==0:
                            if ch != '\n' and ch != ' ' and ch !='\t':
                                current_state=1
                                # print("incrementing")
                                word_count+=1
                        else:
                            if ch == '\n' or ch == ' ' or ch == '\t':
                                current_state=0
                            
                    print("Total Words: " , word_count)
        except:
            print("Something went wrong.")
            sys.exit()


if __name__ == "__main__":
    main(sys.argv)
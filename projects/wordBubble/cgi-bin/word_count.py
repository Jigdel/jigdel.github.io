#!/usr/bin/env python

"""Word frequency calculated for text files in input folder"""

from collections import Counter
from collections import OrderedDict
import sys
from glob import glob
import os
import re
import codecs
from timeit import default_timer

__author__ = "Jigdel K"
__copyright__ = "See license"
__credits__ = ["Python for Data Analysis - Wes Mckinney", "Intro to Data Science - Udacity", "Stack Overflow members"]
__license__ = "MIT License"
__version__ = "1.0"
__maintainer__ = "Jigdel K"
__email__ = "jigdel.k@gmail.com"
__status__ = "Always improving"


def cleanFile(file):
    """Strip/split/combine the text files in wc_input folder"""
    # all words into lowercase
    file = file.lower()

    # combining hypenated words and conjunctions
    file = re.sub(r"{([a-z])-([a-z])}|{([a-z])'([a-z])}", r'\1\2', file)

    # split the words (starting with letters, numbers ignored per FAQ)
    file = re.split(r'[^a-z]', file)
    return(file)  # return "cleaned" file
        

def writeFile(dict, file_name):
    """Write word frequency list to wc_output.txt"""
    # write in utf-8 to avoid future decoding issues (easier to parse)
    with codecs.open(file_name, 'w', 'utf-8') as f_out:
        for k, v in dict.items():
            # tab separated as mentioned in FAQs
            f_out.write("{}\t{} \n".format(k,v))

def main():
    
    # command line
    # python ./src/word_count.py ./wc_input ./wc_output/wc_result.txt
    input_directory = sys.argv[1]
    output_file= sys.argv[2]

    # define filepath and sort the file list
    files_list = glob(os.path.join(input_directory, '*.txt'))
    num_files = len(files_list)
    sorted_file_list = sorted(files_list)
    
    # word freq counter declaration
    word_freq = Counter()
    
    # track elapsed time to read files - testing purposes
    # tic = default_timer()
    
    # read text files in wc_input directory
    for f in sorted_file_list:
        # assuming encoding is ASCII(default for codecs) as mentioned in FAQ
        with codecs.open(f, 'r') as f_in:
        	# update our word counter dict with 'cleaned' file 
            word_freq.update(cleanFile(f_in.read()))

    # sort word freq list in alphabetical order
    sorted_words = OrderedDict(sorted(word_freq.items(), key=lambda t: t[0]))
    
    # toc = default_timer()
    # elapsed time in seconds
    # print("Read time:  ", (toc - tic)) 

	# track elapsed time to write files
    # tic = default_timer()
    
    # write to wc_result.txt
    writeFile(sorted_words, output_file)
    
    # toc = default_timer()
    # elapsed time in seconds
    # print("Write time: ", (toc - tic)) 

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    main()


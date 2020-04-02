"""
Currently working on Task 1 for the NLP project.
goal is to preprocess the language in the datasets by taking out punctuation and stopwords and 
preform stemming. 3 functions used in this program are: stem, remove_stopwords, and remove_punctuation. 
"""
import sys
#need to make sure we install nltk and nltk data to use these functions:
from nltk.corpus import stopwords               #remove_stopwords
from nltk.stem import PorterStemmer as ps       #stem
from nltk.tokenize import RegexpTokenizer       #remove_punctuation

input = []      #list of lists to store data from dataset file

with open(sys.argv[1], 'r') as file:
    for line in file:
        if len(line) == 1:      #checks if the line is blank/empty
            continue            #does not store it if it is empty
        else:
            input.append(line.split())

#print(input)
#print out the data line by line:
for line in input:
    for i in line:
        print(i)
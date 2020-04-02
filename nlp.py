import sys
#need to make sure we install nltk and nltk data to use these functions:
"""
from nltk.corpus import remove_stopwords    #library for remove_stopwords function
from nltk.stem import PorterStemmer as ps   #library for stem function
"""

"""
Currently working on Task 1 for the NLP project.
goal is to preprocess the language in the datasets by taking out punctuation and stopwords and 
preform stemming. 3 functions used in this program are: stem, remove_stopwords, and remove_punctuation. 
"""

#empty dictionary to be later used when the data is parsed
dict = {}

with open(sys.argv[1], 'r') as file:
    input = file.read()

print(input)



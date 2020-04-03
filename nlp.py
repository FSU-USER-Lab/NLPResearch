"""
Currently working on Task 1 for the NLP project.
goal is to preprocess the language in the datasets by taking out punctuation and stopwords and 
preform stemming. 3 functions used in this program are: stem, remove_stopwords, and remove_punctuation. 
"""
import sys
import nltk
#need to make sure we install nltk and nltk data to use these functions:
from nltk.corpus import stopwords               #remove_stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize         #remove_stopwords
from nltk.stem import PorterStemmer as ps       #stem
from nltk.tokenize import RegexpTokenizer       #remove_punctuation
nltk.download('punkt')

input = []      #list of lists to store data from dataset file
new_input = []  #list to contain updated parsed sentences

with open(sys.argv[1], 'r') as file:
    for line in file:
        if len(line) == 1:      #checks if the line is blank/empty
            continue            #does not store it if it is empty
        else:
            input.append(line)

#removing stopwords:
for _ in range(len(input)):
    text = input[_]
    tokens = word_tokenize(text)    #tokenize the sentence
    """tokens without stopwords:
    in the following line I iterate through all the words in the sentence tokens
    list and check if the word exists in the stop words collection or not.
    If it doesnt exist, meaning it is not a stopword, then it is appended to tokens_wo_sw.
    tokens_wo_sw contains a list of the sentence tokenized without stopwords.
    """
    tokens_wo_sw = [word for word in tokens if not word in stopwords.words()]
    #Joining the list of tokens without stopwords to create a sentence:
    new_sentence = (" ").join(tokens_wo_sw)
    new_input.append(new_sentence)

for _ in range(len(new_input)):
    print(new_input[_], end="\n")
import csv
import os
import random
import sys

# from enchant import Dict
# from enchant.checker import SpellChecker
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
# from nltk.stem.snowball import EnglishStemmer, ItalianStemmer
from nltk.tokenize import word_tokenize
# from pathlib import Path

# Loads data for albergate, eanci, etour, itrust, kepler, modis
# corpus = CC, queries=uc


def load_data(path, set_name, encoding='latin-1'):
    data = []
    files = []
    corpora_dict = {}
    queries_dict = {}

    with open(path+set_name+'_Corpus.txt', newline='', encoding=encoding) as corporafile:
        corpora_reader = csv.reader(corporafile, delimiter='\n')

        for corpus in corpora_reader:
            if corpus != []:
                data.append(word_tokenize(corpus[0]))

    with open(path+set_name+'_CorpusMapping.txt', newline='', encoding=encoding) as mapfile:
        map_reader = csv.reader(mapfile, delimiter='\n')

        for filename in map_reader:
            if filename != []:
                files.append(filename[0])

    for filename, contents in zip(files, data):
        corpora_dict[filename] = contents

    data.clear()
    files.clear()

    with open(path+set_name+'_Queries.txt', newline='', encoding=encoding) as queriesfile:
        queries_reader = csv.reader(queriesfile, delimiter='\n')

        for query in queries_reader:
            if query != []:
                data.append(word_tokenize(query[0]))

    with open(path+set_name+'_QueriesMapping.txt', newline='', encoding=encoding) as mapfile:
        map_reader = csv.reader(mapfile, delimiter='\n')

        for filename in map_reader:
            if filename != []:
                files.append(filename[0])

    for filename, contents in zip(files, data):
        queries_dict[filename] = contents

    return corpora_dict, queries_dict


def remove_stopwords(token_list, word_list):
    return [token for token in token_list if not token in word_list]


def remove_num_punct(token_list):
    return [token for token in token_list if token.isalnum() and not token.isnumeric()]


def stem(token_list):
    stemmed_tokens = []
    stemmer = PorterStemmer()

    for token in token_list:
        stemmed_tokens.append(stemmer.stem(token))

    return stemmed_tokens


def concatenate_data(queries_data, corpora_data, path, set_name, encoding='latin-1'):
    labeled_list = []

    with open(path+set_name+'_Oracle.txt', newline='', encoding=encoding) as oraclefile:
        oracle_reader = csv.reader(oraclefile, delimiter=',')
            
        for row in oracle_reader:
            #print('hello')
            for query in queries_data.keys():
                #print('world')
                for token in row:                
                    # if the corpus filename is in the given oracle row
                    if query in token or token in query:
                        for corpus in corpora_data.keys():
                            label = 0
                            #print(corpus)
                            for token in row:
                                #print(corpus, toke)
                                #print('looking')
                                # if the query filename is in the given oracle row update label
                                if corpus in token or token.lstrip() in corpus:
                                    #print('found')
                                    label = 1
                                    break 
                            #return None                                   
                                
                            # Clean filename string and shuffle CC+UC tokens
                            fname_str = query + '__' + corpus
                            concat_tokens = queries_data[query] + corpora_data[corpus]
                            random.shuffle(concat_tokens)
                            data_str = ' '.join(concat_tokens)

                            # save filename, joined data, and label as a tuple in list   
                            labeled_list.append((fname_str, data_str, label))
                        break

    return labeled_list


if __name__ == "__main__":
    download('stopwords')
    download('punkt')
    
    nltk_stopwords = stopwords.words()
    java_c_stopwords = []
    
    with open('data/java_c_stopwords.txt', newline='') as file:
        reader = csv.reader(file, delimiter='\n')
    
        for row in reader:
            java_c_stopwords.append(row[0])
            
    all_stopwords = nltk_stopwords + java_c_stopwords

    # dictionary of lists of tokens keyed by filename
    corpora_data, queries_data = load_data(sys.argv[1], sys.argv[2])
    print(len(corpora_data) * len(queries_data))


    # user_input = input('Please select stemming algorithm (porter or snowball): ')
    # user_input = user_input.lower()

    # clean each code class' tokenized list
    for corpus in corpora_data.keys():
        corpora_data[corpus] = remove_stopwords(corpora_data[corpus], all_stopwords)
        corpora_data[corpus] = remove_num_punct(corpora_data[corpus])
        corpora_data[corpus] = stem(corpora_data[corpus])

    # clean each use case's tokenized list
    for query in queries_data.keys():
        queries_data[query] = remove_stopwords(queries_data[query], all_stopwords)
        queries_data[query] = remove_num_punct(queries_data[query])
        queries_data[query] = stem(queries_data[query])

    output_list = concatenate_data(queries_data, corpora_data, sys.argv[1], sys.argv[2])

    with open('data/'+sys.argv[2]+'_filenames.txt', 'w', newline='') as fnfile:
        filename_writer = csv.writer(fnfile, quoting=csv.QUOTE_MINIMAL)

        with open('data/'+sys.argv[2]+'_data.txt', 'w', newline='') as datafile:
            data_writer = csv.writer(datafile, quoting=csv.QUOTE_MINIMAL)

            with open('data/'+sys.argv[2]+'_labels.txt', 'w', newline='') as labelfile:
                label_writer = csv.writer(labelfile, quoting=csv.QUOTE_MINIMAL)
    
                for labeled_link in output_list:
                    filename_writer.writerow([labeled_link[0]])
                    data_writer.writerow([labeled_link[1]])
                    label_writer.writerow([labeled_link[2]])    

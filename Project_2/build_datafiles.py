import csv
import sys

from nltk import download
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from numpy.random import shuffle

# Loads data for albergate, eanci, etour, itrust, kepler, modis
# corpora are UCs, queries are CCs


def load_data(path, set_name, encoding='latin-1'):
    data = []
    files = []
    corpora_dict = {}
    queries_dict = {}

    with open(path+set_name+'_Corpus.txt', newline='', encoding=encoding) as corporafile:
        corpora_reader = csv.reader(corporafile, delimiter='\n')

        for corpus in corpora_reader:
            if not (corpus == [] or corpus == [' ']):
                data.append(word_tokenize(corpus[0]))

    with open(path+set_name+'_CorpusMapping.txt', newline='', encoding=encoding) as mapfile:
        map_reader = csv.reader(mapfile, delimiter='\n')

        for filename in map_reader:
            if not (filename == [] or filename == [' ']):
                files.append(filename[0])

    for filename, contents in zip(files, data):
        corpora_dict[filename] = contents

    data.clear()
    files.clear()

    with open(path+set_name+'_Queries.txt', newline='', encoding=encoding) as queriesfile:
        queries_reader = csv.reader(queriesfile, delimiter='\n')

        for query in queries_reader:
            if not (query == [] or query == [' ']):
                data.append(word_tokenize(query[0]))

    with open(path+set_name+'_QueriesMapping.txt', newline='', encoding=encoding) as mapfile:
        map_reader = csv.reader(mapfile, delimiter='\n')

        for filename in map_reader:
            if not (filename == [] or filename == [' ']):
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

        oracle_queries = []
        queries_found = dict([(filename, False) for filename in queries_data.keys()])

        if set_name == 'kepler':
            oracle_reader = csv.reader(oraclefile, delimiter=' ')
        else:
            oracle_reader = csv.reader(oraclefile, delimiter=',')
            
        correct_valid_links = 0
        valid_links = 0
            
        for row in oracle_reader:
            
            if not (row == [] or row == [''] or row == [' ']):
                oracle_queries.append(row[0])
                correct_valid_links += len(row[1:])

            # Remove leading whitespace from values in oracle
            for i in range(len(row)):
                row[i] = row[i].lstrip()

            for query in queries_data.keys():
                # eanci and itrust set have extensions in mapping files but not in oracle file
                # we need to remove the extension so the comparisons will work
                if set_name == 'eanci' or set_name == 'itrust':
                    query = query.split('.')[0]

                for token in row:                
                    # if the corpus filename is in the given oracle row
                    if query == token:
                        # Update queries_found dict to indicate we have found code class in oracle
                        if set_name == 'eanci' or set_name == 'itrust':
                            queries_found[query+'.txt'] = True
                        else:
                            queries_found[query] = True

                        for corpus in corpora_data.keys():
                            if set_name == 'eanci' or set_name == 'itrust':
                                #corpus = corpus.rstrip('.txt')
                                corpus = corpus.split('.')[0]

                            label = 0

                            for token in row:
                                # if the query filename is in the given oracle row update label
                                if corpus == token:
                                    valid_links += 1
                                    label = 1
                                    break                                   
                                
                            fname_str = query + '__' + corpus

                            # If we are working with eanci we need to add the extension back
                            # Queries dict is keyed by filename+extension
                            if set_name == 'eanci' or set_name == 'itrust':
                                concat_tokens = queries_data[query+'.txt'] + corpora_data[corpus+'.txt']
                            else:
                                concat_tokens = queries_data[query] + corpora_data[corpus]

                            # Shuffle and join CC+UC tokens
                            shuffle(concat_tokens)
                            data_str = ' '.join(concat_tokens)

                            # Save filename, joined data, and label as a tuple in list   
                            labeled_list.append((fname_str, data_str, label))
                        break

    print('\n***** METADOC LINKS *****\n')
    print('There should be',correct_valid_links, 'valid links written.')
    print('Valid links written:',valid_links)

    not_found = 0
    print('\n***** ORACLE QUERIES NOT IN MAP FILE *****\n')
    for query in oracle_queries:
        if query not in queries_data.keys():
            print(query)
            not_found += 1

    print('\nTotal missing classes:', not_found)


    not_found=0
    # Generate metadocs for code classes not found in oracle file
    print('\n***** MAPPED QUERIES NOT IN ORACLE *****\n')
    for query, found in queries_found.items():
        if not found:
            print(query)
            not_found += 1
            for corpus in corpora_data.keys():
                fname_str = query + '__' + corpus

                concat_tokens = queries_data[query] + corpora_data[corpus]
                # Shuffle and join CC+UC tokens
                shuffle(concat_tokens)
                data_str = ' '.join(concat_tokens)

                # save filename, joined data, and label as a tuple in list   
                labeled_list.append((fname_str, data_str, 0))

    print('\nTotal missing classes:', not_found)

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
    

    # Clean each code class' tokenized list
    print('\n***** CLEANING CORPORA TOKEN LISTS*****\n')
    for corpus in corpora_data.keys():
        if len(corpora_data[corpus]) == 0:
            print(corpus, 'empty before clean')

        corpora_data[corpus] = remove_stopwords(corpora_data[corpus], all_stopwords)
        corpora_data[corpus] = remove_num_punct(corpora_data[corpus])
        corpora_data[corpus] = stem(corpora_data[corpus])

        if len(corpora_data[corpus]) == 0:
            print(corpus, 'empty after clean')

    # clean each use case's tokenized list
    print('\n***** CLEANING QUERIES TOKEN LISTS*****\n')
    for query in queries_data.keys():
        if len(queries_data[query]) == 0:
            print(query, 'empty before clean')

        queries_data[query] = remove_stopwords(queries_data[query], all_stopwords)
        queries_data[query] = remove_num_punct(queries_data[query])
        queries_data[query] = stem(queries_data[query])

        if len(queries_data[query]) == 0:
            print(query, 'empty after clean')

    # Create metadocs
    output_list = concatenate_data(queries_data, corpora_data, sys.argv[1], sys.argv[2])

    print('\n***** METADOC FILES *****\n')
    print('There should be', len(corpora_data) * len(queries_data), 'metadocs generated.')
    print('Metadocs generated: ', len(output_list))

    # Write metadoc filenames, data, and labels to files
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

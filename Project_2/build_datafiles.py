import csv
import os
import sys

from enchant import Dict
from enchant.checker import SpellChecker
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.snowball import EnglishStemmer, ItalianStemmer
from nltk.tokenize import word_tokenize
from pathlib import Path


def load_data(cc_path, uc_path, encoding='latin-1'):
    cc_files = os.listdir(cc_path)
    uc_files = os.listdir(uc_path)

    cc_dict = {}
    uc_dict = {}

    for cc in cc_files:
        # convert contents of cc file to a string then tokenize
        cc_dict[cc] = word_tokenize(Path(cc_path+cc).read_text(encoding=encoding))
    
    for uc in uc_files:
        # convert contents of uc file to a string then tokenize
        uc_dict[uc] = word_tokenize(Path(uc_path+uc).read_text(encoding=encoding))

    return cc_dict, uc_dict


def remove_stopwords(token_list, word_list):
    return [token for token in token_list if not token in word_list]


def remove_num_punct(token_list):
    return [token for token in token_list if token.isalnum() and not token.isnumeric()]


def stem(token_list, stem_alg):
    stemmed_tokens = []

    if stem_alg == 'porter':
        stemmer = PorterStemmer()

        for token in token_list:
            stemmed_tokens.append(stemmer.stem(token))

    else:
        d = Dict('it')   # create dictionary for Italian
        stemmer = EnglishStemmer() # Snowball
        stemmer_alt = ItalianStemmer() # Snowball

        for token in token_list:
            if d.check(token):
                stemmed_tokens.append(stemmer_alt.stem(token))
            else:
                stemmed_tokens.append(stemmer.stem(token))

    return stemmed_tokens


def concatenate_data(cc_data, uc_data, oracle_path):
    labeled_list = []

    with open(oracle_path, newline='') as oraclefile:
        oracle_reader = csv.reader(oraclefile, delimiter=',')
            
        for row in oracle_reader:
            # remove leading whitespace from comma separated values in smos_oracle
            for i in range(len(row)):
                row[i] = row[i].lstrip()

            for cc in cc_data.keys():                
                # if the cc filename w/o extension is in the given smos_oracle row
                if cc.replace('.txt', '') in row:
                    for uc in uc_data.keys():
                        # if the uc filename w/o extension is in the given smos_oracle row
                        if uc.replace('.txt', '') in row:
                            label = 1
                        else:
                            label = 0
                        
                        fname_str = cc.strip('.txt') + '_' + uc.strip('.txt')
                        data_str = ' '.join(cc_data[cc]) + ' ' + ' '.join(uc_data[uc])

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
    cc_data, uc_data = load_data(sys.argv[1], sys.argv[2])

    user_input = input('Please select stemming algorithm (porter or snowball): ')
    user_input = user_input.lower()

    # clean each code class' tokenized list
    for cc in cc_data.keys():
        cc_data[cc] = remove_stopwords(cc_data[cc], all_stopwords)
        cc_data[cc] = remove_num_punct(cc_data[cc])
        cc_data[cc] = stem(cc_data[cc], stem_alg=user_input)

    # clean each use case's tokenized list
    for uc in uc_data.keys():
        uc_data[uc] = remove_stopwords(uc_data[uc], all_stopwords)
        uc_data[uc] = remove_num_punct(uc_data[uc])
        uc_data[uc] = stem(uc_data[uc], stem_alg=user_input)

    output_list = concatenate_data(cc_data, uc_data, sys.argv[3])

    with open('data/'+sys.argv[4]+'_filenames.txt', 'w', newline='') as fnfile:
        filename_writer = csv.writer(fnfile, quoting=csv.QUOTE_MINIMAL)

        with open('data/'+sys.argv[4]+'_data_'+user_input+'.txt', 'w', newline='') as datafile:
            data_writer = csv.writer(datafile, quoting=csv.QUOTE_MINIMAL)

            with open('data/'+sys.argv[4]+'_labels.txt', 'w', newline='') as labelfile:
                label_writer = csv.writer(labelfile, quoting=csv.QUOTE_MINIMAL)
    
                for labeled_link in output_list:
                    filename_writer.writerow([labeled_link[0]])
                    data_writer.writerow([labeled_link[1]])
                    label_writer.writerow([labeled_link[2]])    

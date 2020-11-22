def get_vocabulary(str_list):
    wordID = 1
    vocabulary = {'UNK': 0, }

    for string in str_list:
        token_list = string.split()
        for token in token_list:
            if token not in vocabulary.keys():
                vocabulary[token] = wordID
                wordID += 1
        
    return vocabulary


def vocabulary_size(str_list):
    vocab = set()
    
    for string in str_list:
        token_list = string.split()
        for token in token_list:
            vocab.add(token)
                
    return len(vocab)
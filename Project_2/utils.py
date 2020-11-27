def get_vocabulary(str_list):
    vocabulary = set()

    for string in str_list:
        token_list = string.split()
        for token in token_list:
            vocabulary.add(token)
        
    return list(vocabulary)


def vocabulary_size(str_list):                
    return len(get_vocabulary(str_list))
def build_vocabulary(str_list,  k=None):

    language = {}
    vocabulary = {'UNK': 0, }

    for string in str_list:
        token_list = string.split()
        for token in token_list:
            if token in language:
                language[token] += 1
            else:
                language[token] = 1

    #print({key: value for key, value in sorted(language.items(), key=lambda item: item[1])})
    language = {key: value for key, value in sorted(
        language.items(), key=lambda item: item[1], reverse=True)}
    
    if k is None:
        vocabulary = vocabulary.update(dict(list(language.items())[0:]))
    else:
        vocabulary =  vocabulary.update(dict(list(language.items())[0:k]))
        
    return vocabulary


def vocabulary_size(str_list):
    vocab = set()
    
    for string in str_list:
        token_list = string.split()
        for token in token_list:
            vocab.add(token)
                
    return len(vocab)
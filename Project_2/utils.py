def build_vocabulary(str_list,  k):

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

    vocabulary.update(dict(list(language.items())[0: k]))

    return vocabulary


def encode(sentence, vocabulary):
	pass


def decode(sentence_list, vocabularys):
	pass

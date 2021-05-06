from math import log
from imblearn.over_sampling import SMOTE
from numpy import array, zeros
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

def get_vocabulary(str_list):
    vocabulary = set()

    for string in str_list:
        token_list = string.split()
        for token in token_list:
            vocabulary.add(token)

    # Remove TF reserved token 
    if '[UNK]' in vocabulary:            
        vocabulary.remove('[UNK]')
        
    return list(vocabulary)


def vocabulary_size(str_list):                
    return len(get_vocabulary(str_list))


def calculate_entropy(prob):    
    return -1 * (prob * log(prob, 2) + (1-prob) * log(1-prob, 2))


def balance_data(data, labels, SEQUENCE_LENGTH, BALANCE_RATIO):
    balanced_data = []
    
    '''
    Use the text vectorization layer to split, prune and map strings to integers.
    Set maximum_sequence length as all samples are not of the same length.
    '''
    vectorize_layer = TextVectorization(output_sequence_length=SEQUENCE_LENGTH)

    # Load vocab into vectorization layer
    vectorize_layer.set_vocabulary(get_vocabulary(data))
    
    # Get original vocabulary from unbalanced training data
    tf_vocab = vectorize_layer.get_vocabulary()
    inverse_vocab = {}
    
    '''
    Create an inverse vocabulary so we can decode the balanced vectorized data.
    Index of word in vectorization layer's vocabulary maps to it's int encoding.
    '''
    for i, word in enumerate(tf_vocab):
        inverse_vocab[i] = word
    
    # Create np arrays to store vectorized data
    vectorized_data = zeros((len(data), SEQUENCE_LENGTH))
    vectorized_labels = zeros(len(data))
    i = 0

    # Vectorize data and arrays for data balancing
    #for batch in unbalanced_ds:
    for sequence in vectorize_layer(data):
        vectorized_data[i] = sequence 
        i += 1

    # Perform SMOTE on loaded dataset
    balanced_data_enc, balanced_labels = SMOTE(sampling_strategy=BALANCE_RATIO).fit_resample(vectorized_data, labels)
    
    for row, label in zip(balanced_data_enc, balanced_labels):
        decoded = []
        for val in row:
            decoded.append(inverse_vocab[int(val)])
        
        balanced_data.append(' '.join(decoded))
    
    balanced_data = array(balanced_data, dtype=object)
    
    return balanced_data, balanced_labels
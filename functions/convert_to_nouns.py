#!/usr/bin/env python
# coding: utf-8

# In[1]:


# credit: https://stackoverflow.com/questions/14489309/convert-words-between-verb-noun-adjective-forms

from nltk.corpus import wordnet as wn

# Just to make it a bit more readable
WN_NOUN = 'n'
WN_VERB = 'v'
WN_ADJECTIVE = 'a'
WN_ADJECTIVE_SATELLITE = 's'
WN_ADVERB = 'r'

def convert(word, from_pos, to_pos):    
    """ 
    @param word:string
    @param from_pos: string
    @param to_pos: string
    
    @return result: string
    
    Description:
        Transform words given from/to POS tags 
        the possible values for from_pos and to_pos:
            NOUN = 'n'
            VERB = 'v'
            ADJECTIVE = 'a'
            ADJECTIVE_SATELLITE = 's'
            ADVERB = 'r'
    """

    synsets = wn.synsets(word, pos=from_pos)

    # Word not found
    if not synsets:
        return word

    # Get all lemmas of the word (consider 'a'and 's' equivalent)
    lemmas = []
    for s in synsets:
        for l in s.lemmas():
            if s.name().split('.')[1] == from_pos or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and s.name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                lemmas += [l]

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]

    # filter only the desired pos (consider 'a' and 's' equivalent)
    related_noun_lemmas = []

    for drf in derivationally_related_forms:
        for l in drf[1]:
            if l.synset().name().split('.')[1] == to_pos or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and l.synset().name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                related_noun_lemmas += [l]

    # Extract the words from the lemmas
    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w)) / len_words) for w in set(words)]
    result.sort(key=lambda w:-w[1])
    
    if result:
        return result[0][0]
    else:
        return word
import contractions, re, spacy

nlp = spacy.load("en_core_web_sm")

def create_doc_entity_list(doc):
    entity_index = []
    for ent in doc.ents:
        entity_index.append((ent.start, ent.end-1,ent.label_))
    return entity_index

def preprocessing(text, min_word_length=2, include_entity=True):
    '''
    @param text: str, the transcript text
    @param min_word_length: the threshold lengths set for each word, word with length below the value will be removed
    @param include_entity: bool, default True; whether or not the tokens will include the recognized entities
    @param onlly_tags: list, default []; to specify the types of tokens to be included, by default all tokens will be included

    @return tokens: default list, a list of tokens after preprocessing; if string_sperator is sepecified, return string
    
    Description:
        The function first fix all contractions in the text (don't --> do not), followed by removed words in parenthesis (e.g. (Laughters)). The words in the parenthesis are often audience reactions. 
        Entities in the text are recognized with their types. If the include_entity param is True, and the type of the entity is not Date/Time/Percent/Money/Quantity/Ordinal/Cardinal, the entity phrase is included.
        For non-entity tokens, they are added to the tokens list after lemmatization and lowering the case, only if they are alphabetic and not part of the stopwords, the token type meet the only_tags requirement and the length of the lemmatized token meet the threhold.
    '''
    fixed_contractions = contractions.fix(text)  # 1
    removed_parenthesis = re.sub("[\\(].*?[\\)]","",string=fixed_contractions)  #2
    doc = nlp(removed_parenthesis)
    entity_index = create_doc_entity_list(doc)
    entity = ''
    tokens = []
    for i, token in enumerate(doc):
        is_entity = False
        for ent in entity_index:
            if i >= ent[0] and i <= ent[1]:
                if ent[2] not in ['DATE','TIME','PERCENT','MONEY','QUANTITY','ORDINAL','CARDINAL']:
                    if entity =='':
                        entity = token.text
                    else:
                        entity += " "+token.text
                is_entity = True

        if is_entity:
            continue
        if entity != '' and include_entity:
            tokens.append(entity)
            entity = ''
        if token.is_stop == False and token.is_alpha == True and len(token.lemma_) >= min_word_length:
            tokens.append(token.lemma_.lower())
    return tokens
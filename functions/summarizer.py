import pickle, pandas as pd, numpy as np
import spacy, contractions, re
import networkx as nx
from itertools import combinations,product

nlp = spacy.load("en_core_web_lg")
vectorizer = pickle.load(open('model/tfidf_vectorizer.p','rb'))

def get_top_tfidf_dict(input_text_tokens):
    transcript_str = "{@}".join(input_text_tokens)
    tfidf_matrix = vectorizer.transform([transcript_str])
    feature_array = np.array(vectorizer.get_feature_names())
    tfidf_idx_score =  sorted([(i,score) for i,score in enumerate(tfidf_matrix.toarray().flatten())],key=lambda x:x[1],reverse=True)
    top_words_dict = {feature_array[i]:score for i,score in tfidf_idx_score[:15]}
    return top_words_dict

def sentence_tokenize(text):
    fixed_contractions = contractions.fix(text)
    removed_parenthesis = re.sub("[\\(].*?[\\)]","",string=fixed_contractions) 
    doc = nlp(removed_parenthesis)
    return [sent.text for sent in doc.sents]

def build_similarity_matrix(sentences):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    docs = [nlp(doc) for doc in sentences] 
    
    for idx1,idx2 in combinations(range(len(docs)),r=2):
        if idx1 != idx2:
            score = docs[idx1].similarity(docs[idx2])
            similarity_matrix[idx1][idx2] = score
            similarity_matrix[idx2][idx1] = score
    return similarity_matrix   

def textRank_all_sents(sents):
    sentence_similarity_martix = build_similarity_matrix(sents)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph,max_iter=500)

    ranked_sentence = sorted([(s,scores[i],) for i,s in enumerate(sents)], key=lambda x:x[1], reverse=True)     
    return ranked_sentence
 

def generate_summary(input_text, input_text_tokens, input_title_tokens, topicKeywords):

    input_sents = sentence_tokenize(input_text)
    tfidf_dict = get_top_tfidf_dict(input_text_tokens)
    
    topic_keywords_dict = {}
    for (score,w) in topicKeywords:
        if w not in topic_keywords_dict or score > topic_keywords_dict[w]:
            topic_keywords_dict[w] = score
                
    keywords = set(input_title_tokens) | set(tfidf_dict.keys()) | set(topic_keywords_dict.keys())
    keyword_weight_dict = {}
    for keyword in keywords:
        keyword_weight_dict[keyword] = 0
        if keyword in set(input_title_tokens):
            keyword_weight_dict[keyword] +=1 
        if keyword in set(tfidf_dict.keys()):
            keyword_weight_dict[keyword] +=1 
        if keyword in set(topic_keywords_dict.keys()):
            keyword_weight_dict[keyword] +=1 
    
    sents_score_dict = {}          
    for i, sent in enumerate(input_sents):
        sents_score_dict[i] = 0
        for keyword in keywords:
            if keyword in sent:
                sents_score_dict[i] += keyword_weight_dict[keyword]
            elif keyword.lower() in sent:
                sents_score_dict[i] += keyword_weight_dict[keyword]
            elif keyword.title() in sent:
                sents_score_dict[i] += keyword_weight_dict[keyword]
                
    sents_score_list = sorted(zip(sents_score_dict.keys(),sents_score_dict.values()), key=lambda x:x[1],reverse=True)
    filtered_sents = [input_sents[x[0]] for x in sents_score_list[:100]]
    
    ranked_sents = textRank_all_sents(filtered_sents)
    
    return ranked_sents[:10]   
    
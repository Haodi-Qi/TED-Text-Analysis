from functions.preprocessing import preprocessing
import pickle, numpy as np

vectorizer = pickle.load(open('model/tfidf_vectorizer.p','rb'))

df = pickle.load(open('data/pickle/filtered_talks.p','rb'))[['title']]
df['tokens'] = pickle.load(open('data/pickle/transcript_tokens.p','rb'))

def cosine_sim(text1, text2):
    tfidf = vectorizer.transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def generate_recommendation(input_tokens):
    scores = []
    input_text = "{@}".join(input_tokens)
    for index,row in df.iterrows():
        reference_talk = "{@}".join(row['tokens'])
        score  = cosine_sim(reference_talk, input_text)
        scores.append(score)
    scores = np.array(scores)
    indices = np.argsort(scores)[::-1]
    
    recommended_titles = [df.iloc[indices[x],0] for x in range(3)]

    return recommended_titles
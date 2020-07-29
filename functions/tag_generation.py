import pickle, pandas as pd, gensim, ast, numpy
from gensim.models.ldamodel import LdaModel

# credit: https://stackoverflow.com/questions/54684552/issue-with-topic-word-distributions-after-malletmodel2ldamodel-in-gensim
def ldaMalletConvertToldaGen(mallet_model):
    model_gensim = LdaModel(id2word=mallet_model.id2word, num_topics=mallet_model.num_topics, alpha=mallet_model.alpha, eta=0, iterations=1000, gamma_threshold=0.001, dtype=numpy.float32)
    model_gensim.state.sstats[...] = mallet_model.wordtopics
    model_gensim.sync_state()
    return model_gensim

lda_mallet = pickle.load(open('model/ldamallet_tuned.p','rb'))
lda_model = ldaMalletConvertToldaGen(lda_mallet)

id2word = pickle.load(open('data/pickle/gensim_id2words.p','rb'))

topic_tag_dict = pickle.load(open('data/pickle/topic_concepts.p','rb'))
topicWordMatrix = pd.read_csv('data/output/topicWordMatrix.csv')

def tag_generation(input_transcript_tokens):
    transcript_bow = id2word.doc2bow(input_transcript_tokens)
    lda_model.update([transcript_bow])
    topic_dist = sorted(lda_model[transcript_bow],key=lambda x:x[1],reverse=True)
    top3Topics= [topic_dist[i][0] for i in range(3)]
    mainTopicKeywords = [ast.literal_eval(t)[1] for t in topicWordMatrix.iloc[:,top3Topics[0]]]
    topicKeywords = [ast.literal_eval(t) for i in top3Topics for t in topicWordMatrix.iloc[:,i]]
    
    return (topicKeywords, mainTopicKeywords, topic_tag_dict[top3Topics[0]])
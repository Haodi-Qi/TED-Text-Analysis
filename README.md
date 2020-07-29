# TED-Text-Analysis
A text analysis project on TED Talk dataset for tag extraction, summarization and related talk recommendation.

This project was carried out under SMU IS450 Text Mining and Natural Language Processing in AY2019-2020 Semster 2. The team consists of Wende B., Chengzi Z., May M., Suyee K., Xiaowei L., and myself. 

The topic of the project is to analyse TED Talk transcripts and achieve automated tag extraction, transcript summarization, and related talk recommendation with a given new transcript and title.

The TED talk dataset is available on <a href='https://www.kaggle.com/rounakbanik/ted-talks'>Kaggle</a>, with information and transcripts of talks uploaded to the official TED.com until September 21st, 2017. In total, there is the information of 2550 talks with 2464 transcripts.

You may wish to read our <a href='https://medium.com/@haodi.qi/ted-talk-tag-generator-and-summarizer-27ec831a7caa'>Medium article</a> to learn more about our system.

<hr>
<h2> System Design</h2> 

![System Design](data/output/system-design.png?raw=True)

## Technology employed
<table>
  <tr><th>Step</th><th>Main technology</th></tr>
  <tr><td>Transcript Preprocessing</td><td>Spacy</td></tr>
  <tr><td>Topic Modelling</td><td>Gensim, Scikit-Learn, LDA Mallet</td></tr>
  <tr><td>TF-IDF Metric Computation</td><td>Scikit-learn</td></tr>
  <tr><td>Tag Generation</td><td>WordNet, Networkx</td></tr>
  <tr><td>Summarization</td><td>TextRank</td></tr>
  <tr><td>Related Talks Recommendation</td><td>Scikit-learn</td></tr>
</table>
<hr>
<h2> GUI </h2> 
Besides implementing the system backend, we also created a simple GUI for easy use of our system. 

The instructions are as the following:
  1. Navigate to the project directory after downloading and unzipping/cloning
  2. ```python SummarySystem``` in Command Prompt
  3. Fill in the ```Title``` and ```Input your   Text``` fields
  4. Click ```Generate``` button

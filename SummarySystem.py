'''
    This initiates the summary page
'''
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from functions.Text import Text

from functions.tfidf_vectorizer_functions import preprocessor, tokenizer
from functions import tag_generation, summarizer,recommendation
from functions.preprocessing import preprocessing

qtCreatorFile = "data/gui/TextGUI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class SummarySystem(QMainWindow, Ui_MainWindow):
    def __init__(self):        
        super().__init__()
        self.setupUi(self)
        self.Button.clicked.connect(self.analyze)
       
    def analyze(self):
        
        input_title = self.InputTitle.text()
        input_text = self.InputText.text()
        input_text_tokens = preprocessing(input_text)
        input_title_tokens = preprocessing(input_title)
        
        # tag generation
        topicKeywords, mainTopicKeywords, mainTopicConcepts = tag_generation.tag_generation(input_text_tokens)
        tag_string = ''
        for idx, concept_words in mainTopicConcepts.items():
            tag_string += "Concept {}:\n".format(idx+1) 
            tag_string += ", ".join(concept_words) + "\n\n"
        mainTopicKeywords_str = "Topic keywords: "+', '.join(mainTopicKeywords)
        tag_string = mainTopicKeywords_str+ "\n" + tag_string.strip()
        
        # related talks recommendation
        recomm_titles = recommendation.generate_recommendation(input_text_tokens)
        recomm_titles_str = '\n'.join(recomm_titles)
        
        summary_sents = summarizer.generate_summary(input_text, input_text_tokens, input_title_tokens, topicKeywords)
        summary_string = " ".join([s[0].strip() for s in summary_sents])

        self.SummaryOutput.setText(summary_string)
        self.Tagoutput.setText(tag_string)
        self.output2.setText(recomm_titles_str)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    bc = SummarySystem()
    bc.show()
    sys.exit(app.exec_())


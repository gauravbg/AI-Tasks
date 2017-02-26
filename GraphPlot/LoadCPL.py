'''
Created on Dec 3, 2016

@author: Gaurav BG
'''
from nltk.stem.porter import PorterStemmer
from sklearn import metrics
from sklearn.datasets import load_files
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC


newsgroups_test = load_files('C:\\Users\\gaura\\Desktop\\Course Material\\Artificial Intelligence - 537\\Assignments\\HW3\\Selected 20NewsGroup\\Test', encoding='latin-1')

stemmer = PorterStemmer()
analyzer = TfidfVectorizer().build_analyzer()

def stemmed_words(doc):
    return (stemmer.stem(w) for w in analyzer(doc))

classifier = joblib.load("gauravConfig.pkl")
prediction = classifier.predict(newsgroups_test.data)
print("F1-Score : ", metrics.f1_score(newsgroups_test.target, prediction, average='macro'))
print("Recall-Score : ", metrics.recall_score(newsgroups_test.target, prediction, average='macro'))
print("Precision-Score : ", metrics.precision_score(newsgroups_test.target, prediction, average='macro'))

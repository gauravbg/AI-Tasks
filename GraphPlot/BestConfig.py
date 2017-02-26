'''
Created on Dec 2, 2016

@author: Gaurav BG
'''
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from astropy.constants.si import alpha
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib 

newsgroups_train = load_files('C:\\Users\\gaura\\Desktop\\Course Material\\Artificial Intelligence - 537\\Assignments\\HW3\\Selected 20NewsGroup\\Training', encoding='latin-1')
newsgroups_test = load_files('C:\\Users\\gaura\\Desktop\\Course Material\\Artificial Intelligence - 537\\Assignments\\HW3\\Selected 20NewsGroup\\Test', encoding='latin-1')

stemmer = PorterStemmer()
analyzer = TfidfVectorizer().build_analyzer()

def stemmed_words(doc):
    return (stemmer.stem(w) for w in analyzer(doc))


# --------------------------------------------------------------------------------
# Config 1
# vectorizer = CountVectorizer(lowercase=True)
# vectors = vectorizer.fit_transform(newsgroups_train.data)
# vectors_test = vectorizer.transform(newsgroups_test.data)
# classifier = MultinomialNB()
# classifier.fit(vectors, newsgroups_train.target)
# prediction = classifier.predict(vectors_test)




# --------------------------------------------------------------------------------
# Config 2
# vectorizer = TfidfVectorizer(analyzer=stemmed_words, lowercase=True)
# vectors = vectorizer.fit_transform(newsgroups_train.data)
# vectors_test = vectorizer.transform(newsgroups_test.data)
# classifier = MultinomialNB()
# classifier.fit(vectors, newsgroups_train.target)
# prediction = classifier.predict(vectors_test)


# --------------------------------------------------------------------------------
# Config 3
# vectorizer = TfidfVectorizer(analyzer=stemmed_words, stop_words='english')
# vectors = vectorizer.fit_transform(newsgroups_train.data)
# vectors_test = vectorizer.transform(newsgroups_test.data)
# classifier = LogisticRegression()
# classifier.fit(vectors, newsgroups_train.target)
# prediction = classifier.predict(vectors_test)



# --------------------------------------------------------------------------------
# Config 4
# vectorizer = TfidfVectorizer(analyzer=stemmed_words, lowercase=True, stop_words='english')
# vectors = vectorizer.fit_transform(newsgroups_train.data)
# vectors_test = vectorizer.transform(newsgroups_test.data)
# classifier = LogisticRegression(max_iter=1000)
# classifier.fit(vectors, newsgroups_train.target)
# prediction = classifier.predict(vectors_test)



# --------------------------------------------------------------------------------
# Config 5
# vectorizer = CountVectorizer(analyzer=stemmed_words, lowercase=True, stop_words='english')
# vectors = vectorizer.fit_transform(newsgroups_train.data)
# vectors_test = vectorizer.transform(newsgroups_test.data)
# classifier = LinearSVC()
# classifier.fit(vectors, newsgroups_train.target)
# prediction = classifier.predict(vectors_test)



# --------------------------------------------------------------------------------
# # Config 6
# vectorizer = TfidfVectorizer(analyzer=stemmed_words, lowercase=True, stop_words='english', sublinear_tf=True)
# vectors = vectorizer.fit_transform(newsgroups_train.data)
# vectors_test = vectorizer.transform(newsgroups_test.data)
# classifier = LinearSVC()
# classifier.fit(vectors, newsgroups_train.target)
# prediction = classifier.predict(vectors_test)



# --------------------------------------------------------------------------------
# Config 7 - Best Configuration
vectorizer = TfidfVectorizer(analyzer=stemmed_words, lowercase=True, stop_words='english', sublinear_tf=True)
vectors = vectorizer.fit_transform(newsgroups_train.data)
select_best = SelectKBest(chi2, k=13000)
X_best = select_best.fit_transform(vectors, newsgroups_train.target)
vectors_test = vectorizer.transform(newsgroups_test.data)
X_best_new = select_best.transform(vectors_test)
classifier = LinearSVC()
classifier.fit(X_best, newsgroups_train.target)
prediction = classifier.predict(X_best_new)

# configChoices = [('vectorizer', TfidfVectorizer(analyzer=stemmed_words, lowercase=True, stop_words='english', sublinear_tf=True)), 
#                  ('select_best', SelectKBest(chi2, k=13000)), #approximately half the features
#                  ('classifier', LinearSVC())]
# pipeline = Pipeline(configChoices)
# pipeline.fit(newsgroups_train.data, newsgroups_train.target)
# prediction = pipeline.predict(newsgroups_test.data)
# joblib.dump(pipeline, "gauravConfig.pkl")

# --------------------------------------------------------------------------------
# Config 8
# vectorizer = TfidfVectorizer(analyzer=stemmed_words, lowercase=True, stop_words='english', sublinear_tf=True)
# vectors = vectorizer.fit_transform(newsgroups_train.data)
# select_best = SelectKBest(chi2, k=13000)
# X_best = select_best.fit_transform(vectors, newsgroups_train.target)
# vectors_test = vectorizer.transform(newsgroups_test.data)
# X_best_new = select_best.transform(vectors_test)
# classifier = RandomForestClassifier(n_estimators=10, max_depth=None)
# classifier.fit(X_best, newsgroups_train.target)
# prediction = classifier.predict(X_best_new)


print("F1-Score : ", metrics.f1_score(newsgroups_test.target, prediction, average='macro'))
print("Recall-Score : ", metrics.recall_score(newsgroups_test.target, prediction, average='macro'))
print("Precision-Score : ", metrics.precision_score(newsgroups_test.target, prediction, average='macro'))

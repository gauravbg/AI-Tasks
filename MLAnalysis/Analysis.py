'''
Created on Dec 1, 2016

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

categories = ['rec.sport.hockey', 'sci.med', 'soc.religion.christian', 'talk.religion.misc']
#newsgroups_train = fetch_20newsgroups(subset='train', remove='header', categories=categories)
#newsgroups_test = fetch_20newsgroups(subset='test', categories=categories)

newsgroups_train = load_files('C:\\Users\\gaura\\Desktop\\Course Material\\Artificial Intelligence - 537\\Assignments\\HW3\\Selected 20NewsGroup\\Training', encoding='latin-1')
newsgroups_test = load_files('C:\\Users\\gaura\\Desktop\\Course Material\\Artificial Intelligence - 537\\Assignments\\HW3\\Selected 20NewsGroup\\Test', encoding='latin-1')

# Unigram representation
# vectorizer = CountVectorizer()

# Bigram representation
#vectorizer = CountVectorizer(ngram_range=(2, 2), token_pattern=r'\b\w+\b' , min_df=1)
#analyze = vectorizer.build_analyzer()
#print type(analyze)

#TF-IDF
#vectorizer = TfidfVectorizer(use_idf=False)

#MBC
#vectorizer = CountVectorizer(stop_words=None)

#Random Forest - Unigram
uni_vectorizer = CountVectorizer()
uni_vectors = uni_vectorizer.fit_transform(newsgroups_train.data)
uni_vectors_test = uni_vectorizer.transform(newsgroups_test.data)
clf = RandomForestClassifier()
clf.fit(uni_vectors, newsgroups_train.target)
pred = clf.predict(uni_vectors_test)
print("Random Forest (Unigram):")
print("F1-Score : ", metrics.f1_score(newsgroups_test.target, pred, average='macro'))
print("Recall-Score : ", metrics.recall_score(newsgroups_test.target, pred, average='macro'))
print("Precision-Score : ", metrics.precision_score(newsgroups_test.target, pred, average='macro'))

#Random Forest - Bigram
bi_vectorizer = CountVectorizer(ngram_range=(2, 2), token_pattern=r'\b\w+\b' , min_df=1)
bi_vectors = bi_vectorizer.fit_transform(newsgroups_train.data)
bi_vectors_test = bi_vectorizer.transform(newsgroups_test.data)
clf.fit(bi_vectors, newsgroups_train.target)
pred = clf.predict(bi_vectors_test)
print("Random Forest (Bigram):")
print("F1-Score : ", metrics.f1_score(newsgroups_test.target, pred, average='macro'))
print("Recall-Score : ", metrics.recall_score(newsgroups_test.target, pred, average='macro'))
print("Precision-Score : ", metrics.precision_score(newsgroups_test.target, pred, average='macro'))

# ------------------------------------------------------------------------------------------------------------
print("-----------------------------------------------------------------")
#Naive Bayes - Unigram
NB_clf = MultinomialNB(alpha=.01)
NB_clf.fit(uni_vectors, newsgroups_train.target)
pred = NB_clf.predict(uni_vectors_test)
print("Naive Bayes (Unigram):")
print("F1-Score : ", metrics.f1_score(newsgroups_test.target, pred, average='macro'))
print("Recall-Score : ", metrics.recall_score(newsgroups_test.target, pred, average='macro'))
print("Precision-Score : ", metrics.precision_score(newsgroups_test.target, pred, average='macro'))

#Naive Bayes - Bigram
NB_clf.fit(bi_vectors, newsgroups_train.target)
pred = NB_clf.predict(bi_vectors_test)
print("Naive Bayes (Bigram):")
print("F1-Score : ", metrics.f1_score(newsgroups_test.target, pred, average='macro'))
print("Recall-Score : ", metrics.recall_score(newsgroups_test.target, pred, average='macro'))
print("Precision-Score : ", metrics.precision_score(newsgroups_test.target, pred, average='macro'))

# ------------------------------------------------------------------------------------------------------------
print("-----------------------------------------------------------------")
#Logistic regression - Unigram
clf = LogisticRegression()
clf.fit(uni_vectors, newsgroups_train.target)
pred = clf.predict(uni_vectors_test)
print("Logistic regression (Unigram):")
print("F1-Score : ", metrics.f1_score(newsgroups_test.target, pred, average='macro'))
print("Recall-Score : ", metrics.recall_score(newsgroups_test.target, pred, average='macro'))
print("Precision-Score : ", metrics.precision_score(newsgroups_test.target, pred, average='macro'))

#Logistic regression - Bigram
clf.fit(bi_vectors, newsgroups_train.target)
pred = clf.predict(bi_vectors_test)
print("Logistic regression (Bigram):")
print("F1-Score : ", metrics.f1_score(newsgroups_test.target, pred, average='macro'))
print("Recall-Score : ", metrics.recall_score(newsgroups_test.target, pred, average='macro'))
print("Precision-Score : ", metrics.precision_score(newsgroups_test.target, pred, average='macro'))


# ------------------------------------------------------------------------------------------------------------
print("-----------------------------------------------------------------")
#SVC - Unigram
clf = LinearSVC()
clf.fit(uni_vectors, newsgroups_train.target)
pred = clf.predict(uni_vectors_test)
print("SVC (Unigram):")
print("F1-Score : ", metrics.f1_score(newsgroups_test.target, pred, average='macro'))
print("Recall-Score : ", metrics.recall_score(newsgroups_test.target, pred, average='macro'))
print("Precision-Score : ", metrics.precision_score(newsgroups_test.target, pred, average='macro'))

#SVC - Bigram
clf.fit(bi_vectors, newsgroups_train.target)
pred = clf.predict(bi_vectors_test)
print("SVC (Bigram):")
print("F1-Score : ", metrics.f1_score(newsgroups_test.target, pred, average='macro'))
print("Recall-Score : ", metrics.recall_score(newsgroups_test.target, pred, average='macro'))
print("Precision-Score : ", metrics.precision_score(newsgroups_test.target, pred, average='macro'))


# print(metrics.classification_report(newsgroups_test.target, clf.predict(vectors_test)))
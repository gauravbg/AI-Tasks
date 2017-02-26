from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_files
import matplotlib.pyplot as plt


def split_test_classifier(clf, data, testData, target, test_target):
    results = []
    i_ = []
    vectorizer = CountVectorizer()
    print('=================')
    
    for i in range(10, 101, 10):
        print(i)
        i_.append(i)
        if i==100:
            i=99
        percent = i/100.0

        # split
        data_train, data_test, target_train, target_test = train_test_split(data, target, train_size=percent)
        vectors = vectorizer.fit_transform(data_train)
        
        # learn the model
        clf.fit(vectors, target_train)
        test_vectors = vectorizer.transform(testData)

        # predict
        y_predicted = clf.predict(test_vectors)
        f1_score = metrics.f1_score(test_target, y_predicted, average='macro')
        results.append(f1_score)

    return i_, results


def plot_results(i, results_list, labels_list):
    colors_list = ['red', 'blue', 'black', 'green', 'cyan', 'yellow']

    if not len(results_list) == len(labels_list):
        print('un equal len in results and labels')
        raise Exception

    
    for (result, label, color) in zip(results_list, labels_list, colors_list):
        plt.plot(i, result, color = color, lw=2.0, label=label)
    plt.legend(loc=4)
    plt.show()


categories = ['rec.sport.hockey', 'sci.med', 'soc.religion.christian', 'talk.religion.misc']

newsgroups_train = load_files('C:\\Users\\gaura\\Desktop\\Course Material\\Artificial Intelligence - 537\\Assignments\\HW3\\Selected 20NewsGroup\\Training', encoding='latin-1')
newsgroups_test = load_files('C:\\Users\\gaura\\Desktop\\Course Material\\Artificial Intelligence - 537\\Assignments\\HW3\\Selected 20NewsGroup\\Test', encoding='latin-1')

clf_nb = MultinomialNB(alpha=.01)
clf_lr = LogisticRegression()
clf_svc = LinearSVC()
clf_rf = RandomForestClassifier()

i, NB_results = split_test_classifier(clf_nb, newsgroups_train.data, newsgroups_test.data, newsgroups_train.target, newsgroups_test.target)

i, LR_results = split_test_classifier(clf_lr, newsgroups_train.data, newsgroups_test.data, newsgroups_train.target, newsgroups_test.target)

i, SVM_results = split_test_classifier(clf_svc, newsgroups_train.data, newsgroups_test.data, newsgroups_train.target, newsgroups_test.target)

i, RF_results = split_test_classifier(clf_rf, newsgroups_train.data, newsgroups_test.data, newsgroups_train.target, newsgroups_test.target)
    
# plot
plot_results(i, [NB_results, LR_results, SVM_results, RF_results], ['NB', 'LR', 'SVM', 'RF'])


from glob import glob

import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder


txt_files = glob("dataset/bbc/*/*.txt")

data = []
targets = []

for txt_file in txt_files:
    category = txt_file.split("/")[-2]
    with open(txt_file) as f:
        text = f.read()
    data.append(text)
    targets.append(category)

le = LabelEncoder()

encoded_targets = le.fit_transform(targets)

joblib.dump(le, "label_encoder.pkl")

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(data)
joblib.dump(count_vect, "count_vect.pkl")


print(X_train_counts.shape)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
joblib.dump(tfidf_transformer, "tfidf_transformer.pkl")

print(X_train_tfidf.shape)

X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, encoded_targets, test_size=0.33)

clf = MultinomialNB().fit(X_train, y_train)
joblib.dump(clf, "clf.pkl")
y_predicted = clf.predict(X_test)

print(f1_score(y_test, y_predicted, average='weighted'))

print(le.classes_)

# with open("x.txt") as f:
#     test_text = f.read()
#
# out_count = count_vect.transform([test_text])
# out = tfidf_transformer.transform(out_count)
#
# print(clf.predict(out))

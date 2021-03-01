import pandas as pd
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import plot_confusion_matrix


def iris_type(row):
    if row['Target'] == 0:
        return "Iris-setosa"
    elif row['Target'] == 1:
        return "Iris-versicolor"
    elif row['Target'] == 2:
        return "Iris-virginica"


iris = load_iris()
df = pd.DataFrame(iris.data)
df.columns = ['Sepal_Length',
              'Sepal_Width',
              'Petal_Length',
              'Petal_Width']
df['Target'] = iris.target
df['Iris_Type'] = df.apply(iris_type, axis=1)

X = df[df.columns[0:4]].values
y = df[df.columns[5]].values

X_train, X_test, y_train, y_test = model_selection.train_test_split(
    X, y, test_size=0.2)

knn_clf = KNeighborsClassifier(n_neighbors=9)
knn_clf.fit(X_train, y_train)
knn_predictions = knn_clf.predict(X_test)
print(accuracy_score(y_test, knn_predictions))

confusion_matrix(y_test, knn_predictions)
print(confusion_matrix(y_test, knn_predictions))

matrix = plot_confusion_matrix(knn_clf, X_test, y_test, cmap=plt.cm.Reds)
matrix.ax_.set_title('Confusion Matrix', color='white')
plt.xlabel('Predicted Label', color='white')
plt.ylabel('Predicted Label', color='white')
plt.gcf().axes[0].tick_params(colors='white')
plt.gcf().axes[1].tick_params(colors='white')
plt.gcf().set_size_inches(10, 6)
plt.show()

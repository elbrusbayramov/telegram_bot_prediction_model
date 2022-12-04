import pandas as pd
from sklearn import tree

titanic_data = pd.read_csv('data.csv')

X = titanic_data.drop(['PassengerId', 'Ticket', 'Name', 'Survived'], axis=1)
# print(X.head(7))
y = titanic_data.Survived
# print(y)

X = pd.get_dummies(X)
# print(X.head(7))

clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=3)

clf.fit(X, y)
print(clf.score(X, y))

sample = {
    'Pclass':1,
    'Age': 45.0,
    'Parch': 1,
    'Fare': 7.25,
    'Sex_female': 0,
    'Sex_male': 1
}


def predict_me(value=sample):
    my_data = pd.DataFrame(sample,
                           index=[0],
                           columns=['Pclass', 'Age', 'Parch', 'Fare', 'Sex_female', 'Sex_male'])

    my_result = clf.predict(my_data)
    return 'Survived' if my_result[0] == 1 else 'Died'


def main():
    print(predict_me())


if __name__ == '__main__':
    main()

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Get the data
data = load_iris()
X, y = data.data, data.target

# 2. Split it (80% for training, 20% for testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Pick a "Brain" (Model) and Train it
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 4. See how smart it is
predictions = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions) * 100}%")
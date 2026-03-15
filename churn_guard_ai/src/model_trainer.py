from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os


def train_and_save_model(df, target_col='churn'):
    """
    Trains a Random Forest Classifier and saves the .pkl file.
    """
    X = df.drop(['customer_id', target_col], axis=1)
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Using Random Forest as it handles non-linear relationships well
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf.fit(X_train, y_train)

    # Save Model
    model_path = os.path.join(os.path.dirname(__file__), '../models/churn_classifier.pkl')
    joblib.dump(clf, model_path)

    accuracy = clf.score(X_test, y_test)
    return accuracy
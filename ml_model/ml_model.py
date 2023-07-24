from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class ML_Model:
    def __init__(self, dataset):
        self.train_data = dataset.train
        self.train_labels = dataset.labels_train
        self.val_data = dataset.validation
        self.val_labels = dataset.labels_validation
        self.test_data = dataset.test
        self.test_labels = dataset.labels_test
        self.classifier = self.train()

    def train(self):
        classifier = RandomForestClassifier(n_estimators=100, n_jobs=5,
                                            criterion="log_loss",
                                            max_features="log2")
        classifier.fit(self.train_data, self.train_labels)
        self.importances = classifier.feature_importances_
        return classifier

    def predict(self, instance):
        prediction = self.classifier.predict(instance)
        return prediction

    def test(self):
        predictions = self.classifier.predict(self.test_data)
        accuracy = accuracy_score(self.test_labels, predictions)
        print("Accuracy:", accuracy)
        print("Classification report:\n", classification_report(self.test_labels, predictions))

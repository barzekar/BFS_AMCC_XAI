from anchor import utils


class DatasetLoader:
    def __init__(self, data_path, target_idx, delimiter=',', feature_names=None):
        self.data_path = data_path
        self.target_idx = target_idx
        self.delimiter = delimiter
        self.feature_names = feature_names
        self.dataset = self.load_csv_dataset()

    def load_csv_dataset(self):
        dataset = utils.load_csv_dataset(self.data_path, self.target_idx,
                                         self.delimiter, self.feature_names,
                                         discretize=True,
                                         test_size=.2)
        return dataset


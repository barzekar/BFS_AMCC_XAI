from collections import deque
import re


class BFSAMCCModifier:
    def __init__(self, dataset_loader, predictor, explainer, transition_rules=None):
        self.dataset_loader = dataset_loader
        self.predictor = predictor
        self.explainer = explainer
        self.transition_rules = transition_rules

    @staticmethod
    def extract_features(anchor):
        features = re.findall(r'([A-Za-z_]+)(?: =| <=| >=| < | > )', anchor)
        return features

    def bfs_amcc(self, instance, original_prediction, categorical_names, specific_indices=None,
                 ignore_indices=None):
        if ignore_indices is None:
            ignore_indices = []
        queue = deque([([], instance)])
        best_modified_instance = None

        while queue:
            changed_indices, current_instance = queue.popleft()
            current_prediction = self.predictor.classifier.predict(current_instance.reshape(1, -1))[0]

            if current_prediction != original_prediction:
                best_modified_instance = current_instance
                break

            if specific_indices is None:
                indices_to_modify = [i for i in categorical_names.keys() if i not in ignore_indices]
            else:
                indices_to_modify = [i for i in specific_indices if i not in ignore_indices]

            for index in indices_to_modify:
                if index not in changed_indices and index in categorical_names:
                    for value in range(len(categorical_names[index])):
                        if value != current_instance[index]:
                            if self.transition_rules and index in self.transition_rules:
                                if not self.transition_rules[index](current_instance[index], value):
                                    continue
                            modified_instance = current_instance.copy()
                            modified_instance[index] = value
                            queue.append((changed_indices + [index], modified_instance))

        return best_modified_instance

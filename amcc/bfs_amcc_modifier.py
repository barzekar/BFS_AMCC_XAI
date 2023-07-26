from collections import deque
import re


class BFSAMCCModifier:
    """
        A class that uses Breadth-First Search (BFS) to find counterfactual instances based on the concept of
        "Achievable Minimally Contrastive Counterfactual Explanations."

        Attributes:
        ----------
        dataset_loader : object
            An object responsible for loading and managing the dataset.
        predictor : object
            An object that provides classification predictions. It should have a 'classifier.predict' method.
        explainer : object
            An instance from the "Anchors: High-Precision Model-Agnostic Explanations" specifically designed for providing explanations on tabular data.
        transition_rules : dict, optional
            A dictionary where keys are feature indices and values are functions that accept two parameters:
            the current feature value and the new value. The function should return a boolean indicating
            whether the transition between these values is allowed.

        Methods:
        -------
        extract_features(anchor: str) -> list
            Extracts and returns feature names from a given anchor string.

        bfs_amcc(instance: array_like, original_prediction: int, categorical_names: dict,
                 specific_indices: list=None, ignore_indices: list=None) -> array_like
            Applies BFS to find a counterfactual instance that leads to a different classification than the original.
            Returns the modified instance.
    """

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

        """
        Uses BFS to find a modified instance (based on specific criteria) that results in a different
        prediction than the original prediction.

        Parameters:
        ----------
        instance : array_like
            The original instance for which a counterfactual is sought.
        original_prediction : int
            The original prediction/classification of the instance.
        categorical_names : dict
            A dictionary where keys are feature indices and values are the possible categorical values
            for that feature.
        specific_indices : list, optional
            A list of feature indices to be specifically considered for modification. If None, all features
            except those in `ignore_indices` are considered.
        ignore_indices : list, optional
            A list of feature indices that should not be modified.

        Returns:
        -------
        array_like
            The counterfactual instance if found, otherwise None.
        """

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

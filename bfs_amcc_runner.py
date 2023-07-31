from ml_model.dataset_loader import DatasetLoader
from ml_model.ml_model import ML_Model
from amcc.bfs_amcc_modifier import BFSAMCCModifier
from utils.timing import Timeout
import numpy as np
import pandas as pd
from anchor import anchor_tabular
from logger import Logger

log = Logger()


def parse_transition_rules(transition_rules, feature_names):
    """
    Parses transition rules from a given dictionary and maps feature names to their corresponding indices.

    Parameters:
    ----------
    transition_rules : dict
        Dictionary containing transition rules for specific features.
    feature_names : list
        List of feature names in the dataset.

    Returns:
    -------
    dict
        A dictionary where keys are feature indices and values are lambda functions representing
        the respective transition rules.
    """
    condition_map = {
        "old >= new": lambda old, new: old >= new,
        "old <= new": lambda old, new: old <= new,
        "old == new": lambda old, new: old == new,
        "old != new": lambda old, new: old != new,
        "old > new": lambda old, new: old > new,
        "old < new": lambda old, new: old < new
    }

    rules = {}
    for feature, rule in transition_rules.items():
        if rule in condition_map:
            idx = feature_names.index(feature)
            rules[idx] = condition_map[rule]

    return rules


# @time_it
def run_bfs_amcc(config):
    """
        Runs the Breadth-First Search process based on "Achievable Minimally Contrastive Counterfactual Explanations"
        on instances labeled suboptimal. The goal is to modify these instances in a way that changes their prediction
        from a negative (BAD) classification to a positive (GOOD) one.

        Parameters:
        ----------
        config : dict
            Configuration dictionary containing parameters and paths related to the dataset,
            machine learning model, and the counterfactual explanation process.

        Returns:
        -------
        dict
            A dictionary containing:
            - 'metrics': A dictionary with results of the process (success, failure, time taken, etc.).
            - 'messages': A list of log messages generated during the process.
    """

    dataset_loader = DatasetLoader(config["data_path"], config["target_idx"], delimiter=config["delimiter"],
                                   feature_names=config["feature_names"])
    predictor = ML_Model(dataset_loader.dataset)
    explainer = anchor_tabular.AnchorTabularExplainer(
        dataset_loader.dataset.class_names,
        dataset_loader.dataset.feature_names,
        dataset_loader.dataset.train,
        dataset_loader.dataset.categorical_names)

    # If transition_rules parameter is None, try to parse it from the config
    feature_names = config["feature_names"]
    if "transition_rules" in config:
        transition_rules_str = config["transition_rules"]
        transition_rules = parse_transition_rules(transition_rules_str, feature_names)
    else:
        transition_rules = None
    modifier = BFSAMCCModifier(dataset_loader, predictor, explainer, transition_rules)

    categorical_names = dataset_loader.dataset.categorical_names

    ignore_indices = config["ignore_indices"]

    metrics = {
        "success": [],
        "failure": [],
        "time": [],
        "modified_instances": [],
        "changes": []
    }
    messages = []  # For collecting logs to send to frontend

    suboptimal_indices = np.where(dataset_loader.dataset.labels_test == 1)[0]

    for instance_index in suboptimal_indices:
        original_instance = dataset_loader.dataset.test[instance_index]
        original_prediction = predictor.classifier.predict(original_instance.reshape(1, -1))[0]

        if dataset_loader.dataset.labels_test[instance_index] == original_prediction == 1:
            exp = explainer.explain_instance(original_instance, predictor.classifier.predict,
                                             threshold=config["thresh_prob"])
            feature_indices = BFSAMCCModifier.extract_features(" AND ".join(exp.names()))
            specific_indices = [feature_names.index(feature) for feature in feature_indices if
                                feature_names.index(feature) not in ignore_indices]

            timeout_checker = Timeout(5)
            with timeout_checker:
                try:
                    modified_instance = modifier.bfs_amcc(original_instance, original_prediction,
                                                          categorical_names, specific_indices, ignore_indices)
                except TimeoutError as e:
                    print(e)
                    continue
            elapsed = timeout_checker.elapsed_time
            if elapsed is not None:
                metrics["time"].append(elapsed)

            if modified_instance is not None:
                metrics["success"].append(1)
                metrics["failure"].append(0)
                success_message = "Successful modification."
                log.log_info(success_message)
                messages.append(success_message)
                metrics["modified_instances"].append(modified_instance)
                changes_for_instance = {feature_names[i]: (original_instance[i], modified_instance[i])
                                        for i in np.where(original_instance != modified_instance)[0]}
                metrics["changes"].append(changes_for_instance)
                changes_message = f"Modified Instances: {changes_for_instance}"
                log.log_info(changes_message)
                messages.append(changes_message)
            else:
                metrics["success"].append(0)
                metrics["failure"].append(1)
                failure_message = "Failed modification."
                log.log_info(failure_message)
                messages.append(failure_message)
                metrics["modified_instances"].append(None)
                metrics["changes"].append(None)

    metrics["modified_instances"] = [instance.tolist() if instance is not None else None for instance in
                                     metrics["modified_instances"]]

    results_df = pd.DataFrame(metrics)
    results_df.to_csv(config["output_file"], index=False)

    return {"metrics": metrics, "messages": messages}


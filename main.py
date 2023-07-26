"""
Script to execute the Breadth-First Search Achievable Minimally Contrastive Counterfactual (BFS_AMCC) Algorithm.

This script loads the configuration from a JSON file, adjusts the data path, runs the BFS_AMCC process, and prints the obtained metrics.

Functions:
----------
load_config() -> dict:
    Load the configuration parameters for the BFS_AMCC process from a JSON file.

main():
    Main driver function. Loads configuration from a JSON file, modifies data path, runs BFS_AMCC, and prints the results.

"""

import json
from bfs_amcc_runner import run_bfs_amcc

def load_config():
    """
    Load the configuration parameters for the BFS_AMCC process from a JSON file.

    Returns:
    -------
    dict
        Dictionary containing configuration parameters loaded from the JSON file.
    """
    with open("config/bfs_amcc_config.json", "r") as file:
        return json.load(file)


def main():
    """
    Main driver function to execute the BFS_AMCC process.

    Configuration is loaded from a JSON file, the data path is then adjusted,
    and the BFS_AMCC process is run. The resulting metrics are printed.
    """
    config = load_config()
    config["data_path"] = "data/" + config["data_path"]
    metrics = run_bfs_amcc(config)
    print(metrics)


if __name__ == "__main__":
    main()

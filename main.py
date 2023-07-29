import json
from bfs_amcc_runner import run_bfs_amcc


def load_config():
    with open("config/bfs_amcc_config.json", "r") as file:
        return json.load(file)


def main():
    config = load_config()
    metrics = run_bfs_amcc(config)
    print(metrics)


if __name__ == "__main__":
    main()

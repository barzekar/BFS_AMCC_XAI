import os
import json
import logging
import multiprocessing
from flask import Flask, render_template, request, jsonify

from logger import Logger
from bfs_amcc_runner import run_bfs_amcc

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

MAX_PROCESSING_TIME = 240  # 4 minutes
log = Logger()


@app.route('/', methods=['GET'])
def index():
    try:
        config = load_config('config/bfs_amcc_config.json')
        data = {
            "ignore_indices": config["ignore_indices"],
            "data_path": config["data_path"],
            "thresh_prob": config["thresh_prob"],
            "output_file": config["output_file"]
        }
        return render_template('index.html', data=data)
    except Exception as e:
        app.logger.error(f"Error loading index: {e}", exc_info=True)
        return "Error loading the page", 500


@app.route('/log', methods=['GET'])
def get_logs():
    try:
        logs = log.collect()
        return jsonify(logs)
    except Exception as e:
        app.logger.error(f"Error fetching logs: {e}", exc_info=True)
        return "Error fetching logs", 500


def worker(config, return_dict):
    try:
        result = run_bfs_amcc(config)
        return_dict['result'] = result
    except Exception as e:
        app.logger.error(f"Error processing BFS-AMCC: {e}", exc_info=True)
        return_dict['error'] = str(e)


@app.route('/run', methods=['POST'])
def run_amcc():
    try:
        body = request.form
        config = validate_and_extract_config(body)

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        p = multiprocessing.Process(target=worker, args=(config, return_dict))
        p.start()
        p.join(MAX_PROCESSING_TIME)

        if p.is_alive():
            p.terminate()
            p.join()
            app.logger.warning("Processing timed out!")
            return jsonify(status='fail',
                           message="Processing is taking longer than expected. Please try again later.")

        if 'error' in return_dict:
            return jsonify(status='fail', message=return_dict['error'])

        results = return_dict.get('result', None)

        if results:
            return jsonify(status='success', messages=results["messages"], metrics=results["metrics"])
        else:
            return jsonify(status='fail', message="Processing failed!")

    except ValueError as ve:
        return jsonify(status='fail', message=str(ve))
    except Exception as e:
        app.logger.error(f"Error in run_amcc route: {e}", exc_info=True)
        return jsonify(status='fail', message="An unexpected error occurred.")


def validate_and_extract_config(body):
    config = load_config('config/bfs_amcc_config.json')

    # Validate data path
    data_path = body.get("data_path", "").strip()
    if not os.path.exists(data_path):
        raise ValueError("Provided data path does not exist.")
    config["data_path"] = data_path

    # Validate output path
    output_file = body.get("output_file", "").strip()
    if not output_file:
        raise ValueError("Output path cannot be empty.")
    config["output_file"] = output_file

    # Extract and validate threshold probability
    config["thresh_prob"] = extract_float(body, "thresh_prob")

    # Extract and validate ignore indices
    config["ignore_indices"] = extract_int_list(body, "ignore_indices")

    return config


def extract_float(body, key):
    try:
        value = float(body.get(key, "").strip())
        if 0 <= value <= 1:
            return value
        else:
            raise ValueError(f"{key} must be between 0 and 1.")
    except ValueError:
        raise ValueError(f"Invalid value provided for {key}")


def extract_int_list(body, key):
    try:
        indices_str = body.get(key, "").strip().split(',')
        return [int(idx.strip()) for idx in indices_str if idx.strip()]
    except ValueError:
        raise ValueError(f"{key} must be a comma-separated list of integers")


def load_config(config_path):
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise ValueError(f"Failed to load the config file. Reason: {str(e)}")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

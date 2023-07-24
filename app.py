import json
import logging
import multiprocessing
from flask import Flask, render_template, request, jsonify

# Assuming you have these two modules
from logger import Logger
from bfs_amcc_runner import run_bfs_amcc

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

MAX_PROCESSING_TIME = 240  # 4 minutes
log = Logger()


@app.route('/', methods=['GET'])
def index():
    config = load_config('config/bfs_amcc_config.json')
    data = {
        "ignore_indices": config["ignore_indices"],
        "data_path": str(config["data_path"]),
        "thresh_prob": config["thresh_prob"],
        "output_file": config["output_file"]
    }
    return render_template('index.html', data=data)



@app.route('/log', methods=['GET'])
def get_logs():
    logs = log.collect()
    return jsonify(logs)


def worker(config, return_dict):
    try:
        result = run_bfs_amcc(config)
        return_dict['result'] = result
    except Exception as e:
        app.logger.error(f"Error processing BFS AMCC: {e}", exc_info=True)
        return_dict['error'] = str(e)


@app.route('/run', methods=['POST'])
def run_amcc():
    log.log_info("Running request")

    try:
        body = request.form
        config = load_config('config/bfs_amcc_config.json')

        # Convert the comma-separated indices from the frontend to a list of integers.
        config["ignore_indices"] = [int(idx) for idx in body["ignore_indices"].strip().strip(',').split(',')]

        config["data_path"] = body["data_path"].strip()
        config["output_file"] = body["output_file"].strip()
        config["thresh_prob"] = float(body["thresh_prob"].strip())

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        p = multiprocessing.Process(target=worker, args=(config, return_dict))
        p.start()
        p.join(MAX_PROCESSING_TIME)

        if p.is_alive():
            p.terminate()
            p.join()
            app.logger.warning("BFS processing timed out!")
            return jsonify(status='fail',
                           message="BFS processing is taking longer than expected. Please try again later.")

        if 'error' in return_dict:
            return jsonify(status='fail', message=return_dict['error'])

        results = return_dict.get('result', None)

        if results:
            return jsonify(status='success', messages=results["messages"], metrics=results["metrics"])
        else:
            return jsonify(status='fail', message="BFS processing failed!")

    except Exception as e:
        app.logger.error(f"Error in run_amcc route: {e}", exc_info=True)
        return jsonify(status='fail', message=f"An error occurred: {e}")


def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)


if __name__ == "__main__":
    app.run(debug=True)  # Keeping it True for detailed debugging.

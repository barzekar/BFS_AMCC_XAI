# [Achievable Minimally Contrastive Counterfactual Explanations](https://www.preprints.org/manuscript/202307.0786/v1)


## Overview

Decision support systems grounded on machine learning models have increasingly become essential in deciphering complex datasets. While existing model-agnostic explanation models highlight influential factors underpinning predictions, they often fall short in providing actionable insights for more favorable outcomes. Addressing this, our novel method offers specific, feasible changes impacting the predictions of intricate black-box AI models for specific instances. Additionally, our method introduces high-precision explanations, applying secondary techniques to identify minimally contrastive yet maximally probable high-precision counterfactual explanations. By focusing on achievable contrasted features, we ensure real-time utility, positioning our approach as ideal for systems demanding immediate responses.
For a comprehensive understanding, refer to our article titled "Achievable Minimally Contrastive Counterfactual Explanations", which delves deep into our method's mechanics and its suitability for real-time applications.

## Setup

### Prerequisites

- Python 3.10 or higher
- Flask
- Necessary Python libraries and packages mentioned in `requirements.txt`

### Installation

1. Clone the [repository](https://github.com/barzekar/BFS_AMCC_XAI):
   ```bash
   git clone https://github.com/barzekar/BFS_AMCC_XAI.git

2. Install the required packages:
    pip install -r requirements.txt



## Usage

Initiate the Flask application and visit `http://localhost:5000` on your browser. Engage with the BFSAMCC XAI tool, provide your data, and receive precise model-agnostic explanations.

### Note on Timing
When evaluating the `BFS_AMCC` algorithm's efficiency, note that the recorded time pertains solely to our method. While we use the anchor algorithm to identify key anchors, its execution time isn't reflected in the `BFS_AMCC` timings.
Our primary interest is how quickly `BFS_AMCC` can modify a prediction based on parameters like ignore indices, specific indices, and transition rules. If you're using your own machine learning model without the anchor algorithm, ensure you provide the essential input arguments for our algorithm to operate effectively.



## Docker Deployment

For those who prefer using Docker for deployment, we provide a Dockerfile for building a Docker image of the application.

### Prerequisites
- Ensure you have Docker installed on your machine. If not, you can get it from [Docker's official website](https://www.docker.com/get-started).

### Building the Docker Image
To build a Docker image of the application, navigate to the root directory of the project (where the `Dockerfile` is located) and run:

```bash
docker build -t yourdockername .
```

This will create a Docker image named "yourdockername".

### Running the Application Using Docker
Once the image is built, you can run the application using the following command:

```bash
docker run -p 5000:5000 yourdockername
```
This command maps port 5000 in the container to port 5000 on your host machine, allowing you to access the application at `http://localhost:5000`.




## Feedback & Collaboration

Discover any anomalies or areas of improvement? Raise an issue in the repository. We are open to collaborations and value contributions. For proposals or fixes, initiate a pull request or open a descriptive issue.

## Acknowledgments
We acknowledge the authors of **Anchors: High-Precision Model-Agnostic Explanations** for their contributions in the field of anchor-based explanations. Their work has been foundational for our research. For further details, refer to their [repository](https://github.com/marcotcr/anchor).



## Citation

Should you find this repository beneficial to your research or endeavors, please consider citing us with the provided reference:

```bash
@article{barzekar2023achievable,
  title={Achievable Minimally Contrastive Counterfactual Explanations},
  author={Barzekar, Hosein and McRoy, Susan},
  year={2023},
  publisher={Preprints}
}




# [Achievable Minimally Contrastive Counterfactual Explanations](https://www.preprints.org/manuscript/202307.0786/v1)


## Overview

Decision support systems, anchored in machine learning models, have emerged as vital tools for dissecting complex tabular datasets. Existing model-agnostic explanation models excel in elucidating influential factors driving predictions. However, they often don't bridge the gap to offer actionable insights towards desired outcomes. Our method steps in here, proposing precise, actionable changes tailored to influence predictions of intricate black-box AI models for specific instances.

This method is twofold: Initially, we utilize the high-precision explanations from "Anchors". Subsequently, we deploy a technique to derive achievable minimally contrastive counterfactual explanations (AMCC), within the realm of domain-specific constraints. A significant advantage lies in the flexibility our approach affords: researchers can skip the first step, plugging in their machine learning models directly into our AMCC framework, making our method both adaptable and efficient. The focus on achievable contrasting features ensures our model's relevance in real-time applications, ideal for systems where immediate responses are paramount.

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
Initiate the Flask application and visit `http://localhost:5000` on your browser. 
Engage with the BFS-AMCC interface, input your data, and receive actionable suggestions towards favorable outcomes.
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

#### Running the Application Using Docker
Once the image is built, you can run the application using the following command:

```bash
docker run yourdockername
```

This will execute your main script inside the container, and you should see the printed metrics as output.



## Feedback & Collaboration

Discover any anomalies or areas of improvement? Raise an issue in the repository. We are open to collaborations and value contributions. For proposals or fixes, initiate a pull request or open a descriptive issue.

## Acknowledgments
We acknowledge the authors of **Anchors: High-Precision Model-Agnostic Explanations** for their contributions in the field of anchor-based explanations. Their work has been foundational for our research. For further details, refer to their [repository](https://github.com/marcotcr/anchor).



## Citation

Should you find this repository beneficial to your research or endeavors, please consider citing us with the provided reference:

#### BibTeX
```bash
@Article{make5030048,
  AUTHOR = {Barzekar, Hosein and McRoy, Susan},
  TITLE = {Achievable Minimally-Contrastive Counterfactual Explanations},
  JOURNAL = {Machine Learning and Knowledge Extraction},
  VOLUME = {5},
  YEAR = {2023},
  NUMBER = {3},
  PAGES = {922--936},
  URL = {https://www.mdpi.com/2504-4990/5/3/48},
  ISSN = {2504-4990},
  DOI = {10.3390/make5030048}
}
```



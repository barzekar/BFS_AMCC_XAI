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

## Feedback & Collaboration

Discover any anomalies or areas of improvement? Raise an issue in the repository. We are open to collaborations and value contributions. For proposals or fixes, initiate a pull request or open a descriptive issue.

## Acknowledgments
We acknowledge the authors of **Anchors: High-Precision Model-Agnostic Explanations** for their contributions in the field of anchor-based explanations. Their work has been foundational for our research. For further details, refer to their [repository](https://github.com/marcotcr/anchor).



## Citation

If our repository aids your research or project, kindly reference our work using the following citation:

```bash
@article{barzekar2023achievable,
  title={Achievable Minimally Contrastive Counterfactual Explanations},
  author={Barzekar, Hosein and McRoy, Susan},
  year={2023},
  publisher={Preprints}
}



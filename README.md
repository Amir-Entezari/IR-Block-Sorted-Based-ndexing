# Information Retrieval: BSBI Algorithm for Inverted Indexing

## Overview
This project implements the Blocked Sort-Based Indexing (BSBI) algorithm to efficiently build an inverted index for large datasets. It is designed for educational purposes to demonstrate how modern search engines might structure their indexing systems.

## Features
- **Efficient Indexing:** Uses the BSBI algorithm to manage memory efficiently when indexing large datasets.
- **Scalability:** Handles large collections of documents by breaking them into manageable blocks.
- **Search Capability:** Includes basic search functionality to query the created index.

## Installation
```bash
git clone https://github.com/Amir-Entezari/IR-boolean-search.git
pip install -r requirements.txt
```

## Description
The project uses Python to implement the Blocked Sort-Based Indexing (BSBI) algorithm, which involves reading documents, tokenizing text, and sorting tokens before indexing. This method is particularly effective for large-scale information retrieval systems.

### Project Organization
The repository contains:
- `preprocessing.py`: Script for data cleaning and preparation.
- `indexing.py`: Utilities for data indexing.
- `querying.py`: Implementation of various data querying methods.
- `experiments.ipynb`: Jupyter notebook containing experimental analysis and results.
- `report.ipynb`: Detailed report on the project, including methodology and results.
- 
This structure supports a clear separation of functionality, making it easy to manage and extend the project.



## Contributing
Contributions are welcome! Please fork the repository and submit pull requests with your suggested changes. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
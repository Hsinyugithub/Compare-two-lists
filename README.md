# List Comparator (Streamlit App)

A lightweight and interactive Streamlit application for comparing two
lists using set operations.

## Features

-   Flexible delimiter handling (newline, comma, semicolon, whitespace,
    custom)
-   Case-sensitive or case-insensitive comparison
-   Optional whitespace trimming
-   Optional deduplication
-   Optional alphabetical sorting
-   Summary metrics
-   Jaccard similarity
-   Overlap coefficient
-   Interactive region explorer
-   Download results as TXT or CSV

------------------------------------------------------------------------

## Installation

Clone the repository or download the app script.

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Run the App

``` bash
streamlit run app.py
```

Replace `app.py` with your script filename if different.

------------------------------------------------------------------------

## Similarity Metrics

**Jaccard Similarity**\
Intersection ÷ Union

**Overlap Coefficient**\
Intersection ÷ Smaller set size

------------------------------------------------------------------------

## Example Use Cases

-   Comparing gene lists
-   Comparing accession IDs
-   Comparing ontology term sets
-   General text-based list comparison

------------------------------------------------------------------------

## License

MIT License

# Twitter-Data-ETL-Pipeline

Data pipeline using Twitter API and MySQL.
- Uses Luigi to do the pipline. 
- Word cloud analysis
- Easy to change Twitter topics

## Setup and install

1. Clone/download this repo.

2. Install dependencies
```
python3 -m pip install -r requirements.txt
```

## How to use
To start streaming data
```
python3 start_streaming_data.py
```
To run data pipline
```
python3 pipeline.py
```
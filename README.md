Simple script to get shortest distance between all 16 provincial cities in Poland.

#### Setup

1. Create venv
```python
python -m venv venv
```

2. Activate venv
```python
source venv/bin/activate
```

3. Install requirements
```python
pip install -r requirements.txt
```

4. Create gcp project, enable Google Maps API and get API key

5. Create .env file with Google Maps API key
```python
GOOGLE_MAPS_API_KEY=your_api_key
```

6. Run script
```python
python main.py
```
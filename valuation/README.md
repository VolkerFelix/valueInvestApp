# Valuation App
## Run
Activate venv  
```
python .\app\main.py --help
```
### Single stock evaluation
```
python .\app\main.py --stockSymbol NVDA --verbose True
```
### Whole index evaluation
```
python .\app\main.py --indexName SP500 --verbose True
```
## Docker
```
docker build -t valuation .
docker run -it valuation
python3 main.py --stockSymbol NVDA --verbose True
```
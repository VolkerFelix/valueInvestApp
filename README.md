# valueInvestApp

## How to run the app
Activate venv and run:
```
uvicorn stock_valuation_db.main:app --reload
```
## Docker
```
docker-compose build
docker-compose up
```
Access at 'localhost:8008/docs'  
Continue here:
https://testdriven.io/blog/fastapi-docker-traefik/#postgres
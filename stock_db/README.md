# RESTful API to interact with a DB storing financial data
In order to find substantially undervalued companies in the global stock markets, different calculation techniques can be used e.g. discounted cash flow method. The results of such calculations shall be stored in a database for later evaluation purposes.
## Features
- Authenticate user based on OAuth 2.0
- List all stored valuation info on stocks
- Add new valuation info
- Get specific stock valuation
## How to run
### Linux using SQLite
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python uvicorn main:app --host 0.0.0.0
```
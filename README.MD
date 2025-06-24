https://medium.com/@codingwitharyan/introduction-to-django-for-backend-development-2db67768ee62

## top gainer, loser api
https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=demo

## news sentiment api
https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo

## start a django app 
python3 manage.py startapp appname

afterwards add to INSTALLED_APPS in project > settings.py

## start a django project (projects > apps)
django-admin startproject 

## After adding model orm
python3 manage.py makemigrations

-> to map sql commands

python3 manage.py migrate

### to populate ticker db, run
python3 manage.py fill_tickers

### mocking lambda function, run
python3 mock_lambda_fetch
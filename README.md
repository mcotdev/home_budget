# Budget Forecast
This project provides me with an easy overview my my household budget, but can ealy be adapted for other purposes.
I've used an sqlite database, but could just have easly used a plain CSV file or Excel spreasheet to enter the expense and incomes.
Feel free to change and improve it.

This is built in python using pandas and is uses a SQLite3 database transactions.db

## Requirements:
```
import plotly.express as px
import pandas as pd
import sqlite3
import os
```
Edit the database as required with income and expenses.

## Usage:

Run the app from the commandline.

```
python3 python3 budget-forecast.py
```

> Enter the current balance of your account:

> Enter forecast length in years:

The result will be a table on the command line and a streamlit line graph in your browser.

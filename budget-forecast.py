import plotly.express as px
import pandas as pd
import sqlite3
import os

# read sqlite transactions.db into a dataframe
conn = sqlite3.connect('transactions.db')
df = pd.read_sql_query("SELECT * FROM transactions", conn)
conn.close()

# ask for todays current balance
todays_balance = int(input('What is the account balance? '))

# ask for years_span
years_span = int(input('How many years do you want to span? '))

# Where 'Start' is not specified, Start = todays date in format YYYY-MM-DD
df['Start'] = df['Start'].fillna(pd.Timestamp.today().strftime('%Y-%m-%d'))
# Where 'End' is not specified, End = Start + years_span in format YYYY-MM-DD
df['End'] = df['End'].fillna((pd.to_datetime(
    df['Start']) + pd.DateOffset(years=years_span)).dt.strftime('%Y-%m-%d'))

# if End date is greater than todays date + years_span, set End = todays date + years_span
df['End'] = df['End'].where(pd.to_datetime(df['End']) <= (pd.Timestamp.today() + pd.DateOffset(
    years=years_span)), (pd.Timestamp.today() + pd.DateOffset(years=years_span)).strftime('%Y-%m-%d'))

df = pd.concat([pd.DataFrame({'Start': pd.date_range(row.Start, row.End, freq=row.Period),
                              'Category': row.Category,
                              'Note': row.Note,
                              'Amount': row.Amount}, columns=['Start', 'Category', 'Note', 'Amount'])
                for i, row in df.iterrows()], ignore_index=True)
##
# sort by date and format date column as YYYY-MM-DD
df = df.sort_values(by='Start').reset_index(drop=True)
df['Start'] = df['Start'].dt.strftime('%Y-%m-%d')

df.loc[-1] = [pd.Timestamp.today().strftime('%Y-%m-%d'), 'Balance Adjustment',
              'Balance Adjustment', todays_balance]
df.index = df.index + 1
df = df.sort_index()

# add new column 'Balance' and populate with cumulative sum of 'Amount'
df['Balance'] = df['Amount'].cumsum()
print(df.to_markdown())  # print markdown table 

# write dataframe to budget.csv
df.to_csv('budget.csv', index=False)

# if no negative balance, print "No Negative Balance Found"
# if negative balance, print "Negative Balance Found"
if df['Balance'].min() >= 0:
    print('No Negative Balance Found during the forecast period')
else:
    # show first row in df where Balance is negative
    print('\n There was Negative Balance Found during the forecast period startring on: \n')
    print(df[df['Balance'] < 0].head(1))

print('\n Balance is under the 18000 threshold on: ')
# print the first date in Start that Balance is under 18000 threshold
under_18000 = (df[df['Balance'] < 18000].head(1)) 
# from under_18000 dataframe, print the Start column and Balance column values
print(under_18000[['Start','Balance']])


# plot budget.csv using plotly
monthly_minimum = 0
df = pd.read_csv('budget.csv')
# add monthly_minimum as a horizontal line
fig = px.line(df, x='Start', y='Balance', title='Budget')
fig.add_hline(y=monthly_minimum, line_dash='dash', line_color='red',
              annotation_text='Zero Line', annotation_position='bottom right')
fig.show() # show plot



 




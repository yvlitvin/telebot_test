from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

location = 'atm_numbers.sqlite'
table_name = 'currency'

conn = sqlite3.connect(location)
c = conn.cursor()
sql_create = 'create table if not exists ' + table_name + ' (date text, currency text, buy text, sell text, nbu text)'
# sql_drop = 'drop table ' + table_name
c.execute(sql_create)
conn.commit()

result = requests.get("https://credit-agricole.ua/press/exchange-rates")
data = result.content
soup = BeautifulSoup(data, "html.parser")
now = datetime.datetime.now()
date = str(now.strftime("%d%m%Y"))
# print(date)
table = soup.find('tbody')
# print(table)
for row in table.find_all('tr')[1:]:
    # Create a variable of all the <td> tag pairs in each <tr> tag pair,
    col = row.find_all('td')
    currency = col[0].string.strip()
    buy = col[1].string.strip()
    sell = col[2].string.strip()
    nbu = col[3].string.strip()
    c.execute('insert into ' + table_name + ' (date, currency, buy, sell, nbu) values (?, ?, ?, ?, ?);',
             (date, currency, buy, sell, nbu))
    conn.commit()


c.close()
conn.close()



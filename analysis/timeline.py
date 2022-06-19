import sys
import csv
import datetime
import psycopg2
import os

START_DATE = datetime.datetime(2022, 4, 6)
NUMBER_OF_DAYS = 60

conn = psycopg2.connect(
    host=os.environ['PG_HOST'],
    database=os.environ['PG_NAME'],
    user=os.environ['PG_USERNAME'],
    password=os.environ['PG_PASSWORD'],
)

print('connected to pg')

cur = conn.cursor()

date = START_DATE
next_date = date + datetime.timedelta(days=1)
sql = "select count(*) from posts where crawled_at >= %s and crawled_at < %s;"
args = (date, next_date,)
counts = []

for i in range(NUMBER_OF_DAYS):
    cur.execute(sql, args)
    rows = cur.fetchall()

    date += datetime.timedelta(days=1)
    next_date = date + datetime.timedelta(days=1)

    args = (date, next_date,)

    for row in rows:
        print(row[0])
        counts.append(row[0])

cur.close()

date = START_DATE

with open('timeline.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for c in counts:
        if int(c) == 0:
            break
        writer.writerow([date, c])
        date += datetime.timedelta(days=1)

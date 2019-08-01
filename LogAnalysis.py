#!/usr/bin/env python3

import psycopg2

DBNAME = 'news'


"""Return What are the most popular three articles of all time ? """
try:
    db = psycopg2.connect(database=DBNAME)
except psycopg2.Error as e:
    print("Unable to connect to the database")
    print(e.pgerror)
    print(e.diag.message_detail)
    sys.exit(1)

a = db.cursor()
a.execute("select substr(path,10) articles,count(path) num from log \
           where status = '200 OK' group by path order by num desc \
           limit 3 offset 1;")
a_records = a.fetchall()

print("\n")
print("*** What are the most popular three articles of all time ? ***\
      " + "\n")

for row in a_records:
    print("* " + str(row[0]) + " -- " + str(row[1]) + " views")

print("\n")

"""Return Who are the most popular article authors of all time ? """
b = db.cursor()
b.execute("select ath.name,sum(m_art.num) sum_views from \
           authors ath,articles art ,most_articles m_art where \
           ath.id= art.author and art.slug = m_art.article \
           group by (ath.name) order by sum_views desc;")

b_records = b.fetchall()

print("*** Who are the most popular article authors of all time ? *** \
      " + "\n")

for row in b_records:
    print("* " + str(row[0]) + " -- " + str(row[1]) + " views")


print("\n")

"""Return On which days did more than 1% of requests lead to errors ? \
   """
c = db.cursor()
c.execute("select REPLACE(TO_CHAR(time,'Month DD,YYYY'),'      ',' ') \
           as days,((bad_req_sum*100)/count(status)::float) as Percent\
           from log,bad_req_days where TO_CHAR(time,'Month DD,YYYY')= \
           day group by (days,bad_req_sum) having ((bad_req_sum*100) \
           /count(status))>1;")

c_records = c.fetchall()

print("*** On which days did more than 1% of requests lead to errors ?\
 ***" + "\n")

for row in c_records:
    print("* " + str(row[0]) + " -- " + str(round(row[1], 2)) +
          "% errors")

db.close()

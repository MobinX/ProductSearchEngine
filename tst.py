import psycopg2

cnn = psycopg2.connect(
  dbname="productSearch:main",
  user="Mobin-Chowdhury-s-workspace-eh41hn",
  password="xau_vhTUq5SIpC2R5u7ua6zDHPKjQhkpGT9e2",
  host="us-east-1.sql.xata.sh",
  port=5432,
)
cur = cnn.cursor()
cur.execute("SELECT 1")
print(cur.fetchone())
# (1,)
cnn.close()
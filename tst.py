import psycopg2

cnn = psycopg2.connect(
  dbname="<DATABASE_NAME>:<BRANCH>",
  user="<WORKSPACE_ID>",
  password="<API_KEY>",
  host="<REGION>.sql.xata.sh",
  port=5432,
)
cur = cnn.cursor()
cur.execute("SELECT 1")
print(cur.fetchone())
# (1,)
cnn.close()
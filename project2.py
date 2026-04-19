#Step 1 = is to establish correct connection to the datebase in my case it was connection to bdeaver
from sqlalchemy import create_engine #sqlalchemy to bridge python and sql
import pandas as pd #pandas library for analysis

engine = create_engine(
    "mysql+pymysql://root:1234@localhost:3306/mydb"  #connecting to my database in docker
)

df = pd.read_sql("SHOW TABLES;", engine) #reading the query
print(df)


# query for making the table
query = """
SELECT 
    a.account_id,
    a.industry, 
    a.plan_tier, 
    s.mrr_amount, 
    c.churn_date
    CASE WHEN c.churn_date IS NOT NULL THEN 1 ELSE 0 END as is_churned
FROM ravenstack_accounts a
LEFT JOIN ravenstack_subscriptions s ON a.account_id = s.account_id
LEFT JOIN ravenstack_churn_events c ON a.account_id = c.account_id;
"""
#if we don't have churn_date 'that means the user is active
# using pandas for reading the table
df = pd.read_sql(query, engine)

print("step two is done and the table")
df.head() # showing 5 lines


# if we don't have info about clients info ,mrr info so we will put 0
df['mrr_amount'] = df['mrr_amount'].fillna(0)


print("how many nulls we have")
print(df.isnull().sum())

# saving the table in csv format
df.to_csv('churn_analysis_final.csv', index=False)

print("the file is ready")
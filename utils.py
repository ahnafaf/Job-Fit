import peewee
import psycopg2
import psycopg2.extras
import datetime
import os
# Common functions 

def connect_to_db():
    db1 = PostgresqlDatabase(
    os.getenv('DB_NAME'), 
    user=os.getenv('DB_USERNAME'), 
    password=os.getenv('DB_PASSWORD'), 
    host=os.getenv('DB_HOST'), 
    port=os.getenv('DB_PORT')
    )
    return db1.connect()
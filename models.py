# Table Creation Query for Postgres
import notlangchain
from peewee import *
import os

db1 = PostgresqlDatabase(
    os.getenv('DB_NAME'), 
    user=os.getenv('DB_USERNAME'), 
    password=os.getenv('DB_PASSWORD'), 
    host=os.getenv('DB_HOST'), 
    port=os.getenv('DB_PORT')
)

class BaseModel(Model):
    class Meta:
        database = db1

class initialData(BaseModel):
    id = PrimaryKeyField()
    created_at = DateTimeField()
    keywords = TextField()
    location_searched = TextField()
    websites = TextField()
    results_wanted = IntegerField()


class scraperData(BaseModel):
    id = PrimaryKeyField()
    link_id = ForeignKeyField(initialData, backref='jobs')
    site = TextField(null=True)
    title = TextField(null=True)
    company = TextField(null=True)
    location = TextField(null=True)
    date_posted = DateTimeField(null=True)
    job_type = TextField(null=True)
    interval = TextField(null=True)
    min_amount = IntegerField(null=True)
    max_amount = IntegerField(null=True)
    currency = TextField(null=True)
    job_url = TextField(null=True)
    description = TextField(null=True)
    
    class Meta:
        database = db1


if __name__ == '__main__':
    try:
        db1.connect()
        print(db1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db1.close()
        
"""

class processedData(BaseModel):
    id = PrimaryKeyField()
    link = ForeignKeyField(initialData, backref='processed_data') # Each processed_data is linked to a initial_data entry
    langchain_summary = TextField()
    langchain_analysis = TextField()

    
class jobData(BaseModel):
    id = PrimaryKeyField()
    link = ForeignKeyField(initialData, backref='jobs') # Each job_data is linked to a initial_data entry
    created_at = DateTimeField()
    job_site = TextField()
    job_title = TextField()
    job_company = TextField()
    job_description = TextField()
    job_location = TextField()
    job_datetime = TextField()
    job_url = TextField()
    
"""
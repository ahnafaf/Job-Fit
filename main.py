from linkedin_api import Linkedin
import json
import langchain
import peewee
import utils
from models import *
import pandas
from jobspy import scrape_jobs
import pandas as pd
import peewee
from datetime import datetime
from tabulate import tabulate
import notlangchain
import tiktoken

"""
    Purpose of this code is to make a webpage where the user can input the link for a job, the job gets processed through GPT and a final result is returned
    with the summarizations of the skills required, most common keywords by percentages.
"""
# Searches the jobs and returns a dictionary of it.
def jobSearcher(keywords: str, locations: str, websites: list, results_want: int):
    print("jobSearcher function called")
    jobs = scrape_jobs(
        site_name=websites,
        search_term=keywords,
        location=locations,
        results_wanted=results_want,
    )
    return jobs.to_dict(orient='records')

# Inserts into the first table where the basic data is stored, such as the link and the amount of results wanted.
def first_table_insert(keywords: str, locations: str, websites: list, results_want: int):
    query = initialData.insert({
        initialData.created_at: datetime.now(), 
        initialData.keywords: keywords, 
        initialData.location_searched: locations,
        initialData.websites: websites, 
        initialData.results_wanted: results_want
    })
    return query.execute()

# Inserts into the second table where the job data is stored.
def save_query_details(keywords: str, locations: str, websites: list, results_want: int):
    # Insert into initialData and get the id of the inserted row
    link_id = first_table_insert(keywords, locations, websites, results_want)
    
    # Get the job data
    try:
        dictionary_of_jobs = jobSearcher(keywords, locations, websites, results_want)
    except:
        print("Error in jobSearcher")
        return "Error in jobSearcher"
    
    # Add the link_id to each job dictionary
    for job in dictionary_of_jobs:
        job['link_id'] = link_id  # Use a different key for the link_id
    
    # Insert into scraperData
    with db1.atomic():
        scraperData.insert_many(dictionary_of_jobs).execute()
        
    return link_id

def combine(keywords: str, locations: str, websites: list, results_want: int, resume: str = None) -> str:
    print("combine function called")
    Link_id = save_query_details(keywords, locations, websites, results_want) # Insert into the database and get the link_id
    query = (scraperData.select().where(scraperData.link_id == Link_id)) # Query the database for the link_id and gets the jobs
    jobs_str = turnQueryToString(query) # Turns the jobs into a string
    if len(resume) > 1:
        content = notlangchain.process_raw_job_data_resume(jobs_str, resume) # Processes the jobs and resume through GPT3.5-Turbo
    else:
        content = notlangchain.process_raw_job_data(jobs_str) # Processes the jobs through GPT3.5-Turbo
    return content.content # Returns the LLM output
    # First get link id and add to table*, then query the table for link id, process the data*, then add to langchain/return


def processor():
    pass


def turnQueryToString(query):
    result = ""
    for job in query:
        result += f"ID: {job.id}\n"
        result += f"Link ID: {job.link_id}\n"
        result += f"Site: {job.site}\n"
        result += f"Title: {job.title}\n"
        result += f"Company: {job.company}\n"
        result += f"Location: {job.location}\n"
        result += f"Date Posted: {job.date_posted}\n"
        result += f"Job Type: {job.job_type}\n"
        result += f"Interval: {job.interval}\n"
        result += f"Min Amount: {job.min_amount}\n"
        result += f"Max Amount: {job.max_amount}\n"
        result += f"Currency: {job.currency}\n"
        result += f"Job URL: {job.job_url}\n"
        result += f"Description: {job.description}\n\n"
    return result



    
"""
Ancient code, don't bother looking at this. Kept it just in case.

def insert_into_scraperData(data: dict):
    Function to insert data into scraperData table.
    :param data: List of dictionaries containing the data to be inserted.
    # Convert the data into a format that can be inserted into the scraperData table
    insert_data = []
    for item in data:
        insert_data.append({
            'link': item.get('link', None),  # This should be the id of the corresponding initialData entry
            'site': item.get('site', None),
            'title': item.get('title', None),
            'company': item.get('company', None),
            'location': item.get('location', None),
            'date_posted': item.get('date_posted', None),
            'job_type': item.get('job_type', None),
            'interval': item.get('interval', None),
            'min_amount': item.get('min_amount', None),
            'max_amount': item.get('max_amount', None),
            'currency': item.get('currency', None),
            'job_url': item.get('job_url', None),
            'description': item.get('description', None)
        })
    # Insert the data into the scraperData table
    with db.atomic():
        scraperData.insert_many(insert_data).execute()

"""
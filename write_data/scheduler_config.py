# scheduler_config.py

import datetime
from google.cloud import scheduler

def configure_scheduler():
    # Schedule the tasks
    scheduler_client = scheduler.CloudSchedulerClient()
    parent = "projects/apt-entropy-410721/locations/us-central1"  # Replace with your project and location

    # Schedule data insertion task
    topic_name = "projects/apt-entropy-410721/topics/write_data_to_bq-topic"  # Replace with your tapic name
    job = {
        "name": f"{parent}/jobs/data-insertion-job", 
        "schedule": "every 1 hours",
        "pubsub_target": {
            "topic_name": topic_name,
            "data": b'{"action": "write_input_data"}',
        },
    }

    data_insertion_job = scheduler_client.create_job(parent=parent, job=job)

if __name__ == "__main__":
    configure_scheduler()

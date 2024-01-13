import datetime
from google.cloud import bigquery, pubsub

def write_input_data(event, context):
    clock = datetime.datetime.now()

    # Your Pub/Sub topic for ML simulation
    project_id = "apt-entropy-410721"  # Your Project ID
    topic_name = "ml_simulation-topic"  # Your Topic name

    # Create a BigQuery client
    bq_client = bigquery.Client(project=project_id)

    # Define the schema for the BigQuery table
    schema = [
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("tag", "STRING"),
        bigquery.SchemaField("value", "INTEGER"),
    ]

    # Prepare data to be inserted into BigQuery
    rows_to_insert = [
        {
            "timestamp": clock,  # Timestamp
            "tag": '227FC001.PV',  # Identification
            "value": 207,  # Constant value for simulation purpose.
        }
    ]

    # Create a reference to the BigQuery table
    table_ref = bq_client.dataset("IndustrialDataset").table("InputTable")
    table = bq_client.get_table(table_ref)

    # Insert data into BigQuery
    errors = bq_client.insert_rows(table, rows_to_insert, selected_fields=schema)

    if errors == []:
        print('New rows have been added to BigQuery')
    else:
        print(f'Encountered errors while inserting rows to BigQuery: {errors}')

    # Publish a minimal message to the ml_simulation-topic with random numeric data
    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project_id, topic_name)

    # Random number as data menssage
    random_numeric_data = 42
    print(f'random number: {random_numeric_data}')

    # Convert the number to bytes before publishing
    data_to_publish = str(random_numeric_data).encode('utf-8')

    pubsub_client.publish(topic_path, data=data_to_publish)
    print(f'Message published to ml_simulation-topic with numeric data: {data_to_publish}')
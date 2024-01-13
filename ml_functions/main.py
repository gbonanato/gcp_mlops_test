from google.cloud import bigquery, pubsub_v1

def ml_simulation_function(event, context):


    # Extract latest values from InputTable
    bq_client = bigquery.Client()
    dataset_id = 'apt-entropy-410721.IndustrialDataset'
    input_table_id = 'InputTable'
    prediction_table_id = 'TablePrediction'

    # Query the latest row from InputTable
    query_latest = f"SELECT * FROM `{dataset_id}.{input_table_id}` ORDER BY timestamp DESC LIMIT 1"
    query_job = bq_client.query(query_latest)
    latest_row = next(query_job.result())

    # Simulate machine learning (add numbers in this example)
    simulated_result = latest_row['value'] + 10  # Adjust this as needed for your simulation

    # Insert the values into TablePrediction
    prediction_table = bq_client.get_table('apt-entropy-410721.IndustrialDataset.TablePrediction')

    # Create a new row with the required fields
    new_row = {
        'timestamp': latest_row['timestamp'],
        'tag': latest_row['tag'],
        'value': latest_row['value'],
        'prediction': simulated_result
    }

    # Insert the new row into TablePrediction
    errors = bq_client.insert_rows(prediction_table, [new_row])

    if errors == []:
        print('New row inserted into TablePrediction')
    else:
        print(f'Error inserting new row into TablePrediction: {errors}')

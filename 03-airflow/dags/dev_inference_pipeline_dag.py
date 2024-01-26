from datetime import datetime
from airflow.decorators import dag, task

default_args = {
    "owner": "airflow",  # Owner of the DAG, typically set to 'airflow' or username
    "depends_on_past": False,  # Ensures tasks do not depend on past runs
}

@dag(
    "dev_inference_pipe_dag",  # Unique identifier for the DAG
    default_args=default_args,  # Links to the default arguments defined above
    description="DAG for inference using a scikit-learn model",  # Description of the DAG's purpose
    catchup=False,  # Prevents backfilling, ensuring DAG runs only for the latest data
    schedule=None,  # Schedule for DAG runs; None means it's manually triggered
    start_date=datetime(2023, 11, 13),  # The start date for the DAG
    tags=["inference", "scikit-learn", "dev"],  # Tags for categorizing the DAG
)
def dag_model_inference():
    """DAG for performing model inference using a trained scikit-learn model."""

    ################ Task to generate inference data
    @task.virtualenv(
        task_id="generate_inf_data",  # Unique identifier for the task
        requirements=["pandas"],  # Required packages to be installed in the virtualenv
        system_site_packages=False,  # Ensures a clean virtual environment
    )
    def generate_inf_data():
        """
        Generates data for model inference.

        This task creates a DataFrame with mock features and saves it as a CSV file.
        The filename includes a timestamp to ensure uniqueness.

        Returns:
            str: File path of the generated CSV file.
        """
        import pandas as pd

        # Create a timestamp for the data generation
        inference_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create a DataFrame with mock data
        df = pd.DataFrame({"feature1": range(20), "feature2": range(20, 40)})
        df["feature1"] = df["feature1"] * 2  # Simple manipulation

        # Filename includes timestamp for uniqueness
        csv_filename = f"/tmp/data_inf_{inference_timestamp}.csv"

        # Save DataFrame to CSV
        df.to_csv(csv_filename, index=False)
        return csv_filename

    ################ Task to execute model inference
    @task.virtualenv(
        task_id="model_inference",  # Unique identifier for the task
        requirements=["pandas", "scikit-learn", "joblib"],  # Required packages for the task
        system_site_packages=False,  # Ensures a clean virtual environment
    )
    def inference(csv_path: str):
        """
        Performs model inference using the generated data.

        Reads the latest model from the log file, loads it, and performs predictions
        on the provided data. Inference details and errors (if any) are logged.

        Args:
            csv_path (str): File path of the data for inference.

        Returns:
            str: JSON string of the model predictions.
        """
        import joblib
        import pandas as pd
        import json
        import logging

        env = 'dev'  # Set environment to development

        try:
            # Load the data for inference
            df = pd.read_csv(csv_path)

            # Read log file to find the latest model file for the current environment
            # Read the JSON in reverse, to fetch the latest model with the condidion environment = env
            with open("/opt/airflow/models/log.txt", "r") as fp:
                lines = fp.readlines()
                for line in reversed(lines):
                    model_info = json.loads(line)
                    if model_info.get("environment") == env:
                        model_filename = model_info["model_filename"]
                        break

            # Load the latest model
            model = joblib.load(f"/opt/airflow/models/{model_filename}")

            # Perform inference
            predictions = model.predict(df[["feature1", "feature2"]])
            df["prediction"] = predictions

            # Prepare and write inference log
            inference_log = {
                "inference_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "environment": env,
                "inference_data": csv_path,
                "model_used": model_filename,
                "predictions": df["prediction"].tolist()
            }
            with open("/opt/airflow/models/log_inference.txt", "a") as log_file:
                log_file.write(json.dumps(inference_log) + "\n")

            # Return predictions as JSON
            return df["prediction"].to_json()

        except Exception as e:
            # Log any errors during inference
            error_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.error(f"Error during inference: {e}")
            error_log = {
                "error_time": error_timestamp,
                "error_message": str(e)
            }
            with open("/opt/airflow/models/log_inference.txt", "a") as log_file:
                log_file.write(json.dumps(error_log) + "\n")
            raise  # Reraise the exception to ensure Airflow knows the task failed

    # Link tasks in the DAG
    generate_data_op = generate_inf_data()
    inference_op = inference(generate_data_op)

# Instantiate the DAG
dag_model_inference_instance = dag_model_inference()

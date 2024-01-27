from datetime import datetime
from airflow.decorators import dag, task

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
}

@dag(
    "prd_inference_pipe_dag",
    default_args=default_args,
    description="DAG for inference using a scikit-learn model",
    catchup=False,
    schedule=None,
    start_date=datetime(2023, 11, 13),
    tags=["inference", "scikit-learn", "prd"],
)

def dag_model_inference():
    
    ################ Task to generate raw inference data
    @task.virtualenv(
        task_id="generate_inf_data",
        requirements=["pandas"],
        system_site_packages=False,
    )
    def generate_inf_data():
        """Function to generate inference data.

        Returns:
            str: Path to the generated data CSV file.
        """
        import pandas as pd
        from datetime import datetime

        inference_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        df = pd.DataFrame(
            {"feature1": range(20), "feature2": range(20, 40)}
            )
        
        # Filename with timestamp
        csv_filename = f"/tmp/data_inf_{inference_timestamp}.csv"

        df.to_csv(csv_filename, index=False)
        return csv_filename
    
    ################ Task to preprocess the generated  inference data as done in training phase
    @task.virtualenv(
        task_id="preprocess_inf_data",
        requirements=["pandas"],
        system_site_packages=False,
    )
    def preprocessing(csv_path: str):
        """Function to preprocess the generated inference data.

        Args:
            csv_path (str): Path to the raw data CSV file.

        Returns:
            str: Path to the preprocessed data CSV file.
        """
        import pandas as pd
        df = pd.read_csv(csv_path)
        df["feature1"] = df["feature1"] * 2
        preprocessed_csv_filename = csv_path.replace("raw", "preprocessed")
        df.to_csv(preprocessed_csv_filename, index=False)
        return preprocessed_csv_filename

    ################ Task to execute model inference
    @task.virtualenv(
        task_id="model_inference",
        requirements=["pandas", "scikit-learn", "joblib"],
        system_site_packages=False,
    )
    def inference(csv_path: str):
        """Function to execute model inference.

        Args:
            csv_path (str): Path to the generated data CSV file.

        Returns:
            str: Model predictions.
        """
        import joblib
        import pandas as pd
        import json
        import logging
        from datetime import datetime

        # Set environment
        env = 'prd'

        try:
            df = pd.read_csv(csv_path)

            # Read the latest model for the right environment
            with open("/opt/airflow/models/log.txt", "r") as fp:
                lines = fp.readlines()
                for line in reversed(lines):
                    model_info = json.loads(line)
                    if model_info.get("environment") == env:
                        model_filename = model_info["model_filename"]
                        break

            # Load the model
            model = joblib.load(f"/opt/airflow/models/{model_filename}")

            # Perform inference
            predictions = model.predict(df[["feature1", "feature2"]])
            df["prediction"] = predictions

            # Log the inference details
            inference_log = {
                "inference_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "environment": env,
                "inference_data": csv_path,
                "model_used": model_filename,
                "predictions": df["prediction"].tolist()
            }

            with open("/opt/airflow/models/log_inference.txt", "a") as log_file:
                log_file.write(json.dumps(inference_log) + "\n")

            return df["prediction"].to_json()

        except Exception as e:
            error_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.error(f"Error during inference: {e}")
            # Log the error details
            error_log = {
                "error_time": error_timestamp,
                "error_message": str(e)
            }
            with open("/opt/airflow/models/log_inference.txt", "a") as log_file:
                log_file.write(json.dumps(error_log) + "\n")
            raise


    raw_data_op = generate_inf_data()
    preprocess_data_op = preprocessing(raw_data_op)
    inference_op = inference(preprocess_data_op)

dag_model_inference_instance = dag_model_inference()

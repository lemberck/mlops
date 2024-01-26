from datetime import datetime
from airflow.decorators import dag, task

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
}

@dag(
    "prd_train_model_dag",  
    default_args=default_args,  
    description="A DAG for training a scikit-learn model",  
    catchup=False,  
    schedule=None,  
    start_date=datetime(2023, 11, 13),  
    tags=["training", "scikit-learn", "prd"],  
)
def train_model_dag():
    """A DAG for training a ML model"""

    ################ Task to perform data preprocessing
    @task.virtualenv(
        task_id="preprocessing",  
        requirements=["pandas",], 
        system_site_packages=False,
    )

    def preprocessing():
        """Preprocessing the data required for model training.
        
        Returns:
            str: Path to the preprocessed data csv file
        """
        import pandas as pd
        import logging
    
        try:
            # Create a dataframe with mock data
            df = pd.DataFrame(
                {"feature1": range(20), "feature2": range(20, 40), "target": range(40, 60)}
            )

            # Manipulate data as part of preprocessing
            df["feature1"] = df["feature1"] * 2  

            df.to_csv("/tmp/data.csv", index=False)
            return "/tmp/data.csv"
        except Exception as e:
            logging.error(f"Error in preprocessing: {e}")
            raise

    ################ Task to train the machine learning model
    @task.virtualenv(
        task_id="train_model",  
        requirements=["pandas", "scikit-learn", "joblib"],  
        system_site_packages=False,
    )
    def train(csv_path: str):
        """
        Trains a machine learning model using the preprocessed data.

        Args:
            csv_path (str): Path to the preprocessed data csv file.

        Returns:
            bool: True if the training was successful.
        """
        try:
            import joblib  
            import pandas as pd  
            from sklearn.linear_model import LinearRegression  
            import logging
            import json
            from datetime import datetime

            # Define the environment
            env='prd' 

            df = pd.read_csv(csv_path)
            X = df[["feature1", "feature2"]]
            y = df["target"]
            model = LinearRegression()
            model.fit(X, y)
            model_hash = joblib.hash(model)
            training_timestamp = datetime.now().strftime("%Y-%m-%d:%H-%M-%S")

            # Model Registry path
            mr_path=f'/opt/airflow/models'

            model_filename = f"model_{training_timestamp}_{model_hash}.pkl"

            with open("/opt/airflow/models/log.txt", "a") as f:
                f.write(
                    json.dumps(
                        {
                        "model_hash": model_hash,
                        "model_filename": model_filename,
                        "training_timestamp": training_timestamp,
                        "environment": env
                        }
                    ) + "\n"  
                )
            joblib.dump(model, f'{mr_path}/{model_filename}')
            return True  
        except Exception as e:
            logging.error(f"Error in training: {e}")
            error_timestamp = datetime.now().strftime("%Y-%m-%d:%H-%M-%S")
            with open("/opt/airflow/models/log.txt", "a") as f:
                f.write(
                    json.dumps(
                    {   "error_timestamp": error_timestamp,
                        "detail": str(e)
                        }
                    ) + "\n")
            raise

    ################ Define the task flow
    preprocessing_op = preprocessing()  
    train_op = train(preprocessing_op)  


train_model_dag()

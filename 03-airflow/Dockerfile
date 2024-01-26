# First-time build can take upto 10 mins.

FROM apache/airflow:2.7.3

ENV AIRFLOW_HOME=/opt/airflow

WORKDIR $AIRFLOW_HOME

USER root
RUN apt-get update -qq && apt-get install vim -qqq && apt-get install -y python3-pip
# git gcc g++ -qqq


# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

# SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]


# COPY requirements.txt .

# RUN python3 -m pip install --upgrade pip

# RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY scripts scripts
RUN chmod +x scripts

USER $AIRFLOW_UID
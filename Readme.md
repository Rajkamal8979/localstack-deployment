# Data Ingestion Pipeline using LocalStack,Postgres,Airflow running in Docker Container

## Architecture
We are using Kinesis Data steams to capture event streaming data. This is being processed using the AWS Lambda functions triggerd by kinesis event trigger. the lambda function will read data from data stream in batches and insert into 2 postgresql tables based on the corresponsing record it has received.

* Scaling
	* The Kinesis data streams can be provisioned for on-demand scaling and increasing the shard counts to capture records at high rate. 
	* Lambda functions concurrent invocations can be increased to process faster with the stream as well as setting up concurrency to setup warm start in lambda functions reducing invocation time.
	
## Requirements
* Install make if not already installed
* Install [Docker](https://www.docker.com/products/docker-desktop)
* Install [Docker Compose](https://docs.docker.com/compose/install/)
* Install [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

## Setup 
Change directory within the repository and run `make start`. This will perform the following:

* Based on the definition of `docker-compose.yml` it will download necessary image to setup the project.
	* `postgres` : DB for Airflow to connect and store task execution information as well as tables we want to create.
	* `airflow` : Airflow web-server and scheduler
	* `LocalStack` : Local development environment for AWS (current configuration : Kinesis,Lambda,S3)

## Create AWS services locally
* In project folder
	* Step-1 `terraform init`
	* Step-2 `terraform plan`
	* Step-3 `terraform apply`
	This will setup Kinesis stream, Lambda and Kinesis trigger in Localstack env using `create_aws.tf` file.

## Insert data into Kinesis Data Stream 
* Use `kinesis_generator/generate_kinesis_record.py` to generate Kinesis records.
* It inserts one static JSON record. This can be modified for inserting records as JSON streams

## How to run the DAGs
* Once everyting is up and running, navigate to Airflow UI http://localhost:8080
	* In case of Amazon EC2 instance, navigate to <EC2-public-DNS>:8080
* Trigger `Initialize_tables` DAG. This will initialize all tables based on SQL files in `/dags/sql` folder.
* Trigger `Snapshot_tables` DAG. This will generate snapshot records in the tables and update the records based on UPSERT Statements.

## de-commission the environement 
* Run `make docker-cleanup`. This will stop all containers and Volumes created.
# Coding exercise

This repo holds the coding exercise for engineering positions in the core data platform team.

## Process description

Dear candidate, in our company as a Data Engineer you will work with various data sources (integrating and transforming
the data). Some of those data sources are event based, while others follow a batch approach. Below, you will find
details regarding a task that will be used to help us better understand your ease at coding. We will review your
response and ask that you join us for an additional interview with two of our team members if we see that it provides
the areas that we hope you will address and/or include.

The task and data at hand is imaginary, but please treat it as a workflow, which is important to the business.

After reviewing your solution we will invite you to an interview, where you will have the chance to present your
challenge results and discuss them with two members of our team.

## Submission of the Challenge

The team uses the code provided in the challenge as an initial assessment of the ease at which you create an
application based on efficient, clean code. We will review the details to get an understanding of your current approach
to coding. The review will determine if we would like to continue the interview process and have you join us for a
technical interview with two of our team members to pair on the code that you provided.

We ask that you provide us with a zip file containing your solution within three business days of its receipt.
Please do not submit your code to any public git repository as this would make the challenge unusable for future
interviewees.

We will then review and notify you of the movement to the next step of the process.

## The Coding Challenge

The coding challenge is to get ETL pipelines working in a local Airflow environment.

Please provide an application that creates the expected results (solving the tasks described below). Please work
towards the expected result but do not spend more than 3-4 hours on the challenge. We suggest that you stop at a point
where the code is working and document which next steps or future improvements would make sense.

A working example that demonstrates your knowledge of tools and code structure is far more important than an application
that provides all features listed below.

### Setup Requirements

The following tools should be installed to run this setup

- make
- python 3.7 and pip of at least 22.1.0
- docker (please make sure that you have enough resources available for docker. E.g. More than 2GB of RAM)
- docker compose (v2): Usually invoked via `docker compose` without a `-`

All development command should be in the `Makefile` including comments about the commands.

In order to start the docker environment you can run `make start`. When starting for the first time it can take a while.
The username and password for the Airflow UI is `airflow`.

For local development and testing you should setup the environment with `make venv` and then `make test` should work.

### Tasks

Please solve the following tasks. If applicable and useful please also add tests for the code.

#### Fix the API load

There is already a DAG called "api-load", which loads data from a mocked API and should insert this into our PostgreSQL
database. This DAG is broken, however. Please fix the DAG to work.
The only thing that is fixed is the response from the API (everything in dags/api_load/scripts/extract.py). The other
parts of the DAG can all be adjusted if required.

#### Create a backup of the loaded data

For long term archival purposes we want to store the data we load from the API in an S3 bucket "ad-data/backup".
Please use the already existing local S3 setup to store all the data we get from API in S3 before inserting it to
PostgreSQL.

#### Archive the PostgreSQL data

Please create a new DAG that runs every day and takes old data from PostgreSQL (determined by the "shown_at" column),
stores the old data in the S3 bucket "ad-data/archive" and deletes the data from PostgreSQL.

# Multinational Retail Data Centralisation Project
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

# Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [File Structure](#file-structure)
4. [Personal Reflection](#personal-reflection)
   1. [What have I learned?](#what-have-i-learned)
   2. [Future Improvements](#future-improvements)
   3. [Resources](#resources)
5. [Licence Information](#licence-information)

## Introduction 

Welcome to the Multinational Retail Data Centralisation Project! 

This project is part of my journey through the Cloud Engineering pathway at AiCore. The projects aim is to centralise and query data from a multinational retail business using cloud technologies.

The script retrieves data from a multitude of sources on AWS, including an Amazon Relational Database Service (RDS) instance, a PDF document, JSON and CSV files in an AWS S3 bucket, and through interactions with an API. It then cleans these DataFrames and uploads them to a PostgreSQL database, generates the schema and runs SQL queries relating to the business model.

## Installation 

Create a folder where you want this repo to be in and move into it.
Clone the repository into this folder on your local machine by running the following command inside your terminal:

```
git clone https://github.com/Claudiomics/multinational-retail-data-centralisation-project.git
```
Then move into within the folder, run the following code:
```
python3 main.py

```

This generates a sales_data database in postgresql, set up the schema (shown below) and run queries on it.

![ERD of sales_data](https://i.imgur.com/mKZaZOp.png)

To upload to the sales_data database and query the database through SQL scripts, the database needed to be initialised and connected to:

- Right click on Databases in PgAdmin4 and create sales_data
- In VSCode install the SQL Tools extension
- To connect to PostgreSQL, open the extension and configure connection by entering the connection details, including host, port, username, password, and database name

To retrieve the data from the S3 bucket, the CLI needed to be connected to:

- Install AWS CLI
- Configure AWS CLI by typing the following into the terminal:
```
aws configure
```
- Enter your AWS Access Key ID, Secret Access Key, default region, and default output format to access the S3 bucket.

## Libraries Required for this project

- [Pandas](#
```

```

## File Structure 
```

```


## Personal Reflection

### What Have I Learned?

####Methods and Tools of data extraction and cleaning (huge!)
- handled authentication using an API key/integrating with an API to fetch store-related data 
- visualised unclean and clean data to be able to create the cleaning methods (then can delete the files as not in the actual code anymore)
Database management (set up and managed a PostgreSQL database, including schema creation, SQL queries, and interactions with SQLAlchemy + discuss the process of connecting to an AWS RDS database and handling data retrieval.
seperating code into different classes and methods
creation and execution of postgresql statements :)
Experimented with Matplotlib for data visualization, such as creating a pie chart to represent sales by store type.
####Creation and execution of SQL queries to answer business-related questions.
-- What did I learn from the database? Interesting......

####challenges paragraph:
fetching data - developing methods
cleaning - which rows to keep, which to delete, which to modify? methods
figuring out ctes
figuring out lead() in sql
keeping credentials secret while trying to connect to database

### Future Improvements

To improve optimizing code, enhancing data visualization, or expanding functionality.
Increase security of my project by using -- patrick
Idk how to test it to create a new db to see if it actually runs in one go.
Use if __name__ = "__main__": 
  script
Improve file structure to use more folders - increase readability (modules)

### Resources

Below are some of the resoucres I found useful in the development of this project:

- ismael for regex training
- patrick github credentials
- check code indentation from reno 

## Licence Information

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.




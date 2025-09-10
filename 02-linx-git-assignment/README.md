# 📖 Linux & Git Assignments (CoreDataEngineers Bootcamp Task)

## 📌 Project Overview
This Assignment project is divided into two sections.

1. **Individual Assignment**
2. **Group Assignment**

----

## 🛠️ Individual Assignment
### Question 1: ETL Pipeline with Bash Scripting

This aspect of the project implements a **simple ETL (Extract, Transform, Load) pipeline** using **Bash scripting**.  

The pipeline is designed to:  
1. **Extract** data from a given source.  
2. **Transform** the data into a clean, standardized format.  
3. **Load** the processed data into a target location for further use.  

All configuration values (e.g., file paths, source URLs) are stored in a `.env` file to keep the script flexible and environment-independent.

---

### Question 2: Bash Script Schedulling
This aspect of the project demonstrates how to schedule a **Bash script** to run at specified intervals using **cron jobs**.
The above script was scheduled to run 12AM daily using cron.

---

### Question 3: Bash Scripts That Moves CSV and JSON Files From One Folder to Another
This Aspect of the project implements a **Bash script** that moves **CSV** and **JSON** files from one folder to another.

---

### Question 4: Bash Scripts That Download files from Source and Load into a databae
This aspect of the project created a **Bash script** that download **CSVs** from a data source and load the data into respectives tables for downstream analysis.

### Question 5: SQL queries to Answer business questions

1. Find a list of order IDs where either gloss_qty or poster_qty is greater than 4000 Only include the id field in the resulting table.
2. Write a query that returns a list of orders where the standard_qty is zero and either the gloss_qty or poster_qty is over 1000.
3. Find all company names that: start with 'C' or 'W' AND their primary contact contains 'ana' or 'Ana' BUT does not contain 'eana'
4. Show the region for each sales rep with their accounts. Columns: region name, sales rep name, account name. Sort alphabetically by account name.

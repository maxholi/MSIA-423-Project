# Predicting the Probability that an NBA Player Makes the Hall of Fame: Mid-Project Checkpoint

## Dataset

The dataset used in this project can be found here https://www.kaggle.com/drgilermo/nba-players-stats#Seasons_Stats.csv

The Seasons_Stats.csv file contains season stats for all players between 1950 - 2017, with one record per player for each season he played in the NBA.

There are 24.7K records representing 3.9K players,  and 53 columns representing a statistic for each player in a season.


## Instructions for QA Partner to run the process:

### All files used are in the midtermQA folder

### 1.  After cloning branch of the repo, open a terminal and change the working directory to midtermQA

### 2. Create a conda environment
 	
	```
	conda create --name myenv python=3.7
	conda activate myenv
	pip install -r requirements.txt

	``` 
### 3. Acquire data: this step is run to acquire data from the source (S3) and land it into a preconfigured S3 bucket

	1.  Open the config.py with the command `vi config.py`
	2.  Update the following parameters:
		
		a. `AWS_ACCESS_KEY_ID`
		b. `AWS_SECRET_ACCESS_KEY`
		c. `DEST_BUCKET`  (S3 bucket name where the file should be transfered)
		d. `DEST_KEY` (name of the file that will be transfered to the S3 bucket)
	3.  Run `python s3.py` in the terminal from the current working directory (midtermQA)
	4.  Check AWS S3 to make sure the file has been transferred

### 4. Initialize the database

	#### Initialize the database in RDS
		
		1.  SSH into EC2 instance **all files used in running this process must be SFTP'd to EC2**
		2.  Open config.py with command `vi config.py`
		3.  Update the following paramters:
		
			a. `MYSQL_USER`
			b. `MYSQL_PASSWORD`
			c. `MYSQL_HOST` 
			d. `MYSQL_PORT`
		4.  Run `python models.py --rds=True` to create an empty database in S3 with the tables `historical` and `current`
	
	#### Initialize the database locally in SQLite
	
		1.  In the current working directory (not in EC2), run the command `python models.py`
		2.  Check that the file hof.db is now in the current working directory




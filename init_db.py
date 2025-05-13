import os
import csv
#provides a MySQL database connector for python
import mysql.connector

#creates database, creates tables, and populates tables with CSV file
def setup_database(csvfile):
    create_database()
    create_tables()
    populate_tables(csvfile)

#connects to MySQL database using the host, username, and password from the .env files
def create_database():
    conn = mysql.connector.connect(
        host=os.getenv("DBHOST"),
        user=os.getenv("DBUSERNAME"),
        password=os.getenv("DBPASSWORD")
    )
    cursor = conn.cursor(dictionary=True)
    # cursor.execute(f"DROP DATABASE IF EXISTS {os.getenv('DATABASE')};")
    # cursor.execute(f"CREATE DATABASE {os.getenv('DATABASE')};")
    cursor.close()
    conn.close()

#creates the DogOwnerDetails view
def create_views():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE VIEW DogOwnerDetails AS
        SELECT
            Dogs.DogID,
            Dogs.name AS DogName,
            Dogs.age AS DogAge,
            Dogs.breed AS DogBreed,
            Owners.OwnerID,
            Owners.FirstName AS OwnerFirstName,
            Owners.LastName AS OwnerLastName,
            Owners.ContactNumber,
            Owners.Email
        FROM Dogs
        INNER JOIN Owners ON Dogs.OwnerID = Owners.OwnerID;
        '''
    )

    cursor.close()
    conn.close()

#connects to MySQL to create tables
def create_tables():
    conn = mysql.connector.connect(
        host=os.getenv("DBHOST"),
        user=os.getenv("DBUSERNAME"),
        password=os.getenv("DBPASSWORD"),
        database="DogCompetitionDatabase"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"use {os.getenv('DATABASE')};")

    #create Owners table with primary key
    cursor.execute(
        '''
        CREATE TABLE Owners
        (
            OwnerID INT AUTO_INCREMENT PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            ContactNumber VARCHAR(15),
            Email VARCHAR(100)
        );
        '''
    )

    #create Dogs table with primary key
    cursor.execute(
        '''
        CREATE TABLE Dogs
        (
            DogID INT AUTO_INCREMENT PRIMARY KEY,
            DogName VARCHAR(50),
            Age TINYINT UNSIGNED,
            Breed VARCHAR(100),
            OwnerID INT,
            FOREIGN KEY (OwnerID) REFERENCES Owners(OwnerID)
        );
        '''
    )

    #create Events table with primary key
    cursor.execute(
        '''
        CREATE TABLE Events
        (
            EventID INT AUTO_INCREMENT PRIMARY KEY,
            EventName VARCHAR(100),
            Location VARCHAR(100),
            Date DATE,
            StartTime TIME,
            EndTime TIME
        );
        '''
    )

    #create Scores table with primary key
    cursor.execute(
        '''
        CREATE TABLE Scores
        (
            ScoreID INT AUTO_INCREMENT PRIMARY KEY,
            EventID INT,
            DogID INT,
            Score INT,
            JudgeFirstName VARCHAR(50),
            JudgeLastName VARCHAR(50),
            FOREIGN KEY (EventID) REFERENCES Events(EventID),
            FOREIGN KEY (DogID) REFERENCES Dogs(DogID)
        );
        '''
    )

    cursor.close()
    conn.close()

#populates dog table with data from CSV file and has to option to populate other tables with a CSV file as well 
def populate_tables(csvfile):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    #insert into Dogs table
    with open(csvfile, "r") as csv_input:
        reader = csv.DictReader(csv_input)
        sql_insert_dog = "INSERT INTO Dogs (DogName, Age, Breed) VALUES (%s, %s, %s)"
        for row in reader:
            insert_values = (row['DogName'], int(row['Age']), row['Breed'])
            cursor.execute(sql_insert_dog, insert_values)

    #insert into Owners table
    with open(csvfile, "r") as csv_input:
        reader = csv.DictReader(csv_input)
        sql_insert_owner = "INSERT INTO Owners (FirstName, LastName, ContactNumber, Email) VALUES (%s, %s, %s, %s)"
        if 'OwnerFirstName' in reader.fieldnames:
            for row in reader:
                owner_values = (row['OwnerFirstName'], row['OwnerLastName'], row['ContactNumber'], row['Email'])
                cursor.execute(sql_insert_owner, owner_values)

    #insert into Events table
    with open(csvfile, "r") as csv_input:
        reader = csv.DictReader(csv_input)
        sql_insert_event = "INSERT INTO Events (EventName, Location, Date, StartTime, EndTime) VALUES (%s, %s, %s, %s, %s)"
        if 'EventName' in reader.fieldnames:
            for row in reader:
                date_value = row.get('Date', None)  # Handle empty date values
                event_values = (row['EventName'], row.get('Location', ''), date_value, row.get('StartTime', ''), row.get('EndTime', ''))
                cursor.execute(sql_insert_event, event_values)

    #insert into Scores table
    with open(csvfile, "r") as csv_input:
        reader = csv.DictReader(csv_input)
        sql_insert_score = "INSERT INTO Scores (EventID, DogID, Score, JudgeFirstName, JudgeLastName) VALUES (%s, %s, %s, %s, %s)"
        if 'Score' in reader.fieldnames:
            for row in reader:
                score_values = (int(row.get('EventID', 0)), int(row.get('DogID', 0)), int(row['Score']), row.get('JudgeFirstName', ''), row.get('JudgeLastName', ''))
                cursor.execute(sql_insert_score, score_values)

    conn.commit()
    cursor.close()
    conn.close()


#returns the established database connection (conn)
def connect_db():
    conn = mysql.connector.connect(
        host=os.getenv("DBHOST"),
        user=os.getenv("DBUSERNAME"),
        password=os.getenv("DBPASSWORD"),
        database=os.getenv("DATABASE")
    )
    return conn

import mysql.connector


#creates an object to represent an owner
class Owner:
    def __init__(self, first_name, last_name, contact_number, email):
        self.first_name = first_name
        self.last_name = last_name
        self.contact_number = contact_number
        self.email = email


#creates an object to represent an event 
class Event:
    def __init__(self, event_name, location, date, start_time, end_time):
        self.event_name = event_name
        self.location = location
        self.date = date
        self.start_time = start_time
        self.end_time = end_time


#creates an object to represent a score
class Score:
    def __init__(self, event_id, dog_id, score, judge_first_name, judge_last_name):
        self.event_id = event_id
        self.dog_id = dog_id
        self.score = score
        self.judge_first_name = judge_first_name
        self.judge_last_name = judge_last_name


#creates an object to represent a dog
class Dog:
    def __init__(self, name, age, breed, owner_id=None):  # Make sure this matches the call
        self._name = name
        self._age = age
        self._breed = breed
        self._owner_id = owner_id

    def __repr__(self):
        """
        Create a string representation of a dog.

        The format is as follows:

           <name>, a <age> year old <breed>

        :return: the string representation of the dog
        """
        return '{}, a {} year old {}'.format(self._name, self._age,
                                             self._breed)

    """
    d = Dog("Joe", 30, "Shepherd");
    print(d.name);  # this is a property
    print(d.name());  # this is a function
    """

    #getter method for retrieving the value of the private attribute _name.
    @property
    def name(self):
        return self._name

    #getter method for retrieving the value of the private attribute _age.
    @property
    def age(self):
        return self._age

    #getter method for retrieving the value of the private attribute _breed.
    @property
    def breed(self):
        return self._breed

    #getter method for retrieving the value of the private attribute _owner_id. 
    @property
    def owner_id(self):
        return self._owner_id

    #method to increment the age of the object by 1.
    def increment_age(self):
        self._age += 1


class DogDB:
    """
    This class provides an interface for interacting with a database of dogs.
    """

    def __init__(self, host, username, password, database):
        self._conn = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database="DogCompetitionDatabase"
        )

   #function to create an SQL query to insert a new dog record into the Dogs table with specified attributes
    def add_dog(self, dog):

        query = '''
            INSERT INTO Dogs (name, age, breed, OwnerID)
            VALUES (%s, %s, %s, %s);
        '''

        cur = self._conn.cursor()
        cur.execute(query, (dog.name, dog.age, dog.breed, dog.owner_id))
        self._conn.commit()

        print(cur.rowcount, "record(s) affected")
        cur.close()

    #function to delete a dog through an SQL query 
    def delete_dog(self, name):
        """
        Remove a dog record from the database

        :param name: name of the dog to be removed from the database
        """
        query = 'DELETE FROM Dogs WHERE name=%s;'

        cur = self._conn.cursor()
        cur.execute(query, (name,))
        self._conn.commit()

        print(cur.rowcount, "record(s) affected")
        cur.close()

    #function to update a dog through an SQL query 
    def update_dog(self, dog_name, new_dog):

        query = '''
            UPDATE Dogs SET name=%s, age=%s, breed=%s, OwnerID=%s
            WHERE name=%s;
        '''

        cur = self._conn.cursor()
        cur.execute(query, (new_dog.name, new_dog.age,
                            new_dog.breed, new_dog.owner_id, dog_name))
        self._conn.commit()

        print(cur.rowcount, "record(s) affected")
        cur.close()

        return self.get_dogs_by_name(new_dog.name)

    def get_dogs_by_name(self, name):
        """
        Find a dog's record in the database using the name

        :param name: name of the dog
        :return: list of all dogs with a matching name
        """

        query = '''
            SELECT name, age, breed
            FROM Dogs
            WHERE name = %s
        '''

        cur = self._conn.cursor()
        cur.execute(query, (name,))

        dogs = []

        for row in cur.fetchall():
            dog = Dog(row[0], row[1], row[2])
            dogs.append(dog)

        cur.close()
        return dogs

    def get_owners_by_name(self, name):
        """
        Find an owner's record in the database using the name

        :param name: name of the owner
        :return: list of all owners with a matching name
        """

        query = '''
            SELECT FirstName, LastName, ContactNumber, Email
            FROM Owners
            WHERE FirstName = %s OR LastName = %s
        '''

        cur = self._conn.cursor()
        cur.execute(query, (name, name))

        owners = []

        for row in cur.fetchall():
            owner = Owner(row[0], row[1], row[2], row[3])
            owners.append(owner)

        cur.close()
        return owners

    def get_events_by_name(self, name):
        """
        Find an event's record in the database using the name

        :param name: name of the event
        :return: list of all events with a matching name
        """

        query = '''
            SELECT EventName, Location, Date, StartTime, EndTime
            FROM Events
            WHERE EventName = %s
        '''

        cur = self._conn.cursor()
        cur.execute(query, (name,))

        events = []

        for row in cur.fetchall():
            event = Event(row[0], row[1], row[2], row[3], row[4])
            events.append(event)

        cur.close()
        return events
   
   #function to query for and display DogOwnerDetails view 
    def get_dog_owner_details(self):
        query = 'SELECT * FROM DogOwnerDetails'
        cur = self._conn.cursor()
        cur.execute(query)

        details = []

        for row in cur.fetchall():
            details.append(row)
       
        cur.close()
        return details

    def get_scores_by_dog_name(self, name):
        """
        Find a dog's scores in the database using the name

        :param name: name of the dog
        :return: list of all scores for a dog with a matching name
        """

        query = '''
            SELECT Score, JudgeFirstName, JudgeLastName
            FROM Scores
            INNER JOIN Dogs ON Scores.DogID = Dogs.ID
            WHERE Dogs.name = %s
        '''

        cur = self._conn.cursor()
        cur.execute(query, (name,))

        scores = []

        for row in cur.fetchall():
            score = Score(row[0], row[1], row[2])
            scores.append(score)

        cur.close()
        return scores

    def disconnect(self):
        self._conn.close()

    #function to create a new owner record in Datagrip using an SQL query 
    def add_owner(self, owner):
        query = '''
            INSERT INTO Owners (FirstName, LastName, ContactNumber, Email)
            VALUES (%s, %s, %s, %s);
        '''
        cur = self._conn.cursor()
        cur.execute(query, (owner.first_name, owner.last_name, owner.contact_number, owner.email))
        self._conn.commit()
        print(cur.rowcount, "record(s) affected")
        cur.close()

    #function to create a new event record in Datagrip using an SQL query 
    def add_event(self, event):
        query = '''
            INSERT INTO Events (EventName, Location, Date, StartTime, EndTime)
            VALUES (%s, %s, %s, %s, %s);
        '''
        cur = self._conn.cursor()
        cur.execute(query, (event.event_name, event.location, event.date, event.start_time, event.end_time))
        self._conn.commit()
        print(cur.rowcount, "record(s) affected")
        cur.close()

    #function to create a new score record in Datagrip using an SQL query 
    def add_score(self, score):
        query = '''
            INSERT INTO Scores (EventID, DogID, Score, JudgeFirstName, JudgeLastName)
            VALUES (%s, %s, %s, %s, %s);
        '''
        cur = self._conn.cursor()
        cur.execute(query, (score.event_id, score.dog_id, score.score, score.judge_first_name, score.judge_last_name))
        self._conn.commit()
        print(cur.rowcount, "record(s) affected")
        cur.close()

    

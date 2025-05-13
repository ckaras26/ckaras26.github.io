import os
from dotenv import load_dotenv
from dog_db import DogDB, Dog, Owner, Event, Score
from init_db import setup_database

load_dotenv()


#function to search for a dog record
def find_dogs(database):
    dog_name = input("Enter dog by name: ")
    result_set = database.get_dogs_by_name(dog_name)

    print(len(result_set), "record(s) found")
    for dog in result_set:
        print(">", dog)


#function to search for an owner record
def find_owners(database):
    owner_name = input("Enter owner by name: ")
    result_set = database.get_owners_by_name(owner_name)

    print(len(result_set), "record(s) found")
    for owner in result_set:
        print(">", owner.first_name, owner.last_name)


#funtion to search for an event record 
def find_events(database):
    event_name = input("Enter event by name: ")
    result_set = database.get_events_by_name(event_name)

    print(len(result_set), "record(s) found")
    for event in result_set:
        print(">", event.event_name)


#function to search for a score record
def find_scores(database):
    dog_name = input("Enter dog by name: ")
    result_set = database.get_scores_by_dog_name(dog_name)

    print(len(result_set), "record(s) found")
    for score in result_set:
        print(">", score.score)


#function to update a dog
def update_dog(database):
    old_dog_name = input("Enter the name of the dog to update: ")
    new_dog_name = input("Enter the updated dog name: ")
    new_dog_age = int(input("Enter the updated dog age: "))
    new_dog_breed = input("Enter the updated dog breed: ")

    updated_dogs = database.update_dog(
        old_dog_name, Dog(new_dog_name, new_dog_age, new_dog_breed)
    )

    for dog in updated_dogs:
        print(">", dog)

#function to remove a dog
def remove_dog(database):
    dog_name = input("Enter the name of the dog to delete: ")
    database.delete_dog(dog_name)


#function to add a dog 
def add_dog(database):
    dog_name = input("Enter the dog's name: ")
    dog_age = int(input("Enter the dog's age: "))
    dog_breed = input("Enter the dog's breed: ")
    owner_id = int(input("Enter the owner's ID: "))  #OwnerID is an integer in database
    database.add_dog(Dog(dog_name, dog_age, dog_breed, owner_id))  #matches the Dog constructor

#function to see the view DogOwnerDetails
def view_dog_owner_details(database):
    details = database.get_dog_owner_details()
    for detail in details:
        print(detail)


#function to create an owner
def add_owner(database):
    first_name = input("Enter the owner's first name: ")
    last_name = input("Enter the owner's last name: ")
    contact_number = input("Enter the owner's contact number: ")
    email = input("Enter the owner's email: ")

    database.add_owner(Owner(first_name, last_name, contact_number, email))


#function to add an event record
def add_event(database):
    event_name = input("Enter the event name: ")
    location = input("Enter the event location: ")
    date = input("Enter the event date: ")
    start_time = input("Enter the event start time: ")
    end_time = input("Enter the event end time: ")

    database.add_event(Event(event_name, location, date, start_time, end_time))


#function to add a score record
def add_score(database):
        event_id = int(input("Enter the event ID: "))
        dog_id = int(input("Enter the dog ID: "))
        score_value = int(input("Enter the score: "))
        judge_first_name = input("Enter the judge's first name: ")
        judge_last_name = input("Enter the judge's last name: ")
        database.add_score(Score(event_id, dog_id, score_value, judge_first_name, judge_last_name))


#function to print and implement functions in the command line
def main():
    database = DogDB(
        os.getenv("DBHOST"),
        os.getenv("DBUSERNAME"),
        os.getenv("DBPASSWORD"),
        "DogCompetitionDatabase"
    )

    quit = False

    while not quit:
        print("What operation would you like to perform?")
        print("1) Create a new dog record")
        print("2) Create a new owner record")
        print("3) Create a new event record")
        print("4) Create a new score record")
        print("5) Search for a dog record")
        print("6) Search for an owner record")
        print("7) Search for an event record")
        print("8) Search for a score record")
        print("9) View Dog and Owner Details")
        print("q) Quit")
        option = input("Please make your selection: ")

        if option == "1":
            add_dog(database)
        elif option == "2":
            add_owner(database)
        elif option == "3":
            add_event(database)
        elif option == "4":
            add_score(database)
        elif option == "5":
            find_dogs(database)
        elif option == "6":
            find_owners(database)
        elif option == "7":
            find_events(database)
        elif option == "8":
            find_scores(database)
        elif option == "9":
            view_dog_owner_details(database)
        else:
            quit = option.lower() == 'q'

        print('')

if __name__ == "__main__":
    main()
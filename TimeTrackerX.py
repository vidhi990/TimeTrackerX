#!/usr/bin/env python
# coding: utf-8

# In[14]:


# Title: Weekly Timetable Manager
# File: TimeTrackerX.py
# Author: Vidhi S. Shah
# Email ID: vidhishah2121@gmail.com

import datetime
import os 
import time

# Constants (we can change as per our requirewmnets to schedule an event) 
WORK_HOURS_START = datetime.time(9, 0)  # Work hours start time
WORK_HOURS_END = datetime.time(17, 0)  # Work hours end time

def print_title(**kwargs):
    """Prints the program's title""" #docstrings
    print("Title: Weekly TimeTable Manager")

def print_author_info(**kwargs):
    """Prints the author's name and UniSA email"""
    print("Author: Vidhi S. Shah")
    print("UniSA Email ID: vidhishah2121@gmail.com")

# Function to print the timetable overview for the whole week
def print_timetable(timetable):
    daydict = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print('\nWeekly Time-Table:')
    print('-' * 80)
    print('{:<10s} {:<25s} {:<20s} {:<15s}'.format('Day', 'Title', 'Time', 'Location'))
    print('-' * 80)
    for day in range(7):
        events = timetable[day]
        for event in events:
            title = event['title']
            onset_time = event['start'].strftime('%I:%M%p')
            offset_time = event['end'].strftime('%I:%M%p')
            location = event['location']
            print('{:<10s} {:<25s} {:<20s} {:<15s}'.format(daydict[day], title, onset_time + '-' + offset_time, location))
    print('-' * 80)

# Function to print the events for a specific day
def print_day_events(timetable, day):
    daydict = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    events = timetable[day]
    if not events:
        print(f"No events scheduled for {daydict[day]}")
        return
    print(f"Events scheduled for {daydict[day]}:")
    print('-' * 80)
    for event in events:
        title = event['title']
        onset_time = event['start'].strftime('%I:%M%p')
        offset_time = event['end'].strftime('%I:%M%p')
        location = event['location']
        print('Title: {}\nTime: {}-{}\nLocation: {}\n'.format(title, onset_time, offset_time, location))
    print('-' * 80)


# Function to create a new event
def create_event(timetable):
    """Creates a new event"""
    
    daydict = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    title = input("Input Title For the Event: ")
    onset_time_str = input("Input the starting time for the event (e.g., 10:00am): ")
    offset_time_str = input("Input the ending time for the event (e.g., 10:30am): ")
    location = input("Input the location of the event (optional): ")
    day = int(input("Enter the day of the week (1-7, where 1 is Monday): ")) - 1

    # Parse start and end times (validate time)
    onset_time = datetime.datetime.strptime(onset_time_str, '%I:%M%p').time()
    offset_time = datetime.datetime.strptime(offset_time_str, '%I:%M%p').time()

    # Check if the event falls within work hours
    if onset_time < WORK_HOURS_START or offset_time > WORK_HOURS_END:
        print("Events must be scheduled within work hours (9am - 5pm).")
        return

    # Check for overlap with existing events (validate events)
    for event in timetable[day]:
        if (onset_time >= event['start'] and onset_time < event['end']) or            (offset_time > event['start'] and offset_time <= event['end']) or            (onset_time <= event['start'] and offset_time >= event['end']):
            print("There is a scheduling conflict. Please reschedule the event.")
            return

    new_event = {
        'title': title,
        'start': onset_time,
        'end': offset_time,
        'location': location
    }
    timetable[day].append(new_event)
    print("Event scheduled successfully.")
    
    """
    daydict = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    title = input("Input Title For the Event: ")
    onset_time_str = input("Input the starting time for the event (e.g., 10:00am): ")
    onset_date_str = input("Input the date for the event (e.g., 2023-06-25): ")
    offset_time_str = input("Input the ending time for the event (e.g., 10:30am): ")
    offset_date_str = input("Input the date for the event (e.g., 2023-06-25): ")
    location = input("Input the location of the event (optional): ")
    day = int(input("Enter the day of the week (1-7, where 1 is Monday): ")) - 1

    # Parse start and end times (validate time)
    onset_datetime = datetime.datetime.strptime(onset_date_str + " " + onset_time_str, '%Y-%m-%d %I:%M%p')
    offset_datetime = datetime.datetime.strptime(offset_date_str + " " + offset_time_str, '%Y-%m-%d %I:%M%p')
    onset_time = onset_datetime.time()
    offset_time = offset_datetime.time()

    # Check if the event falls within work hours
    if onset_time < WORK_HOURS_START or offset_time > WORK_HOURS_END:
        print("Events must be scheduled within work hours (9am - 5pm).")
        return

    # Check for overlap with existing events (validate events)
    for event in timetable[day]:
        if (onset_datetime >= event['start'] and onset_datetime < event['end']) or \
           (offset_datetime > event['start'] and offset_datetime <= event['end']) or \
           (onset_datetime <= event['start'] and offset_datetime >= event['end']):
            print("There is a scheduling conflict. Please reschedule the event.")
            return

    new_event = {
        'title': title,
        'start': onset_datetime,
        'end': offset_datetime,
        'location': location
    }
    timetable[day].append(new_event)
    print("\nEvent scheduled successfully.")
    """

# Function to delete an event
def delete_event(timetable):
    keyword = input("Enter a keyword to search for the event you want to delete: ")
    day = int(input("Enter the day of the week (1-7, where 1 is Monday) of the event you want to delete: ")) - 1

    events = timetable[day]
    matching_events = []
    for event in events:
        if keyword.lower() in event['title'].lower() or (event['location'] and keyword.lower() in event['location'].lower()):
            matching_events.append(event)

    if not matching_events:
        print("No events found matching the given keyword.")
        return

    print(f"Found {len(matching_events)} events matching the keyword '{keyword}':")
    print('-' * 80)
    for i, event in enumerate(matching_events):
        title = event['title']
        onset_time = event['start'].strftime('%I:%M%p')
        offset_time = event['end'].strftime('%I:%M%p')
        location = event['location']
        print(f"Event {i+1}:")
        print('Title: {}\nWhen: {}-{}\nWhere: {}\n'.format(title, onset_time, offset_time, location))
    print('-' * 80)

    event_num = int(input("Enter the event number you want to delete: ")) - 1
    if event_num < 0 or event_num >= len(matching_events):
        print("Invalid event number.")
        return

    event_to_delete = matching_events[event_num]
    timetable[day].remove(event_to_delete)
    print("Event deleted successfully.")

# Function to update an event
def update_event(timetable):
    """Updates an existing event"""
    keyword = input("Enter a keyword to search for the event you want to update: ")
    day = int(input("Enter the day of the week (1-7, where 1 is Monday) of the event you want to update: ")) - 1

    events = timetable[day]
    matching_events = []
    for event in events:
        if keyword.lower() in event['title'].lower() or (event['location'] and keyword.lower() in event['location'].lower()):
            matching_events.append(event)

    if not matching_events:
        print("No events found matching the given keyword.")
        return

    print(f"Found {len(matching_events)} events matching the keyword '{keyword}':")
    print('-' * 80)
    for i, event in enumerate(matching_events):
        title = event['title']
        onset_time = event['start'].strftime('%I:%M%p')
        offset_time = event['end'].strftime('%I:%M%p')
        location = event['location']
        print(f"Event {i+1}:")
        print('Title: {}\nWhen: {}-{}\nWhere: {}\n'.format(title, onset_time, offset_time, location))
    print('-' * 80)

    event_num = int(input("Enter the event number you want to update: ")) - 1
    if event_num < 0 or event_num >= len(matching_events):
        print("Invalid event number.")
        return

    event_to_update = matching_events[event_num]

    print("Enter the updated event details (leave blank to keep existing values):")
    new_title = input(f"Title ({event_to_update['title']}): ")
    new_onset_time_str = input(f"Start time ({event_to_update['start'].strftime('%I:%M%p')}): ")
    new_offset_time_str = input(f"End time ({event_to_update['end'].strftime('%I:%M%p')}): ")
    new_location = input(f"Location ({event_to_update['location']}): ")

    if new_title:
        event_to_update['title'] = new_title
    if new_onset_time_str:
        new_onset_time = datetime.datetime.strptime(new_onset_time_str, '%I:%M%p').time()
        event_to_update['start'] = new_onset_time
    if new_offset_time_str:
        new_offset_time = datetime.datetime.strptime(new_offset_time_str, '%I:%M%p').time()
        event_to_update['end'] = new_offset_time
    if new_location:
        event_to_update['location'] = new_location

    print("Event updated successfully.")

def set_reminder(timetable):
    event_title = input("Enter the title of the event to set a reminder: ")

    for events in timetable:
        for event in events:
            if event['title'] == event_title:
                event_time = event['start']
                current_time = datetime.datetime.now().time()

                if event_time > current_time:
                    time_difference = datetime.datetime.combine(datetime.date.today(), event_time) - datetime.datetime.combine(datetime.date.today(), current_time)
                    time.sleep(time_difference.seconds)

                    print(f"Reminder: It's time for the event '{event['title']}' at {event_time.strftime('%I:%M%p')}!")
                else:
                    print("The event has already passed. Cannot set a reminder.")

                return

    print(f"No event found with the title '{event_title}'.")

#Function to save the Timetable
def save_timetable(timetable, DocumentTitle):
    """Function to save the scheduled events into a file using file handling"""
    dictt = r"C:\Users\Happy Patel\Desktop\timetable_folder"  # dictt to store the timetable files

    #  generate a new dict if not in existence
    if not os.path.exists(dictt):
        os.makedirs(dictt)

    filepath = os.path.join(dictt, DocumentTitle)  # Full file path

    with open(filepath, 'w') as file:
        for day, events in enumerate(timetable):
            day_name = datetime.datetime.strptime(str(day), "%w").strftime("%A")  # Convert day index to day name
            for event in events:
                file.write("{}|{}|{}|{}|{}\n".format(day_name,
                                                     event['title'],
                                                     event['start'].strftime("%I:%M%p"),
                                                     event['end'].strftime("%I:%M%p"),
                                                     event['location']))

#Function to load tiimetable
def load_timetable(DocumentTitle):
    """Function to load the scheduled events back from the saved file"""
    dictt = r"C:\Users\Happy Patel\Desktop\timetable_folder"  # dictt where the timetable files are stored
    filepath = os.path.join(dictt, DocumentTitle)  # Full file path

    timetable = [[] for _ in range(7)]  # Initialize an empty timetable

    with open(filepath, 'r') as file:
        for line in file:
            data = line.strip().split('|')
            day_name = data[0]
            title = data[1]
            onset_time = datetime.datetime.strptime(data[2], "%I:%M%p").time()
            offset_time = datetime.datetime.strptime(data[3], "%I:%M%p").time()
            location = data[4]
            event = {'title': title, 'start': onset_time, 'end': offset_time, 'location': location}

            day = datetime.datetime.strptime(day_name, "%A").weekday()  # Convert day name to day index
            timetable[day].append(event)

    return timetable
    
# Main function
def main():
    """Main function to manage the weekly timetable"""
    # Initialize the timetable
    print_title()
    print_author_info()
    timetable = [[] for _ in range(7)]
    #calling the doc_string function
   
    while True:
        # Print menu options
        print("\nMenu Options:")
        print("1. Schedule a New Event")
        print("2. View The Events For A Specific Day")
        print("3. Update an Existing Event")
        print("4. View The Timetable Overview For The Whole Week")
        print("5. Delete an Existing Event")
        print("6. Save timetable to a file")
        print("7. Load timetable from a file")
        print("8. Set Reminder")
        print("9. Exit The Program\n")

        choice = input("Enter your choice from (1-8): ")

        if choice == '1':  # Create an event
            create_event(timetable)
        elif choice == '2': # Print events for a specific day
            day = int(input("Enter the day of the week (1-7, where 1 is Monday): ")) - 1
            if day < 0 or day >= 7:
                print("Invalid Day Choice. Please Enter A Day From Given Options!!")
                continue
            print_day_events(timetable, day)
        elif choice == '3':  # Update an event
             update_event(timetable)
        elif choice == '4': # Print timetable for the whole week
            print_timetable(timetable)
        elif choice == '5': # Delete an event
            delete_event(timetable)
        elif choice == '6':  # Save timetable to a file
            DocumentTitle = input("Enter the DocumentTitle to save the timetable: ")
            save_timetable(timetable, DocumentTitle)
            print("Timetable saved successfully.")
        elif choice == '7':  # Load timetable from a file
            DocumentTitle = input("Enter the DocumentTitle to load the timetable from: ")
            timetable = load_timetable(DocumentTitle)
            print("Timetable loaded successfully.")
        elif choice == '8': # Set a reminder for an event
            set_reminder(timetable)
        elif choice == '9': # Quit/Exit
            print("Program Exited!! Thank you for using the Weekly TimeTable Manager!")
            return 0
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()


# In[ ]:





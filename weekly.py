import datetime
import calendar

def get_weekly_schedule(year, frequency):
    # Get the current date and day of the week
    today = datetime.date.today()
    current_day = today.weekday()  # Monday is 0 and Sunday is 6
    current_month = today.month

    # Calculate number of schedules in the year
    num_schedules = frequency  # Frequency defines how many times the schedule should occur in a year
    
    schedules = []
    
    # Generate schedule for the year
    for i in range(num_schedules):
        # Calculate the start date of the week for this schedule
        start_date = get_start_date_of_week(year, i, frequency)
        # The end date is the Saturday of that week (start_date + 5 days)
        end_date = start_date + datetime.timedelta(days=5)  # Monday to Saturday

        schedules.append({
            'schedule': i + 1,
            'start_date': start_date,
            'end_date': end_date
        })

    return schedules

def get_start_date_of_week(year, index, frequency):
    """ Get the start date (Monday) of the week for the schedule """
    # Determine which week to start on based on the index and frequency
    week_interval = 52 // frequency  # Divide the year into approximately equal intervals
    
    # We assume the first Monday of the year is the start of the first week
    first_day_of_year = datetime.date(year, 1, 1)
    # Find the first Monday of the year
    first_monday = first_day_of_year + datetime.timedelta(days=(7 - first_day_of_year.weekday()) % 7)

    # Calculate the start of the desired week
    start_date = first_monday + datetime.timedelta(weeks=week_interval * index)
    
    # Ensure the date is valid (not out of range)
    if start_date.year != year:
        raise ValueError(f"The calculated start date {start_date} is out of the specified year {year}.")
    
    return start_date

# Test the function
year = 2025
frequency = 2  # Schedule 2 times a year
schedule = get_weekly_schedule(year, frequency)
for entry in schedule:
    print(f"Schedule {entry['schedule']} - Start: {entry['start_date']} End: {entry['end_date']}")

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
            
VALID_MONTH_OPTIONS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

VALID_WEEKDAY_OPTIONS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_user_input(prompt, valid_input_list):
    """
    Displays prompt and gets input from user. 
    Repeats until user enters one of the valid inputs (case insensitive).

    Args:
        (str) prompt - prompt displayed to user. If prompt contains {} replaces with title-cased
                       version of valid_input_list
        (list of str) valid_input_list - lower case list of strings of acceptable inputs

    Returns:
        (str) lower-case response by user from one of the valid_input_list
    """

    # add valid_input_list options to {} (if any) in prompt
    prompt = prompt.format(', '.join(valid_input_list).title())

    while True:
        response = input(prompt).lower()
        if response in valid_input_list:
            return response
        else:
            print('\nSorry, that is not a valid input.')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_user_input('\nEnter city ({}): ', CITY_DATA.keys())

    month = get_user_input('\nEnter month ({}): ', VALID_MONTH_OPTIONS)

    weekday = get_user_input('\nEnter day of week ({}): ', VALID_WEEKDAY_OPTIONS)

    print('-'*40)
    return city, month, weekday

def show_raw_data(df):
    """ 
    Displays first 5 rows of raw dataframe on user request 
    """

    while True:
        do_preview = input('\nWould you like to preview the first five rows of this table? (y/n): ').lower() == 'y'
        print()

        if do_preview:
            print(df.head())
        else:
            break
        
    

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    show_raw_data(df)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and start hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')
    df['start_hour'] = df['Start Time'].dt.strftime('%I %p')

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month =  VALID_MONTH_OPTIONS.index(month)
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def column_exists(df, col_name):
    """ 
    Checks that col_name is a valid column in df. Displays an error message if not.

    Returns: true if col_name is valid, else false.
    """

    if col_name not in df.columns:
        print('Warning: \'{}\' not in data file.'.format(col_name))
        return False
    return True

def display_popular_stats(df, col_name, col_display_name, display_lookup_list = None):
    """
    Displays the most popular stats for a single column element (e.g., month, day of week, or start time).

    Args:
        (str) col_name - name of the column to analyze
        (str) col_display_name - the display name for this data column (e.g., "day of the week")
        (str) display_lookup_list - optional lookup list for display of the most popular element rather
            than displaying the raw data in the table (e.g., "June" instead of 6)
    """

    # check first that this column exists in the dataframe
    if not column_exists(df, col_name):
        return

    popular_element = df[col_name].mode()[0]
    popular_element_str = str(popular_element)

    if display_lookup_list:
        popular_element_str = display_lookup_list[popular_element].title()

    popular_element_trips = df[col_name].value_counts()[popular_element]
    total_trips = df[col_name].notnull().sum()

    popular_element_percent = popular_element_trips / total_trips * 100

    print('The most popular {} was: {} with {} trips out of {} total ({:.2f}%).\n'.format(
        col_display_name,
        popular_element_str,
        popular_element_trips,
        total_trips,
        popular_element_percent))

def print_run_time(start_time):
    """ 
    Helper function to print the duration of each task run as delta time 
    from start_time to current time.

    Args:
        (float) start_time: time when task was begun.
    """

    print("\nThis took {:.5f} seconds.".format(time.time() - start_time))
    print('-'*40)

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    display_popular_stats(df, 'month', 'Month', VALID_MONTH_OPTIONS)
  
    # display the most common day of week
    display_popular_stats(df, 'day_of_week', 'Day of the Week')
 
    # display the most common start hour
    display_popular_stats(df, 'start_hour', 'Start Hour for a Trip')

    print_run_time(start_time)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    display_popular_stats(df, 'Start Station', 'Trip Starting Station')

    # display most commonly used end station
    display_popular_stats(df, 'End Station', 'Trip Ending Station')

    # display most frequent combination of start station and end station trips
    if column_exists(df, 'Start Station') and column_exists(df, 'End Station'):
        popular_start_end = df.groupby(['Start Station', 'End Station'])['End Station'].count().sort_values(ascending=False)
        total_trips = df['End Station'].notnull().sum()

        print('The most popular Start Station/End Station Pair was: {}'.format(popular_start_end.index[0]))
        print('    with {} trips out of {} total trips ({:.2f}%).\n'.format(
            popular_start_end[0],
            total_trips,
            popular_start_end[0] / total_trips * 100))

    print_run_time(start_time)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    if column_exists(df, 'Trip Duration'):
        # display total travel time
        total_duration = df['Trip Duration'].sum()
        print('Total Duration of all trips (sec): {}\n'.format(total_duration))

        # display mean travel time
        avg_duration = df['Trip Duration'].mean()
        print('Mean Duration of all trips (sec): {:.2f}\n'.format(avg_duration))

    print_run_time(start_time)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if column_exists(df, 'User Type'):
        user_types = df['User Type'].value_counts().to_frame()
        user_types['Percent'] = df['User Type'].value_counts(normalize = True).to_frame()
        print(user_types)
        print()

    # Display counts of gender
    if column_exists(df, 'Gender'):
        genders = df['Gender'].value_counts().to_frame()
        genders['Percent'] = df['Gender'].value_counts(normalize = True).to_frame()
        print(genders)

    if column_exists(df, 'Birth Year'):
        # Display earliest, most recent, and most common year of birth
        oldest_user_birth_year = int(df['Birth Year'].min())
        print('\nBirth year of Oldest User: {}\n'.format(oldest_user_birth_year))

        youngest_user_birth_year = int(df['Birth Year'].max())
        print('Birth year of Youngest User: {}\n'.format(youngest_user_birth_year))

        commonest_birth_year = int(df['Birth Year'].mode()[0])
        print('Most Common birth year: {}\n'.format(commonest_birth_year))

    print_run_time(start_time)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? (y/n): ').lower() == 'y'
        print()
        if not restart:
            break

if __name__ == "__main__":
	main()

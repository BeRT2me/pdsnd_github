import time
import calendar
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (int/string) hour - hour of the day to filter by, or "all" to apply no hour filter
    """
    city, month, day, hour = '', '', '', ''
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in CITY_DATA.keys():
        city = input("Which city would you like to analyze? Valid choices include: {}.\n".format(
            ', '.join(CITY_DATA.keys()).title()))
        city = city.lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("Invalid city, please try again.")
    # get user input for month (all, january, february, ... , june)
    while month not in valid_months:
        month = input("Which month would you like to analyze? Valid choices include: {}.\n".format(
            ', '.join(valid_months).title()))
        month = month.lower()
        if month in valid_months:
            break
        else:
            print("Invalid choice, please try again.")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in valid_days:
        day = input(
            "Which day would you like to analyze? Valid choices include: {}.\n".format(', '.join(valid_days).title()))
        day = day.lower()
        if day in valid_days:
            break
        else:
            print("Invalid choice, please try again.")
    while hour not in range(0, 24):
        hour = input("Which start hour would you like to analyze? Valid choices range from [0 to 23] or All.\n")
        try:
            hour = int(hour)
        except ValueError:
            hour = hour.lower()
            if hour == 'all':
                break
            print("Invalid choice, please try again.")
            continue
        if hour in range(0, 24):
            break
        else:
            print("Invalid choice, please try again.")
    print('-' * 40)
    return city, month, day, hour


def load_data(city, month, day, hour):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (int/string) hour - hour of day to filter by, or "all" to apply no hour filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # drop random first column
    df.drop(df.columns[[0]], inplace=True, axis=1)
    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]
    # creates start hours column
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df['start_hour'] = df['Start Time'].dt.hour
    # filter by hour of day if applicable
    if hour != 'all':
        df = df[df['start_hour'] == hour]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month was: {}.".format(calendar.month_name[popular_month]))
    # display the most common day of week using calendar to go from int to name
    popular_day = df['day_of_week'].mode()[0]
    print("The most common day of week was: {}.".format(calendar.day_name[popular_day]))
    # display the most common start hour
    popular_hour = df['start_hour'].mode()[0]
    print("The most common start hour was:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most common Start Station was:", popular_start_station + ".")
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most common End Station was:", popular_end_station + ".")
    # creates trip column
    df['Trip'] = df['Start Station'] + ' -> ' + df['End Station']
    # display most frequent combination of start station and end station trip
    popular_combination = df['Trip'].mode()[0]
    print("The most common trip was:", popular_combination + ".")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df["End Time"] = pd.to_datetime(df["End Time"])
    df['travel time'] = df["End Time"] - df["Start Time"]
    total_time = df['travel time'].sum()
    print("The total travel time was: {} days, {} hours, {} minutes and {} seconds.".format(
        total_time.days,
        total_time.seconds // 3600,
        total_time.seconds % 3600 // 60,
        total_time.seconds % 3600 % 60))
    # display mean travel time
    avg_time = df['travel time'].mean()
    print("The mean travel time was: {} days, {} hours, {} minutes and {} seconds.".format(
        avg_time.days,
        avg_time.seconds // 3600,
        avg_time.seconds % 3600 // 60,
        avg_time.seconds % 3600 % 60))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Types:")
    for index, row in zip(user_types.index, user_types):
        print("\t", index, "\n\t\tCount:", row)
    try:
        # Display counts of gender
        genders = df['Gender'].value_counts()
        print("\nGenders:")
        for index, row in zip(genders.index, genders):
            print("\t", index, "\n\t\tCount:", row)
        # Display earliest, most recent, and most common year of birth
        print("\nYoungest traveler birth year:", int(df['Birth Year'].max()))
        print("\nOldest traveler birth year:", int(df['Birth Year'].min()))
        print("\nMost frequent traveler birth year:", int(df['Birth Year'].mode()[0]))
    except KeyError:
        print("\nInformation about Gender and/or Birth Year not available for {}.".format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_panda(df):
    """Displays 5 rows of the filtered data frame and prompts to allow additional rows to be viewed."""
    i = 0
    display = ''
    while True:
        display = input("\nWould you like to see 5 {more}lines of raw data? Enter yes to continue or anything to "
                        "stop.\n".format(more="more " if display == "yes" else ''))
        if display.lower() != 'yes':
            print("\nStopping...")
            print('-' * 40)
            return
        else:
            print(df[i:i+5])
            i += 5


def main():
    while True:
        city, month, day, hour = get_filters()
        df = load_data(city, month, day, hour)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_panda(df)
        restart = input('\nWould you like to restart? Enter yes to continue or anything to exit.\n')
        if restart.lower() != 'yes':
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()

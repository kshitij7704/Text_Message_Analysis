import re
import pandas as pd

def preprocess(data):
    """
    Preprocesses the chat data to create a structured DataFrame with relevant information.

    Args:
        data (str): Raw chat data.

    Returns:
        pd.DataFrame: Processed DataFrame containing structured chat information.
    """
    # Regex pattern to identify timestamps in the format "dd/mm/yy, hh:mm am/pm"
    pattern = r'\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{1,2}\s(?:am|pm)'

    # Split the raw data into message parts and dates using regex pattern
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Replace non-breaking spaces with regular spaces in dates
    dates = [date.replace('\u202f', ' ') for date in dates]

    # Create a DataFrame with messages and corresponding dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert the 'message_date' to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p')

    # Rename column 'message_date' to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract user and message information
    users, messages = [], []
    for message in df['user_message']:
        # Split message by the first occurrence of a user: 'user_name: message'
        entry = re.split(r'([\w\W]+?):\s', message)
        
        # If the split was successful, append the user and the message
        if len(entry) > 1:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            # Handle group notifications where no user is mentioned
            users.append('group_notification')
            messages.append(entry[0])

    # Add 'user' and 'message' columns to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the 'user_message' column as it's no longer needed
    df.drop(columns=['user_message'], inplace=True)

    # Extract date-related columns
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Assign time periods based on the hour of the day (e.g., 0-1, 1-2, ..., 23-00)
    df['period'] = df['hour'].apply(lambda hour: f'{hour:02d}-{(hour+1)%24:02d}')

    return df
import re
import pandas as pd

def preprocess(data):
    """
    Processes WhatsApp chat data to extract messages, timestamps, and user details.

    Parameters:
        data (str): Raw chat export data.

    Returns:
        pd.DataFrame: Processed chat data.
    """

    # WhatsApp timestamp pattern (supports AM/PM format)
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2}\s(?:AM|PM)'

    # Extract messages and timestamps
    messages = re.split(pattern, data)[1:]  # Skip first empty split
    dates = re.findall(pattern, data)

    # Handle non-breaking spaces in timestamps
    dates = [date.replace('\u202f', ' ') for date in dates]

    # Ensure the lengths match
    if len(messages) != len(dates):
        print(f"Warning: Mismatch found! Messages: {len(messages)}, Dates: {len(dates)}")
        min_len = min(len(messages), len(dates))
        messages = messages[:min_len]
        dates = dates[:min_len]

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert 'message_date' column to datetime (handles invalid dates)
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p', errors='coerce')

    # Drop rows with invalid dates
    df = df.dropna(subset=['message_date'])
    
    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract users and messages
    users, messages_clean = [], []

    for message in df['user_message']:
        # Improved regex for extracting usernames properly
        entry = re.split(r'^([^:]+):\s', message.strip(), maxsplit=1)
        
        if len(entry) > 2:  # Message contains a username
            users.append(entry[1])
            messages_clean.append(entry[2])
        else:  # System notification (e.g., "User joined the group")
            users.append('group_notification')
            messages_clean.append(entry[0])

    df['user'] = users
    df['message'] = messages_clean
    df.drop(columns=['user_message'], inplace=True)

    # Extract date components
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Define time periods efficiently
    df['period'] = df['hour'].astype(str) + "-" + ((df['hour'] + 1) % 24).astype(str)

    return df
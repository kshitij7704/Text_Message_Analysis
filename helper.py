from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

# Initialize URL extractor
extract = URLExtract()

def fetch_stats(selected_user, df):
    """
    Fetch statistics like number of messages, words, media messages, and links for a given user.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Number of messages
    num_messages = df.shape[0]

    # Number of words
    words = [word for message in df['message'] for word in message.split()]

    # Number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    # Number of links shared
    links = [link for message in df['message'] for link in extract.find_urls(message)]

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    """
    Get the most active users and the percentage of messages they contributed.
    """
    user_counts = df['user'].value_counts().head()
    
    user_percentages = (df['user'].value_counts() / df.shape[0]) * 100
    user_percentages = round(user_percentages, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    
    return user_counts, user_percentages


def create_wordcloud(selected_user, df):
    """
    Generate a word cloud for the messages of the selected user.
    """
    with open('stop_hinglish.txt', 'r') as file:
        stop_words = file.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out group notifications and media messages
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]

    # Function to remove stop words from a message
    def remove_stop_words(message):
        return " ".join([word for word in message.lower().split() if word not in stop_words])

    # Apply stop word removal and generate word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    wordcloud = wc.generate(temp['message'].str.cat(sep=" "))
    
    return wordcloud


def most_common_words(selected_user, df):
    """
    Get the most common words used by the selected user.
    """
    with open('stop_hinglish.txt', 'r') as file:
        stop_words = file.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out group notifications and media messages
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]

    # Collect words and filter stop words
    words = [word for message in temp['message'] for word in message.lower().split() if word not in stop_words]

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    """
    Analyze the emojis used by the selected user.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Extract emojis from the messages
    emojis = [c for message in df['message'] for c in message if emoji.is_emoji(c)]

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    """
    Create a timeline of message counts per month for the selected user.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Create a timeline with month-year format
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    
    return timeline


def daily_timeline(selected_user, df):
    """
    Create a timeline of message counts per day for the selected user.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    """
    Create a map of message activity by day of the week for the selected user.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    """
    Create a map of message activity by month for the selected user.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    """
    Generate a heatmap of user activity by day and time period.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap
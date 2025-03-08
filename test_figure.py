from wordcloud import WordCloud


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
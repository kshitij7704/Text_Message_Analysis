import streamlit as st
import preprocess, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title of the sidebar
st.set_page_config(page_title="Text Message Analyzer", page_icon="📊", layout="wide")
st.sidebar.title("Text Message Analyzer")

# Add a background color to the sidebar for better visibility
st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f0f5;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# File uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a file")

# Check if a file is uploaded
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)

    # Fetch unique users and create a user list
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    # User selection for analysis
    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    # Show Analysis Button
    if st.sidebar.button("Show Analysis"):

        # Top Statistics Section
        st.title("📊 Top Statistics")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        
        # Arrange statistics in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.subheader(num_messages)
        with col2:
            st.header("Total Words")
            st.subheader(words)
        with col3:
            st.header("Media Shared")
            st.subheader(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.subheader(num_links)

        # Monthly Timeline Section
        st.title("📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Daily Timeline Section
        st.title("📅 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Activity Map Section
        st.title("🗓️ Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        # Weekly Activity Map Section
        st.title("📅 Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Busiest Users (Group level)
        if selected_user == 'Overall':
            st.title('👥 Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud Section
        st.title("🌸 Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        # Most Common Words Section
        st.title("📝 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='teal')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Emoji Analysis Section
        st.title("😀 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f", colors=sns.color_palette("Set3", len(emoji_df[0].head())))
            st.pyplot(fig)
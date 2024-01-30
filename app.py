import streamlit as st 
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='2024 Bookshelf', page_icon='📚', layout='wide')

# Colors
# Green - #8da683
# Yellow/Brown - #be8f3c
# Yellow - #d99d29
# Off-White - #f2dcb1
# Orange - #dc8920

st.title("📚 2024 Bookshelf")

# book data

jan_book_data = [
    {"Title": "Beyond the Story: 10 Year Record of BTS", "Author": "Kang Myeong-seok, BTS", "Genre": "Nonfiction", "Language": "English", "Start Date": '12-26-2023', "End Date": '01-02-2024', "Rating": 4, "Pages": 544},
    {"Title": "Jujutsu Kaisen #10", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '01-03-2024', "End Date": '01-06-2024', "Rating": 5, "Pages": 192},
    {"Title": "The Exiled Fleet", "Author": "J.S. Dewes", "Genre": "Science Fiction", "Language": "English", "Start Date": '01-21-2024', "End Date": '01-27-2024', "Rating": 5, "Pages": 420},
    {"Title": "A Court of Thorns and Roses", "Author": "Sarah J. Dewes", "Genre": "Fantasy", "Language": "English", "Start Date": '01-28-2024', "End Date": '02-03-2024', "Rating": 5, "Pages": 419}
]
jan_books = pd.DataFrame(jan_book_data)


with st.sidebar:
    st.write("Select a month")
    selected_month = st.selectbox("month", options=["Entire Year", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], label_visibility="collapsed")


if selected_month == "Entire Year":
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Books Read", value=f"{len(jan_books)}")
    with col2:
        st.metric(label="Average Rating", value=f"{round(jan_books['Rating'].mean(), 2)}")
    with col3:
        st.metric(label="Favorite Genre", value=f"{jan_books['Genre'].value_counts().idxmax()}")

    col4, col5 = st.columns(2)

    with col4:
        colors = ["#be8f3c", "#d99d29", "#f2dcb1", "#dc8920"]
        fig = px.pie(jan_books, names='Genre', title='Genre Distribution',  color_discrete_sequence=colors)
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

elif selected_month == "January":
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Books Read", value=f"{len(jan_books)}")
    with col2:
        st.metric(label="Average Rating", value=f"{round(jan_books['Rating'].mean(), 2)}")
    with col3:
        st.metric(label="Favorite Genre", value=f"{jan_books['Genre'].value_counts().idxmax()}")

    col4, col5 = st.columns(2)

    with col4:
        colors = ["#be8f3c", "#d99d29", "#f2dcb1", "#dc8920"]
        fig = px.pie(jan_books, names='Genre', title='Genre Distribution',  color_discrete_sequence=colors)
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)
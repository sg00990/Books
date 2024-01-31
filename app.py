import streamlit as st 
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title='2024 Bookshelf', page_icon='📚', layout='wide')

# Colors
# Green - #8da683
# Yellow/Brown - #be8f3c
# Yellow - #d99d29
# Off-White - #f2dcb1
# Orange - #dc8920

st.title("📚 2024 Bookshelf")

# get book info
def get_author(book_title):
    author = df.loc[df['Title'] == book_title, 'Author'].iloc[0]
    return author if not pd.isnull(author) else f"No information found for '{book_title}'"

def get_genre(book_title):
    author = df.loc[df['Title'] == book_title, 'Genre'].iloc[0]
    return author if not pd.isnull(author) else f"No information found for '{book_title}'"

def get_language(book_title):
    author = df.loc[df['Title'] == book_title, 'Language'].iloc[0]
    return author if not pd.isnull(author) else f"No information found for '{book_title}'"

def get_pages(book_title):
    author = df.loc[df['Title'] == book_title, 'Pages'].iloc[0]
    return author if not pd.isnull(author) else f"No information found for '{book_title}'"

# book data per month
jan_book_data = [
    {"Title": "Beyond the Story: 10 Year Record of BTS", "Author": "Kang Myeong-seok, BTS", "Genre": "Nonfiction", "Language": "English", "Start Date": '12-26-2023', "End Date": '01-02-2024', "Rating": 4, "Pages": 544},
    {"Title": "Jujutsu Kaisen #10", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '01-03-2024', "End Date": '01-06-2024', "Rating": 5, "Pages": 192},
    {"Title": "The Exiled Fleet", "Author": "J.S. Dewes", "Genre": "Science Fiction", "Language": "English", "Start Date": '01-21-2024', "End Date": '01-27-2024', "Rating": 5, "Pages": 420}
]
jan_books = pd.DataFrame(jan_book_data)

feb_book_data = [
        {"Title": "A Court of Thorns and Roses", "Author": "Sarah J. Dewes", "Genre": "Fantasy", "Language": "English", "Start Date": '01-28-2024', "End Date": '02-03-2024', "Rating": 5, "Pages": 419}
]
feb_books = pd.DataFrame(feb_book_data)


with st.sidebar:
    st.write("Select a month")
    selected_month = st.selectbox("month", options=["Entire Year", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], label_visibility="collapsed")

colors = ["#8da683", "#be8f3c", "#d99d29", "#f2dcb1", "#dc8920"]

if selected_month == "Entire Year":
    col1, col2, col3 = st.columns(3)

    book_df = pd.concat([jan_books, feb_books], axis=0)
    book_dict = book_df.to_dict(orient="records")


    with col1:
        st.metric(label="Books Read", value=f"{len(book_df)}")
    with col2:
        st.metric(label="Average Rating", value=f"{round(book_df['Rating'].mean(), 2)}")
    with col3:
        st.metric(label="Favorite Genre", value=f"{book_df['Genre'].value_counts().idxmax()}")

    col4, col5 = st.columns(2)

    with col4:

        st.write("###")
        
        # language dist
        languages = [book["Language"] for book in book_dict]

        language_counts = {lang: languages.count(lang) for lang in set(languages)}

        st.write("**Language Distribution in Books**")

        language_data = {"Language": list(language_counts.keys()), "# of Books": list(language_counts.values())}
        fig = px.bar(language_data, x="Language", y="# of Books", color="Language", color_discrete_sequence=colors)
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

        st.write("###")

        # page count vs. rating
        st.write("**Book Ratings vs. Page Count**")
        fig = px.scatter(book_df, x='Pages', y='Rating', color='Title', hover_data=['Title', 'Author'], color_discrete_sequence=colors)
        fig.update_yaxes(range=[.5, 5.5])
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

        
    
    with col5:

        st.write("###")
        # duration chart
        book_df['End Date'] = pd.to_datetime(book_df['End Date'])

        book_df['Cumulative Pages'] = book_df['Pages'].cumsum()

        st.write("**Reading Progress Over Time**")

        fig = px.line(book_df, x='End Date', y='Cumulative Pages',
                    labels={'Cumulative Pages': 'Total Pages Read', 'End Date': 'Date'}, color_discrete_sequence=colors)
        
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)

        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Total Pages Read',
            hovermode='x unified'
        )

        st.plotly_chart(fig)

        st.write("###")

        # author wordcloud
        authors_text = ", ".join([book["Author"] for book in book_dict])

        def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            return random.choice(colors)

        # Create a word cloud
        wordcloud = WordCloud(width=800, height=700, background_color='white', color_func=custom_color_func).generate(authors_text)

        # Plot the word cloud using Matplotlib
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        # Streamlit app
        st.write("**Author Word Cloud**")
        st.pyplot(plt)



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

        # genre dist
        fig = px.pie(jan_books, names='Genre', title='Genre Distribution',  color_discrete_sequence=colors)
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

        # page count
        df_sorted = jan_books.sort_values(by="Pages", ascending=False)

        # Create a bar chart for page counts using Plotly Express
        fig = px.bar(x=df_sorted["Title"], y=df_sorted["Pages"], labels={'x':'Book Title', 'y':'Page Count'}, color=df_sorted["Title"], title='Page Count', color_discrete_sequence=colors)
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)
    
    with col5:

        # duration chart
        for book in jan_book_data:
            book["Start Date"] = pd.to_datetime(book["Start Date"])
            book["End Date"] = pd.to_datetime(book["End Date"])
        for book in jan_book_data:
            book["Duration"] = (book["End Date"] - book["Start Date"]).days
        
        df = pd.DataFrame(jan_book_data)
        df = df.sort_values(by="Duration", ascending=False)

        fig = px.bar(df, x="Title", y="Duration", color="Title", title="Book Durations", labels={"Duration": "Days"}, color_discrete_sequence=colors)
        fig.update_layout(barmode='stack')
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

        # page count vs. rating
        fig = px.box(jan_books, y='Rating', title='Book Ratings', color_discrete_sequence=colors)
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    st.subheader("About")

    with st.expander("Beyond the Story: 10 Year Record of BTS"):
        col6, col7 = st.columns(2)

        with col6:
            st.image("img/bts_book.png", width=350)

        with col7:
            st.write("**Title:** Beyond the Story: 10 Year Record of BTS")

            author_result = get_author("Beyond the Story: 10 Year Record of BTS")
            st.write(f"**Author:** {author_result}")

            genre_result = get_genre("Beyond the Story: 10 Year Record of BTS")
            st.write(f"**Genre:** {genre_result}")

            language_result = get_language("Beyond the Story: 10 Year Record of BTS")
            st.write(f"**Language:** {language_result}")

            page_result = get_pages("Beyond the Story: 10 Year Record of BTS")
            st.write(f"**Number of Pages:** {page_result}")

        st.write("**Summary:** BTS shares personal, behind-the-scenes stories of their journey so far through interviews and more than three years of in-depth coverage by Myeongseok Kang, who has written about K-pop and other Korean pop culture in various media. Presented chronologically in seven chapters from before the debut of BTS to the present, their vivid voices and opinions harmonize to tell a sincere, lively, and deep story. In individual interviews that have been conducted without a camera or makeup, they illuminate their musical journey from multiple angles and discuss its significance.")


    with st.expander("Jujutsu Kaisen #10"):
        col6, col7 = st.columns(2)

        with col6:
            st.image("img/jjk_10.jpg", width=250)

        with col7:
            st.write("**Title:** Jujutsu Kaisen #10")

            author_result = get_author("Jujutsu Kaisen #10")
            st.write(f"**Author:** {author_result}")

            genre_result = get_genre("Jujutsu Kaisen #10")
            st.write(f"**Genre:** {genre_result}")

            language_result = get_language("Jujutsu Kaisen #10")
            st.write(f"**Language:** {language_result}")

            page_result = get_pages("Jujutsu Kaisen #10")
            st.write(f"**Number of Pages:** {page_result}")

        st.write("**Summary:** In order to regain use of his crippled body, Kokichi Muta, otherwise known as Mechamaru, has been acting as an informant for the cursed spirits. He’s prepared for the betrayal when he’s thrust into a battle to the death against Mahito, but is knowing his enemy enough against a cursed spirit whose powers keep growing exponentially?")


    with st.expander("The Exiled Fleet"):
        col6, col7 = st.columns(2)

        with col6:
            st.image("img/tef_book.jpg", width=350)

        with col7:
            st.write("**Title:** The Exiled Fleet")

            author_result = get_author("The Exiled Fleet")
            st.write(f"**Author:** {author_result}")

            genre_result = get_genre("The Exiled Fleet")
            st.write(f"**Genre:** {genre_result}")

            language_result = get_language("The Exiled Fleet")
            st.write(f"**Language:** {language_result}")

            page_result = get_pages("The Exiled Fleet")
            st.write(f"**Number of Pages:** {page_result}")

        st.write("**Summary:** The Sentinels narrowly escaped the collapsing edge of the Divide. They have mustered a few other surviving Sentinels, but with no engines they have no way to leave the edge of the universe before they starve. Adequin Rake has gathered a team to find the materials they'll need to get everyone out.")


elif selected_month == "February":
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Books Read", value=f"{len(feb_books)}")
    with col2:
        st.metric(label="Average Rating", value=f"{round(feb_books['Rating'].mean(), 2)}")
    with col3:
        st.metric(label="Favorite Genre", value=f"{feb_books['Genre'].value_counts().idxmax()}")

    col4, col5 = st.columns(2)

    colors = ["#8da683", "#be8f3c", "#d99d29", "#f2dcb1", "#dc8920"]

    with col4:

        # genre dist
        fig = px.pie(feb_books, names='Genre', title='Genre Distribution',  color_discrete_sequence=colors)
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

        # page count
        df_sorted = feb_books.sort_values(by="Pages", ascending=False)

        # Create a bar chart for page counts using Plotly Express
        fig = px.bar(x=df_sorted["Title"], y=df_sorted["Pages"], labels={'x':'Book Title', 'y':'Page Count'}, color=df_sorted["Title"], title='Page Count', color_discrete_sequence=colors)
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)
    
    with col5:

        # duration chart
        for book in feb_book_data:
            book["Start Date"] = pd.to_datetime(book["Start Date"])
            book["End Date"] = pd.to_datetime(book["End Date"])
        for book in feb_book_data:
            book["Duration"] = (book["End Date"] - book["Start Date"]).days
        
        df = pd.DataFrame(feb_book_data)
        df = df.sort_values(by="Duration", ascending=False)

        fig = px.bar(df, x="Title", y="Duration", color="Title", title="Book Durations", labels={"Duration": "Days"}, color_discrete_sequence=colors)
        fig.update_layout(barmode='stack')
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

        # page count vs. rating
        fig = px.box(feb_books, y='Rating', title='Book Ratings', color_discrete_sequence=colors)
        fig.update_layout(width=400, height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    st.subheader("About")

    with st.expander("A Court of Thorns and Roses"):
        col6, col7 = st.columns(2)

        with col6:
            st.image("img/acotar_book.jpg", width=250)

        with col7:
            st.write("**Title:** A Court of Thorns and Roses")

            author_result = get_author("A Court of Thorns and Roses")
            st.write(f"**Author:** {author_result}")

            genre_result = get_genre("A Court of Thorns and Roses")
            st.write(f"**Genre:** {genre_result}")

            language_result = get_language("A Court of Thorns and Roses")
            st.write(f"**Language:** {language_result}")

            page_result = get_pages("A Court of Thorns and Roses")
            st.write(f"**Number of Pages:** {page_result}")

        st.write("**Summary:** When nineteen-year-old huntress Feyre kills a wolf in the woods, a terrifying creature arrives to demand retribution. Dragged to a treacherous magical land she knows about only from legends, Feyre discovers that her captor is not truly a beast, but one of the lethal, immortal faeries who once ruled her world.")

elif selected_month == "March":
    st.write("No data yet.")

elif selected_month == "April":
    st.write("No data yet.")

elif selected_month == "May":
    st.write("No data yet.")

elif selected_month == "June":
    st.write("No data yet.")

elif selected_month == "July":
    st.write("No data yet.")

elif selected_month == "August":
    st.write("No data yet.")

elif selected_month == "September":
    st.write("No data yet.")

elif selected_month == "October":
    st.write("No data yet.")

elif selected_month == "November":
    st.write("No data yet.")

elif selected_month == "December":
    st.write("No data yet.")
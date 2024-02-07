# imports
import streamlit as st 
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random
from typing import List

st.set_page_config(page_title='2024 Bookshelf', page_icon='📚', layout='wide')

# get book info
def get_author(book_title, df):
    author = df.loc[df['Title'] == book_title, 'Author'].iloc[0]
    return author if not pd.isnull(author) else f"No information found for '{book_title}'"

def get_genre(book_title, df):
    author = df.loc[df['Title'] == book_title, 'Genre'].iloc[0]
    return author if not pd.isnull(author) else f"No information found for '{book_title}'"

def get_language(book_title, df):
    author = df.loc[df['Title'] == book_title, 'Language'].iloc[0]
    return author if not pd.isnull(author) else f"No information found for '{book_title}'"

def get_pages(book_title, df):
    author = df.loc[df['Title'] == book_title, 'Pages'].iloc[0]
    return author if not pd.isnull(author) else f"No information found for '{book_title}'"

def filter_data(data: pd.DataFrame, column: str, values: List[str]) -> pd.DataFrame:
    return data[data[column].isin(values)] if values else data

def display_sidebar(df: pd.DataFrame):
    with st.sidebar:
        st.write("**Filters**")
        selected_month = st.selectbox("Select a month", options=["Entire Year"] + list(df["Month"].unique()))

        if selected_month != "Entire Year":
            filtered_data = filter_data(df, 'Month', [selected_month])
            selected_genre = st.multiselect("Select genre(s)", options=filtered_data["Genre"].unique())
            filtered_data = filter_data(filtered_data, 'Genre', selected_genre)
            selected_author = st.multiselect("Select author(s)", options=filtered_data["Author"].unique())
            filtered_data = filter_data(filtered_data, 'Author', selected_author)

            highest_page_number = filtered_data['Pages'].max()
            pages = st.slider("Page Range", min_value=0, max_value=highest_page_number, value = highest_page_number, step=10)


        else:
            selected_genre = st.multiselect("Select genre(s)", options=df["Genre"].unique())
            filtered_data = filter_data(df, 'Genre', selected_genre)
            selected_author = st.multiselect("Select author(s)", options=filtered_data["Author"].unique())
            filtered_data = filter_data(filtered_data, 'Author', selected_author)
            highest_page_number = filtered_data['Pages'].max()
            pages = st.slider("Page Range", min_value=0, max_value=highest_page_number, value=highest_page_number, step=10)


    return selected_month, selected_genre, selected_author, pages

def display_charts(selected_month, df):
    colors = ["#8da683", "#be8f3c", "#d99d29", "#f2dcb1", "#dc8920"]
    
    if selected_month == "Entire Year":

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="Books Read", value=f"{len(df)}")
        with col2:
            st.metric(label="Average Rating", value=f"{round(df['Rating'].mean(), 2)}")
        with col3:
            st.metric(label="Favorite Genre", value=f"{df['Genre'].value_counts().idxmax()}")

        col4, col5 = st.columns(2)

        with col4:

            st.write("###")
            
            # language dist
            df_dict = df.to_dict(orient="records")
            languages = [book['Language'] for book in df_dict]

            language_counts = {lang: languages.count(lang) for lang in set(languages)}

            st.write("**Language Distribution in Books**")

            language_data = {"Language": list(language_counts.keys()), "# of Books": list(language_counts.values())}
            fig = px.bar(language_data, x="Language", y="# of Books", color="Language", color_discrete_sequence=colors)
            fig.update_layout(width=350, height=400)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

            st.write("###")

            # page count vs. rating
            st.write("**Book Ratings vs. Page Count**")
            fig = px.scatter(df, x='Pages', y='Rating', color='Title', hover_data=['Title', 'Author'], color_discrete_sequence=colors)
            fig.update_yaxes(range=[.5, 5.5])
            fig.update_layout(width=350, height=400)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

            
        with col5:

            st.write("###")
           
            # duration chart
            df['End Date'] = pd.to_datetime(df['End Date'])

            df['Cumulative Pages'] = df['Pages'].cumsum()

            st.write("**Reading Progress Over Time**")

            fig = px.line(df, x='End Date', y='Cumulative Pages',
                        labels={'Cumulative Pages': 'Total Pages Read', 'End Date': 'Date'}, color_discrete_sequence=colors)
            
            fig.update_layout(width=350, height=400)
            fig.update_layout(showlegend=False)

            fig.update_layout(
                xaxis_title='Date',
                yaxis_title='Total Pages Read',
                hovermode='x unified'
            )

            st.plotly_chart(fig)

            st.write("###")

            # author wordcloud
            authors_text = ", ".join([book["Author"] for book in df_dict])

            def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                return random.choice(colors)

            # Create a word cloud
            wordcloud = WordCloud(width=750, height=700, background_color='white', color_func=custom_color_func).generate(authors_text)

            # Plot the word cloud using Matplotlib
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')

            # Streamlit app
            st.write("**Author Word Cloud**")
            st.pyplot(plt)

    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="Books Read", value=f"{len(df)}")
        with col2:
            st.metric(label="Average Rating", value=f"{round(df['Rating'].mean(), 2)}")
        with col3:
            st.metric(label="Favorite Genre", value=f"{df['Genre'].value_counts().idxmax()}")

        col4, col5 = st.columns(2)

        colors = ["#8da683", "#be8f3c", "#d99d29", "#f2dcb1", "#dc8920"]

        with col4:

            # genre dist
            fig = px.pie(df, names='Genre', title='Genre Distribution',  color_discrete_sequence=colors)
            fig.update_layout(width=350, height=400)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

            # page count
            df_sorted = df.sort_values(by="Pages", ascending=False)

            # Create a bar chart for page counts using Plotly Express
            fig = px.bar(x=df_sorted["Title"], y=df_sorted["Pages"], labels={'x':'Book Title', 'y':'Page Count'}, color=df_sorted["Title"], title='Page Count', color_discrete_sequence=colors)
            fig.update_layout(width=350, height=400)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)
        
        with col5:

            df_dict = df.to_dict(orient="records")
           
            # duration chart
            for book in df_dict:
                book['Start Date'] = pd.to_datetime(book['Start Date'])
                book["End Date"] = pd.to_datetime(book["End Date"])
            for book in df_dict:
                book["Duration"] = (book["End Date"] - book["Start Date"]).days
            
            duration = pd.DataFrame(df_dict)
            duration = duration.sort_values(by="Duration", ascending=False)

            fig = px.bar(duration, x="Title", y="Duration", color="Title", title="Book Durations", labels={"Duration": "Days"}, color_discrete_sequence=colors)
            fig.update_layout(barmode='stack')
            fig.update_layout(width=350, height=400)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

            # page count vs. rating
            fig = px.box(df, y='Rating', title='Book Ratings', color_discrete_sequence=colors)
            fig.update_layout(width=350, height=400)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)




def main():
    st.title("📚 2024 Bookshelf")

    # book data per month
    jan_book_data = [
        {"Month": "January", "Title": "Beyond the Story: 10 Year Record of BTS", "Author": "Kang Myeong-seok, BTS", "Genre": "Nonfiction", "Language": "English", "Start Date": '12-26-2023', "End Date": '01-02-2024', "Rating": 4, "Pages": 544},
        {"Month": "January", "Title": "Jujutsu Kaisen #10", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '01-03-2024', "End Date": '01-06-2024', "Rating": 5, "Pages": 192},
        {"Month": "January", "Title": "The Exiled Fleet", "Author": "J.S. Dewes", "Genre": "Science Fiction", "Language": "English", "Start Date": '01-21-2024', "End Date": '01-27-2024', "Rating": 5, "Pages": 420}
    ]
    jan_books = pd.DataFrame(jan_book_data)

    feb_book_data = [
            {"Month": "February", "Title": "A Court of Thorns and Roses", "Author": "Sarah J. Maas", "Genre": "Fantasy", "Language": "English", "Start Date": '01-28-2024', "End Date": '02-01-2024', "Rating": 4, "Pages": 419},
            {"Month": "February", "Title": "Jujutsu Kaisen #11", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '02-04-2024', "End Date": '02-04-2024', "Rating": 5, "Pages": 192},
            {"Month": "February", "Title": "A Court of Mist and Fury", "Author": "Sarah J. Maas", "Genre": "Fantasy", "Language": "English", "Start Date": '02-02-2024', "End Date": '02-14-2024', "Rating": 5, "Pages": 624}
    ]
    feb_books = pd.DataFrame(feb_book_data)


    # all books
    book_df = pd.concat([jan_books, feb_books], axis=0)

    selected_month, selected_genre, selected_author, pages = display_sidebar(book_df)

    if selected_month == "Entire Year":
        filtered_data = filter_data(book_df, 'Genre', selected_genre)
        filtered_data = filter_data(filtered_data, 'Author', selected_author)
        filtered_data = filtered_data[filtered_data['Pages'] <= pages]
        
        try:
            display_charts(selected_month, filtered_data)
        except:
            st.warning("No data to display")
    
    
    elif selected_month == "January":
        filtered_data = filter_data(book_df, 'Month', [selected_month])
        filtered_data = filter_data(filtered_data, 'Genre', selected_genre)
        filtered_data = filter_data(filtered_data, 'Author', selected_author)
        filtered_data = filtered_data[filtered_data['Pages'] <= pages]
        
        try:
            display_charts(selected_month, filtered_data)
        except:
            st.warning("No data to display")

        st.subheader("About")

        genre_result = get_genre("Beyond the Story: 10 Year Record of BTS", book_df)
        page_result = get_pages("Beyond the Story: 10 Year Record of BTS", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Beyond the Story: 10 Year Record of BTS"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/bts_book.png", width=350)

                with col7:
                    st.write("**Title:** Beyond the Story: 10 Year Record of BTS")

                    author_result = get_author("Beyond the Story: 10 Year Record of BTS", filtered_data)
                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Beyond the Story: 10 Year Record of BTS", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                st.write("**Summary:** BTS shares personal, behind-the-scenes stories of their journey so far through interviews and more than three years of in-depth coverage by Myeongseok Kang, who has written about K-pop and other Korean pop culture in various media. Presented chronologically in seven chapters from before the debut of BTS to the present, their vivid voices and opinions harmonize to tell a sincere, lively, and deep story. In individual interviews that have been conducted without a camera or makeup, they illuminate their musical journey from multiple angles and discuss its significance.")


        genre_result = get_genre("Jujutsu Kaisen #10", book_df)
        page_result = get_pages("Jujutsu Kaisen #10", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Jujutsu Kaisen #10"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/jjk_10.jpg", width=250)

                with col7:
                    st.write("**Title:** Jujutsu Kaisen #10")

                    author_result = get_author("Jujutsu Kaisen #10", filtered_data)
                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Jujutsu Kaisen #10", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                st.write("**Summary:** In order to regain use of his crippled body, Kokichi Muta, otherwise known as Mechamaru, has been acting as an informant for the cursed spirits. He’s prepared for the betrayal when he’s thrust into a battle to the death against Mahito, but is knowing his enemy enough against a cursed spirit whose powers keep growing exponentially?")


        genre_result = get_genre("The Exiled Fleet", book_df)
        page_result = get_pages("The Exiled Fleet", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("The Exiled Fleet"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/tef_book.jpg", width=350)

                with col7:
                    st.write("**Title:** The Exiled Fleet")

                    author_result = get_author("The Exiled Fleet", filtered_data)
                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("The Exiled Fleet", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                st.write("**Summary:** The Sentinels narrowly escaped the collapsing edge of the Divide. They have mustered a few other surviving Sentinels, but with no engines they have no way to leave the edge of the universe before they starve. Adequin Rake has gathered a team to find the materials they'll need to get everyone out.")

    elif selected_month == "February":
        filtered_data = filter_data(book_df, 'Month', [selected_month])
        filtered_data = filter_data(filtered_data, 'Genre', selected_genre)
        filtered_data = filter_data(filtered_data, 'Author', selected_author)
        filtered_data = filtered_data[filtered_data['Pages'] <= pages]

        try:
            display_charts(selected_month, filtered_data)
        except:
            st.warning("No data to display")

        st.subheader("About")

        genre_result = get_genre("A Court of Thorns and Roses", book_df)
        page_result = get_pages("A Court of Thorns and Roses", book_df)
        author_result = get_author("A Court of Thorns and Roses", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("A Court of Thorns and Roses"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/acotar_book.jpg", width=250)

                with col7:
                    st.write("**Title:** A Court of Thorns and Roses")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("A Court of Thorns and Roses", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                st.write("**Summary:** When nineteen-year-old huntress Feyre kills a wolf in the woods, a terrifying creature arrives to demand retribution. Dragged to a treacherous magical land she knows about only from legends, Feyre discovers that her captor is not truly a beast, but one of the lethal, immortal faeries who once ruled her world.")

        genre_result = get_genre("Jujutsu Kaisen #11", book_df)
        page_result = get_pages("Jujutsu Kaisen #11", book_df)
        author_result = get_author("Jujutsu Kaisen #11", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Jujutsu Kaisen #11"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/jjk_11.jpg", width=250)

                with col7:
                    st.write("**Title:** Jujutsu Kaisen #11")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Jujutsu Kaisen #11", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                st.write("**Summary:** Despite the crowd of civilians and transfigured humans, Satoru Gojo is able to defeat the cursed spirits at Shibuya Station. But it's a trap! The cursed spirits possess a special item that can even seal the all-powerful Gojo! Meanwhile, an unlikely ally suddenly contacts Yuji Itadori, who is on his way to the station!")


    

if __name__ == '__main__':
    main()
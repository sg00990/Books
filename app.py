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

def get_rating(book_title, df):
    author = df.loc[df['Title'] == book_title, 'Rating'].iloc[0]
    return author if not pd.isnull(author) else f"No information found for '{book_title}'"

# filters data
def filter_data(data: pd.DataFrame, column: str, values: List[str]) -> pd.DataFrame:
    return data[data[column].isin(values)] if values else data

# sidebar configuration
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

# creates charts
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
    book_data = [
        {"Month": "January", "Title": "Beyond the Story: 10 Year Record of BTS", "Author": "Kang Myeong-seok, BTS", "Genre": "Nonfiction", "Language": "English", "Start Date": '12-26-2023', "End Date": '01-02-2024', "Rating": 4.5, "Pages": 544},
        {"Month": "January", "Title": "Jujutsu Kaisen #10", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '01-03-2024', "End Date": '01-06-2024', "Rating": 5, "Pages": 192},
        {"Month": "January", "Title": "The Exiled Fleet", "Author": "J.S. Dewes", "Genre": "Science Fiction", "Language": "English", "Start Date": '01-21-2024', "End Date": '01-27-2024', "Rating": 5, "Pages": 420},
        {"Month": "February", "Title": "A Court of Thorns and Roses", "Author": "Sarah J. Maas", "Genre": "Fantasy", "Language": "English", "Start Date": '01-28-2024', "End Date": '02-01-2024', "Rating": 4, "Pages": 419},
        {"Month": "February", "Title": "Jujutsu Kaisen #11", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '02-04-2024', "End Date": '02-04-2024', "Rating": 5, "Pages": 192},
        {"Month": "February", "Title": "A Court of Mist and Fury", "Author": "Sarah J. Maas", "Genre": "Fantasy", "Language": "English", "Start Date": '02-02-2024', "End Date": '02-07-2024', "Rating": 5, "Pages": 624},
        {"Month": "February", "Title": "Naruto #1", "Author": "Masashi Kishimoto", "Genre": "Action", "Language": "Japanese", "Start Date": '02-07-2024', "End Date": '02-08-2024', "Rating": 5, "Pages": 187},
        {"Month": "February", "Title": "A Court of Wings and Ruin", "Author": "Sarah J. Maas", "Genre": "Fantasy", "Language": "English", "Start Date": '02-08-2024', "End Date": '02-11-2024', "Rating": 5, "Pages": 699},
        {"Month": "February", "Title": "A Court of Frost and Starlight", "Author": "Sarah J. Maas", "Genre": "Fantasy", "Language": "English", "Start Date": '02-12-2024', "End Date": '02-12-2024', "Rating": 4, "Pages": 229},
        {"Month": "February", "Title": "A Court of Silver Flames", "Author": "Sarah J. Maas", "Genre": "Fantasy", "Language": "English", "Start Date": '02-13-2024', "End Date": '02-17-2024', "Rating": 4.5, "Pages": 751},
        {"Month": "February", "Title": "Hunter x Hunter #1", "Author": "Yoshihito Togashi", "Genre": "Action", "Language": "Japanese", "Start Date": '02-18-2024', "End Date": '02-20-2024', "Rating": 5, "Pages": 183},
        {"Month": "February", "Title": "Haikyu!! #1", "Author": "Haruichi Furudate", "Genre": "Sports", "Language": "Japanese", "Start Date": '02-20-2024', "End Date": '02-22-2024', "Rating": 5, "Pages": 189},
        {"Month": "February", "Title": "Jujutsu Kaisen #12", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '02-23-2024', "End Date": '02-23-2024', "Rating": 5, "Pages": 189},
        {"Month": "February", "Title": "Jujutsu Kaisen #13", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '02-24-2024', "End Date": '02-25-2024', "Rating": 5, "Pages": 191},
        {"Month": "February", "Title": "Jujutsu Kaisen #14", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '02-29-2024', "End Date": '02-29-2024', "Rating": 5, "Pages": 191},
        {"Month": "March", "Title": "Jujutsu Kaisen #15", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '03-02-2024', "End Date": '03-02-2024', "Rating": 5, "Pages": 191},
        {"Month": "March", "Title": "Starter Villain", "Author": "John Scalzi", "Genre": "Science Fiction", "Language": "English", "Start Date": '03-03-2024', "End Date": '03-04-2024', "Rating": 5, "Pages": 268},
        {"Month": "March", "Title": "Throne in the Dark", "Author": "A.K. Caggiano", "Genre": "Fantasy", "Language": "English", "Start Date": '03-04-2024', "End Date": '03-07-2024', "Rating": 5, "Pages": 459},
        {"Month": "March", "Title": "Summoned to the Wilds", "Author": "A.K. Caggiano", "Genre": "Fantasy", "Language": "English", "Start Date": '03-07-2024', "End Date": '03-10-2024', "Rating": 5, "Pages": 426},
        {"Month": "March", "Title": "Jujutsu Kaisen #16", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '03-11-2024', "End Date": '03-11-2024', "Rating": 5, "Pages": 191},
        {"Month": "March", "Title": "Jujutsu Kaisen #17", "Author": "Gege Akutami", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '03-11-2024', "End Date": '03-11-2024', "Rating": 5, "Pages": 191},
        {"Month": "March", "Title": "Eclipse of the Crown", "Author": "A.K. Caggiano", "Genre": "Fantasy", "Language": "English", "Start Date": '03-13-2024', "End Date": '03-17-2024', "Rating": 5, "Pages": 464},
        {"Month": "March", "Title": "JoJo's Bizarre Adventure: Part 1 #1", "Author": "Hirohiko Araki", "Genre": "Action", "Language": "Japanese", "Start Date": '03-26-2024', "End Date": '03-28-2024', "Rating": 5, "Pages": 187},
        {"Month": "April", "Title": "Demon Slayer #1", "Author": "Koyoharu Gotouge", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '04-16-2024', "End Date": '04-20-2024', "Rating": 4, "Pages": 192},
        #{"Month": "April", "Title": "Harry Potter and the Sorcerer's Stone", "Author": "J.K. Rowling", "Genre": "Fantasy", "Language": "Japanese", "Start Date": '04-20-2024', "End Date": '05-20-2024', "Rating": 5, "Pages": 483},
        {"Month": "June", "Title": "Carry On", "Author": "Rainbow Rowell", "Genre": "Fantasy", "Language": "English", "Start Date": '06-15-2024', "End Date": '06-20-2024', "Rating": 5, "Pages": 517},
        {"Month": "July", "Title": "Wayward Son", "Author": "Rainbow Rowell", "Genre": "Fantasy", "Language": "English", "Start Date": '07-14-2024', "End Date": '07-17-2024', "Rating": 5, "Pages": 354},
        {"Month": "July", "Title": "Given #1", "Author": "Natsuki Kizu", "Genre": "Drama", "Language": "Japanese", "Start Date": '07-30-2024', "End Date": '07-31-2024', "Rating": 4.5, "Pages": 181},
        #{"Month": "July", "Title": "The Serpent and the Wings of Night", "Author": "Carissa Broadbent", "Genre": "Fantasy", "Language": "English", "Start Date": '07-18-2024', "End Date": '07-??-2024', "Rating": 5, "Pages": 452}
    ]


    # all books
    book_df = pd.DataFrame(book_data)

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
        author_result = get_author("Beyond the Story: 10 Year Record of BTS", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Beyond the Story: 10 Year Record of BTS"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/bts_book.png", width=350)

                with col7:
                    st.write("**Title:** Beyond the Story: 10 Year Record of BTS")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Beyond the Story: 10 Year Record of BTS", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Beyond the Story: 10 Year Record of BTS", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** BTS shares personal, behind-the-scenes stories of their journey so far through interviews and more than three years of in-depth coverage by Myeongseok Kang, who has written about K-pop and other Korean pop culture in various media. Presented chronologically in seven chapters from before the debut of BTS to the present, their vivid voices and opinions harmonize to tell a sincere, lively, and deep story. In individual interviews that have been conducted without a camera or makeup, they illuminate their musical journey from multiple angles and discuss its significance.")
                st.write("**Thoughts:** As a devoted fan of BTS, I eagerly anticipated the release of a book commemorating their 10-year anniversary. Kang Myeong-seok skillfully narrates the storyline, and the inclusion of interviews with the members adds a valuable layer of insight. Overall, I found the book to be an insightful and enjoyable read.")

        genre_result = get_genre("Jujutsu Kaisen #10", book_df)
        page_result = get_pages("Jujutsu Kaisen #10", book_df)
        author_result = get_author("Jujutsu Kaisen #10", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Jujutsu Kaisen #10"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/jjk_10.jpg", width=250)

                with col7:
                    st.write("**Title:** Jujutsu Kaisen #10")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Jujutsu Kaisen #10", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Jujutsu Kaisen #10", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** In order to regain use of his crippled body, Kokichi Muta, otherwise known as Mechamaru, has been acting as an informant for the cursed spirits. He’s prepared for the betrayal when he’s thrust into a battle to the death against Mahito, but is knowing his enemy enough against a cursed spirit whose powers keep growing exponentially?")
                st.write('**Thoughts:** Having been captivated by the masterpiece that is season 2 of the anime Jujutsu Kaisen, I was compelled to purchase several volumes while in Japan. This initial volume was a fantastic start to the series, filled with non-stop action from start to finish. However, it did take me a while to read; who knew I\'d have to learn how to say "cursed technique", "curses", and "sorcerers" in Japanese?')

        genre_result = get_genre("The Exiled Fleet", book_df)
        page_result = get_pages("The Exiled Fleet", book_df)
        author_result = get_author("The Exiled Fleet", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("The Exiled Fleet"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/tef_book.jpg", width=350)

                with col7:
                    st.write("**Title:** The Exiled Fleet")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("The Exiled Fleet", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("The Exiled Fleet", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** The Sentinels narrowly escaped the collapsing edge of the Divide. They have mustered a few other surviving Sentinels, but with no engines they have no way to leave the edge of the universe before they starve. Adequin Rake has gathered a team to find the materials they'll need to get everyone out.")
                st.write("**Thoughts:** The Exiled Fleet serves as an amazing sequel to The Last Watch, a novel I read in 2022. Throughout this gripping read, you'll find yourself on the edge of your seat. The characters indulge in witty banter and unravel colossal secrets, all while navigating perilous life-and-death scenarios. I must admit, I did not understand a lot of the terminology about space physics and engineering, but I enjoyed it nonetheless!")
    
    
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

                    rating_result = get_rating("A Court of Thorns and Roses", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** When nineteen-year-old huntress Feyre kills a wolf in the woods, a terrifying creature arrives to demand retribution. Dragged to a treacherous magical land she knows about only from legends, Feyre discovers that her captor is not truly a beast, but one of the lethal, immortal faeries who once ruled her world.")
                st.write("**Thoughts:** After seeing this book all over TikTok and my local Barnes & Noble, I eventually gave in and bought it. The first two-thirds of the book were a bit slow-paced, likely due to world-building, but the story really picked up momentum towards the end. Hopefully the sequel has more plot.")
        
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

                    rating_result = get_rating("Jujutsu Kaisen #11", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Despite the crowd of civilians and transfigured humans, Satoru Gojo is able to defeat the cursed spirits at Shibuya Station. But it's a trap! The cursed spirits possess a special item that can even seal the all-powerful Gojo! Meanwhile, an unlikely ally suddenly contacts Yuji Itadori, who is on his way to the station!")
                st.write("**Thoughts:** In Volume 11 of Jujutsu Kaisen, the focus shifts to the other characters in Shibuya. While it may contain less action compared to the last volume, I appreciated the opportunity to delve deeper into various characters' situations and battles.")
        
        
        page_result = get_pages("A Court of Mist and Fury", book_df)
        author_result = get_author("A Court of Mist and Fury", book_df)
        genre_result = get_genre("A Court of Mist and Fury", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("A Court of Mist and Fury"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/acomaf_book.jpg", width=250)

                with col7:
                    st.write("**Title:** A Court of Mist and Fury")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("A Court of Mist and Fury", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("A Court of Mist and Fury", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Feyre has undergone more trials than one human woman can carry in her heart. Though she's now been granted the powers and lifespan of the High Fae, she is haunted by her time Under the Mountain and the terrible deeds she performed to save the lives of Tamlin and his people. As her marriage to Tamlin approaches, Feyre's hollowness and nightmares consume her. She finds herself split into two different people: one who upholds her bargain with Rhysand, High Lord of the feared Night Court, and one who lives out her life in the Spring Court with Tamlin. While Feyre navigates a dark web of politics, passion, and dazzling power, a greater evil looms. She might just be the key to stopping it, but only if she can harness her harrowing gifts, heal her fractured soul, and decide how she wishes to shape her future-and the future of a world in turmoil.")
                st.write("**Thoughts:** Ah, now I understand the hype surrounding this series! I found myself utterly captivated by this book, devouring about 100 pages each day. It's so, so good! With its intricate plot, themes of betrayal, complex relationships, and gripping depiction of an upcoming war between Fae and humans alike, it's truly a compelling read. Also, love having a strong female lead!")

        
        page_result = get_pages("Naruto #1", book_df)
        author_result = get_author("Naruto #1", book_df)
        genre_result = get_genre("Naruto #1", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Naruto #1"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/naruto_1.jpg", width=200)

                with col7:
                    st.write("**Title:** Naruto #1")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Naruto #1", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Naruto #1", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Twelve years ago the Village Hidden in the Leaves was attacked by a fearsome threat. A nine-tailed fox spirit claimed the life of the village leader, the Hokage, and many others. Today, the village is at peace and a troublemaking kid named Naruto is struggling to graduate from Ninja Academy.")
                st.write("**Thoughts:** After binge-watching the entire series (yes, all 500+ episodes) over two months years ago, I was thrilled to discover this book at a nearby Kinokuniya. It proved to be a much easier read compared to Jujutsu Kaisen.")

        
        page_result = get_pages("A Court of Wings and Ruin", book_df)
        author_result = get_author("A Court of Wings and Ruin", book_df)
        genre_result = get_genre("A Court of Wings and Ruin", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("A Court of Wings and Ruin"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/acowar_book.jpg", width=250)

                with col7:
                    st.write("**Title:** A Court of Wings and Ruin")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("A Court of Wings and Ruin", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("A Court of Wings and Ruin", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Feyre has returned to the Spring Court, determined to gather information on Tamlin’s maneuverings and the invading king threatening to bring Prythian to its knees. But to do so she must play a deadly game of deceit-and one slip may spell doom not only for Feyre, but for her world as well. As war bears down upon them all, Feyre must decide who to trust amongst the dazzling and lethal High Lords-and hunt for allies in unexpected places. In this thrilling third book in the #1 New York Times and USA Today bestselling series from Sarah J. Maas, the earth will be painted red as mighty armies grapple for power over the one thing that could destroy them all.")
                st.write("**Thoughts:** In 'A Court of Wings and Ruin,' war, betrayals, and unexpected alliances dominated the narrative. I found it enjoyable (and sometimes frustrating) to read!")

        page_result = get_pages("A Court of Frost and Starlight", book_df)
        author_result = get_author("A Court of Frost and Starlight", book_df)
        genre_result = get_genre("A Court of Frost and Starlight", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("A Court of Frost and Starlight"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/acofas_book.jpg", width=250)

                with col7:
                    st.write("**Title:** A Court of Frost and Starlight")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("A Court of Frost and Starlight", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("A Court of Frost and Starlight", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Feyre, Rhysand, and their friends are still busy rebuilding the Night Court and the vastly altered world beyond, recovering from the war that changed everything. But Winter Solstice is finally approaching, and with it, the joy of a hard-earned reprieve.  Yet even the festive atmosphere can't keep the shadows of the past from looming. As Feyre navigates her first Winter Solstice as High Lady, her concern for those dearest to her deepens. They have more wounds than she anticipated--scars that will have a far-reaching impact on the future of their court.")
                st.write("**Thoughts:** This book (short and sweet) read almost like an epilogue as it delves into the months following the war, predominantly exuding feel-good vibes. However, the alternating use of first and third-person narratives felt somewhat jarring, and the storyline lacked the same level of plot and action found in the preceding books. Overall, it was cute, but definitely not my favorite from this series.")
    
        page_result = get_pages("A Court of Silver Flames", book_df)
        author_result = get_author("A Court of Silver Flames", book_df)
        genre_result = get_genre("A Court of Silver Flames", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("A Court of Silver Flames"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/acosf_book.jpg", width=250)

                with col7:
                    st.write("**Title:** A Court of Silver Flames")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("A Court of Silver Flames", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("A Court of Silver Flames", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Nesta Archeron has always been prickly—proud, swift to anger, and slow to forgive. And ever since being forced into the Cauldron and becoming High Fae against her will, she’s struggled to find a place for herself within the strange, deadly world she inhabits. Worse, she can’t seem to move past the horrors of the war with Hybern and all she lost in it. The one person who ignites her temper more than any other is Cassian, the battle-scarred warrior whose position in Rhysand and Feyre’s Night Court keeps him constantly in Nesta’s orbit. But her temper isn’t the only thing Cassian ignites. The fire between them is undeniable, and only burns hotter as they are forced into close quarters with each other. Meanwhile, the treacherous human queens who returned to the Continent during the last war have forged a dangerous new alliance, threatening the fragile peace that has settled over the realms. And the key to halting them might very well rely on Cassian and Nesta facing their haunting pasts. Against the sweeping backdrop of a world seared by war and plagued with uncertainty, Nesta and Cassian battle monsters from within and without as they search for acceptance—and healing—in each other’s arms.")
                st.write("**Thoughts:** Initially, I wasn't particularly enthusiastic about delving into a book centered around Nesta. However, this novel completely transformed my perspective, as Nesta evolved into one of my beloved characters. Witnessing her conquer the traumas of war, establish genuine friendships, and pioneer a female-exclusive warrior unit was incredibly empowering. Nevertheless, I couldn't overlook certain plot inconsistencies, which detracted from the overall experience for me (looking at you Reys and Feyre).")

        page_result = get_pages("Hunter x Hunter #1", book_df)
        author_result = get_author("Hunter x Hunter #1", book_df)
        genre_result = get_genre("Hunter x Hunter #1", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Hunter x Hunter #1"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/hh_1.jpg", width=250)

                with col7:
                    st.write("**Title:** Hunter x Hunter #1")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Hunter x Hunter #1", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Hunter x Hunter #1", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Gon leaves home and befriends two other hunter hopefuls: the mysterious Kurapika, who is the last of [his] clan, and Leorio, who seems a superficial moneygrubber yet actually has a heart of gold. Together they solve riddles and overcome obstacles, but their journey is only beginning.")
                st.write("**Thoughts:** Going into this, I figured it'd be an easy read given Gon's age of 12. However, I found it to be slightly more challenging compared to Naruto due to the lengthy explanations throughout the book. I was still able to grasp a general understanding of the story and enjoyed the manga regardless.")
     
        page_result = get_pages("Haikyu!! #1", book_df)
        author_result = get_author("Haikyu!! #1", book_df)
        genre_result = get_genre("Haikyu!! #1", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Haikyu!! #1"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/haikyuu_1.jpg", width=250)

                with col7:
                    st.write("**Title:** Haikyu!! #1")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Haikyu!! #1", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Haikyu!! #1", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Shoyo Hinata is inspired by the Small Giant playing volleyball on TV. Three years later, Hinata goes to his first ever volleyball tournament and his team is paired against Kitagawa Daiichi, the school of Tobio Kageyama, also known as the King of the Court.")
                st.write("**Thoughts:** Being a huge fan of sports anime, Haikyuu has always held a special place in my heart. When I stumbled upon the book at Kinokuniya, I couldn't resist adding it to my collection. I anticipated that its portrayal of real-life scenarios would make for a smoother read compared to series like Jujutsu Kaisen or Naruto, and my assumption was partially correct! Despite its abundant use of informal speech, the overall readability of the book was surprisingly good.")
        
        page_result = get_pages("Jujutsu Kaisen #12", book_df)
        author_result = get_author("Jujutsu Kaisen #12", book_df)
        genre_result = get_genre("Jujutsu Kaisen #12", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Jujutsu Kaisen #12"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/jjk_12.jpg", width=250)

                with col7:
                    st.write("**Title:** Jujutsu Kaisen #12")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Jujutsu Kaisen #12", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Jujutsu Kaisen #12", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** The incident in Shibuya becomes dire when Toji Zenin reappears! Meanwhile, Mei Mei confronts the traitorous Geto on a subway platform, and Nanami’s furious over the casualties suffered by the assistant managers. Then more grade 1 sorcerers enter the fray as Itadori fights the eldest Cursed Womb: Death Painting brother, Choso!")
                st.write("**Thoughts:** In these upcoming volumes of the series, I found some of my personal favorites. The confrontation between Yuuji and Choso was wonderfully done, although I have a preference for experiencing it through animation. Additionally, Nanami emerged as another standout character within this volume.")
        
        page_result = get_pages("Jujutsu Kaisen #13", book_df)
        author_result = get_author("Jujutsu Kaisen #13", book_df)
        genre_result = get_genre("Jujutsu Kaisen #13", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Jujutsu Kaisen #13"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/jjk_13.jpg", width=250)

                with col7:
                    st.write("**Title:** Jujutsu Kaisen #13")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Jujutsu Kaisen #13", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Jujutsu Kaisen #13", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Dagon has evolved into a terrifying curse, releasing a flood of endless cursed energy attacks at Naobito, Maki and Nanami! At the same time, a group of curse users devoted to Geto attempt to summon the jujutsu world’s most terrifying threat.")
                st.write("**Thoughts:** In this volume, the story takes an intense turn, building upon the already established tension. With unexpected appearances like Toji and the chaotic events orchestrated by Jogo and Sukuna, this book delivers an exhilarating read.")

        page_result = get_pages("Jujutsu Kaisen #14", book_df)
        author_result = get_author("Jujutsu Kaisen #14", book_df)
        genre_result = get_genre("Jujutsu Kaisen #14", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Jujutsu Kaisen #14"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/jjk_14.jpg", width=250)

                with col7:
                    st.write("**Title:** Jujutsu Kaisen #14")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Jujutsu Kaisen #14", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Jujutsu Kaisen #14", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** While Sukuna, who has been temporarily unleashed, is wrecking Shibuya, Fushiguro suffers a serious injury from a curse user who caught him unawares. Fushiguro comes up with a desperate plan to deal with both the rampaging Sukuna and the curse user, but it comes with grave consequences…")
                st.write("**Thoughts:** Volume 14 was another wild read. The intense showdown between Sukuna and Jougo reaches its climax, Fushiguro faces relentless challenges, and Yuuji confronts the series' most hated villain. Amidst the action, the narrative doesn't shy away from impactful character deaths.")
     
     
    
    elif selected_month == "March":
        filtered_data = filter_data(book_df, 'Month', [selected_month])
        filtered_data = filter_data(filtered_data, 'Genre', selected_genre)
        filtered_data = filter_data(filtered_data, 'Author', selected_author)
        filtered_data = filtered_data[filtered_data['Pages'] <= pages]
        
        try:
            display_charts(selected_month, filtered_data)
        except:
            st.warning("No data to display")

        
        page_result = get_pages("Jujutsu Kaisen #15", book_df)
        author_result = get_author("Jujutsu Kaisen #15", book_df)
        genre_result = get_genre("Jujutsu Kaisen #15", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Jujutsu Kaisen #15"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/jjk_15.jpg", width=250)

                with col7:
                    st.write("**Title:** Jujutsu Kaisen #15")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Jujutsu Kaisen #15", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Jujutsu Kaisen #15", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Sukuna is on a murderous rampage. Meanwhile, invaluabe Jujutsu Sorcerers have been taken down, and even Kugisaki falls into Mahito's trap! Feeling the burden of his sins, Itadori finds it hard to keep going, but he rushes off to help Kugisaki anyway. Can he reach her in time?!")
                st.write("**Thoughts:** This book delves into the finale of season 2 of the anime (well most of it anyway), featuring another character death, Itadori's return and an unexpected turn of events. Like all of these so far, I really enjoyed it! ")


        page_result = get_pages("Starter Villain", book_df)
        author_result = get_author("Starter Villain", book_df)
        genre_result = get_genre("Starter Villain", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Starter Villain"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/starter_villain_book.jpg", width=250)

                with col7:
                    st.write("**Title:** Starter Villain")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Starter Villain", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Starter Villain", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Inheriting your uncle's supervillain business is more complicated than you might think. Particularly when you discover who's running the place. Charlie's life is going nowhere fast. A divorced substitute teacher living with his cat in a house his siblings want to sell, all he wants is to open a pub downtown, if only the bank will approve his loan. Then his long-lost uncle Jake dies and leaves his supervillain business (complete with island volcano lair) to Charlie. But becoming a supervillain isn't all giant laser death rays and lava pits. Jake had enemies, and now they're coming after Charlie. His uncle might have been a stand-up, old-fashioned kind of villain, but these are the real thing: rich, soulless predators backed by multinational corporations and venture capital. It's up to Charlie to win the war his uncle started against a league of supervillains. But with unionized dolphins, hyper-intelligent talking spy cats, and a terrifying henchperson at his side, going bad is starting to look pretty good. In a dog-eat-dog world...be a cat.")
                st.write("**Thoughts:** Starter Villain marks my return to Kindle reading after years, and it did not disappoint! From the adorable cat on the cover to the witty storyline filled with intelligent cats, unionized dolphins, and unexpected plot twists, it was a delightful and comedic read. ")


        page_result = get_pages("Throne in the Dark", book_df)
        author_result = get_author("Throne in the Dark", book_df)
        genre_result = get_genre("Throne in the Dark", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Throne in the Dark"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/titd_book.jpg", width=250)

                with col7:
                    st.write("**Title:** Throne in the Dark")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Throne in the Dark", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Throne in the Dark", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Dark lord, demon spawn, prophesied realm destroyer. With a demon for a father, Damien Maleficus Bloodthorne’s destiny could be nothing but nefarious, and with the completion of his most vicious spell, Damien is on the cusp of fulfilling the evil inevitability all of his dark machinations have led to. And then, her—bubbly, obnoxious, blonde. Harboring secrets of her own, a tiny yet troublesome thief calling herself Amma completely upsets Damien’s malevolent plans when she mistakenly gets chained to his side through magic, forcing him to drag her across the realm. Killing her would fix things, of course, but the nauseatingly sweet Amma proves herself useful on Damien's unholy crusade and then proves herself the source of something even more sinister: feelings. Will Damien be forced to abandon his villainous birthright to help the tender thorn in his side? Or will he manage to overcome the virtue Amma insists on inspiring and instead cut it out at the heart?")
                st.write("**Thoughts:** After coming across recommendations for Throne in the Dark on Reddit and noticing its positive reviews and affordable price of \$4 (seriously, why are books \$20+ now??), I decided to give it a try. I'm pleased to say I thoroughly enjoyed it! Filled with adventure, humor, and a delightful slow-burn romance, I can't wait to dive into the sequel.")


        page_result = get_pages("Summoned to the Wilds", book_df)
        author_result = get_author("Summoned to the Wilds", book_df)
        genre_result = get_genre("Summoned to the Wilds", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Summoned to the Wilds"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/sttw_book.jpg", width=250)

                with col7:
                    st.write("**Title:** Summoned to the Wilds")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Summoned to the Wilds", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Summoned to the Wilds", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Lady Ammalie Avington, Baroness of Faebarrow, has discovered the truth, and it should not come as a surprise: the blood mage who threatened, spellbound, and abducted her intends to bring ruin to the realm--the very one she is sworn to serve. It's just a terribly inconvenient fact to learn because, well...he's rather cute. But it's not safe to pine after the son of a demon, especially not whilst locked up in a tower surrounded by infernal beings and a rival for your affection, nor trapped below ground in a den of beguiling vampires, nor even in the heart of a wild jungle under the tutelage of esoteric witches. Amma just can't help herself around Damien Maleficus Bloodthorne, danger be damned, but, truly, what danger is there? Damien's heart, the one he swears to not have, has been softening right before her eyes. Nevermind the weird smoke that sometimes unwittingly emanates from his hands or that faraway look he gets to his eyes, and a voice she can't hear telling him that he's meant to be a vessel? Surely it's all just a bad dream. After finally tasting freedom and learning that Amma may have ancient, innate magical powers of her own, why not use them to do exactly as she pleases?")
                st.write("**Thoughts:** This was a great book full of plot twists and humor! Damien continued to get derailed from his main mission (world domination, of course) while Amma finally discovered her magic. It did end on a cliffhanger, so I am excited to read the final book.")

        page_result = get_pages("Jujutsu Kaisen #16", book_df)
        author_result = get_author("Jujutsu Kaisen #16", book_df)
        genre_result = get_genre("Jujutsu Kaisen #16", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Jujutsu Kaisen #16"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/jjk_16.jpg", width=250)

                with col7:
                    st.write("**Title:** Jujutsu Kaisen #16")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Jujutsu Kaisen #16", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Jujutsu Kaisen #16", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** After he consumes Mahito’s soul, Geto reveals part of his nefarious plan to Itadori and gang. In that moment, Choso recognizes the evil sorcerer possessing Geto's body and is filled with rage! Who is this evil sorcerer, and what relation do they have to Choso? Meanwhile, now that Gojo is imprisoned and the foundations of the jujutsu society are crumbling, what will happen to the world as it devolves into destruction and chaos?!")
                st.write("**Thoughts:** This volume marks the conclusion of season 2's finale, so I am finally on to the new stuff! I enjoyed seeing Choso and Yuuji as a team (though it didn't last long) and while I knew of Yuuta's true role in this volume, I was still excited by his appearance. ")


        page_result = get_pages("Jujutsu Kaisen #17", book_df)
        author_result = get_author("Jujutsu Kaisen #17", book_df)
        genre_result = get_genre("Jujutsu Kaisen #17", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Jujutsu Kaisen #17"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/jjk_17.jpg", width=250)

                with col7:
                    st.write("**Title:** Jujutsu Kaisen #17")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Jujutsu Kaisen #17", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Jujutsu Kaisen #17", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Hunted down by Okkotsu and on the brink of death, Itadori recalls a troubling family scene from his past. But why is the former form of Noritoshi Kamo there? As the sorcerers begin to take action toward suppressing the lethal culling game, Maki pays the Zenin Clan a visit…")
                st.write("**Thoughts:** This volume was by far the most difficult to read as it was super wordy; I think I got the gist of things though. Yuuji remembers Kenjaku's role in his past, the sorcerers confront Tengen and best of all, Maki destroys the Zenin clan. It was truly action-packed! ")

        page_result = get_pages("Eclipse of the Crown", book_df)
        author_result = get_author("Eclipse of the Crown", book_df)
        genre_result = get_genre("Eclipse of the Crown", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Eclipse of the Crown"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/eofc.jpg", width=250)

                with col7:
                    st.write("**Title:** Eclipse of the Crown")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Eclipse of the Crown", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Eclipse of the Crown", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Their destinies are irrevocably entangled, but will their bond be the realm’s undoing? Damien and Amma have landed themselves in the midst of Yvlcon, the preeminent congregation of the vilest and most unscrupulous villains in existence. Once again amongst his peers, Damien’s moral growth is threatened just when he’s learning to be slightly less evil. Consequently, Amma finds her own virtue in peril when faced with so much temptation, namely in the form of a domineering blood mage she can’t—or doesn’t want—to say no to. But a burgeoning romance is doused in the coldest of baths when the Grand Order of Dread commands Damien to once again face the swirling vortex of entropy that’s been hunting them all over the realm. The coming eclipse points to devastation and destruction, and there seems to be no avoiding annihilation, prophecy being, well, prophecy, after all. But there’s an entire fortnight before the world is supposed to end, and surely that’s enough time to find some way around it, or to at least confess one’s devotion to the other before it all burns down around them.")
                st.write("**Thoughts:**  Eclipse of the Crown was an amazing conclusion to the trilogy! What initially appeared as side quests in previous books seamlessly converged in this installment—bringing together friends, foes, and more. I really enjoyed the romcom elements and humor. Additionally, the book concludes with a heartwarming happy ending.")


        page_result = get_pages("JoJo's Bizarre Adventure: Part 1 #1", book_df)
        author_result = get_author("JoJo's Bizarre Adventure: Part 1 #1", book_df)
        genre_result = get_genre("JoJo's Bizarre Adventure: Part 1 #1", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("JoJo's Bizarre Adventure: Part 1 #1"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/jojo1.jpg", width=150)

                with col7:
                    st.write("**Title:** JoJo's Bizarre Adventure: Part 1 #1")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("JoJo's Bizarre Adventure: Part 1 #1", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("JoJo's Bizarre Adventure: Part 1 #1", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Young Jonathan Joestar’s life is forever changed when he meets his new adopted brother, Dio. For some reason, Dio has a smoldering grudge against him and derives pleasure from seeing him suffer. But every man has his limits, as Dio finds out. This is the beginning of a long and hateful relationship!")
                st.write("**Thoughts:**  I may be biased since JoJo's Bizarre Adventure is my all-time favorite anime, but I really enjoyed reading this first volume in Japanese. Though it starts out fairly normal (nothing supernatural...yet), there were plenty of plot twists and epic rivalries. It was also cool to see the artistic differences since this volume is from the 80s.")


    elif selected_month == "April":
        filtered_data = filter_data(book_df, 'Month', [selected_month])
        filtered_data = filter_data(filtered_data, 'Genre', selected_genre)
        filtered_data = filter_data(filtered_data, 'Author', selected_author)
        filtered_data = filtered_data[filtered_data['Pages'] <= pages]
        
        try:
            display_charts(selected_month, filtered_data)
        except:
            st.warning("No data to display")

        
        page_result = get_pages("Demon Slayer #1", book_df)
        author_result = get_author("Demon Slayer #1", book_df)
        genre_result = get_genre("Demon Slayer #1", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Demon Slayer #1"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/ds_1.jpg", width=250)

                with col7:
                    st.write("**Title:** Demon Slayer #1")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Demon Slayer #1", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Demon Slayer #1", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("**Summary:** Tanjiro sets out on the path of the Demon Slayer to save his sister and avenge his family! In Taisho-era Japan, kindhearted Tanjiro Kamado makes a living selling charcoal. But his peaceful life is shattered when a demon slaughters his entire family.")
                st.write("**Thoughts:** The first volume of Demon Slayer is another book I bought while in Japan. I was actually able to get past the first 20 or so pages without using a dictionary! I enjoyed this volume, but it's not my favorite. It took me a bit longer to get through.")
    

    elif selected_month == "May":
        st.write("I was busy preparing and moving to an apartment, so no time for books...")

    elif selected_month == "June":
        filtered_data = filter_data(book_df, 'Month', [selected_month])
        filtered_data = filter_data(filtered_data, 'Genre', selected_genre)
        filtered_data = filter_data(filtered_data, 'Author', selected_author)
        filtered_data = filtered_data[filtered_data['Pages'] <= pages]
        
        try:
            display_charts(selected_month, filtered_data)
        except:
            st.warning("No data to display")

        
        page_result = get_pages("Carry On", book_df)
        author_result = get_author("Carry On", book_df)
        genre_result = get_genre("Carry On", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Carry On"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/co_book.jpg", width=225)

                with col7:
                    st.write("**Title:** Carry On")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Carry On", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Carry On", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("""**Summary:** Simon Snow is the worst Chosen One who's ever been chosen. That's what his roommate, Baz, says. And Baz might be evil and a vampire and a complete git, but he's probably right. Half the time, Simon can't even make his wand work, and the other half, he starts something on fire. His mentor's avoiding him, his girlfriend broke up with him, and there's a magic-eating monster running around, wearing Simon's face. Baz would be having a field day with all this, if he were here — it's their last year at the Watford School of Magicks, and Simon's infuriating nemesis didn't even bother to show up.""")
                st.write("""**Thoughts:** Life has been pretty hectic lately with moving to a new apartment and my grandpa's passing, so I haven’t had much time for reading. However, I decided to pick up Carry On again because it’s such an easy and enjoyable read (and perfect for Pride Month!). Carry On is a spinoff from the book Fangirl, both of which I last read in high school. It's like a modern twist on Harry Potter, with its own unique spins and charm. If you’re looking for something fun and magical, this book is a great pick!""")
    
    elif selected_month == "July":
        filtered_data = filter_data(book_df, 'Month', [selected_month])
        filtered_data = filter_data(filtered_data, 'Genre', selected_genre)
        filtered_data = filter_data(filtered_data, 'Author', selected_author)
        filtered_data = filtered_data[filtered_data['Pages'] <= pages]
        
        try:
            display_charts(selected_month, filtered_data)
        except:
            st.warning("No data to display")

        
        page_result = get_pages("Wayward Son", book_df)
        author_result = get_author("Wayward Son", book_df)
        genre_result = get_genre("Wayward Son", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Wayward Son"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/ws_book.jpg", width=225)

                with col7:
                    st.write("**Title:** Wayward Son")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Wayward Son", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Wayward Son", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("""**Summary:** The story is supposed to be over. Simon Snow did everything he was supposed to do. He beat the villain. He won the war. He even fell in love. Now comes the good part, right? Now comes the happily ever after… So why can’t Simon Snow get off the couch? What he needs, according to his best friend, is a change of scenery. He just needs to see himself in a new light… That’s how Simon and Penny and Baz end up in a vintage convertible, tearing across the American West. They find trouble, of course. (Dragons, vampires, skunk-headed things with shotguns.) And they get lost. They get so lost, they start to wonder whether they ever knew where they were headed in the first place…""")
                st.write("""**Thoughts:** Between first reading Carry On in high school and rereading it last month, what was once a single book has now become a trilogy. Wayward Son is a fantastic sequel, continuing the adventures of Simon and his friends after Simon loses his magic. I thoroughly enjoyed the hilarious quips about America, especially the commentary on the outrageous gun laws (😂). One of my favorite quotes is, "Go ahead and shoot me. This isn't my favorite shirt." It perfectly captures the book's witty and sarcastic tone.""")

        page_result = get_pages("Given #1", book_df)
        author_result = get_author("Given #1", book_df)
        genre_result = get_genre("Given #1", book_df)

        if (genre_result in selected_genre or not selected_genre) and (page_result <= pages) and (author_result in selected_author or not selected_author):
            with st.expander("Given #1"):
                col6, col7 = st.columns(2)

                with col6:
                    st.image("img/g1.jpg", width=225)

                with col7:
                    st.write("**Title:** Given #1")

                    st.write(f"**Author:** {author_result}")

                    st.write(f"**Genre:** {genre_result}")

                    language_result = get_language("Given #1", filtered_data)
                    st.write(f"**Language:** {language_result}")

                    st.write(f"**Number of Pages:** {page_result}")

                    rating_result = get_rating("Given #1", filtered_data)
                    st.write(f"**My Rating:** {rating_result}/5.0")

                st.write("""**Summary:** Ritsuka Uenoyama is bored with it all—with school, with his basketball club, and even with his one true passion: playing guitar. That is, until the day he finds his favorite hidden napping spot occupied by a strange boy cradling a broken-stringed guitar. At first, Uenoyama is nonplussed by Mafuyu Sato and his slightly odd behavior, but when, on a whim, he asks Mafuyu to sing, the power of that song pierces him to the core.""")
                st.write("""**Thoughts:** I've watched both the show and the movie for Given, so I thought the manga would be an easy read in Japanese since it's a bit more slice-of-life... Turns out, not so much! It’s packed with slang and band-specific vocabulary that I hadn’t encountered before. Despite the challenge, I found the story absolutely adorable (and sad at times). Uenoyama reluctantly agrees to teach Mafuyu how to play the guitar, but when he hears Mafuyu sing for the first time, he's blown away and just has to have him in the band. Overall, it's a cute and heartwarming story.""")
    

if __name__ == '__main__':
    main()
import streamlit as st
import pandas as pd
import plotly.express as px
import os

#File with data
data_file = "books_data.csv"

#If we have file, upload data
if os.path.exists(data_file):
    data = pd.read.csv(data_file)
else:
    data = pd.DataFrame(columns=["Название", "Автор", "Тип", "Жанр", "Дата начала", "Дата конца", "Моя оценка"])

#Title
st.title("Интерактивная инфографика по книгам")

#Форма для ввода данных
with st.form("book_form"):
    st.header("Добавьте новую книгу")
    title = st.text_input("Название книги")
    author = st.text_input("Автор")

#Выбор типа книги
    book_type = st.selectbox("Тип книги", ["Бумажная", "Электронная", "Аудио"])

#Выпадающий список жанров
    genre = st.selectbox("Жанр", ["Фантастика", "Детектив", "Роман", "Нон-фикшн", "Поэзия", "Другой"])

#Календарь для выбора даты
    start_date = st.date_input("Дата начала")
    end_date = st.date_input("Дата конца")

#Оценка книги
    rating = st.slider("Оценка", 1, 5, 3)

    submit = st.form_submit_button("Добавить")

#Obrabotka dannih from form 
if submit:
    new_data = pd.DataFrame({
        "Название": [title],
        "Автор": [author],
        "Тип": [book_type],
        "Жанр": [genre],
        "Дата начала": [start_date],
        "Дата конца": [end_date],
        "Моя оценка": [rating]
    })
    st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
    st.success(f"Книга '{title}' добавлена!")

#Добавляем новые данные в таблицу
    data = pd.concat([data, new_data], ignore_index=True)

#Сохраняем данные в CSV
    data.to_csv(data_file, index=False)

    st.success(f"Книга '{title}' добавлена!")

#If we have data, we show grafick
if not data.empty:
    st.subheader("Ваши данные:")
    st.dataframe(data)
    
#Create interactive graphic 
   fig = px.timeline(
        st.session_state.data,
        x_start="Дата начала",
        x_end="Дата конца",
        y="Тип",
        color="Жанр",
        hover_data=["Название", "Автор", "Моя оценка"]
    )
    fig.update_layout(title="Темп чтения", xaxis_title="Время", yaxis_title="Тип книги")
    st.plotly_chart(fig)
else:
    st.info("Добавьте хотя бы одну книгу, чтобы увидеть график.")
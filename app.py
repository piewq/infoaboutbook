import streamlit as st
import pandas as pd
print(pd.__version__)
import plotly.express as px
import os
import requests 
from datetime import datetime

def get_books(query):
    url=f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=10'
    response = requests.get(url)
    books = response.json().get('items', [])
    return books
st.title("Библиотека книг")

#Ввод запроса для поиска
query = st.text_input("Поиск книги", "Harry Potter")

#Find authors and genres
authors = set()
genres = set()

if query:
    books = get_books(query)
    if books:
        for book in books:
            author_list = book['volumeInfo'].get('authors', [])
            genre_list = book['volumeInfo'].get('categories', [])
            authors.update(author_list)
            genres.update(genre_list)

#Выводим авторов и жанры в виде выпадающего списка
selected_author = st.selectbox("Выберите автора", list(authors))
selected_genre = st.selectbox("Выберите жанр", list(genres))

#Показать информацию о книгах
for book in books:
    title = book['volumeInfo'].get('title', 'Неизвестно')
    authors = ', '.join(book['volumeInfo'].get('authors', ['Неизвестно']))
    description = book['volumeInfo'].get('description', 'Нет описания')
    st.write(f"Название: {title}")
    st.write(f"Авторы: {authors}")
    st.write(f"Описание: {description}")
    st.write("---")
    else:
        st.write("Книги не найдены.")

#File with data
data_file = "books_data.csv"

#If we have file, upload data
if os.path.exists(data_file):
    data = pd.read_csv(data_file)
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

    if end_date < start_date:
        st.error("Неа")
    else:
        st.success("Ok")

#Оценка книги
    rating = st.slider("Оценка",min_value=1.0, max_value=5.0, step=0.5)
    st.write(f"Вы выбрали оценку: {rating}")

    submit = st.form_submit_button("Добавить")

#Обрабатываем данные из формы
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

#Добавляем новые данные в таблицу
    data = pd.concat([data, new_data], ignore_index=True)

#Сохраняем данные в CSV
    data.to_csv(data_file, index=False)

    st.success(f"Книга '{title}' добавлена!")

#Если есть данные, показываем график
if not data.empty:
    st.subheader("Ваши данные:")
    st.dataframe(data)

    # Преобразуем колонки с датами в тип datetime
    try:
        data["Дата начала"] = pd.to_datetime(data["Дата начала"])
        data["Дата конца"] = pd.to_datetime(data["Дата конца"])
        st.success("Даты преобразованы успешно.")
    except Exception as e:
        st.error(f"Ошибка преобразования дат: {e}")
        data["Дата начала"] = pd.to_datetime(data["Дата начала"], errors='coerce')
        data["Дата конца"] = pd.to_datetime(data["Дата конца"], errors='coerce')

    # Проверяем структуру данных перед созданием графика
    st.write("Проверка данных перед созданием графика:")
    st.write(data)

    # Создаем интерактивный график
    try:
        fig = px.timeline(
            data,
            x_start="Дата начала",
            x_end="Дата конца",
            y="Тип",
            color="Жанр",
            hover_data=["Название", "Автор", "Моя оценка"]
        )
        fig.update_layout(title="Темп чтения", xaxis_title="Время", yaxis_title="Тип книги")
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Ошибка при создании графика: {e}")
else:
    st.info("Добавьте хотя бы одну книгу, чтобы увидеть график.")

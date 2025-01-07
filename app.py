import streamlit as st
import pandas as pd
print(pd.__version__)
import plotly.express as px
import os

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

#Оценка книги
    rating = st.slider("Оценка", 1, 5, 3)

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

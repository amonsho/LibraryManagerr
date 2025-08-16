import asyncio

from logic import LibraryManager
from database import DatabaseConfig


async def main():
    db = DatabaseConfig(
            user='postgres',
            password='Am.on$sh_op',
            db_name='lib_manager_db'
        )
    await db.connect()
    await db.create_table()
    manager = LibraryManager(db)

    while True:
        print("""
    1. Добавить книгу
    2. Показать все книги
    3. Найти книгу
    4. Зарегистрировать читателя
    5. Показать всех читателей
    6. Выдать книгу
    7. Вернуть книгу
    8. Показать активные выдачи
    0. Выход
""")
        choice = input('Choose one: ')
        if choice == '1':
            title = input('Введите название книги: ')
            author = input('Введите имя автора: ')
            genre = input('Введите жанр книги: ')
            year = input('Введите год выпуска книги: ')
            copies = input('Введите количество копий: ')
            await manager.add_book(title, author, genre, year, copies)
        elif choice == '2':
            await manager.get_books()
        elif choice == '3':
            text = input('Что ищите?')
            await manager.search_book(text)
        elif choice == '4':
            full_name = input('Введите ваше полное имя: ')
            email = input('Введите адрес электронной почты: ')
            phone = input('Введите номер телефона: ')
            await manager.add_reader(full_name, phone, email)
        elif choice == '5':
            await manager.get_users()
        elif choice == '6':
            book_title = input('Введите название книги: ')
            full_name = input('Введите ваше полное имя: ')
            await manager.borrow_book(book_title, full_name)
        elif choice == '7':
            book_title = input('Введите название книги: ')
            full_name = input('Введите ваше полное имя: ')
            await manager.return_book(book_title, full_name)
        elif choice == '8':
            await manager.get_loans()
        elif choice == '0':
            print('Вы вышли из системы!')
            break


if __name__ == '__main__':
    asyncio.run(main())
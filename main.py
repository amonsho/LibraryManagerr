import asyncio
from database import DatabaseConfig
from logic import Book, Reader,LibraryManager,Loan
from datetime import datetime

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
            title = input('Enter title: ')
            author = input('Enter author: ')
            genre = input('Enter genre: ')
            year = int(input('Enter year: '))
            copies = int(input('Enter copies: '))
            book = Book(title, author, genre, year, copies)
            await manager.add_book(book)

        elif choice == '2':
            books = await manager.get_all_books()
            for book in books:
                print(f'(id: {book['id']}) {book['title']} - {book['author']} - {book['genre']} - {book['year']} - {book['copies']} copies')
             
            
        elif choice == '3':
            keyword = input('Enter title or author: ')
            await manager.find_book(keyword)

        elif choice == '4':
            full_name = input('Enter full name: ')
            phone = input('Enter phone: ')
            email = input('Enter email: ')
            reader = Reader(full_name, phone, email)
            await manager.add_reader(reader)

        elif choice == '5':
             await manager.get_all_readers()

        elif choice == '6':
            book_id = int(input('Enter book ID: '))
            reader_id = int(input('Enter reader ID: '))
            issue_date = datetime.now()
            return_date = datetime.strptime(input('Enter return date (YYYY-MM-DD): '), "%Y-%m-%d")
            loan = Loan(book_id, reader_id, issue_date, return_date, returned=False)
            await manager.issue_book(loan)

        elif choice == '7':
            loan_id = int(input('Enter loan ID to return: '))
            await manager.return_book(loan_id)
            print('Book returned!')

        elif choice == '8':
            await manager.get_active_loans()

        elif choice == '0':
            break

            

   


if __name__ == '__main__':
    asyncio.run(main())
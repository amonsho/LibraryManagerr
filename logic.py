from database import DatabaseConfig
from datetime import date, timedelta


async def registration(db, user, password_hash):
    try:
        async with db.pool.acquire() as conn:
            await conn.execute("""
            INSERT INTO users (username, password)
            VALUES ($1, $2);
    """, user, str(password_hash))
    except Exception as e:
        print('Error:', e)


async def login(db: DatabaseConfig, username, password):
    try:
        async with db.pool.acquire() as conn:
            user = await conn.fetchrow("""
        SELECT id FROM users WHERE username = $1 and password = $2
""", username, password)
            return user if user else None

    except Exception as e:
        print('Error:', e)


async def create_task(db: DatabaseConfig,
                      title: str,
                      description: str,
                      user_id: int):
    try:
        async with db.pool.acquire() as conn:
            await conn.execute("""
            INSERT INTO todos (title, description, user_id)
            VALUES ($1, $2, $3);
    """, title, description, user_id)
            print('Task added!')
    except Exception as e:
        print('Error:', e)


async def get_tasks(db, user_id):

    try:
        async with db.pool.acquire() as conn:
            # Baroi navistani zaprosoi get inro istifoda bared (conn.fetch())
            tasks = await conn.fetch("""
        SELECT * FROM todos WHERE user_id = $1;
""", user_id)
        return tasks
    except Exception as e:
        print('Error:', e)


async def update_task(db: DatabaseConfig,
                      task_id: int,
                      title: str,
                      description: str):
    try:
        async with db.pool.acquire() as conn:
            await conn.execute("""
    UPDATE todos SET title=$1, description=$2 WHERE id=$3;
""", title, description, int(task_id))
            print('Task updated!')
    except Exception as e:
        print('Error:', e)


class Book:

    def __init__(self, title, author, genre, year, copies):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.copies = copies

    async def save(self, db):
        async with db.pool.acquire() as conn:
            await conn.execute("""
    INSERT INTO books (title, author, genre, year, copies)
    VALUES ($1, $2, $3, $4, $5)
""", self.title, self.author, self.genre, int(self.year), int(self.copies))
        print('Book saved')

    @staticmethod
    async def decremment(db, book_id):
        try:
            async with db.pool.acquire() as conn:
                await conn.execute("""
                UPDATE books SET copies = copies - 1 WHERE id = $1;
                """, book_id)
        except Exception as e:
            print('Error from decrimment:', e)

    @staticmethod
    async def incremment(db, book_id):
        try:
            async with db.pool.acquire() as conn:
                await conn.execute("""
                UPDATE books SET copies = copies + 1 WHERE id = $1;
                """, book_id)
        except Exception as e:
            print('Error from decrimment:', e)


class Readers:
    def __init__(self, full_name, phone, email):
        self.full_name = full_name
        self.phone = phone
        self.email = email
    
    async def save(self, db):
        async with db.pool.acquire() as conn:
            await conn.execute("""
            insert into readers (full_name,phone,email)
            values($1,$2,$3)
""", self.full_name, self.phone, self.email)
        print('Readers Saved')
            

class Loan:
    def __init__(self, book_id, reader_id, issue_date, return_date):
        self.book_id = book_id
        self.reader_id = reader_id
        self.issue_date = issue_date
        self.return_date = return_date
        self.returned = False

        async def save(self, db):
            async with db.pool.acquire() as conn:
             await conn.execute("""
            insert into(book_id,reader_id,lissue_date,return_date,returned)
            values($1,$2,$3,$4,$5)

""", self.book_id, self.reader_id, self.issue_date, self.return_date, self.returned)
        print('Loans Saved')


class LibraryManager:
    def __init__(self, db):
        self.db = db

    async def add_book(self, title, author, genre, year, copies):
        book = Book(title, author, genre, year, copies)
        await book.save(self.db)

    async def get_books(self):
        try:
            async with self.db.pool.acquire() as conn:
                books = await conn.fetch("""
            select * from books
""")
                for i, book in enumerate(books, 1):
                    print(f'{i}. {book['title']} - {book['author']} - {book['year']}')
        except Exception as e:
            print('Error', e)

    async def search_book(self, text):
        try:
            async with self.db.pool.acquire() as conn:
                books = await conn.fetch(f"""
        SELECT * FROM books WHERE title ilike '%{text}%' OR genre ilike '%{text}%';
    """)
                for i, book in enumerate(books, 1):
                    print(f'{i}. {book['title']} - {book['author']} - {book['year']}')
        except Exception as e:
            print('Error from search:', e)

    async def add_reader(self, full_name, phone, email):
        reader = Readers(full_name, phone, email)
        await reader.save(self.db)
        print('Вы зарегистрировались!')

    async def get_users(self):
        try:
            async with self.db.pool.acquire() as conn:
                users = await conn.fetch("""
            select * from readers
""")
                for i, user in enumerate(users, 1):
                    print(f'{i}. {user['full_name']} - {user['phone']}')
        except Exception as e:
            print('Error', e)

    async def borrow_book(self, book_title, full_name):
        try:
            async with self.db.pool.acquire() as conn:
                book = await conn.fetchrow("""
        SELECT id FROM books WHERE title = $1;
    """, book_title)
                reader = await conn.fetchrow("""
        SELECT id FROM readers WHERE full_name = $1;
    """, full_name)
        except Exception as e:
            print('Error from borrow:', e)

        if not book:
            print('Такой книги нету!')
            return
        if not reader:
            print('Читатель не найден!')
            return
        issue_date = date.today()
        return_date = issue_date + timedelta(days=3)
        loan = Loan(book['id'], reader['id'], issue_date, return_date)
        await Book.decremment(self.db, book['id'])
        await loan.save(self.db)
        print('Вы взяли книгу!')

        async def return_book(self, book_title, full_name):
            try:
                async with self.db.pool.acquire() as conn:
                    book = await conn.fetchrow("""
         SELECT id FROM books WHERE title = $1;
      """, book_title)
                reader = await conn.fetchrow("""
          SELECT id FROM readers WHERE full_name = $1;
     """, full_name)
                if not book:
                    print('Такой книги нету!')
                    return
                if not reader:
                    print('Читатель не найден!')
                    return
                await conn.execute("""
    UPDATE loans SET returned = true WHERE book_id=$1 and reader_id=$2;
""", book['id'], reader['id'])
                await Book.incremment(self.db, book['id'])
                print('Книга возвращена!')
            except Exception as e:
                 print('Error from borrow:', e)
    
    async def get_loans(self):
        async with self.db.pool.acquire() as conn:
            loans = await conn.fetch("""
    select r.full_name, b.title, l.return_date from loans as l
    join books as b on b.id = l.book_id
    join readers as r on r.id = l.reader_id;
""")
            for i, loan in enumerate(loans, 1):
                print(f'{i}. {loan['full_name']} - {loan['title']} - {loan['return_date']}')
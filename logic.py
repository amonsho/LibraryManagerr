from database import DatabaseConfig

class Book:

    def __init__(self, title, author, genre, year, copies):
        self.title=title
        self.author=author
        self.genre=genre
        self.year=year
        self.copies=copies

    async def save(self, db:DatabaseConfig):
        async with db.pool.acquire() as conn:
            await conn.execute("""
    INSERT INTO books (title, author, genre, year, copies)
    VALUES($1, $2, $3, $4, $5)
""", self.title, self.author, self.genre, self.year, self.copies)
            print('Book saved!')

class Reader:

    def __init__(self, full_name, phone, email):
        self.full_name=full_name
        self.phone=phone
        self.email=email

    async def save(self,db:DatabaseConfig):
        async with db.pool.acquire() as conn:
            await conn.execute("""
    INSERT INTO readers (full_name, phone, email)
    VALUES($1, $2, $3)
""", self.full_name, self.phone, self.email)
            print('Readers saved!')


class Loan:

    def __init__(self, book_id, reader_id, issue_date, return_date, returned=False):
        self.book_id = book_id
        self.reader_id = reader_id
        self.issue_date = issue_date
        self.return_date = return_date
        self.returned = returned

    async def save(self, db:DatabaseConfig):
        async with db.pool.acquire() as conn:
            await conn.execute("""
    INSERT INTO loans (book_id, reader_id, issue_date, return_date, returned)
    VALUES($1, $2, $3, $4, $5)
""",self.book_id, self.reader_id, self.issue_date, self.return_date, self.returned)
         
               


class LibraryManager:

    def __init__(self,db:DatabaseConfig):
        self.db=db

    async def add_book(self, book:Book):
        await book.save(self.db)

    async def get_all_books(self):
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM books")
            return rows
        
    async def find_book(self, keyword):
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch("""
    SELECT * FROM books
    WHERE title ILIKE $1 OR author ILIKE $1
""", f'%{keyword}%')
            return rows

    async def add_reader(self,reader:Reader):
       await reader.save(self.db)

    async def get_all_readers(self):
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM readers")
            for row in rows:
                print(f"(id: {row['id']}) {row['full_name']} — {row['phone']} — {row['email']}")
            return rows
        
    async def issue_book(self,loan:Loan):
       await loan.save(self.db)

    async def get_active_loans(self):
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch("""
    SELECT * FROM loans WHERE returned = false
""")
            return rows
    
    async def return_book(self, loan_id):
        async with self.db.pool.acquire() as conn:
            await conn.execute("""
    UPDATE loans SET returned = true
    WHERE id = $1
""", loan_id)
        



    
        
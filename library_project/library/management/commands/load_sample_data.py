from django.core.management.base import BaseCommand
from library.models import Book, Member, BorrowRecord
from django.utils import timezone
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Load sample data for the library management system'

    def handle(self, *args, **options):
        # Clear existing data
        BorrowRecord.objects.all().delete()
        Book.objects.all().delete()
        Member.objects.all().delete()

        # Create sample books
        books_data = [
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': '978-0-06-112008-4',
                'publication_date': '1960-07-11',
                'is_available': True
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '978-0-452-28423-4',
                'publication_date': '1949-06-08',
                'is_available': True
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'isbn': '978-0-14-143951-8',
                'publication_date': '1813-01-28',
                'is_available': False
            },
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '978-0-7432-7356-5',
                'publication_date': '1925-04-10',
                'is_available': True
            },
            {
                'title': 'Lord of the Flies',
                'author': 'William Golding',
                'isbn': '978-0-571-05686-2',
                'publication_date': '1954-09-17',
                'is_available': False
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'isbn': '978-0-316-76948-0',
                'publication_date': '1951-07-16',
                'is_available': True
            }
        ]

        books = []
        for book_data in books_data:
            book = Book.objects.create(**book_data)
            books.append(book)
            self.stdout.write(f'Created book: {book.title}')

        # Create sample members
        members_data = [
            {
                'name': 'Alice Johnson',
                'email': 'alice.johnson@email.com',
                'member_id': 'MEM001',
                'join_date': timezone.now() - timedelta(days=365)
            },
            {
                'name': 'Bob Smith',
                'email': 'bob.smith@email.com',
                'member_id': 'MEM002',
                'join_date': timezone.now() - timedelta(days=200)
            },
            {
                'name': 'Carol Davis',
                'email': 'carol.davis@email.com',
                'member_id': 'MEM003',
                'join_date': timezone.now() - timedelta(days=100)
            },
            {
                'name': 'David Wilson',
                'email': 'david.wilson@email.com',
                'member_id': 'MEM004',
                'join_date': timezone.now() - timedelta(days=50)
            }
        ]

        members = []
        for member_data in members_data:
            member = Member.objects.create(**member_data)
            members.append(member)
            self.stdout.write(f'Created member: {member.name}')

        # Create sample borrow records
        borrow_records = [
            # Current borrows
            {
                'book': books[2],  # Pride and Prejudice
                'member': members[0],  # Alice
                'borrow_date': timezone.now() - timedelta(days=10),
                'is_returned': False
            },
            {
                'book': books[4],  # Lord of the Flies
                'member': members[1],  # Bob
                'borrow_date': timezone.now() - timedelta(days=5),
                'is_returned': False
            },
            # Past returns
            {
                'book': books[0],  # To Kill a Mockingbird
                'member': members[0],  # Alice
                'borrow_date': timezone.now() - timedelta(days=30),
                'return_date': timezone.now() - timedelta(days=15),
                'is_returned': True
            },
            {
                'book': books[1],  # 1984
                'member': members[2],  # Carol
                'borrow_date': timezone.now() - timedelta(days=25),
                'return_date': timezone.now() - timedelta(days=10),
                'is_returned': True
            },
            {
                'book': books[3],  # The Great Gatsby
                'member': members[3],  # David
                'borrow_date': timezone.now() - timedelta(days=20),
                'return_date': timezone.now() - timedelta(days=5),
                'is_returned': True
            }
        ]

        for record_data in borrow_records:
            record = BorrowRecord.objects.create(**record_data)
            self.stdout.write(f'Created borrow record: {record}')

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )
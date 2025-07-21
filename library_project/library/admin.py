from django.contrib import admin
from .models import Book, Member, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'is_available', 'publication_date')
    list_filter = ('is_available', 'author', 'publication_date')
    search_fields = ('title', 'author', 'isbn')
    list_editable = ('is_available',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_id', 'email', 'join_date')
    search_fields = ('name', 'member_id', 'email')
    list_filter = ('join_date',)

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'borrow_date', 'return_date', 'is_returned')
    list_filter = ('is_returned', 'borrow_date', 'return_date')
    search_fields = ('book__title', 'member__name')
    list_editable = ('is_returned',)

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    member_id = models.CharField(
        max_length=20, 
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9]+$', 'Member ID must contain only uppercase letters and numbers')]
    )
    join_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} ({self.member_id})"
    
    class Meta:
        ordering = ['name']

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(
        max_length=17, 
        unique=True,
        validators=[RegexValidator(r'^[0-9-]+$', 'ISBN must contain only numbers and hyphens')]
    )
    publication_date = models.DateField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    class Meta:
        ordering = ['title']

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.book.title} borrowed by {self.member.name}"
    
    class Meta:
        ordering = ['-borrow_date']

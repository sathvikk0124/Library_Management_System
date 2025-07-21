from django import forms
from .models import Book, Member, BorrowRecord

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date', 'is_available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 978-3-16-148410-0'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'member_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'member_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MEM001'}),
        }

class BorrowForm(forms.Form):
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(is_available=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a book"
    )
    member = forms.ModelChoiceField(
        queryset=Member.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a member"
    )
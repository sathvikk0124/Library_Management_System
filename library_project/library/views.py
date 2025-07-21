from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils import timezone
import csv
from .models import Book, Member, BorrowRecord
from .forms import BookForm, MemberForm, BorrowForm

def dashboard(request):
    """Dashboard view with statistics and recent activities"""
    total_books = Book.objects.count()
    total_members = Member.objects.count()
    borrowed_books = BorrowRecord.objects.filter(is_returned=False).count()
    available_books = Book.objects.filter(is_available=True).count()
    
    recent_borrows = BorrowRecord.objects.filter(is_returned=False).order_by('-borrow_date')[:5]
    recent_returns = BorrowRecord.objects.filter(is_returned=True).order_by('-return_date')[:5]
    
    context = {
        'total_books': total_books,
        'total_members': total_members,
        'borrowed_books': borrowed_books,
        'available_books': available_books,
        'recent_borrows': recent_borrows,
        'recent_returns': recent_returns,
    }
    return render(request, 'library/dashboard.html', context)

# Book Views
def book_list(request):
    """List all books with search and pagination"""
    query = request.GET.get('q')
    books = Book.objects.all()
    
    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) | 
            Q(isbn__icontains=query)
        )
    
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'library/book_list.html', context)

def book_create(request):
    """Create a new book"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Add'})

def book_edit(request, pk):
    """Edit an existing book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Edit'})

def book_delete(request, pk):
    """Delete a book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'library/book_confirm_delete.html', {'book': book})

# Member Views
def member_list(request):
    """List all members with search and pagination"""
    query = request.GET.get('q')
    members = Member.objects.all()
    
    if query:
        members = members.filter(
            Q(name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(member_id__icontains=query)
        )
    
    paginator = Paginator(members, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'library/member_list.html', context)

def member_create(request):
    """Create a new member"""
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added successfully!')
            return redirect('member_list')
    else:
        form = MemberForm()
    
    return render(request, 'library/member_form.html', {'form': form, 'action': 'Add'})

def member_edit(request, pk):
    """Edit an existing member"""
    member = get_object_or_404(Member, pk=pk)
    
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member updated successfully!')
            return redirect('member_list')
    else:
        form = MemberForm(instance=member)
    
    return render(request, 'library/member_form.html', {'form': form, 'action': 'Edit'})

def member_detail(request, pk):
    """View member details and borrowed books history"""
    member = get_object_or_404(Member, pk=pk)
    borrowed_books = BorrowRecord.objects.filter(member=member).order_by('-borrow_date')
    
    context = {
        'member': member,
        'borrowed_books': borrowed_books,
    }
    return render(request, 'library/member_detail.html', context)

# Borrow/Return Views
def borrow_return(request):
    """Handle book borrowing and returning"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'borrow':
            form = BorrowForm(request.POST)
            if form.is_valid():
                book = form.cleaned_data['book']
                member = form.cleaned_data['member']
                
                if book.is_available:
                    # Create borrow record
                    BorrowRecord.objects.create(book=book, member=member)
                    # Update book availability
                    book.is_available = False
                    book.save()
                    messages.success(request, f'Book "{book.title}" borrowed by {member.name}!')
                else:
                    messages.error(request, 'This book is already borrowed!')
        
        elif action == 'return':
            borrow_id = request.POST.get('borrow_id')
            borrow_record = get_object_or_404(BorrowRecord, pk=borrow_id, is_returned=False)
            
            # Update borrow record
            borrow_record.is_returned = True
            borrow_record.return_date = timezone.now()
            borrow_record.save()
            
            # Update book availability
            borrow_record.book.is_available = True
            borrow_record.book.save()
            
            messages.success(request, f'Book "{borrow_record.book.title}" returned successfully!')
        
        return redirect('borrow_return')
    
    # Get current borrowed books
    borrowed_books = BorrowRecord.objects.filter(is_returned=False).order_by('-borrow_date')
    available_books = Book.objects.filter(is_available=True)
    members = Member.objects.all()
    
    context = {
        'borrowed_books': borrowed_books,
        'available_books': available_books,
        'members': members,
        'borrow_form': BorrowForm(),
    }
    return render(request, 'library/borrow_return.html', context)

# Export Views
def export_books_csv(request):
    """Export books to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Author', 'ISBN', 'Publication Date', 'Available'])
    
    for book in Book.objects.all():
        writer.writerow([
            book.title,
            book.author,
            book.isbn,
            book.publication_date,
            'Yes' if book.is_available else 'No'
        ])
    
    return response

def export_members_csv(request):
    """Export members to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="members.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Member ID', 'Email', 'Join Date', 'Books Borrowed'])
    
    for member in Member.objects.all():
        books_borrowed = BorrowRecord.objects.filter(member=member).count()
        writer.writerow([
            member.name,
            member.member_id,
            member.email,
            member.join_date.strftime('%Y-%m-%d'),
            books_borrowed
        ])
    
    return response

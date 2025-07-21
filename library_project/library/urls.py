from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Book URLs
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Member URLs
    path('members/', views.member_list, name='member_list'),
    path('members/add/', views.member_create, name='member_create'),
    path('members/<int:pk>/edit/', views.member_edit, name='member_edit'),
    path('members/<int:pk>/', views.member_detail, name='member_detail'),
    
    # Borrow/Return URLs
    path('borrow-return/', views.borrow_return, name='borrow_return'),
    
    # Export URLs
    path('export/books/', views.export_books_csv, name='export_books'),
    path('export/members/', views.export_members_csv, name='export_members'),
]
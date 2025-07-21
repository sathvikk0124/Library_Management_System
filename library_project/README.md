# Django Library Management System

A complete web-based library management system built with Django, featuring book management, member registration, borrowing/returning functionality, and administrative tools.

## Features

### Core Functionality
- **Book Management**: Add, edit, delete, and search books with detailed information
- **Member Management**: Register and manage library members
- **Borrowing System**: Handle book borrowing and returning with real-time availability tracking
- **Dashboard**: Overview with statistics and recent activities
- **Search & Filter**: Advanced search capabilities for books and members
- **Pagination**: Efficient handling of large datasets

### Advanced Features
- **CSV Export**: Export books and members data to CSV files
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Admin Interface**: Django admin panel for advanced management
- **Form Validation**: Comprehensive input validation and error handling
- **Real-time Updates**: Live statistics and activity tracking

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, Bootstrap 5.1.3
- **Icons**: Font Awesome 6.0.0
- **Python**: 3.12+

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Library_Management_System
   ```

2. **Navigate to the Django project**
   ```bash
   cd library_project
   ```

3. **Install Django**
   ```bash
   pip install django
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python manage.py load_sample_data
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Usage

### Dashboard
- View overall statistics (total books, members, borrowed books)
- See recent borrowing and return activities
- Quick access to common actions

### Book Management
- **Add Books**: Include title, author, ISBN, publication date, and availability status
- **Search Books**: Filter by title, author, or ISBN
- **Edit/Delete**: Modify or remove book records
- **View Status**: Track which books are available or borrowed

### Member Management
- **Register Members**: Add new members with name, email, and unique member ID
- **View Members**: Browse all registered members with search functionality
- **Member Details**: View borrowing history and current status
- **Edit Information**: Update member details

### Borrowing System
- **Borrow Books**: Select available books and assign to members
- **Return Books**: Process book returns with automatic availability updates
- **Track Status**: Monitor currently borrowed books and due dates
- **History**: Complete borrowing and return history

### Data Export
- Export books and members data to CSV format
- Useful for reports and external data analysis

## Project Structure

```
library_project/
├── manage.py                 # Django management script
├── library_project/          # Project settings
│   ├── __init__.py
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
└── library/                 # Main application
    ├── __init__.py
    ├── admin.py             # Admin interface configuration
    ├── apps.py              # App configuration
    ├── models.py            # Database models
    ├── views.py             # View functions
    ├── urls.py              # URL routing
    ├── forms.py             # Django forms
    ├── migrations/          # Database migrations
    ├── management/          # Custom management commands
    │   └── commands/
    │       └── load_sample_data.py
    ├── templates/           # HTML templates
    │   └── library/
    │       ├── base.html
    │       ├── dashboard.html
    │       ├── book_list.html
    │       ├── book_form.html
    │       ├── book_confirm_delete.html
    │       ├── member_list.html
    │       ├── member_form.html
    │       ├── member_detail.html
    │       └── borrow_return.html
    └── static/              # Static files
        └── library/
            └── css/
                └── style.css
```

## Models

### Book
- Title, Author, ISBN, Publication Date
- Availability status tracking
- Validation for ISBN format

### Member
- Name, Email (unique), Member ID (unique)
- Join date tracking
- Validation for member ID format

### BorrowRecord
- Links books and members
- Tracks borrow date, return date, and status
- Complete borrowing history

## Screenshots

The application features a modern, responsive design with:
- Clean dashboard with statistics cards
- Intuitive navigation menu
- Professional forms with validation
- Data tables with search and pagination
- Success/error message notifications

## Development

### Adding New Features
1. Define models in `models.py`
2. Create forms in `forms.py`
3. Implement views in `views.py`
4. Add URL patterns in `urls.py`
5. Create templates in `templates/library/`
6. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Customization
- Modify `static/library/css/style.css` for custom styling
- Update templates for UI changes
- Extend models for additional functionality
- Configure settings in `settings.py`

## Production Deployment

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure allowed hosts
5. Use environment variables for sensitive settings
6. Set up proper logging
7. Consider using Gunicorn/uWSGI with Nginx

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Create an issue in the repository
- Check the Django documentation for framework-specific questions
- Review the code comments for implementation details
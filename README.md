# Campus Marketplace - Harbor

A student services platform for verified university students to advertise services, fundraisers, and items for sale.

## Project Names

- **Project Name**: Harbor
  - Represents the overall marketplace platform for campus services
  
- **Feature 1 Name**: listings
  - Core functionality revolves around creating and browsing listings

## Models

### Student
Represents verified university students. Email verification ensures campus safety.

- **Key Constraint**: Unique university email
- **Ordering**: Newest registrations first

### Category
Organizes listings into Services, Fundraisers, or Sellers for easy filtering.

- **Key Constraint**: Unique name per category type
- **Ordering**: Alphabetical

### Listing
Student-posted services, fundraisers, or items for sale.

- **Key Relationships**:
  - ForeignKey to Student (CASCADE) - If student leaves, their listings should too
  - ForeignKey to Category (PROTECT) - Can't delete categories with active listings
- **Key Constraint**: Student can't create duplicate listing titles
- **Ordering**: Newest listings first

## Setup Instructions

1. Create superuser: `python manage.py createsuperuser`
   - Username: tester
   - Password: uiuc12345

2. Run server: `python manage.py runserver`

3. Access admin: http://127.0.0.1:8000/admin/
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

## API Description
This project provides a public API to allow external applications to access and filter listing data.

1. Active Listings Data Endpoint
   - URL Path: /api/listings/
   - Method: GET
   - Format: JSON
   - Filtering: This endpoint supports filtering via query parameters. You can filter by category name by adding "?cat=" to the url.
   - Data Fields Provided:
     - Title: name of the listing
     - Price: cost of the items/services 
     - Category: the name of the category the listing is filed under
     - Seller: the first name of the student who posted the listing
2. MIME Type Demonstration Endpoint: created to demonstrate and observe the differences in MIME types between standard HTTP responses and JSON responses.
   - URL Path: /api/test/
   - Default Behavior (Json Response): returns the data with a "Content-Type: application/json" header. 
   - HTTP Override Behavior (HttpResponse): by adding "?type=http" to the URL, the view returns the data using HttpResponse
## Section 3: Static Files & UI Styling
	- Created Header and Footer Bar in navy blue 
	- Changed hyperlinks for pages into neat tabs
	- Made listings tabular in look as per the wireframe

## Deployment

**Live URL:** https://your-app-name.onrender.com
**Deployed on:** Render.com (Free Tier)

**Environment:**
- Python 3.11
- Django 5.2
- Gunicorn WSGI server
- WhiteNoise for static files
- SQLite database

**Deployment Process:**
1. Code pushed to GitHub
2. Render automatically builds and deploys
3. Static files collected via WhiteNoise
4. Migrations run automatically
5. App served via Gunicorn

**Environment Variables:**
- DJANGO_ENV=prod
- DEBUG=False
- SECRET_KEY (auto-generated)
# job_portal_website
# Job Portal Application

A complete job portal web application built with Flask, featuring user authentication, job posting, and application management.

## Features

### User Roles
- **Job Seekers**: Register, search jobs, apply for positions
- **Employers**: Post jobs, manage listings, view applications
- **Admin**: Manage users and job postings

### Core Functionality
- User registration and authentication
- Job posting with detailed information (title, description, salary, location, category)
- Advanced job search with filters (location, category, company, keywords)
- Job application system with cover letters
- Application status tracking (pending, accepted, rejected)
- Responsive Bootstrap UI design

## Tech Stack
- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Bootstrap 5.1.3
- **Database**: SQLite
- **Forms**: Flask-WTF with WTForms
- **Authentication**: Flask-Login

## Project Structure
```
job-portal/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── forms.py              # WTForms for user input
├── auth.py               # Authentication blueprint
├── jobs.py               # Job management blueprint
├── applications.py       # Application management blueprint
├── static/
│   └── css/
│       └── style.css     # Custom CSS styles
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── auth/
│   │   ├── login.html    # Login page
│   │   └── register.html # Registration page
│   ├── jobs/
│   │   ├── list.html     # Job listings
│   │   ├── detail.html   # Job details
│   │   └── create.html   # Job creation form
│   └── applications/
│       ├── apply.html    # Job application form
│       └── my_applications.html # User's applications
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Setup Instructions

### 1. Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### 2. Installation (Local Setup)
```bash
# Clone or download the project
cd job-portal

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### 3. Replit Setup (Recommended)
1. Open the project in Replit
2. Dependencies will be automatically installed
3. Click the "Run" button to start the application
4. The app will be available at the provided URL

### 4. Database Setup
The SQLite database (`job_portal.db`) will be automatically created when you first run the application. No manual setup required.

## Usage

### For Job Seekers
1. Register for an account (leave "Register as Employer" unchecked)
2. Browse job listings on the homepage
3. Use search filters to find relevant positions
4. Click on job titles to view details
5. Apply for jobs with a cover letter
6. Track your applications in "My Applications"

### For Employers
1. Register for an account (check "Register as Employer")
2. Navigate to "Post a Job" to create job listings
3. Manage your posted jobs
4. View applications received for your jobs
5. Accept or reject applications

## Key Features Demonstrated

### Authentication System
- Secure password hashing using Werkzeug
- Session management with Flask-Login
- Role-based access control (job seekers vs employers)

### Database Design
- User model with authentication and profile data
- Job model with comprehensive job information
- Application model linking users to jobs
- Proper foreign key relationships

### Search & Filtering
- Keyword search in job titles and descriptions
- Location-based filtering
- Category filtering
- Company name filtering
- Sorting by creation date

### Responsive Design
- Mobile-friendly Bootstrap layout
- Modern CSS styling with custom design elements
- Intuitive user interface

## API Endpoints

### Authentication
- `GET/POST /auth/register` - User registration
- `GET/POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Jobs
- `GET /jobs/` - List all jobs with search
- `GET /jobs/<id>` - Job details
- `GET/POST /jobs/create` - Create new job (employers only)
- `GET/POST /jobs/<id>/edit` - Edit job (owner only)
- `POST /jobs/<id>/delete` - Delete job (owner only)
- `GET /jobs/my-jobs` - Employer's job listings

### Applications
- `GET/POST /applications/job/<id>/apply` - Apply for job
- `GET /applications/my-applications` - User's applications
- `GET /applications/job/<id>/applications` - Job applications (employer)
- `POST /applications/application/<id>/update-status` - Update application status

## Security Features
- Password hashing with salt
- CSRF protection on all forms
- SQL injection prevention through SQLAlchemy ORM
- Session-based authentication
- Role-based access control

## Future Enhancements
- Email notifications for applications
- File upload for resumes
- Advanced employer profiles
- Job recommendation system
- Real-time chat between employers and applicants

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License
This project is created for educational purposes.

## Contact
For questions or support, please contact the development team.

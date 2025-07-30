# 🧑‍💼 Django Job Portal Application with Search

## 📌 Overview

This is a basic **Job Portal Web Application** built using **Django**, where employers can post job listings and applicants can view, search, and apply for those jobs. The project showcases full-stack development skills including user authentication, file uploads, model relationships, and search functionality.

![Job Portal UI](https://github.com/RadoanulArifen/JobPortal/blob/0eee0d9e18833615bf00ab07cabda5250867d289/UI%20of%20JobPortal.png?raw=true)

---

## 🎯 Objective

To develop a role-based job portal with core features:
- Employers can post and manage job listings.
- Applicants can view job postings, search by criteria, and submit applications.

---

## 🔑 Demo Admin Credentials (Optional)

> These credentials are for demo/testing purposes only.

- Username: `admin`
- Password: `admin`

---

## 🔐 User Roles & Authentication

- Two types of users: **Employer** and **Applicant**
- Features:
  - User Registration & Login
  - Logout with Role-Based Redirection
  - Role-Specific Dashboards:
    - Employers: Post & manage jobs, view applicants
    - Applicants: View jobs, apply, and manage applications

---

## 🧱 Models

### `Job`
| Field         | Description                          |
|---------------|--------------------------------------|
| title         | Job title                            |
| company_name  | Company offering the job             |
| location      | Job location                         |
| description   | Detailed job description             |
| posted_by     | ForeignKey to User (Employer only)   |
| created_at    | Timestamp for when the job was posted|

### `Application`
| Field         | Description                          |
|---------------|--------------------------------------|
| job           | ForeignKey to Job                    |
| applicant     | ForeignKey to User (Applicant only)  |
| resume        | Uploaded resume (FileField)          |
| cover_letter  | Text field for applicant's message   |
| applied_at    | Timestamp of application submission  |

---

## ✅ Features

### For Employers:
- Post new jobs
- View all posted jobs
- View applicants for each job

### For Applicants:
- View available job listings
- Apply with resume and cover letter
- View their own submitted applications

---

## 🔍 Job Search

Applicants can filter job listings by:
- **Job Title**
- **Company Name**
- **Location**

A search bar is provided on the job listings page for real-time filtering.

---

## 🖥 Frontend

- Basic responsive UI using HTML/CSS (Bootstrap or plain)
- Role-based navigation
- Job list & detail pages
- File upload support for resumes
- Search functionality on job list page

---

## ⚙️ Admin Panel

- Registered `Job` and `Application` models
- Customized list display for:
  - Job: `title`, `company_name`, `posted_by`
  - Application: `job`, `applicant`, `applied_at`

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Django 4.x
- SQLite (default) or any database of choice

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/RadoanulArifen/JobPortal.git
cd JobPortal

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate         # For Unix/macOS
# OR
venv\Scripts\activate            # For Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Start the development server
python manage.py runserver

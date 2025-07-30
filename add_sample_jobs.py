#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobProject.settings')
django.setup()

from django.contrib.auth.models import User
from job_app.models import Job, Profile

def create_sample_jobs():
    # Create a test user if it doesn't exist
    user, created = User.objects.get_or_create(
        username='test_employee',
        defaults={
            'email': 'employee@test.com',
            'first_name': 'Test',
            'last_name': 'Employee'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        
        # Create profile for the user
        Profile.objects.create(user=user, role='employee')
        print(f"Created test user: {user.username}")
    
    # Sample job data
    sample_jobs = [
        {
            'title': 'Senior Software Engineer',
            'company_name': 'TechCorp Solutions',
            'location': 'San Francisco, CA',
            'description': 'We are looking for a Senior Software Engineer to join our growing team. You will be responsible for developing high-quality software solutions, mentoring junior developers, and collaborating with cross-functional teams. Requirements: 5+ years of experience in Python, JavaScript, and cloud technologies.'
        },
        {
            'title': 'Frontend Developer',
            'company_name': 'Digital Innovations Inc',
            'location': 'New York, NY',
            'description': 'Join our creative team as a Frontend Developer. You will build beautiful, responsive user interfaces using React, Vue.js, and modern CSS. We value creativity, attention to detail, and user experience expertise.'
        },
        {
            'title': 'Data Scientist',
            'company_name': 'Analytics Pro',
            'location': 'Austin, TX',
            'description': 'We are seeking a Data Scientist to help us extract insights from large datasets. You will work with machine learning models, statistical analysis, and data visualization. Experience with Python, R, and SQL required.'
        },
        {
            'title': 'Product Manager',
            'company_name': 'StartupXYZ',
            'location': 'Seattle, WA',
            'description': 'Lead product strategy and development for our innovative SaaS platform. You will work closely with engineering, design, and marketing teams to deliver exceptional user experiences. 3+ years of product management experience required.'
        },
        {
            'title': 'DevOps Engineer',
            'company_name': 'Cloud Systems Ltd',
            'location': 'Remote',
            'description': 'Help us build and maintain our cloud infrastructure. You will work with AWS, Docker, Kubernetes, and CI/CD pipelines. We need someone who is passionate about automation and scalability.'
        },
        {
            'title': 'UX/UI Designer',
            'company_name': 'Creative Studios',
            'location': 'Los Angeles, CA',
            'description': 'Create stunning user experiences and beautiful interfaces. You will work on web and mobile applications, conduct user research, and collaborate with developers. Proficiency in Figma, Sketch, and Adobe Creative Suite required.'
        },
        {
            'title': 'Marketing Specialist',
            'company_name': 'Growth Marketing Co',
            'location': 'Chicago, IL',
            'description': 'Drive our digital marketing efforts across multiple channels. You will manage social media campaigns, email marketing, and content creation. Experience with Google Analytics, Facebook Ads, and email marketing platforms preferred.'
        },
        {
            'title': 'Sales Representative',
            'company_name': 'Enterprise Sales Inc',
            'location': 'Boston, MA',
            'description': 'Join our sales team and help us grow our enterprise client base. You will be responsible for prospecting, qualifying leads, and closing deals. Strong communication skills and sales experience required.'
        },
        {
            'title': 'Customer Success Manager',
            'company_name': 'SaaS Solutions',
            'location': 'Denver, CO',
            'description': 'Ensure our customers achieve their goals with our platform. You will onboard new customers, provide training, and maintain strong relationships. Excellent communication and problem-solving skills required.'
        }
    ]
    
    # Create jobs
    created_count = 0
    for job_data in sample_jobs:
        job, created = Job.objects.get_or_create(
            title=job_data['title'],
            company_name=job_data['company_name'],
            defaults={
                'location': job_data['location'],
                'description': job_data['description'],
                'posted_by': user
            }
        )
        if created:
            created_count += 1
            print(f"Created job: {job.title} at {job.company_name}")
    
    print(f"\nTotal jobs created: {created_count}")
    print(f"Total jobs in database: {Job.objects.count()}")

if __name__ == '__main__':
    create_sample_jobs() 
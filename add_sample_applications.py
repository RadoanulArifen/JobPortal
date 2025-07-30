#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobProject.settings')
django.setup()

from django.contrib.auth.models import User
from job_app.models import Job, Application, Profile

def create_sample_applications():
    # Create a test applicant user if it doesn't exist
    applicant, created = User.objects.get_or_create(
        username='test_applicant',
        defaults={
            'email': 'applicant@test.com',
            'first_name': 'Test',
            'last_name': 'Applicant'
        }
    )
    
    if created:
        applicant.set_password('testpass123')
        applicant.save()
        
        # Create profile for the user
        Profile.objects.create(user=applicant, role='applicant')
        print(f"Created test applicant: {applicant.username}")
    
    # Get some existing jobs
    jobs = Job.objects.all()[:5]  # Get first 5 jobs
    
    if not jobs:
        print("No jobs found. Please run add_sample_jobs.py first.")
        return
    
    # Sample cover letters
    sample_cover_letters = [
        "I am excited to apply for this position. With my background in software development and passion for creating innovative solutions, I believe I would be a great fit for your team. I have experience with modern technologies and a track record of delivering high-quality results.",
        
        "Thank you for considering my application. I am particularly interested in this role because it aligns perfectly with my career goals and technical expertise. I am confident that my skills and experience would make me a valuable addition to your organization.",
        
        "I am writing to express my strong interest in this position. My experience in this field, combined with my enthusiasm for learning and growth, makes me an ideal candidate. I am excited about the opportunity to contribute to your team's success.",
        
        "I am thrilled to apply for this opportunity. This role represents exactly the type of challenge I am looking for in my next career move. I am confident that my background and skills would enable me to make immediate contributions to your organization.",
        
        "I am very interested in this position and believe my qualifications make me an excellent candidate. I am particularly drawn to your company's mission and values, and I am excited about the opportunity to grow with your organization."
    ]
    
    # Create applications
    created_count = 0
    for i, job in enumerate(jobs):
        # Check if application already exists
        existing_application = Application.objects.filter(
            applicant=applicant,
            job=job
        ).first()
        
        if not existing_application:
            application = Application.objects.create(
                applicant=applicant,
                job=job,
                cover_letter=sample_cover_letters[i % len(sample_cover_letters)]
            )
            created_count += 1
            print(f"Created application: {applicant.username} applied to {job.title} at {job.company_name}")
    
    print(f"\nTotal applications created: {created_count}")
    print(f"Total applications for {applicant.username}: {Application.objects.filter(applicant=applicant).count()}")

if __name__ == '__main__':
    create_sample_applications() 
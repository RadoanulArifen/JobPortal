from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Application
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.http import HttpResponseForbidden

# Auth Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.get_full_name()}!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

# Homepage
def homepage(request):
    # Get search parameters
    title_query = request.GET.get('title', '')
    company_query = request.GET.get('company', '')
    location_query = request.GET.get('location', '')
    
    # Start with all jobs
    jobs = Job.objects.all()
    
    # Apply filters if search parameters are provided
    if title_query:
        jobs = jobs.filter(title__icontains=title_query)
    if company_query:
        jobs = jobs.filter(company_name__icontains=company_query)
    if location_query:
        jobs = jobs.filter(location__icontains=location_query)
    
    # Get recent jobs (either filtered or all)
    recent_jobs = jobs.order_by('-created_at')[:9]  # Show latest 9 jobs
    total_jobs = jobs.count()
    
    # Get user's applied job IDs if authenticated
    user_applied_jobs = []
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'applicant':
        user_applied_jobs = list(Application.objects.filter(applicant=request.user).values_list('job_id', flat=True))
    
    context = {
        'recent_jobs': recent_jobs,
        'total_jobs': total_jobs,
        'search_performed': any([title_query, company_query, location_query]),
        'search_params': {
            'title': title_query,
            'company': company_query,
            'location': location_query,
        },
        'user_applied_jobs': user_applied_jobs,
    }
    return render(request, 'homepage.html', context)

# Applicant Views
def applicant_dashboard(request):
    return render(request, 'applicant/dashboard.html')

def job_listings(request):
    # Get search parameters
    title_query = request.GET.get('title', '')
    company_query = request.GET.get('company', '')
    location_query = request.GET.get('location', '')
    
    # Start with all jobs
    jobs = Job.objects.all()
    
    # Apply filters if search parameters are provided
    if title_query:
        jobs = jobs.filter(title__icontains=title_query)
    if company_query:
        jobs = jobs.filter(company_name__icontains=company_query)
    if location_query:
        jobs = jobs.filter(location__icontains=location_query)
    
    # Order by creation date (newest first)
    jobs = jobs.order_by('-created_at')
    
    # Get user's applied job IDs if authenticated
    user_applied_jobs = []
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'applicant':
        user_applied_jobs = list(Application.objects.filter(applicant=request.user).values_list('job_id', flat=True))
    
    context = {
        'jobs': jobs,
        'total_jobs': jobs.count(),
        'search_performed': any([title_query, company_query, location_query]),
        'search_params': {
            'title': title_query,
            'company': company_query,
            'location': location_query,
        },
        'user_applied_jobs': user_applied_jobs,
    }
    return render(request, 'applicant/job_listings.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user has already applied to this job
    has_applied = False
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'applicant':
        has_applied = Application.objects.filter(applicant=request.user, job=job).exists()
    
    # Get similar jobs (same company or similar titles, excluding current job)
    similar_jobs = Job.objects.filter(
        models.Q(company_name=job.company_name) | 
        models.Q(title__icontains=job.title.split()[0])  # Jobs with similar title keywords
    ).exclude(id=job.id).order_by('-created_at')[:3]
    
    context = {
        'job': job,
        'similar_jobs': similar_jobs,
        'has_applied': has_applied,
    }
    return render(request, 'job_detail.html', context)

@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user is an applicant
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'applicant':
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('job_detail', job_id=job_id)
    
    # Check if user has already applied
    existing_application = Application.objects.filter(applicant=request.user, job=job).first()
    if existing_application:
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)
    
    if request.method == 'POST':
        # Handle file upload and application submission
        cover_letter = request.POST.get('cover_letter', '')
        resume = request.FILES.get('resume')
        
        if not cover_letter.strip():
            messages.error(request, 'Please provide a cover letter.')
            return render(request, 'applicant/apply.html', {'job': job})
        
        # Create the application
        application = Application.objects.create(
            applicant=request.user,
            job=job,
            cover_letter=cover_letter,
            resume=resume
        )
        
        messages.success(request, f'Your application for "{job.title}" has been submitted successfully!')
        return redirect('my_applications')
    
    context = {
        'job': job,
    }
    return render(request, 'applicant/apply.html', context)

@login_required
def my_applications(request):
    # Get all applications for the current user
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')
    
    context = {
        'applications': applications,
        'total_applications': applications.count(),
    }
    return render(request, 'applicant/my_applications.html', context)



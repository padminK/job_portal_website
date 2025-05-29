from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models import Job, db
from forms import JobForm, JobSearchForm
from sqlalchemy import or_

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/')
def list_jobs():
    """Display all job listings with optional filtering."""
    form = JobSearchForm()

    # Get query parameters for filtering
    keyword = request.args.get('keyword', '')
    location = request.args.get('location', '')
    category = request.args.get('category', '')
    company = request.args.get('company', '')

    # Base query
    query = Job.query

    # Apply filters if provided
    if keyword:
        query = query.filter(or_(
            Job.title.contains(keyword),
            Job.description.contains(keyword)
        ))
    if location:
        query = query.filter(Job.location.contains(location))
    if category and category != '':
        query = query.filter(Job.category == category)
    if company:
        query = query.filter(Job.company.contains(company))

    # Get results ordered by most recent
    jobs = query.order_by(Job.created_at.desc()).all()

    return render_template('jobs/list.html', title='Job Listings', jobs=jobs, form=form)

@jobs_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_job():
    """Create a new job listing."""
    if not current_user.is_employer:
        flash('Only employers can post jobs.', 'danger')
        return redirect(url_for('jobs.list_jobs'))

    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            company=form.company.data,
            description=form.description.data,
            salary=form.salary.data,
            location=form.location.data,
            category=form.category.data,
            employer_id=current_user.id
        )

        db.session.add(job)
        db.session.commit()

        flash('Your job has been posted!', 'success')
        return redirect(url_for('jobs.detail_job', job_id=job.id))

    return render_template('jobs/create.html', title='Post a Job', form=form)

@jobs_bp.route('/<int:job_id>')
def detail_job(job_id):
    """Display details of a specific job."""
    job = Job.query.get_or_404(job_id)
    return render_template('jobs/detail.html', title=job.title, job=job)

@jobs_bp.route('/my-jobs')
@login_required
def my_jobs():
    """Display jobs posted by the current user."""
    if not current_user.is_employer:
        flash('Only employers can access this page.', 'danger')
        return redirect(url_for('jobs.list_jobs'))

    jobs = Job.query.filter_by(employer_id=current_user.id).order_by(Job.created_at.desc()).all()
    return render_template('jobs/my_jobs.html', title='My Job Listings', jobs=jobs)

@jobs_bp.route('/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    """Edit an existing job listing."""
    job = Job.query.get_or_404(job_id)

    if job.employer_id != current_user.id:
        flash('You can only edit your own job listings.', 'danger')
        return redirect(url_for('jobs.list_jobs'))

    form = JobForm()

    if form.validate_on_submit():
        job.title = form.title.data
        job.company = form.company.data
        job.description = form.description.data
        job.salary = form.salary.data
        job.location = form.location.data
        job.category = form.category.data

        db.session.commit()

        flash('Your job listing has been updated!', 'success')
        return redirect(url_for('jobs.detail_job', job_id=job.id))

    elif request.method == 'GET':
        form.title.data = job.title
        form.company.data = job.company
        form.description.data = job.description
        form.salary.data = job.salary
        form.location.data = job.location
        form.category.data = job.category

    return render_template('jobs/edit.html', title='Edit Job', form=form, job=job)

@jobs_bp.route('/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    """Delete a job listing."""
    job = Job.query.get_or_404(job_id)

    if job.employer_id != current_user.id:
        flash('You can only delete your own job listings.', 'danger')
        return redirect(url_for('jobs.list_jobs'))

    db.session.delete(job)
    db.session.commit()

    flash('Your job listing has been deleted.', 'success')
    return redirect(url_for('jobs.my_jobs'))
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models import Job, Application, db
from forms import JobForm, JobSearchForm

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/')
def list_jobs():
    """List all available jobs with search functionality."""
    form = JobSearchForm()
    jobs = Job.query
    
    if form.validate_on_submit():
        if form.keyword.data:
            jobs = jobs.filter(Job.title.contains(form.keyword.data) | 
                             Job.description.contains(form.keyword.data))
        if form.location.data:
            jobs = jobs.filter(Job.location.contains(form.location.data))
        if form.category.data:
            jobs = jobs.filter(Job.category == form.category.data)
        if form.company.data:
            jobs = jobs.filter(Job.company.contains(form.company.data))
    
    jobs = jobs.order_by(Job.created_at.desc()).all()
    return render_template('jobs/list.html', title='Jobs', jobs=jobs, form=form)

@jobs_bp.route('/<int:job_id>')
def detail_job(job_id):
    """Show job details."""
    job = Job.query.get_or_404(job_id)
    user_applied = False
    
    if current_user.is_authenticated and not current_user.is_employer:
        user_applied = Application.query.filter_by(
            user_id=current_user.id, 
            job_id=job_id
        ).first() is not None
    
    return render_template('jobs/detail.html', title=job.title, job=job, user_applied=user_applied)

@jobs_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_job():
    """Create a new job posting (employers only)."""
    if not current_user.is_employer:
        flash('Only employers can post jobs.', 'danger')
        return redirect(url_for('jobs.list_jobs'))
    
    form = JobForm()
    
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            company=form.company.data,
            location=form.location.data,
            salary=form.salary.data,
            category=form.category.data,
            description=form.description.data,
            employer_id=current_user.id
        )
        
        db.session.add(job)
        db.session.commit()
        
        flash('Your job posting has been created!', 'success')
        return redirect(url_for('jobs.detail_job', job_id=job.id))
    
    return render_template('jobs/create.html', title='Post a Job', form=form)

@jobs_bp.route('/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    """Edit a job posting (employer only)."""
    job = Job.query.get_or_404(job_id)
    
    if not current_user.is_employer or job.employer_id != current_user.id:
        flash('You can only edit your own job postings.', 'danger')
        return redirect(url_for('jobs.detail_job', job_id=job_id))
    
    form = JobForm(obj=job)
    
    if form.validate_on_submit():
        job.title = form.title.data
        job.company = form.company.data
        job.location = form.location.data
        job.salary = form.salary.data
        job.category = form.category.data
        job.description = form.description.data
        
        db.session.commit()
        
        flash('Your job posting has been updated!', 'success')
        return redirect(url_for('jobs.detail_job', job_id=job.id))
    
    return render_template('jobs/edit.html', title='Edit Job', form=form, job=job)

@jobs_bp.route('/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    """Delete a job posting (employer only)."""
    job = Job.query.get_or_404(job_id)
    
    if not current_user.is_employer or job.employer_id != current_user.id:
        flash('You can only delete your own job postings.', 'danger')
        return redirect(url_for('jobs.detail_job', job_id=job_id))
    
    db.session.delete(job)
    db.session.commit()
    
    flash('Your job posting has been deleted.', 'success')
    return redirect(url_for('jobs.list_jobs'))

@jobs_bp.route('/my-jobs')
@login_required
def my_jobs():
    """View jobs posted by the current employer."""
    if not current_user.is_employer:
        flash('This page is for employers only.', 'danger')
        return redirect(url_for('jobs.list_jobs'))
    
    jobs = Job.query.filter_by(employer_id=current_user.id).order_by(Job.created_at.desc()).all()
    return render_template('jobs/my_jobs.html', title='My Job Postings', jobs=jobs)

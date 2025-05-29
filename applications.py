from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models import Application, Job, db
from forms import ApplicationForm

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/job/<int:job_id>/apply', methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    """Apply for a job."""
    if current_user.is_employer:
        flash('Employers cannot apply for jobs.', 'danger')
        return redirect(url_for('jobs.detail_job', job_id=job_id))

    job = Job.query.get_or_404(job_id)

    # Check if user has already applied
    existing_application = Application.query.filter_by(
        user_id=current_user.id, 
        job_id=job_id
    ).first()

    if existing_application:
        flash('You have already applied for this job.', 'info')
        return redirect(url_for('jobs.detail_job', job_id=job_id))

    form = ApplicationForm()

    if form.validate_on_submit():
        application = Application(
            user_id=current_user.id,
            job_id=job_id,
            cover_letter=form.cover_letter.data
        )

        db.session.add(application)
        db.session.commit()

        flash('Your application has been submitted!', 'success')
        return redirect(url_for('jobs.detail_job', job_id=job_id))

    return render_template('applications/apply.html', title='Apply for Job', form=form, job=job)

@applications_bp.route('/my-applications')
@login_required
def my_applications():
    """View applications made by the current user."""
    if current_user.is_employer:
        flash('This page is for job seekers only.', 'danger')
        return redirect(url_for('jobs.list_jobs'))

    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('applications/my_applications.html', title='My Applications', applications=applications)

@applications_bp.route('/job/<int:job_id>/applications')
@login_required
def job_applications(job_id):
    """View applications for a specific job (employer only)."""
    job = Job.query.get_or_404(job_id)

    if not current_user.is_employer or job.employer_id != current_user.id:
        flash('You can only view applications for your own job listings.', 'danger')
        return redirect(url_for('jobs.list_jobs'))

    applications = Application.query.filter_by(job_id=job_id).all()
    return render_template('applications/job_applications.html', title='Applications', applications=applications, job=job)

@applications_bp.route('/application/<int:application_id>/update-status', methods=['POST'])
@login_required
def update_application_status(application_id):
    """Update the status of an application (accept/reject)."""
    application = Application.query.get_or_404(application_id)
    job = Job.query.get_or_404(application.job_id)

    if not current_user.is_employer or job.employer_id != current_user.id:
        flash('You can only update applications for your own job listings.', 'danger')
        return redirect(url_for('jobs.list_jobs'))

    status = request.form.get('status')
    if status in ['accepted', 'rejected']:
        application.status = status
        db.session.commit()
        flash(f'Application has been {status}.', 'success')

    return redirect(url_for('applications.job_applications', job_id=job.id))

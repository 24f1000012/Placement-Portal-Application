from models import db, Student, PlacementDrive, Application
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class StudentService:

    @staticmethod
    def get_student_by_user_id(user_id):
        return Student.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_student_stats(student_id):
        total_applications = Application.query.filter_by(student_id=student_id).count()
        shortlisted = Application.query.filter_by(student_id=student_id, status='shortlisted').count()
        selected = Application.query.filter_by(student_id=student_id, status='selected').count()
        rejected = Application.query.filter_by(student_id=student_id, status='rejected').count()
        available_jobs = PlacementDrive.query.filter_by(status='approved').count()

        return {
            'total_applications': total_applications,
            'shortlisted': shortlisted,
            'selected': selected,
            'rejected': rejected,
            'available_jobs': available_jobs
        }

    @staticmethod
    def update_profile(student_id, name, phone, department, cgpa, skills, resume_file, upload_folder):
       
        student = Student.query.get(student_id)
        if not student:
            return False, "Student not found"

        try:
            student.name = name
            student.phone = phone
            student.department = department
            student.cgpa = float(cgpa) if cgpa else None
            student.skills = skills

            # Handle resume file upload
            if resume_file and resume_file.filename != '':
                if not allowed_file(resume_file.filename):
                    return False, "Invalid file type. Only PDF, DOC, DOCX allowed."

                filename = secure_filename(f"resume_{student_id}_{resume_file.filename}")
                save_path = os.path.join(upload_folder, filename)
                resume_file.save(save_path)
                student.resume = f"static/uploads/{filename}"

            db.session.commit()
            return True, "Profile updated successfully!"

        except Exception as e:
            db.session.rollback()
            return False, f"Update failed: {str(e)}"

    @staticmethod
    def get_approved_drives(search_query=None, search_type=None):
        
        query = PlacementDrive.query.filter_by(status='approved')

        if search_query and search_type:
            if search_type == 'position':
                query = query.filter(PlacementDrive.job_title.ilike(f'%{search_query}%'))
            elif search_type == 'skills':
                query = query.filter(PlacementDrive.eligibility.ilike(f'%{search_query}%'))
            elif search_type == 'company':
                from models import Company
                query = query.join(Company).filter(Company.name.ilike(f'%{search_query}%'))

        return query.order_by(PlacementDrive.created_at.desc()).all()

    @staticmethod
    def apply_to_drive(student_id, drive_id):
        student = Student.query.get(student_id)
        if not student:
            return False, "Student not found"

        if student.is_blacklisted:
            return False, "You are blacklisted and cannot apply."

        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return False, "Drive not found"

        if drive.status != 'approved':
            return False, "This drive is not open for applications."

        existing = Application.query.filter_by(
            student_id=student_id,
            drive_id=drive_id
        ).first()

        if existing:
            return False, "You have already applied to this drive."

        try:
            application = Application(
                student_id=student_id,
                drive_id=drive_id,
                status='applied'
            )
            db.session.add(application)
            db.session.commit()
            return True, f"Successfully applied to '{drive.job_title}'!"

        except Exception as e:
            db.session.rollback()
            return False, f"Application failed: {str(e)}"

    @staticmethod
    def get_student_applications(student_id):
        return Application.query.filter_by(student_id=student_id)\
            .order_by(Application.applied_date.desc()).all()
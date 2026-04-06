from models import db, Company, PlacementDrive, Application
from datetime import datetime

class CompanyService:
    
    @staticmethod
    def get_company_by_user_id(user_id):
        """Get company profile by user_id"""
        return Company.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def get_company_stats(company_id):
        """Get statistics for company dashboard"""
        total_drives = PlacementDrive.query.filter_by(company_id=company_id).count()
        pending_drives = PlacementDrive.query.filter_by(company_id=company_id, status='pending').count()
        approved_drives = PlacementDrive.query.filter_by(company_id=company_id, status='approved').count()
        
        # Count total applications to this company's drives
        drives = PlacementDrive.query.filter_by(company_id=company_id).all()
        total_applications = sum([len(drive.applications) for drive in drives])
        
        return {
            'total_drives': total_drives,
            'pending_drives': pending_drives,
            'approved_drives': approved_drives,
            'total_applications': total_applications
        }
    
    @staticmethod
    def create_drive(company_id, job_title, job_description, eligibility, salary, location, application_deadline):
        """
        Create a new placement drive
        Returns: (success: bool, message: str)
        """
        company = Company.query.get(company_id)
        
        if not company:
            return False, "Company not found"
        
        if company.approval_status != 'approved':
            return False, "Your company is not approved by admin yet"
        
        if company.is_blacklisted:
            return False, "Your company is blacklisted"
        
        try:
            drive = PlacementDrive(
                company_id=company_id,
                job_title=job_title,
                job_description=job_description,
                eligibility=eligibility,
                salary=salary,
                location=location,
                application_deadline=application_deadline,
                status='pending'  # Needs admin approval!
            )
            db.session.add(drive)
            db.session.commit()
            
            return True, "Placement drive created! Waiting for admin approval."
        
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to create drive: {str(e)}"
    
    @staticmethod
    def get_company_drives(company_id):
        """Get all drives created by a company"""
        return PlacementDrive.query.filter_by(company_id=company_id).order_by(PlacementDrive.created_at.desc()).all()
from models import db, Company, Student, Application, PlacementDrive

class AdminService:
##########################################################################
########################### Company ######################################
##########################################################################
    @staticmethod
    def get_all_companies(status=None):
        """Get all companies, optionally filtered by status"""
        if status:
            return Company.query.filter_by(approval_status=status).all()
        return Company.query.all()
    
    @staticmethod
    def get_company_by_name(name):
        """Get company by name"""
        company = Company.query.filter_by(name=name).first()  # ← Added .first()
        if not company:
            return False, "Company not found"
        return True, company
    
    @staticmethod
    def get_company_by_id(company_id):
        """Get company by ID"""
        company = Company.query.get(company_id)  # ← Use .get() for primary key
        if not company:
            return False, "Company not found"
        return True, company
    
    @staticmethod
    def get_company_by_industry(industry):
        """Get companies by industry"""
        companies = Company.query.filter_by(industry=industry).all()  # ← .all() for multiple
        if not companies:
            return False, "No companies found in this industry"
        return True, companies
    
    @staticmethod
    def approve_company(company_id):
        """Approve a company registration"""
        company = Company.query.get(company_id)  # ← Use .get()
        if not company:
            return False, "Company not found"
        
        company.approval_status = 'approved'
        db.session.commit()  # ← Added parentheses!
        return True, f"Company '{company.name}' approved successfully"
    
    @staticmethod
    def reject_company(company_id):
        """Reject a company registration"""
        company = Company.query.get(company_id)  # ← Fixed: use .get()
        if not company:
            return False, "Company not found"
        
        company.approval_status = 'rejected'
        db.session.commit()  # ← Added parentheses!
        return True, f"Company '{company.name}' rejected"
    
    @staticmethod
    def blacklist_company(company_id):
        """Blacklist a company"""
        company = Company.query.get(company_id)  # ← Fixed: use .get()
        if not company:
            return False, "Company not found"
        
        company.is_blacklisted = True
        company.user.is_active = False  # Also deactivate user account
        db.session.commit()  # ← Added parentheses!
        return True, f"Company '{company.name}' blacklisted"

    @staticmethod
    def get_dashboard_stats():
        """Get statistics for admin dashboard"""
        stats = {
            'total_students': Student.query.count(),
            'total_companies': Company.query.count(),
            'pending_companies': Company.query.filter_by(approval_status='pending').count(),
            'approved_companies': Company.query.filter_by(approval_status='approved').count(),
            'total_applications': Application.query.count(),
            'total_drives': PlacementDrive.query.count(),
            'pending_drives': PlacementDrive.query.filter_by(status='pending').count(),
        }
        return stats

##########################################################################
########################### Student ######################################
##########################################################################
    @staticmethod
    def get_all_students():
        """Get all students"""
        return Student.query.all()
    
    @staticmethod
    def get_student_by_name(name):
        """Get student by name"""
        student = Student.query.filter_by(name=name).first()  # ← Already correct
        if not student:
            return False, "Student not found"
        return True, student
    
    @staticmethod
    def get_student_by_id(student_id):
        """Get student by ID"""
        student = Student.query.get(student_id)  # ← Fixed: use .get()
        if not student:
            return False, "Student not found"
        return True, student
    
    @staticmethod
    def get_student_by_contact(contact):
        """Get student by phone number"""
        student = Student.query.filter_by(phone=contact).first()  # ← Fixed: added .first()
        if not student:
            return False, "Student not found"
        return True, student
    
    @staticmethod
    def get_student_by_roll(roll):
        """Get student by roll number"""
        student = Student.query.filter_by(roll_number=roll).first()  # ← Fixed: added .first()
        if not student:
            return False, "Student not found"
        return True, student
    
    @staticmethod
    def blacklist_student(student_id):
        """Blacklist a student"""
        student = Student.query.get(student_id)  # ← Fixed: use .get()
        if not student:
            return False, "Student not found"
        
        student.is_blacklisted = True
        student.user.is_active = False  # Also deactivate user account
        db.session.commit()  # ← Fixed: added parentheses!
        return True, f"Student '{student.name}' blacklisted"
    
    @staticmethod
    def unblacklist_student(student_id):
        """Remove student from blacklist"""
        student = Student.query.get(student_id)  # ← Fixed: use .get()
        if not student:
            return False, "Student not found"
        
        student.is_blacklisted = False
        student.user.is_active = True  # Reactivate user account
        db.session.commit()  # ← Fixed: added parentheses!
        return True, f"Student '{student.name}' removed from blacklist"


##########################################################################
########################### Placement Drives #############################
##########################################################################
    @staticmethod
    def get_all_drives(status=None):
        """Get all placement drives, optionally filtered by status"""
        if status:
            return PlacementDrive.query.filter_by(status=status).order_by(PlacementDrive.created_at.desc()).all()
        return PlacementDrive.query.order_by(PlacementDrive.created_at.desc()).all()
    
    @staticmethod
    def approve_drive(drive_id):
        """Approve a placement drive"""
        drive = PlacementDrive.query.get(drive_id)
        
        if not drive:
            return False, "Drive not found"
        
        if drive.status == 'approved':
            return False, "Drive is already approved"
        
        drive.status = 'approved'
        db.session.commit()
        return True, f"Drive '{drive.job_title}' by {drive.company.name} approved successfully"
    
    @staticmethod
    def reject_drive(drive_id):
        """Reject a placement drive"""
        drive = PlacementDrive.query.get(drive_id)
        
        if not drive:
            return False, "Drive not found"
        
        drive.status = 'rejected'
        db.session.commit()
        return True, f"Drive '{drive.job_title}' by {drive.company.name} rejected"
    
    @staticmethod
    def close_drive(drive_id):
        """Close a placement drive"""
        drive = PlacementDrive.query.get(drive_id)
        
        if not drive:
            return False, "Drive not found"
        
        drive.status = 'closed'
        db.session.commit()
        return True, f"Drive '{drive.job_title}' closed"
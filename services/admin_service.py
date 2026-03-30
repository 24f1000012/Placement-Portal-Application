from models import db, Company, Student
class AdminService:
    
    @staticmethod
    def get_all_companies(status=None):
        # Return all companies, or filter by approval_status
        if status:
            return Company.query.filter_by(approval_status=status).all()
        return Company.query.all()
    
    @staticmethod
    def approve_company(company_id):
        # Find company by ID
        # Change approval_status to 'approved'
        # Return (success: bool, message: str)
        company = Company.query.get(company_id)
        if not company:
            return False, "Company not found"
        company.approval_status = 'approved'
        
        db.session.commit()
        return True, f"Company '{company.name}' approved successfully"
    
    @staticmethod
    def reject_company(company_id):
        # Find company by ID
        # Change approval_status to 'rejected'
        # Return (success: bool, message: str)
        company=Company.query.filter_by(id=company_id)
        if not company:
            return False, "Company not found"
        company.approval_status="rejected"
        
        db.session.commit()
        return True, f"Company '{company.name}' rejected"
    
    @staticmethod
    def get_dashboard_stats():
        # Count total students, companies, pending companies, etc.
        # Return a dictionary with stats
        stats = {
            'total_students': Student.query.count(),
            'total_companies': Company.query.count(),
            'pending_companies': Company.query.filter_by(approval_status='pending').count(),
            'approved_companies': Company.query.filter_by(approval_status='approved').count(),
        }
        return stats
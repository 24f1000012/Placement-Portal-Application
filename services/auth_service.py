# services/auth_service.py
from models import db, User, Student, Company
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    
    @staticmethod
    def create_default_admin():
        """Create default admin user if doesn't exist"""
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin_user = User(
                email='admin@placement.com',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin created: admin@placement.com / admin123")
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate user credentials
        Returns: (success: bool, user: User or None, message: str)
        """
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists
        if not user:
            return False, None, "User not found. Please check your email."
        
        # Check if account is active
        if not user.is_active:
            return False, None, "Your account has been deactivated."
        
        # Verify password
        if not check_password_hash(user.password, password):
            return False, None, "Invalid password. Please try again."
        
        # Special check for company - must be approved
        if user.role == 'company':
            company = Company.query.filter_by(user_id=user.id).first()
            if company and company.approval_status != 'approved':
                return False, None, "Your company registration is pending admin approval."
        
        # All checks passed
        return True, user, "Login successful"
    
    @staticmethod
    def register_student(email, password, name):
        """
        Register a new student
        Returns: (success: bool, message: str)
        """
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return False, "Email already registered. Please login or use a different email."
        
        try:
            # Create new user
            user = User(
                email=email,
                password=generate_password_hash(password),
                role='student',
                is_active=True
            )
            db.session.add(user)
            db.session.flush()  # Get the user ID without committing
            
            # Create student profile
            student = Student(
                user_id=user.id,
                name=name
            )
            db.session.add(student)
            db.session.commit()
            
            return True, "Registration successful!"
        except Exception as e:
            db.session.rollback()
            return False, f"Registration failed: {str(e)}"
    
    @staticmethod
    def register_company(email, password, company_name):
        """
        Register a new company
        Returns: (success: bool, message: str)
        """
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return False, "Email already registered. Please login or use a different email."
        
        try:
            # Create new user
            user = User(
                email=email,
                password=generate_password_hash(password),
                role='company',
                is_active=True
            )
            db.session.add(user)
            db.session.flush()  # Get the user ID without committing
            
            # Create company profile
            company = Company(
                user_id=user.id,
                name=company_name,
                approval_status='pending'  # Company needs admin approval
            )
            db.session.add(company)
            db.session.commit()
            
            return True, "Registration successful! Your company registration is pending admin approval."
        except Exception as e:
            db.session.rollback()
            return False, f"Registration failed: {str(e)}"
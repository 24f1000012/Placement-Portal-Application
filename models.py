from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ─────────────────────────────────────────
# USER TABLE (Admin, Company, Student login)
# ─────────────────────────────────────────
class User(db.Model):
    __tablename__ = 'user'

    id           = db.Column(db.Integer, primary_key=True)
    email        = db.Column(db.String(150), unique=True, nullable=False)
    password     = db.Column(db.String(200), nullable=False)
    role         = db.Column(db.String(20), nullable=False)  # 'admin', 'company', 'student'
    is_active    = db.Column(db.Boolean, default=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student  = db.relationship('Student', backref='user', uselist=False)
    company  = db.relationship('Company', backref='user', uselist=False)


# ─────────────────────────────────────────
# STUDENT TABLE
# ─────────────────────────────────────────
class Student(db.Model):
    __tablename__ = 'student'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name         = db.Column(db.String(100), nullable=False)
    roll_number  = db.Column(db.String(50), unique=True)
    phone        = db.Column(db.String(15))
    department   = db.Column(db.String(100))
    cgpa         = db.Column(db.Float)
    skills       = db.Column(db.Text)
    resume       = db.Column(db.String(200))   # file path
    is_blacklisted = db.Column(db.Boolean, default=False)

    # Relationships
    applications = db.relationship('Application', backref='student', lazy=True)


# ─────────────────────────────────────────
# COMPANY TABLE
# ─────────────────────────────────────────
class Company(db.Model):
    __tablename__ = 'company'

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name            = db.Column(db.String(150), nullable=False)
    hr_contact      = db.Column(db.String(100))
    website         = db.Column(db.String(200))
    industry        = db.Column(db.String(100))
    description     = db.Column(db.Text)
    approval_status = db.Column(db.String(20), default='pending')  # pending/approved/rejected
    is_blacklisted  = db.Column(db.Boolean, default=False)

    # Relationships
    drives = db.relationship('PlacementDrive', backref='company', lazy=True)


# ─────────────────────────────────────────
# PLACEMENT DRIVE TABLE (Job Postings)
# ─────────────────────────────────────────
class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'

    id                  = db.Column(db.Integer, primary_key=True)
    company_id          = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    job_title           = db.Column(db.String(150), nullable=False)
    job_description     = db.Column(db.Text)
    eligibility         = db.Column(db.Text)       # e.g. min CGPA, branch
    salary              = db.Column(db.String(100))
    location            = db.Column(db.String(100))
    application_deadline = db.Column(db.DateTime)
    status              = db.Column(db.String(20), default='pending')  # pending/approved/closed

    created_at          = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='drive', lazy=True)


# ─────────────────────────────────────────
# APPLICATION TABLE
# ─────────────────────────────────────────
class Application(db.Model):
    __tablename__ = 'application'

    id               = db.Column(db.Integer, primary_key=True)
    student_id       = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id         = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    applied_date     = db.Column(db.DateTime, default=datetime.utcnow)
    status           = db.Column(db.String(20), default='applied')
    # applied / shortlisted / selected / rejected

    # Prevent duplicate applications (same student, same drive)
    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),
    )

class Placement(db.Model):
    _tablename_='placement'

    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)
    company_id=db.Column(db.Integer,db.ForeignKey('company.id'),nullable=False)
    drive_id=db.Column(db.Integer,db.ForeignKey('placement_drive.id'),nullable=False)
    application_id=db.Column(db.Integer,db.ForeignKey('application.id'),nullable=False)
    join_date=db.Column(db.DateTime,default=datetime.utcnow)
    salary=db.Column(db.String(100))
    position=db.Column(db.String(100))
    placemnet_date=db.Column(db.DateTime,default=datetime.utcnow)
    offer_letter=db.Column(db.String(200))   # file path

    # Relationships
    student=db.relationship('Student')

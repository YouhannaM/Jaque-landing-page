"""
Database Models for Manufacturing Operations Platform
Includes machines, quality standards, and training data models
"""

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association tables for many-to-many relationships
machine_capabilities = Table(
    'machine_capabilities',
    Base.metadata,
    Column('machine_id', Integer, ForeignKey('machines.id')),
    Column('capability_id', Integer, ForeignKey('capabilities.id'))
)

machine_materials = Table(
    'machine_materials',
    Base.metadata,
    Column('machine_id', Integer, ForeignKey('machines.id')),
    Column('material_id', Integer, ForeignKey('materials.id'))
)


class Machine(Base):
    """Machine/Equipment catalog"""
    __tablename__ = 'machines'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    manufacturer = Column(String(255))
    model = Column(String(255))
    category = Column(String(100), nullable=False)  # CNC_LATHE, CNC_MILL, CMM, etc.

    # Specifications
    price = Column(Float)
    max_part_size_x = Column(Float)  # mm
    max_part_size_y = Column(Float)  # mm
    max_part_size_z = Column(Float)  # mm
    spindle_speed_max = Column(Integer)  # RPM
    feed_rate_max = Column(Float)  # mm/min
    tolerance = Column(Float)  # mm (minimum achievable tolerance)
    repeatability = Column(Float)  # mm

    # Operational details
    cycle_time_factor = Column(Float, default=1.0)  # Efficiency multiplier
    maintenance_interval = Column(Integer)  # hours
    power_consumption = Column(Float)  # kW
    floor_space = Column(Float)  # square meters

    # Features
    features = Column(JSON)  # {"live_tooling": true, "sub_spindle": false, etc.}
    automation_level = Column(String(50))  # MANUAL, SEMI_AUTO, FULLY_AUTO
    control_system = Column(String(100))  # FANUC, HAAS, SIEMENS, etc.

    # Availability and status
    is_available = Column(Boolean, default=True)
    lead_time_weeks = Column(Integer)

    # Metadata
    description = Column(Text)
    datasheet_url = Column(String(500))
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    capabilities = relationship('Capability', secondary=machine_capabilities, back_populates='machines')
    compatible_materials = relationship('Material', secondary=machine_materials, back_populates='machines')
    quality_tools = relationship('QualityTool', back_populates='machine')


class Capability(Base):
    """Manufacturing capabilities"""
    __tablename__ = 'capabilities'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)  # TURNING, MILLING, DRILLING, etc.
    category = Column(String(100))  # MACHINING, INSPECTION, ASSEMBLY, etc.
    description = Column(Text)

    # Relationships
    machines = relationship('Machine', secondary=machine_capabilities, back_populates='capabilities')


class Material(Base):
    """Material specifications"""
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    material_type = Column(String(100))  # METAL, PLASTIC, COMPOSITE, etc.
    grade = Column(String(100))  # 6061-T6, 304, etc.

    # Properties
    hardness = Column(Float)
    tensile_strength = Column(Float)  # MPa
    density = Column(Float)  # g/cm³
    machinability_rating = Column(Float)  # 0-100

    # Cost
    cost_per_kg = Column(Float)

    description = Column(Text)

    # Relationships
    machines = relationship('Machine', secondary=machine_materials, back_populates='compatible_materials')


class QualityTool(Base):
    """Quality control and inspection equipment"""
    __tablename__ = 'quality_tools'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    manufacturer = Column(String(255))
    tool_type = Column(String(100))  # CMM, CALIPER, MICROMETER, PROFILOMETER, etc.

    # Specifications
    measurement_range_min = Column(Float)  # mm
    measurement_range_max = Column(Float)  # mm
    accuracy = Column(Float)  # mm
    resolution = Column(Float)  # mm

    price = Column(Float)
    calibration_interval_days = Column(Integer)

    # Features
    is_automated = Column(Boolean, default=False)
    has_spc_capability = Column(Boolean, default=False)
    software_included = Column(String(255))

    description = Column(Text)
    datasheet_url = Column(String(500))

    machine_id = Column(Integer, ForeignKey('machines.id'), nullable=True)
    machine = relationship('Machine', back_populates='quality_tools')

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QualityStandard(Base):
    """Quality standards and documents (for AI training)"""
    __tablename__ = 'quality_standards'

    id = Column(Integer, primary_key=True)
    standard_id = Column(String(100), unique=True)  # ISO-9001, AS9100, etc.
    title = Column(String(500), nullable=False)
    organization = Column(String(255))  # ISO, ASME, ASTM, etc.
    category = Column(String(100))  # QUALITY_MANAGEMENT, DIMENSIONAL, TESTING, etc.

    # Content
    full_text = Column(Text)  # Full document text for training
    summary = Column(Text)
    key_requirements = Column(JSON)  # Structured requirements

    # Classification
    industry = Column(JSON)  # ["aerospace", "automotive", "medical"]
    applicable_processes = Column(JSON)  # ["machining", "inspection", "assembly"]

    # Vector embeddings for AI
    embedding_vector = Column(JSON)  # Store embedding for similarity search

    # Metadata
    version = Column(String(50))
    publication_date = Column(DateTime)
    document_url = Column(String(500))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QualityPlanTemplate(Base):
    """Pre-configured quality plan templates"""
    __tablename__ = 'quality_plan_templates'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Applicability
    part_types = Column(JSON)  # ["rotational", "prismatic", "assembly"]
    industries = Column(JSON)  # ["aerospace", "automotive", "medical"]
    complexity_level = Column(String(50))  # LOW, MEDIUM, HIGH, CRITICAL

    # Template structure
    inspection_points = Column(JSON)
    control_methods = Column(JSON)
    acceptance_criteria = Column(JSON)
    documentation_requirements = Column(JSON)

    # Related standards
    related_standards = Column(JSON)  # List of standard IDs

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CADAnalysis(Base):
    """CAD file analysis results"""
    __tablename__ = 'cad_analyses'

    id = Column(Integer, primary_key=True)
    analysis_id = Column(String(100), unique=True, nullable=False)

    # Input data
    part_name = Column(String(255))
    material = Column(String(100))
    annual_volume = Column(Integer)

    # Extracted features from CAD
    dimensions = Column(JSON)  # {"length": 150, "width": 50, "height": 30}
    features = Column(JSON)  # ["holes", "threads", "pockets", "surfaces"]
    tolerances = Column(JSON)  # Extracted tolerance information
    surface_finishes = Column(JSON)

    # AI-generated insights
    complexity_score = Column(Float)
    recommended_machines = Column(JSON)  # List of machine IDs
    recommended_processes = Column(JSON)
    estimated_cycle_time = Column(Float)  # minutes
    quality_plan_id = Column(Integer, ForeignKey('quality_plan_templates.id'))

    # Status
    status = Column(String(50))  # PROCESSING, COMPLETED, FAILED

    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)


class TrainingDocument(Base):
    """Documents used for AI model training"""
    __tablename__ = 'training_documents'

    id = Column(Integer, primary_key=True)
    document_type = Column(String(100))  # STANDARD, PROCEDURE, GUIDELINE, CASE_STUDY
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)

    # Metadata for training
    source = Column(String(255))
    language = Column(String(10), default='en')
    word_count = Column(Integer)

    # Annotations
    entities = Column(JSON)  # Named entities extracted
    key_phrases = Column(JSON)
    categories = Column(JSON)

    # Training status
    is_preprocessed = Column(Boolean, default=False)
    is_validated = Column(Boolean, default=False)
    quality_score = Column(Float)  # 0-1, quality of the document

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ModelTrainingJob(Base):
    """Track AI model training jobs"""
    __tablename__ = 'model_training_jobs'

    id = Column(Integer, primary_key=True)
    job_id = Column(String(100), unique=True, nullable=False)
    model_type = Column(String(100))  # QUALITY_PLAN, MACHINE_RECOMMENDATION, etc.

    # Training configuration
    training_config = Column(JSON)
    dataset_size = Column(Integer)

    # Status
    status = Column(String(50))  # QUEUED, TRAINING, COMPLETED, FAILED
    progress = Column(Float, default=0.0)  # 0-100

    # Results
    model_path = Column(String(500))
    metrics = Column(JSON)  # Accuracy, loss, etc.

    # Timing
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    duration_seconds = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

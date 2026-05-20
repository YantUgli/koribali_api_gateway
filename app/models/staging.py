import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, Enum, ForeignKey, Date, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.staging_database import Base

class ProjectType(str, enum.Enum):
    lighting_pole = "lighting_pole"
    acemast = "acemast"
    sign_board = "sign_board"
    multiple = "multiple"

class StagingStatus(str, enum.Enum):
    pending = "pending"
    save = "save"
    discard = "discard"

class DesignStandard(str, enum.Enum):
    jil = "jil"
    haiden = "haiden"
    v60 = "v60"

class MaterialType(str, enum.Enum):
    stk_400 = "stk_400"
    stk_490 = "stk_490"
    stk_500 = "stk_500"


class StagingProject(Base):
    __tablename__ = 'staging_project'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=True)
    report_number = Column(String, nullable=True)
    project_type = Column(Enum(ProjectType), nullable=True, default=ProjectType.lighting_pole)
    status = Column(Enum(StagingStatus), default=StagingStatus.pending)
    
    # Tempat menyimpan output hasil dari Calculation Service
    calculation_result = Column(JSON, nullable=True) 
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships (Cascade delete sangat penting di sini)
    condition = relationship("StagingCondition", back_populates="project", uselist=False, cascade="all, delete-orphan")
    poles = relationship("StagingStepPole", back_populates="project", cascade="all, delete-orphan")
    high_evals = relationship("StagingHighEval", back_populates="project", cascade="all, delete-orphan")
    direct_objects = relationship("StagingDirectObject", back_populates="project", cascade="all, delete-orphan")

class StagingCondition(Base):
    __tablename__ = 'staging_condition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    staging_project_id = Column(String, ForeignKey('staging_project.id', ondelete="CASCADE"))
    design_standard = Column(Enum(DesignStandard), nullable=True)
    wind_speed = Column(Float, nullable=True)
    air_density = Column(Float, nullable=True)
    
    project = relationship("StagingProject", back_populates="condition")

class StagingStepPole(Base):
    __tablename__ = 'staging_step_pole'
    id = Column(Integer, primary_key=True, autoincrement=True)
    staging_project_id = Column(String, ForeignKey('staging_project.id', ondelete="CASCADE"))
    name = Column(String, nullable=False)
    diameter = Column(Float, nullable=False)
    thickness = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    material = Column(Enum(MaterialType), nullable=False)
    quantity = Column(Integer, nullable=True)
    
    project = relationship("StagingProject", back_populates="poles")

class StagingHighEval(Base):
    __tablename__ = 'staging_high_evals'
    id = Column(Integer, primary_key=True, autoincrement=True)
    staging_project_id = Column(String, ForeignKey('staging_project.id', ondelete="CASCADE"))
    name = Column(String, nullable=False)
    point_evaluate = Column(Float, nullable=False)
    
    project = relationship("StagingProject", back_populates="high_evals")

class StagingDirectObject(Base):
    __tablename__ = 'staging_direct_objects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    staging_project_id = Column(String, ForeignKey('staging_project.id', ondelete="CASCADE"))
    name = Column(String, nullable=False)
    front_area = Column(Float, nullable=False)
    side_area = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    coefficient = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=True)
    
    project = relationship("StagingProject", back_populates="direct_objects")
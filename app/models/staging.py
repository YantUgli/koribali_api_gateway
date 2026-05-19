import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, JSON
from app.core.staging_database import Base

class StagingData(Base):
    __tablename__ = 'staging_data'
    
    # Primary Key sekaligus Session ID (UUID)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())) 
    
    # Project Metadata
    project_title = Column(String)
    project_date = Column(String)
    report_number = Column(String)
    request_number = Column(String)
    
    # Conditions
    design_standard = Column(String)
    design_wind_speed = Column(Float)
    design_air_density = Column(Float)
    
    # Payloads
    calculation_input_payload = Column(JSON) # Menyimpan poles, directObjects, dll
    calculation_result_payload = Column(JSON) # Menyimpan response kalkulasi
    
    # Lifecycle Metadata
    status = Column(String, default="pending") # pending, saved, expired
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
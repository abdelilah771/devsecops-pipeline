from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class VulnerabilityModel(Base):
    __tablename__ = "vulnerabilities"

    vuln_id = Column(String, primary_key=True, index=True)
    owasp_category = Column(String)
    severity = Column(String)
    description = Column(String)
    suggested_fix_key = Column(String, nullable=True)
    
    # Storing complex objects as JSON for simplicity in this microservice
    location = Column(JSON) 
    evidence = Column(JSON)

    # Optional: link to a Run ID if we want to query by run
    run_id = Column(String, index=True, nullable=True)

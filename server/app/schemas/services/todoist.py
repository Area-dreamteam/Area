from pydantic import BaseModel, Field

class Task(BaseModel):
    task_id: str = Field(alias='id')
    project_id: str 
    content: str
    description: str
    labels: list[str]
    checked: bool
    is_deleted: bool
    
    class Config:
        validate_by_name = True

class Project(BaseModel):
    project_id: str = Field(alias='id') 
    name: str
    is_deleted: bool
    
    class Config:
        validate_by_name = True

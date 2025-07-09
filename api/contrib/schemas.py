from pydantic import BaseModel, Field

class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True
        
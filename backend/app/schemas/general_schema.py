from pydantic import BaseModel


class CreateResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

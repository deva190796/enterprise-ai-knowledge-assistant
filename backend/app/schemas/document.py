from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    original_filename: str
    filename: str
    filepath: str

    class Config:
        from_attributes = True
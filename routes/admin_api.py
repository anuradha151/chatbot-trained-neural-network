from fastapi import APIRouter
from training import train

admin =  APIRouter()

@admin.post("/admin/tag/create") 
async def create_tag():
    return {"message": "Tag created successfully"}


@admin.get("/admin/model/train")
def train_model():
    return train()

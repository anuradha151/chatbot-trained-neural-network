from fastapi import FastAPI

from routes.admin_api import admin
from routes.chatbot_api import chatbot

app = FastAPI()
app.include_router(admin)
app.include_router(chatbot)


#Done - Create a folder called routes 
#Done - Add chatbot-api.py and admin-api.py in routes folder
#Done - Need to figure how to add separate api files in FastAPI
#Done - Configure route files in main app
#TODO: Test routes
#TODO: Start working on db integration
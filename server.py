'''
Ce fichier ce charge de gérer les intéractions client-server
'''
import user_manager
from fastapi import FastAPI, Form, HTTPException

app = FastAPI()

@app.post("/create_user/")
async def create_user_endpoint(login: str = Form(...), password: str = Form(...)):
    try:
        new_user = user_manager.new_user(login, password)
        return {"message": "User created successfully", "user": new_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


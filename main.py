from fastapi import FastAPI
from premium import router as premium_router
import api_profiles

app = FastAPI()

# mount routes
app.include_router(premium_router)

@app.get("/")
def root():
    return {"message": "Sparko backend running"}

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

roles = ["founder", "investor", "partner"]
fake_profiles = [
    {
        "id": i,
        "name": f"User {i}",
        "role": random.choice(roles),
        "title": random.choice(["AI Engineer", "UX Designer", "Investor", "Startup CEO"]),
        "skills": random.sample(["AI", "Fintech", "Blockchain", "UX", "Marketing", "Cloud"], 3),
        "expectation": random.choice(["Find co-founder", "Find investor", "Find technical partner"]),
        "bio": f"This is a short bio for User {i}. Passionate about startups and new ventures."
    }
    for i in range(1, 21)
]

@app.get("/api/profiles")
def get_profiles(role: str = Query(None)):
    if role:
        return [p for p in fake_profiles if p["role"] == role]
    return fake_profiles

#!/usr/bin/env python3
"""
Simple script to create fake user data for Sparko platform testing
"""

import requests
import json

# API base URL
API_BASE = "http://localhost:5000/api"

# Fake user data
fake_users = [
    {
        "name": "Sarah Chen",
        "email": "sarah.chen@example.com",
        "password": "password123",
        "role": "entrepreneur"
    },
    {
        "name": "David Kim", 
        "email": "david.kim@example.com",
        "password": "password123",
        "role": "investor"
    },
    {
        "name": "Emily Rodriguez",
        "email": "emily.rodriguez@example.com", 
        "password": "password123",
        "role": "entrepreneur"
    },
    {
        "name": "Michael Zhang",
        "email": "michael.zhang@example.com",
        "password": "password123", 
        "role": "investor"
    },
    {
        "name": "Lisa Johnson",
        "email": "lisa.johnson@example.com",
        "password": "password123",
        "role": "partner"
    },
    {
        "name": "Alex Thompson",
        "email": "alex.thompson@example.com",
        "password": "password123",
        "role": "entrepreneur"
    },
    {
        "name": "Jennifer Lee",
        "email": "jennifer.lee@example.com", 
        "password": "password123",
        "role": "investor"
    },
    {
        "name": "Ryan Patel",
        "email": "ryan.patel@example.com",
        "password": "password123",
        "role": "partner"
    }
]

def create_users():
    print("Creating fake users via API...")
    
    for user_data in fake_users:
        try:
            # Register user
            response = requests.post(f"{API_BASE}/auth/register", json=user_data)
            
            if response.status_code == 201:
                print(f"✅ Created user: {user_data['name']} ({user_data['email']})")
            else:
                print(f"❌ Failed to create user {user_data['name']}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error creating user {user_data['name']}: {str(e)}")
    
    print(f"\nCompleted creating {len(fake_users)} fake users!")

if __name__ == "__main__":
    create_users()


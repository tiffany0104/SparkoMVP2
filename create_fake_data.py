#!/usr/bin/env python3
"""
Script to create fake user data for Sparko platform testing
"""

import sys
import os
sys.path.append('/home/ubuntu/sparko_project/sparko-backend/src')

from models.user import db, User, UserProfile
from main import app
import json

# Fake user data
fake_users = [
    {
        "email": "sarah.chen@example.com",
        "password": "password123",
        "name": "Sarah Chen",
        "current_role": "entrepreneur",
        "profiles": {
            "entrepreneur": {
                "age": 28,
                "title": "AI Startup Founder",
                "company": "NeuralFlow",
                "location": "San Francisco, CA",
                "tagline": "Building the future of conversational AI",
                "looking_for": "Series A investors",
                "bio": "Passionate AI entrepreneur with 5+ years in machine learning. Previously led AI initiatives at Google and Microsoft.",
                "needs": "Looking for $2M Series A funding to scale our conversational AI platform",
                "skills": ["Machine Learning", "Product Strategy", "Team Leadership"],
                "photo_url": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400"
            }
        }
    },
    {
        "email": "david.kim@example.com", 
        "password": "password123",
        "name": "David Kim",
        "current_role": "investor",
        "profiles": {
            "investor": {
                "age": 45,
                "title": "Managing Partner",
                "company": "TechVentures Capital",
                "location": "Palo Alto, CA",
                "tagline": "Investing in the next generation of tech startups",
                "looking_for": "Early-stage AI and SaaS startups",
                "bio": "15+ years in venture capital with focus on enterprise software and AI. Led investments in 50+ startups.",
                "needs": "Seeking innovative AI startups for Series A/B investments",
                "skills": ["Venture Capital", "Due Diligence", "Strategic Planning"],
                "photo_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400"
            }
        }
    },
    {
        "email": "emily.rodriguez@example.com",
        "password": "password123", 
        "name": "Emily Rodriguez",
        "current_role": "entrepreneur",
        "profiles": {
            "entrepreneur": {
                "age": 32,
                "title": "Co-Founder & CTO",
                "company": "GreenTech Solutions",
                "location": "Austin, TX",
                "tagline": "Revolutionizing sustainable energy through IoT",
                "looking_for": "Technical co-founder and seed investors",
                "bio": "Former Tesla engineer building next-gen smart grid solutions. MIT graduate with 8 years in cleantech.",
                "needs": "Seeking $500K seed funding and a technical co-founder with IoT expertise",
                "skills": ["IoT Development", "Clean Energy", "Hardware Engineering"],
                "photo_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400"
            }
        }
    },
    {
        "email": "michael.zhang@example.com",
        "password": "password123",
        "name": "Michael Zhang", 
        "current_role": "investor",
        "profiles": {
            "investor": {
                "age": 38,
                "title": "Angel Investor",
                "company": "Zhang Capital",
                "location": "New York, NY",
                "tagline": "Supporting fintech and healthcare innovations",
                "looking_for": "Seed to Series A fintech startups",
                "bio": "Former Goldman Sachs VP turned angel investor. Invested in 30+ startups with 5 successful exits.",
                "needs": "Looking for disruptive fintech and healthtech startups",
                "skills": ["Financial Analysis", "Market Strategy", "Regulatory Compliance"],
                "photo_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"
            }
        }
    },
    {
        "email": "lisa.johnson@example.com",
        "password": "password123",
        "name": "Lisa Johnson",
        "current_role": "partner", 
        "profiles": {
            "partner": {
                "age": 29,
                "title": "Full-Stack Developer",
                "company": "Freelance",
                "location": "Seattle, WA", 
                "tagline": "Building scalable web applications with modern tech",
                "looking_for": "Co-founder opportunity in SaaS or e-commerce",
                "bio": "Senior developer with expertise in React, Node.js, and cloud architecture. Looking to join as technical co-founder.",
                "needs": "Seeking equity-based co-founder role in early-stage startup",
                "skills": ["React", "Node.js", "AWS", "System Architecture"],
                "photo_url": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=400"
            }
        }
    },
    {
        "email": "alex.thompson@example.com",
        "password": "password123",
        "name": "Alex Thompson",
        "current_role": "entrepreneur",
        "profiles": {
            "entrepreneur": {
                "age": 26,
                "title": "Founder & CEO",
                "company": "HealthTrack",
                "location": "Boston, MA",
                "tagline": "Democratizing healthcare through mobile technology",
                "looking_for": "Healthcare investors and regulatory advisors",
                "bio": "Harvard Medical School dropout building patient-centric healthcare solutions. Previously at Apple Health.",
                "needs": "Seeking $1M seed funding and healthcare industry mentorship",
                "skills": ["Healthcare Technology", "Mobile Development", "Regulatory Affairs"],
                "photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400"
            }
        }
    },
    {
        "email": "jennifer.lee@example.com",
        "password": "password123",
        "name": "Jennifer Lee",
        "current_role": "investor",
        "profiles": {
            "investor": {
                "age": 42,
                "title": "Principal",
                "company": "Healthcare Ventures",
                "location": "San Diego, CA",
                "tagline": "Investing in digital health and biotech innovations",
                "looking_for": "Healthcare and biotech startups",
                "bio": "Former Pfizer executive with deep healthcare industry knowledge. Focus on digital therapeutics and medical devices.",
                "needs": "Seeking innovative healthcare startups for Series A investments",
                "skills": ["Healthcare Industry", "Biotech", "Regulatory Strategy"],
                "photo_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400"
            }
        }
    },
    {
        "email": "ryan.patel@example.com",
        "password": "password123",
        "name": "Ryan Patel",
        "current_role": "partner",
        "profiles": {
            "partner": {
                "age": 31,
                "title": "Product Designer",
                "company": "Design Studio",
                "location": "Los Angeles, CA",
                "tagline": "Creating beautiful and intuitive user experiences",
                "looking_for": "Co-founder role in consumer tech startup",
                "bio": "Award-winning product designer with experience at Airbnb and Uber. Passionate about consumer-facing products.",
                "needs": "Looking for technical co-founder to build consumer mobile app",
                "skills": ["UI/UX Design", "Product Strategy", "User Research"],
                "photo_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400"
            }
        }
    }
]

def create_fake_users():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        print("Creating fake users...")
        
        for user_data in fake_users:
            # Create user
            user = User(email=user_data["email"])
            user.set_password(user_data["password"])
            user.name = user_data["name"]
            user.current_role = user_data["current_role"]
            
            db.session.add(user)
            db.session.flush()  # Get user ID
            
            # Create user profiles
            for role, profile_data in user_data["profiles"].items():
                profile = UserProfile(
                    user_id=user.id,
                    role=role,
                    age=profile_data.get("age"),
                    title=profile_data.get("title"),
                    company=profile_data.get("company"),
                    location=profile_data.get("location"),
                    tagline=profile_data.get("tagline"),
                    looking_for=profile_data.get("looking_for"),
                    bio=profile_data.get("bio"),
                    needs=profile_data.get("needs"),
                    photo_url=profile_data.get("photo_url"),
                    is_complete=True
                )
                
                # Set skills
                if profile_data.get("skills"):
                    profile.set_skills(profile_data["skills"])
                
                db.session.add(profile)
            
            print(f"Created user: {user.name} ({user.email})")
        
        db.session.commit()
        print(f"Successfully created {len(fake_users)} fake users!")

if __name__ == "__main__":
    create_fake_users()


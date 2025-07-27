
import os
import sys
from faker import Faker
import random
from datetime import datetime

# Add the parent directory to the sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'sparko-backend')))

from src.main import app
from src.models.user import db, User, UserProfile

faker = Faker()

def generate_fake_data(num_users=100):
    with app.app_context():
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        print("Database cleared and re-created.")

        roles = ['entrepreneur', 'investor', 'partner']
        users_per_role = num_users // len(roles)
        
        all_users = []

        print("Generating fake users...")
        for i in range(num_users):
            email = faker.email()
            password = 'password123'
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
        db.session.commit()

        all_users = User.query.all()

        print("Generating fake profiles...")
        for i, user in enumerate(all_users):
            role = roles[i % len(roles)]
            
            profile = UserProfile(user_id=user.id, role=role)
            profile.full_name = faker.name()
            profile.age = random.randint(20, 60)
            profile.location = faker.city() + ', ' + faker.state_abbr()
            profile.tagline = faker.sentence(nb_words=8)
            profile.bio = faker.paragraph(nb_sentences=3)
            profile.profile_photo_url = faker.image_url()

            if role == 'entrepreneur':
                profile.professional_title = 'Founder & CEO'
                profile.company_organization = faker.company()
                profile.looking_for = 'Seed funding, Angel investors, Co-founders'
                profile.set_skills(random.sample(['AI', 'Machine Learning', 'SaaS', 'FinTech', 'Biotech', 'Marketing', 'Sales', 'Product Management'], k=random.randint(2, 5)))
                profile.what_you_need = faker.paragraph(nb_sentences=2)
            elif role == 'investor':
                profile.professional_title = 'Angel Investor'
                profile.company_organization = faker.company() + ' Ventures'
                profile.looking_for = 'High-growth startups, Innovative ideas, Strong teams'
                profile.set_skills(random.sample(['Venture Capital', 'Due Diligence', 'Market Analysis', 'Negotiation', 'Portfolio Management'], k=random.randint(2, 5)))
                profile.what_you_need = faker.paragraph(nb_sentences=2)
            elif role == 'partner':
                profile.professional_title = 'Business Development Manager'
                profile.company_organization = faker.company() + ' Solutions'
                profile.looking_for = 'Strategic alliances, Joint ventures, Distribution channels'
                profile.set_skills(random.sample(["Partnerships", "Negotiation", "Contract Management", "Relationship Building", "Market Expansion"], k=random.randint(2, 5)))
                profile.what_you_need = faker.paragraph(nb_sentences=2)
            
            db.session.add(profile)
            profile.calculate_completion()
            
        db.session.commit()
        print("Fake data generation complete.")

if __name__ == '__main__':
    generate_fake_data(num_users=100)



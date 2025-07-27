from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User, UserProfile

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profiles', methods=['GET'])
@jwt_required()
def get_user_profiles():
    """Get all profiles for the current user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        profiles = {}
        for role in ['entrepreneur', 'investor', 'partner']:
            profile = UserProfile.query.filter_by(user_id=user_id, role=role).first()
            if profile:
                profile.calculate_completion()
                db.session.commit()
                profiles[role] = profile.to_dict()
            else:
                profiles[role] = {
                    'role': role,
                    'is_complete': False,
                    'completion_percentage': 0
                }
        
        return jsonify({
            'user': user.to_dict(include_private=True),
            'profiles': profiles
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/profiles/<role>', methods=['GET'])
@jwt_required()
def get_profile_by_role(role):
    """Get profile for a specific role"""
    try:
        if role not in ['entrepreneur', 'investor', 'partner']:
            return jsonify({'error': 'Invalid role'}), 400
        
        user_id = get_jwt_identity()
        profile = UserProfile.query.filter_by(user_id=user_id, role=role).first()
        
        if not profile:
            # Create empty profile
            profile = UserProfile(user_id=user_id, role=role)
            db.session.add(profile)
            db.session.commit()
        
        profile.calculate_completion()
        db.session.commit()
        
        return jsonify({'profile': profile.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/profiles/<role>', methods=['PUT'])
@jwt_required()
def update_profile_by_role(role):
    """Update profile for a specific role"""
    try:
        if role not in ['entrepreneur', 'investor', 'partner']:
            return jsonify({'error': 'Invalid role'}), 400
        
        user_id = get_jwt_identity()
        data = request.get_json()
        
        profile = UserProfile.query.filter_by(user_id=user_id, role=role).first()
        if not profile:
            profile = UserProfile(user_id=user_id, role=role)
            db.session.add(profile)
        
        # Update common fields
        if 'title' in data:
            profile.title = data['title']
        if 'company' in data:
            profile.company = data['company']
        if 'tagline' in data:
            profile.tagline = data['tagline']
        if 'bio' in data:
            profile.bio = data['bio']
        if 'skills' in data:
            profile.set_skills(data['skills'])
        
        # Update role-specific fields
        if role == 'entrepreneur':
            entrepreneur_fields = [
                'project_description', 'funding_stage', 'funding_amount',
                'industry', 'team_size', 'looking_for_investor_type'
            ]
            for field in entrepreneur_fields:
                if field in data:
                    setattr(profile, field, data[field])
                    
        elif role == 'investor':
            if 'investment_preferences' in data:
                profile.set_investment_preferences(data['investment_preferences'])
            
            investor_fields = [
                'investment_range', 'past_investments', 'professional_background',
                'geographic_preference', 'value_add_services'
            ]
            for field in investor_fields:
                if field in data:
                    setattr(profile, field, data[field])
                    
        elif role == 'partner':
            if 'expertise' in data:
                profile.set_expertise(data['expertise'])
            
            partner_fields = [
                'availability', 'collaboration_type', 'desired_role',
                'equity_expectation', 'location_preference'
            ]
            for field in partner_fields:
                if field in data:
                    setattr(profile, field, data[field])
        
        # Calculate completion
        profile.calculate_completion()
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': profile.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/switch-role', methods=['POST'])
@jwt_required()
def switch_role():
    """Switch user's current role"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_role = data.get('role')
        
        if new_role not in ['entrepreneur', 'investor', 'partner']:
            return jsonify({'error': 'Invalid role'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.current_role = new_role
        db.session.commit()
        
        # Get profile for the new role
        profile = UserProfile.query.filter_by(user_id=user_id, role=new_role).first()
        if not profile:
            profile = UserProfile(user_id=user_id, role=new_role)
            db.session.add(profile)
            db.session.commit()
        
        profile.calculate_completion()
        db.session.commit()
        
        return jsonify({
            'message': 'Role switched successfully',
            'current_role': new_role,
            'profile': profile.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/check-completion/<role>', methods=['GET'])
@jwt_required()
def check_profile_completion(role):
    """Check if profile is complete for a specific role"""
    try:
        if role not in ['entrepreneur', 'investor', 'partner']:
            return jsonify({'error': 'Invalid role'}), 400
        
        user_id = get_jwt_identity()
        profile = UserProfile.query.filter_by(user_id=user_id, role=role).first()
        
        if not profile:
            return jsonify({
                'is_complete': False,
                'completion_percentage': 0,
                'message': 'Complete your profile to start swiping'
            }), 200
        
        profile.calculate_completion()
        db.session.commit()
        
        message = 'Profile complete' if profile.is_complete else 'Complete your profile to start swiping'
        
        return jsonify({
            'is_complete': profile.is_complete,
            'completion_percentage': profile.completion_percentage,
            'message': message
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


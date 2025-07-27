from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User, UserProfile, Swipe, Match
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
import random

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/discover', methods=['GET'])
@jwt_required()
def discover_profiles():
    """Discover profiles based on current user role"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        current_role = user.current_role
        
        # Check if current role profile is complete
        current_profile = UserProfile.query.filter_by(user_id=user_id, role=current_role).first()
        if not current_profile or not current_profile.is_complete:
            return jsonify({
                'profiles': [],
                'message': 'Complete your profile to start swiping',
                'profile_incomplete': True
            }), 200
        
        # Determine target role based on current role
        if current_role == 'entrepreneur':
            target_role = 'investor'
        elif current_role == 'investor':
            target_role = 'entrepreneur'
        elif current_role == 'partner':
            target_role = 'partner'
        else:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Get users who have been swiped by current user in current role
        swiped_user_ids = db.session.query(Swipe.swiped_id).filter(
            and_(
                Swipe.swiper_id == user_id,
                Swipe.swiper_role == current_role,
                Swipe.swiped_role == target_role
            )
        ).subquery()
        
        # Find users with complete profiles in target role, excluding already swiped
        target_profiles = db.session.query(UserProfile, User).join(
            User, UserProfile.user_id == User.id
        ).filter(
            and_(
                UserProfile.role == target_role,
                UserProfile.is_complete == True,
                UserProfile.user_id != user_id,
                ~UserProfile.user_id.in_(swiped_user_ids)
            )
        ).limit(10).all()
        
        profiles = []
        for profile, profile_user in target_profiles:
            profile_data = profile.to_dict()
            profile_data.update({
                'name': profile_user.name,
                'age': profile_user.age,
                'location': profile_user.location,
                'photo_url': profile_user.photo_url or f"https://images.unsplash.com/photo-{random.choice(['1494790108755-2616b612b786', '1472099645785-5658abf4ff4e', '1438761681033-6461ffad8d80', '1507003211169-0a1dd7228f2d', '1489424731084-a5d8b219a5bb', '1560250097-0b93528c311a'])}?w=400&h=400&fit=crop&crop=face"
            })
            profiles.append(profile_data)
        
        return jsonify({
            'profiles': profiles,
            'current_role': current_role,
            'target_role': target_role,
            'message': f'Swipe right to connect with {target_role}s' if profiles else 'No more profiles'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matching_bp.route('/swipe', methods=['POST'])
@jwt_required()
def swipe_profile():
    """Swipe on a profile"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        swiped_user_id = data.get('user_id')
        action = data.get('action')  # like, skip, super_spark
        
        if not swiped_user_id or not action:
            return jsonify({'error': 'Missing required fields'}), 400
        
        if action not in ['like', 'skip', 'super_spark']:
            return jsonify({'error': 'Invalid action'}), 400
        
        user = User.query.get(user_id)
        swiped_user = User.query.get(swiped_user_id)
        
        if not user or not swiped_user:
            return jsonify({'error': 'User not found'}), 404
        
        current_role = user.current_role
        
        # Determine target role
        if current_role == 'entrepreneur':
            target_role = 'investor'
        elif current_role == 'investor':
            target_role = 'entrepreneur'
        elif current_role == 'partner':
            target_role = 'partner'
        else:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Check if already swiped
        existing_swipe = Swipe.query.filter_by(
            swiper_id=user_id,
            swiped_id=swiped_user_id,
            swiper_role=current_role,
            swiped_role=target_role
        ).first()
        
        if existing_swipe:
            return jsonify({'error': 'Already swiped on this profile'}), 400
        
        # Handle super spark
        if action == 'super_spark':
            if user.super_spark_count <= 0:
                return jsonify({'error': 'No super sparks remaining'}), 400
            user.super_spark_count -= 1
        
        # Create swipe record
        swipe = Swipe(
            swiper_id=user_id,
            swiped_id=swiped_user_id,
            swiper_role=current_role,
            swiped_role=target_role,
            action=action
        )
        db.session.add(swipe)
        
        # Check for match if action is like or super_spark
        match_created = False
        if action in ['like', 'super_spark']:
            # Check if the other user has liked back
            reverse_swipe = Swipe.query.filter_by(
                swiper_id=swiped_user_id,
                swiped_id=user_id,
                swiper_role=target_role,
                swiped_role=current_role,
                action='like'
            ).first() or Swipe.query.filter_by(
                swiper_id=swiped_user_id,
                swiped_id=user_id,
                swiper_role=target_role,
                swiped_role=current_role,
                action='super_spark'
            ).first()
            
            if reverse_swipe:
                # Create match
                match = Match(
                    user1_id=min(user_id, swiped_user_id),
                    user2_id=max(user_id, swiped_user_id),
                    user1_role=current_role if user_id < swiped_user_id else target_role,
                    user2_role=target_role if user_id < swiped_user_id else current_role
                )
                db.session.add(match)
                match_created = True
        
        db.session.commit()
        
        response_data = {
            'message': 'Swipe recorded successfully',
            'match': match_created,
            'super_spark_count': user.super_spark_count
        }
        
        if match_created:
            response_data['message'] = "It's a match! 🎉"
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matching_bp.route('/matches', methods=['GET'])
@jwt_required()
def get_matches():
    """Get matches for current user and role"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        current_role = user.current_role
        
        # Get matches where user is involved in current role
        matches = Match.query.filter(
            or_(
                and_(Match.user1_id == user_id, Match.user1_role == current_role),
                and_(Match.user2_id == user_id, Match.user2_role == current_role)
            )
        ).all()
        
        match_list = []
        for match in matches:
            # Determine the other user
            if match.user1_id == user_id:
                other_user_id = match.user2_id
                other_role = match.user2_role
            else:
                other_user_id = match.user1_id
                other_role = match.user1_role
            
            other_user = User.query.get(other_user_id)
            other_profile = UserProfile.query.filter_by(
                user_id=other_user_id,
                role=other_role
            ).first()
            
            if other_user and other_profile:
                match_data = {
                    'match_id': match.id,
                    'user': {
                        'id': other_user.id,
                        'name': other_user.name,
                        'photo_url': other_user.photo_url,
                        'role': other_role
                    },
                    'profile': other_profile.to_dict(),
                    'created_at': match.created_at.isoformat(),
                    'chat_unlocked': match.chat_unlocked
                }
                match_list.append(match_data)
        
        return jsonify({
            'matches': match_list,
            'current_role': current_role
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matching_bp.route('/super-spark/reset', methods=['POST'])
@jwt_required()
def reset_super_sparks():
    """Reset super sparks if a week has passed"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        
        if user.super_spark_reset_date < week_ago:
            user.super_spark_count = 3
            user.super_spark_reset_date = now
            db.session.commit()
            
            return jsonify({
                'message': 'Super sparks reset successfully',
                'super_spark_count': user.super_spark_count
            }), 200
        else:
            return jsonify({
                'message': 'Super sparks not ready for reset',
                'super_spark_count': user.super_spark_count,
                'next_reset': (user.super_spark_reset_date + timedelta(days=7)).isoformat()
            }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


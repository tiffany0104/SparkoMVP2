from flask import Blueprint, request, jsonify
from src.models.user import db, User, Match, Message
from src.routes.auth import token_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/matches/<int:match_id>/messages', methods=['GET'])
@token_required
def get_messages(current_user, match_id):
    try:
        # Verify user is part of this match
        match = Match.query.filter(
            Match.id == match_id,
            (Match.user1_id == current_user.id) | (Match.user2_id == current_user.id)
        ).first()
        
        if not match:
            return jsonify({'message': 'Match not found or access denied'}), 404
        
        # Get messages
        messages = Message.query.filter_by(match_id=match_id).order_by(Message.created_at.asc()).all()
        
        message_data = []
        for msg in messages:
            message_data.append({
                'id': msg.id,
                'content': msg.content,
                'sender_id': msg.sender_id,
                'is_from_me': msg.sender_id == current_user.id,
                'created_at': msg.created_at.isoformat()
            })
        
        # Get other user info
        other_user_id = match.user2_id if match.user1_id == current_user.id else match.user1_id
        other_user = User.query.get(other_user_id)
        
        return jsonify({
            'messages': message_data,
            'match': {
                'id': match.id,
                'other_user': other_user.to_dict(),
                'created_at': match.created_at.isoformat(),
                'chat_unlocked': match.chat_unlocked
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get messages: {str(e)}'}), 500

@chat_bp.route('/matches/<int:match_id>/messages', methods=['POST'])
@token_required
def send_message(current_user, match_id):
    try:
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({'message': 'Message content is required'}), 400
        
        # Verify user is part of this match
        match = Match.query.filter(
            Match.id == match_id,
            (Match.user1_id == current_user.id) | (Match.user2_id == current_user.id)
        ).first()
        
        if not match:
            return jsonify({'message': 'Match not found or access denied'}), 404
        
        if not match.chat_unlocked:
            return jsonify({'message': 'Chat is not unlocked for this match'}), 403
        
        # Create message
        message = Message(
            match_id=match_id,
            sender_id=current_user.id,
            content=content
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'message': 'Message sent successfully',
            'data': {
                'id': message.id,
                'content': message.content,
                'sender_id': message.sender_id,
                'is_from_me': True,
                'created_at': message.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to send message: {str(e)}'}), 500

@chat_bp.route('/matches/<int:match_id>/unlock', methods=['POST'])
@token_required
def unlock_chat(current_user, match_id):
    """Unlock chat for premium users or after certain conditions"""
    try:
        # Verify user is part of this match
        match = Match.query.filter(
            Match.id == match_id,
            (Match.user1_id == current_user.id) | (Match.user2_id == current_user.id)
        ).first()
        
        if not match:
            return jsonify({'message': 'Match not found or access denied'}), 404
        
        # For now, unlock immediately (in production, add premium checks)
        match.chat_unlocked = True
        db.session.commit()
        
        return jsonify({
            'message': 'Chat unlocked successfully',
            'chat_unlocked': True
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to unlock chat: {str(e)}'}), 500


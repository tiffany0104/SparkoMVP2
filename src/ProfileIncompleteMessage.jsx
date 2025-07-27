import React from 'react';
import './ProfileIncompleteMessage.css';

const ProfileIncompleteMessage = ({ role, completionPercentage, onCompleteProfile }) => {
  const getRoleInfo = (role) => {
    const roleMap = {
      entrepreneur: { icon: '🚀', label: 'Entrepreneur', color: '#FF6B35' },
      investor: { icon: '💰', label: 'Investor', color: '#4CAF50' },
      partner: { icon: '🤝', label: 'Partner', color: '#2196F3' }
    };
    return roleMap[role] || roleMap.entrepreneur;
  };

  const roleInfo = getRoleInfo(role);

  return (
    <div className="profile-incomplete-container">
      <div className="profile-incomplete-card">
        <div className="profile-incomplete-icon" style={{ color: roleInfo.color }}>
          {roleInfo.icon}
        </div>
        
        <h3 className="profile-incomplete-title">
          Complete Your {roleInfo.label} Profile
        </h3>
        
        <p className="profile-incomplete-description">
          You need to complete your profile to start swiping and connecting with others.
        </p>
        
        <div className="completion-progress">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ 
                width: `${completionPercentage}%`,
                backgroundColor: roleInfo.color 
              }}
            />
          </div>
          <span className="progress-text">{completionPercentage}% Complete</span>
        </div>
        
        <button 
          className="complete-profile-button"
          onClick={onCompleteProfile}
          style={{ backgroundColor: roleInfo.color }}
        >
          Complete Profile
        </button>
        
        <div className="profile-incomplete-footer">
          <p>It only takes 2 minutes to set up your profile!</p>
        </div>
      </div>
    </div>
  );
};

export default ProfileIncompleteMessage;


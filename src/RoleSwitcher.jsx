import React, { useState } from 'react';
import './RoleSwitcher.css';

const RoleSwitcher = ({ currentRole, onRoleChange, className = '' }) => {
  const [isOpen, setIsOpen] = useState(false);

  const roles = [
    {
      id: 'entrepreneur',
      label: 'Entrepreneur',
      icon: '🚀',
      color: '#FF6B35',
      description: 'Find investors'
    },
    {
      id: 'investor',
      label: 'Investor',
      icon: '💰',
      color: '#4CAF50',
      description: 'Find startups'
    },
    {
      id: 'partner',
      label: 'Partner',
      icon: '🤝',
      color: '#2196F3',
      description: 'Find co-founders'
    }
  ];

  const currentRoleData = roles.find(role => role.id === currentRole) || roles[0];

  const handleRoleSelect = (roleId) => {
    if (roleId !== currentRole) {
      onRoleChange(roleId);
    }
    setIsOpen(false);
  };

  return (
    <div className={`role-switcher ${className}`}>
      <button
        className="role-switcher-button"
        onClick={() => setIsOpen(!isOpen)}
        style={{ backgroundColor: currentRoleData.color }}
      >
        <span className="role-icon">{currentRoleData.icon}</span>
        <span className="role-label">{currentRoleData.label}</span>
        <span className={`dropdown-arrow ${isOpen ? 'open' : ''}`}>▼</span>
      </button>

      {isOpen && (
        <div className="role-dropdown">
          {roles.map((role) => (
            <button
              key={role.id}
              className={`role-option ${role.id === currentRole ? 'active' : ''}`}
              onClick={() => handleRoleSelect(role.id)}
              style={{ 
                backgroundColor: role.id === currentRole ? role.color : 'transparent',
                color: role.id === currentRole ? 'white' : role.color
              }}
            >
              <span className="role-icon">{role.icon}</span>
              <div className="role-info">
                <span className="role-label">{role.label}</span>
                <span className="role-description">{role.description}</span>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default RoleSwitcher;


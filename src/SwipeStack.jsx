import React, { useState, useEffect } from 'react';
import SwipeCard from './SwipeCard';
import RoleSwitcher from './RoleSwitcher';
import ProfileIncompleteMessage from './ProfileIncompleteMessage';
import apiService from '../services/api';

const SwipeStack = ({ onSwipe, onMatch }) => {
  const [profiles, setProfiles] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [superSparkCount, setSuperSparkCount] = useState(3);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentRole, setCurrentRole] = useState('entrepreneur');
  const [profileIncomplete, setProfileIncomplete] = useState(false);
  const [completionPercentage, setCompletionPercentage] = useState(0);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Get current user role from localStorage
    const user = apiService.getCurrentUser();
    if (user && user.current_role) {
      setCurrentRole(user.current_role);
    }
    
    loadProfiles();
  }, [currentRole]);

  const loadProfiles = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiService.discoverProfiles();
      
      if (response.profile_incomplete) {
        setProfileIncomplete(true);
        setCompletionPercentage(0);
        setMessage(response.message);
        setProfiles([]);
      } else {
        setProfileIncomplete(false);
        setProfiles(response.profiles || []);
        setMessage(response.message || '');
      }
      
      setCurrentIndex(0);
    } catch (err) {
      console.error('Failed to load profiles:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRoleChange = async (newRole) => {
    try {
      setLoading(true);
      await apiService.switchRole(newRole);
      setCurrentRole(newRole);
      
      // Reload profiles for new role
      await loadProfiles();
    } catch (err) {
      console.error('Failed to switch role:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSwipe = async (action) => {
    if (profiles.length === 0) return;

    const swipedProfile = profiles[0];
    
    try {
      const response = await apiService.swipe(swipedProfile.user_id || swipedProfile.id, action);
      
      if (response.super_spark_count !== undefined) {
        setSuperSparkCount(response.super_spark_count);
      }

      // Call parent callback
      onSwipe && onSwipe(swipedProfile, action, response);
      
      // Handle match
      if (response.match) {
        onMatch && onMatch(swipedProfile, response.match_id);
      }

      // Remove the swiped card and show next one
      setTimeout(() => {
        setCurrentIndex(prev => prev + 1);
        setProfiles(prev => prev.slice(1));
        
        // Load more profiles if running low
        if (profiles.length <= 3) {
          loadProfiles();
        }
      }, 300);
      
    } catch (err) {
      console.error('Swipe failed:', err);
      // Still remove the card on error to prevent getting stuck
      setTimeout(() => {
        setCurrentIndex(prev => prev + 1);
        setProfiles(prev => prev.slice(1));
      }, 300);
    }
  };

  const handleCompleteProfile = () => {
    // Navigate to profile completion (you can implement this based on your routing)
    alert('Profile completion feature coming soon!');
  };

  if (loading && profiles.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-[600px] w-80">
        <div className="mb-4 flex justify-between items-center w-full px-4">
          <RoleSwitcher 
            currentRole={currentRole}
            onRoleChange={handleRoleChange}
          />
          <div className="flex items-center gap-1 bg-yellow-100 px-3 py-1 rounded-full">
            <span className="text-yellow-600">⚡</span>
            <span className="text-yellow-800 font-semibold">{superSparkCount}</span>
          </div>
        </div>
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading profiles...</p>
        </div>
      </div>
    );
  }

  if (error && profiles.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-[600px] w-80">
        <div className="mb-4 flex justify-between items-center w-full px-4">
          <RoleSwitcher 
            currentRole={currentRole}
            onRoleChange={handleRoleChange}
          />
          <div className="flex items-center gap-1 bg-yellow-100 px-3 py-1 rounded-full">
            <span className="text-yellow-600">⚡</span>
            <span className="text-yellow-800 font-semibold">{superSparkCount}</span>
          </div>
        </div>
        <div className="text-center">
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            Unable to load profiles
          </h3>
          <p className="text-gray-500 mb-4">{error}</p>
          <button
            onClick={loadProfiles}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (profileIncomplete) {
    return (
      <div className="flex flex-col items-center justify-center h-[600px] w-80">
        <div className="mb-4 flex justify-between items-center w-full px-4">
          <RoleSwitcher 
            currentRole={currentRole}
            onRoleChange={handleRoleChange}
          />
          <div className="flex items-center gap-1 bg-yellow-100 px-3 py-1 rounded-full">
            <span className="text-yellow-600">⚡</span>
            <span className="text-yellow-800 font-semibold">{superSparkCount}</span>
          </div>
        </div>
        <ProfileIncompleteMessage
          role={currentRole}
          completionPercentage={completionPercentage}
          onCompleteProfile={handleCompleteProfile}
        />
      </div>
    );
  }

  if (profiles.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-[600px] w-80">
        <div className="mb-4 flex justify-between items-center w-full px-4">
          <RoleSwitcher 
            currentRole={currentRole}
            onRoleChange={handleRoleChange}
          />
          <div className="flex items-center gap-1 bg-yellow-100 px-3 py-1 rounded-full">
            <span className="text-yellow-600">⚡</span>
            <span className="text-yellow-800 font-semibold">{superSparkCount}</span>
          </div>
        </div>
        <div className="text-center">
          <div className="text-6xl mb-4">🎯</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            No More Profiles
          </h3>
          <p className="text-gray-500 mb-4">
            {message || 'Check back later for new connections!'}
          </p>
          <button
            onClick={loadProfiles}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Refresh
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center w-80">
      <div className="mb-4 flex justify-between items-center w-full px-4">
        <RoleSwitcher 
          currentRole={currentRole}
          onRoleChange={handleRoleChange}
        />
        <div className="flex items-center gap-1 bg-yellow-100 px-3 py-1 rounded-full">
          <span className="text-yellow-600">⚡</span>
          <span className="text-yellow-800 font-semibold">{superSparkCount}</span>
        </div>
      </div>
      
      <div className="relative w-80 h-[500px]">
        {profiles.slice(0, 3).map((profile, index) => (
          <SwipeCard
            key={`${profile.user_id || profile.id}-${currentIndex + index}`}
            profile={profile}
            onSwipe={handleSwipe}
            isTopCard={index === 0}
          />
        ))}
      </div>
      
      <div className="mt-4 text-center">
        <p className="text-sm text-gray-500">
          Swipe left to skip • Swipe right to like • Swipe up for Super Spark
        </p>
      </div>
    </div>
  );
};

export default SwipeStack;


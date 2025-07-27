import { useState, useRef } from 'react'
import { motion, useMotionValue, useTransform, useAnimation } from 'framer-motion'
import { Heart, X, Zap, MapPin, Briefcase, Target } from 'lucide-react'
import { Button } from '@/components/ui/button'

const SwipeCard = ({ profile, onSwipe, isTopCard = false }) => {
  const [exitX, setExitX] = useState(0)
  const x = useMotionValue(0)
  const controls = useAnimation()
  const cardRef = useRef(null)

  // Transform values for rotation and opacity based on drag
  const rotate = useTransform(x, [-200, 200], [-30, 30])
  const opacity = useTransform(x, [-200, -150, 0, 150, 200], [0, 1, 1, 1, 0])

  const handleDragEnd = (event, info) => {
    const threshold = 100
    
    if (info.offset.x > threshold) {
      // Swipe right - Like
      setExitX(200)
      controls.start({ x: 200, opacity: 0 })
      onSwipe('like')
    } else if (info.offset.x < -threshold) {
      // Swipe left - Skip
      setExitX(-200)
      controls.start({ x: -200, opacity: 0 })
      onSwipe('skip')
    } else {
      // Snap back to center
      controls.start({ x: 0, rotate: 0 })
    }
  }

  const handleButtonAction = (action) => {
    if (action === 'like') {
      setExitX(200)
      controls.start({ x: 200, opacity: 0 })
    } else if (action === 'skip') {
      setExitX(-200)
      controls.start({ x: -200, opacity: 0 })
    } else if (action === 'super_spark') {
      setExitX(200)
      controls.start({ x: 200, opacity: 0, scale: 1.1 })
    }
    onSwipe(action)
  }

  // Use default photo if none provided
  const photoUrl = profile.photo_url || `https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face`

  return (
    <motion.div
      ref={cardRef}
      className={`absolute w-80 h-[500px] bg-white rounded-2xl shadow-xl cursor-grab active:cursor-grabbing ${
        isTopCard ? 'z-20' : 'z-10'
      }`}
      style={{
        x,
        rotate,
        opacity: isTopCard ? opacity : 0.8,
        scale: isTopCard ? 1 : 0.95,
      }}
      animate={controls}
      drag={isTopCard ? 'x' : false}
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={handleDragEnd}
      whileDrag={{ scale: 1.05 }}
    >
      {/* Profile Image */}
      <div className="relative h-64 rounded-t-2xl overflow-hidden">
        <img
          src={photoUrl}
          alt={profile.name}
          className="w-full h-full object-cover"
          onError={(e) => {
            e.target.src = `https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face`
          }}
        />
        {profile.isSuperSpark && (
          <div className="absolute inset-0 bg-gradient-to-r from-yellow-400/20 to-orange-400/20 animate-pulse">
            <div className="absolute top-4 right-4 text-yellow-400">
              <Zap className="w-8 h-8 animate-bounce" fill="currentColor" />
            </div>
          </div>
        )}
        
        {/* Swipe indicators */}
        <motion.div
          className="absolute top-8 left-8 px-4 py-2 bg-green-500 text-white font-bold rounded-lg transform -rotate-12"
          style={{ opacity: useTransform(x, [50, 150], [0, 1]) }}
        >
          LIKE
        </motion.div>
        <motion.div
          className="absolute top-8 right-8 px-4 py-2 bg-red-500 text-white font-bold rounded-lg transform rotate-12"
          style={{ opacity: useTransform(x, [-150, -50], [1, 0]) }}
        >
          NOPE
        </motion.div>
      </div>

      {/* Profile Info */}
      <div className="p-6 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">{profile.name}</h3>
          {profile.age && <span className="text-sm text-gray-500">{profile.age}</span>}
        </div>
        
        {profile.title && (
          <div className="flex items-center text-gray-600">
            <Briefcase className="w-4 h-4 mr-2" />
            <span className="text-sm">{profile.title}</span>
          </div>
        )}
        
        {profile.company && (
          <div className="text-sm text-gray-600">
            at <span className="font-medium">{profile.company}</span>
          </div>
        )}
        
        {profile.location && (
          <div className="flex items-center text-gray-600">
            <MapPin className="w-4 h-4 mr-2" />
            <span className="text-sm">{profile.location}</span>
          </div>
        )}
        
        {profile.tagline && (
          <p className="text-sm text-purple-600 font-medium">{profile.tagline}</p>
        )}
        
        {profile.looking_for && (
          <div className="flex items-center text-gray-600">
            <Target className="w-4 h-4 mr-2" />
            <span className="text-sm">{profile.looking_for}</span>
          </div>
        )}
        
        {/* Skills tags */}
        {profile.skills && profile.skills.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {profile.skills.slice(0, 3).map((skill, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
              >
                {skill}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Action Buttons - Only show on top card */}
      {isTopCard && (
        <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-4">
          <Button
            variant="outline"
            size="icon"
            className="w-12 h-12 rounded-full border-2 border-red-500 text-red-500 hover:bg-red-500 hover:text-white"
            onClick={() => handleButtonAction('skip')}
          >
            <X className="w-6 h-6" />
          </Button>
          
          <Button
            variant="outline"
            size="icon"
            className="w-14 h-14 rounded-full border-2 border-yellow-500 text-yellow-500 hover:bg-yellow-500 hover:text-white relative"
            onClick={() => handleButtonAction('super_spark')}
          >
            <Zap className="w-7 h-7" fill="currentColor" />
          </Button>
          
          <Button
            variant="outline"
            size="icon"
            className="w-12 h-12 rounded-full border-2 border-green-500 text-green-500 hover:bg-green-500 hover:text-white"
            onClick={() => handleButtonAction('like')}
          >
            <Heart className="w-6 h-6" />
          </Button>
        </div>
      )}
    </motion.div>
  )
}

export default SwipeCard


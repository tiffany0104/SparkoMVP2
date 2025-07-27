import { useState } from 'react'
import { User, MessageCircle, Settings, Zap, LogOut } from 'lucide-react'
import { Button } from '@/components/ui/button'
import sparkoLogo from '../assets/sparko-logo.png'

const Header = ({ superSparkCount, user, onLogout }) => {
  const [showUserMenu, setShowUserMenu] = useState(false)

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center space-x-3">
          <img src={sparkoLogo} alt="Sparko" className="h-10 w-auto" />
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex items-center space-x-8">
          <Button variant="ghost" className="text-gray-600 hover:text-gray-900">
            Discover
          </Button>
          <Button variant="ghost" className="text-gray-600 hover:text-gray-900">
            Matches
          </Button>
          <Button variant="ghost" className="text-gray-600 hover:text-gray-900">
            Messages
          </Button>
        </nav>

        {/* Right side actions */}
        <div className="flex items-center space-x-4">
          {/* Super Spark Counter */}
          <div className="flex items-center space-x-2 bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-3 py-2 rounded-full">
            <Zap className="w-4 h-4" fill="currentColor" />
            <span className="text-sm font-medium">{superSparkCount || 0}</span>
          </div>

          {/* Action buttons */}
          <Button
            variant="ghost"
            size="icon"
            className="text-gray-600 hover:text-gray-900"
          >
            <MessageCircle className="w-5 h-5" />
          </Button>

          <Button
            variant="ghost"
            size="icon"
            className="text-gray-600 hover:text-gray-900"
          >
            <Settings className="w-5 h-5" />
          </Button>

          {/* User Menu */}
          <div className="relative">
            <Button
              variant="ghost"
              size="icon"
              className="text-gray-600 hover:text-gray-900"
              onClick={() => setShowUserMenu(!showUserMenu)}
            >
              <User className="w-5 h-5" />
            </Button>

            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 border">
                <div className="px-4 py-2 text-sm text-gray-700 border-b">
                  <div className="font-medium">{user?.name || 'User'}</div>
                  <div className="text-gray-500 capitalize">{user?.role || 'Member'}</div>
                </div>
                
                <button
                  onClick={() => {
                    setShowUserMenu(false)
                    // Add profile edit functionality here
                  }}
                  className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  <User className="w-4 h-4 inline mr-2" />
                  Edit Profile
                </button>
                
                <button
                  onClick={() => {
                    setShowUserMenu(false)
                    onLogout()
                  }}
                  className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                >
                  <LogOut className="w-4 h-4 inline mr-2" />
                  Sign Out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header


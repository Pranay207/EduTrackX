import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useEffect } from 'react'
import {
  Home,
  BookOpen,
  FileText,
  Calendar,
  Clock,
  Brain,
  User,
  LogOut,
  Moon,
  Sun,
  Menu,
  X
} from 'lucide-react'
import { useState } from 'react'

const Layout = ({ darkMode, toggleDarkMode }) => {
  const { user, logout, loading } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  useEffect(() => {
    if (!loading && !user) {
      navigate('/login')
    }
  }, [user, loading, navigate])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/subjects', icon: BookOpen, label: 'Subjects & Marks' },
    { path: '/assignments', icon: FileText, label: 'Assignments' },
    { path: '/attendance', icon: Calendar, label: 'Attendance' },
    { path: '/study-planner', icon: Clock, label: 'Study Planner' },
    { path: '/ai-assistant', icon: Brain, label: 'AI Assistant' },
    { path: '/profile', icon: User, label: 'Profile' },
  ]

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      <aside className={`${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0 fixed md:static inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 shadow-lg transition-transform duration-300 ease-in-out`}>
        <div className="flex flex-col h-full">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-primary-600 dark:text-primary-400">EduTrackX</h1>
              <button onClick={() => setSidebarOpen(false)} className="md:hidden">
                <X className="h-6 w-6" />
              </button>
            </div>
            <div className="mt-4">
              <p className="text-sm text-gray-600 dark:text-gray-400">Welcome back,</p>
              <p className="font-semibold text-gray-900 dark:text-gray-100">{user?.name}</p>
              <div className="mt-2 flex items-center space-x-2">
                <div className="bg-primary-100 dark:bg-primary-900 px-2 py-1 rounded text-xs font-medium text-primary-700 dark:text-primary-300">
                  Level {user?.level || 1}
                </div>
                <div className="bg-yellow-100 dark:bg-yellow-900 px-2 py-1 rounded text-xs font-medium text-yellow-700 dark:text-yellow-300">
                  {user?.xp || 0} XP
                </div>
              </div>
            </div>
          </div>

          <nav className="flex-1 p-4 overflow-y-auto">
            <ul className="space-y-2">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <li key={item.path}>
                    <Link
                      to={item.path}
                      onClick={() => setSidebarOpen(false)}
                      className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-primary-600 text-white'
                          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                      <span className="font-medium">{item.label}</span>
                    </Link>
                  </li>
                )
              })}
            </ul>
          </nav>

          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <button
              onClick={toggleDarkMode}
              className="w-full flex items-center justify-center space-x-2 px-4 py-3 mb-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
              <span className="font-medium">{darkMode ? 'Light Mode' : 'Dark Mode'}</span>
            </button>
            <button
              onClick={handleLogout}
              className="w-full flex items-center justify-center space-x-2 px-4 py-3 rounded-lg bg-red-600 hover:bg-red-700 text-white transition-colors"
            >
              <LogOut className="h-5 w-5" />
              <span className="font-medium">Logout</span>
            </button>
          </div>
        </div>
      </aside>

      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white dark:bg-gray-800 shadow-sm md:hidden">
          <div className="p-4 flex items-center justify-between">
            <button onClick={() => setSidebarOpen(true)}>
              <Menu className="h-6 w-6" />
            </button>
            <h1 className="text-xl font-bold text-primary-600 dark:text-primary-400">EduTrackX</h1>
            <div className="w-6"></div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>

      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}
    </div>
  )
}

export default Layout

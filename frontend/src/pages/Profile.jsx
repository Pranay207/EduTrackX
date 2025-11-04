import { useAuth } from '../context/AuthContext'
import { User, Mail, Award, Zap, Trophy } from 'lucide-react'
import api from '../utils/api'

const Profile = () => {
  const { user } = useAuth()

  const handleExportReport = async () => {
    try {
      const response = await api.get('/export/report-card', { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'report_card.pdf')
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      console.error('Error exporting report:', error)
      alert('Failed to export report card')
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Profile</h1>
      
      <div className="card max-w-2xl">
        <div className="flex items-center space-x-4 mb-6">
          <div className="w-20 h-20 bg-primary-600 rounded-full flex items-center justify-center text-white text-3xl font-bold">
            {user?.name?.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{user?.name}</h2>
            <p className="text-gray-600 dark:text-gray-400">{user?.email}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-primary-50 dark:bg-primary-900/20 p-4 rounded-lg text-center">
            <Award className="h-8 w-8 text-primary-600 dark:text-primary-400 mx-auto mb-2" />
            <p className="text-sm text-gray-600 dark:text-gray-400">Level</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">{user?.level || 1}</p>
          </div>
          <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg text-center">
            <Zap className="h-8 w-8 text-yellow-600 dark:text-yellow-400 mx-auto mb-2" />
            <p className="text-sm text-gray-600 dark:text-gray-400">XP Points</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">{user?.xp || 0}</p>
          </div>
          <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg text-center">
            <Trophy className="h-8 w-8 text-purple-600 dark:text-purple-400 mx-auto mb-2" />
            <p className="text-sm text-gray-600 dark:text-gray-400">Streak</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">{user?.streak || 0} days</p>
          </div>
        </div>

        <button onClick={handleExportReport} className="btn-primary w-full">
          Export Report Card (PDF)
        </button>
      </div>
    </div>
  )
}

export default Profile

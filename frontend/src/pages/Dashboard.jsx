import { useState, useEffect } from 'react'
import api from '../utils/api'
import { Bar, Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import {
  BookOpen,
  FileText,
  Calendar,
  Clock,
  TrendingUp,
  Award,
  Zap,
  Target
} from 'lucide-react'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
)

const Dashboard = () => {
  const [stats, setStats] = useState(null)
  const [performanceData, setPerformanceData] = useState(null)
  const [attendanceData, setAttendanceData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [statsRes, perfRes, attRes] = await Promise.all([
        api.get('/dashboard/stats'),
        api.get('/dashboard/charts/performance'),
        api.get('/dashboard/charts/attendance')
      ])

      setStats(statsRes.data)
      setPerformanceData(perfRes.data)
      setAttendanceData(attRes.data)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  const statCards = [
    { icon: BookOpen, label: 'Total Subjects', value: stats?.total_subjects || 0, color: 'bg-blue-500' },
    { icon: TrendingUp, label: 'Average %', value: `${stats?.average_percentage?.toFixed(1) || 0}%`, color: 'bg-green-500' },
    { icon: Award, label: 'CGPA', value: stats?.cgpa?.toFixed(2) || '0.00', color: 'bg-purple-500' },
    { icon: FileText, label: 'Pending Tasks', value: stats?.pending_assignments || 0, color: 'bg-orange-500' },
    { icon: Calendar, label: 'Attendance', value: `${stats?.attendance_percentage?.toFixed(1) || 0}%`, color: 'bg-cyan-500' },
    { icon: Clock, label: 'Study Time', value: `${stats?.total_study_time || 0}m`, color: 'bg-indigo-500' },
    { icon: Zap, label: 'XP Points', value: stats?.xp || 0, color: 'bg-yellow-500' },
    { icon: Target, label: 'Streak', value: `${stats?.streak || 0} days`, color: 'bg-red-500' }
  ]

  const performanceChartData = {
    labels: performanceData?.map(d => d.subject) || [],
    datasets: [{
      label: 'Average Performance (%)',
      data: performanceData?.map(d => d.average) || [],
      backgroundColor: 'rgba(59, 130, 246, 0.8)',
      borderColor: 'rgba(59, 130, 246, 1)',
      borderWidth: 1
    }]
  }

  const attendanceChartData = {
    labels: attendanceData?.map(d => d.subject) || [],
    datasets: [{
      label: 'Attendance (%)',
      data: attendanceData?.map(d => d.percentage) || [],
      backgroundColor: 'rgba(16, 185, 129, 0.8)',
      borderColor: 'rgba(16, 185, 129, 1)',
      borderWidth: 2,
      fill: false,
      tension: 0.4
    }]
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <button onClick={fetchDashboardData} className="btn-secondary">
          Refresh
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, index) => {
          const Icon = card.icon
          return (
            <div key={index} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{card.label}</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{card.value}</p>
                </div>
                <div className={`${card.color} p-3 rounded-lg`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Subject Performance</h2>
          {performanceData && performanceData.length > 0 ? (
            <Bar data={performanceChartData} options={{ responsive: true, maintainAspectRatio: true }} />
          ) : (
            <p className="text-gray-500 dark:text-gray-400 text-center py-8">No performance data available</p>
          )}
        </div>

        <div className="card">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Attendance Overview</h2>
          {attendanceData && attendanceData.length > 0 ? (
            <Line data={attendanceChartData} options={{ responsive: true, maintainAspectRatio: true }} />
          ) : (
            <p className="text-gray-500 dark:text-gray-400 text-center py-8">No attendance data available</p>
          )}
        </div>
      </div>

      {stats?.upcoming_deadlines && stats.upcoming_deadlines.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Upcoming Deadlines</h2>
          <div className="space-y-3">
            {stats.upcoming_deadlines.map((deadline, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">{deadline.assignment}</p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{deadline.subject}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {new Date(deadline.deadline).toLocaleDateString()}
                  </p>
                  <span className={`inline-block px-2 py-1 text-xs rounded ${
                    deadline.priority === 'high' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                    deadline.priority === 'medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                    'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                  }`}>
                    {deadline.priority}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard

import { useState, useEffect } from 'react'
import api from '../utils/api'
import { Play, Pause, RotateCcw } from 'lucide-react'

const StudyPlanner = () => {
  const [subjects, setSubjects] = useState([])
  const [selectedSubject, setSelectedSubject] = useState('')
  const [duration, setDuration] = useState(25)
  const [timeLeft, setTimeLeft] = useState(25 * 60)
  const [isRunning, setIsRunning] = useState(false)

  useEffect(() => {
    fetchSubjects()
  }, [])

  useEffect(() => {
    let interval
    if (isRunning && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft(t => t - 1)
      }, 1000)
    } else if (timeLeft === 0) {
      handleComplete()
    }
    return () => clearInterval(interval)
  }, [isRunning, timeLeft])

  const fetchSubjects = async () => {
    try {
      const response = await api.get('/subjects')
      setSubjects(response.data)
    } catch (error) {
      console.error('Error fetching subjects:', error)
    }
  }

  const handleComplete = async () => {
    setIsRunning(false)
    if (selectedSubject) {
      try {
        await api.post('/study/sessions', { subject_id: selectedSubject, duration, date: new Date().toISOString() })
        alert('Study session completed! +XP earned!')
      } catch (error) {
        console.error('Error saving session:', error)
      }
    }
    reset()
  }

  const reset = () => {
    setTimeLeft(duration * 60)
    setIsRunning(false)
  }

  const minutes = Math.floor(timeLeft / 60)
  const seconds = timeLeft % 60

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Study Planner - Pomodoro Timer</h1>
      <div className="card max-w-2xl mx-auto text-center">
        <div className="text-8xl font-bold text-primary-600 dark:text-primary-400 mb-8">
          {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
        </div>
        <select className="input-field mb-4" value={selectedSubject} onChange={(e) => setSelectedSubject(e.target.value)} disabled={isRunning}>
          <option value="">Select Subject</option>
          {subjects.map(s => <option key={s._id} value={s._id}>{s.name}</option>)}
        </select>
        <div className="flex items-center justify-center space-x-4 mb-6">
          <button onClick={() => !isRunning && setDuration(25)} className={`px-4 py-2 rounded ${duration === 25 ? 'bg-primary-600 text-white' : 'bg-gray-200 dark:bg-gray-700'}`}>25 min</button>
          <button onClick={() => !isRunning && setDuration(50)} className={`px-4 py-2 rounded ${duration === 50 ? 'bg-primary-600 text-white' : 'bg-gray-200 dark:bg-gray-700'}`}>50 min</button>
        </div>
        <div className="flex items-center justify-center space-x-4">
          <button onClick={() => setIsRunning(!isRunning)} className="btn-primary flex items-center space-x-2 px-8 py-4">
            {isRunning ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6" />}
            <span className="text-lg">{isRunning ? 'Pause' : 'Start'}</span>
          </button>
          <button onClick={reset} className="btn-secondary flex items-center space-x-2 px-8 py-4">
            <RotateCcw className="h-6 w-6" />
            <span className="text-lg">Reset</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default StudyPlanner

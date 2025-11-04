import { useState, useEffect } from 'react'
import api from '../utils/api'

const Attendance = () => {
  const [subjects, setSubjects] = useState([])
  const [selectedSubject, setSelectedSubject] = useState('')
  const [date, setDate] = useState(new Date().toISOString().split('T')[0])
  const [status, setStatus] = useState('present')

  useEffect(() => {
    fetchSubjects()
  }, [])

  const fetchSubjects = async () => {
    try {
      const response = await api.get('/subjects')
      setSubjects(response.data)
    } catch (error) {
      console.error('Error fetching subjects:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/attendance', { subject_id: selectedSubject, date, status })
      alert('Attendance marked successfully!')
      setDate(new Date().toISOString().split('T')[0])
    } catch (error) {
      console.error('Error marking attendance:', error)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Attendance</h1>
      <div className="card max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-4">
          <select className="input-field" value={selectedSubject} onChange={(e) => setSelectedSubject(e.target.value)} required>
            <option value="">Select Subject</option>
            {subjects.map(s => <option key={s._id} value={s._id}>{s.name}</option>)}
          </select>
          <input type="date" className="input-field" value={date} onChange={(e) => setDate(e.target.value)} required />
          <div className="flex space-x-4">
            <label className="flex items-center space-x-2">
              <input type="radio" value="present" checked={status === 'present'} onChange={(e) => setStatus(e.target.value)} />
              <span>Present</span>
            </label>
            <label className="flex items-center space-x-2">
              <input type="radio" value="absent" checked={status === 'absent'} onChange={(e) => setStatus(e.target.value)} />
              <span>Absent</span>
            </label>
          </div>
          <button type="submit" className="btn-primary">Mark Attendance</button>
        </form>
      </div>
    </div>
  )
}

export default Attendance

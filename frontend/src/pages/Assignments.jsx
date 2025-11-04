import { useState, useEffect } from 'react'
import api from '../utils/api'
import { Plus, CheckCircle, Clock } from 'lucide-react'

const Assignments = () => {
  const [assignments, setAssignments] = useState([])
  const [subjects, setSubjects] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ subject_id: '', title: '', description: '', deadline: '', priority: 'medium' })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [assignRes, subjRes] = await Promise.all([api.get('/assignments'), api.get('/subjects')])
      setAssignments(assignRes.data)
      setSubjects(subjRes.data)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/assignments', formData)
      setFormData({ subject_id: '', title: '', description: '', deadline: '', priority: 'medium' })
      setShowForm(false)
      fetchData()
    } catch (error) {
      console.error('Error creating assignment:', error)
    }
  }

  const toggleStatus = async (id, currentStatus) => {
    try {
      await api.put(`/assignments/${id}`, { status: currentStatus === 'completed' ? 'pending' : 'completed' })
      fetchData()
    } catch (error) {
      console.error('Error updating assignment:', error)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Assignments</h1>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary flex items-center space-x-2">
          <Plus className="h-5 w-5" />
          <span>Add Assignment</span>
        </button>
      </div>

      {showForm && (
        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-4">
            <select className="input-field" value={formData.subject_id} onChange={(e) => setFormData({ ...formData, subject_id: e.target.value })} required>
              <option value="">Select Subject</option>
              {subjects.map(s => <option key={s._id} value={s._id}>{s.name}</option>)}
            </select>
            <input type="text" placeholder="Assignment Title" className="input-field" value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })} required />
            <textarea placeholder="Description" className="input-field" value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} rows="3" />
            <input type="datetime-local" className="input-field" value={formData.deadline} onChange={(e) => setFormData({ ...formData, deadline: e.target.value })} required />
            <select className="input-field" value={formData.priority} onChange={(e) => setFormData({ ...formData, priority: e.target.value })}>
              <option value="low">Low Priority</option>
              <option value="medium">Medium Priority</option>
              <option value="high">High Priority</option>
            </select>
            <div className="flex space-x-3">
              <button type="submit" className="btn-primary">Add Assignment</button>
              <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="space-y-4">
        {assignments.map((assignment) => {
          const subject = subjects.find(s => s._id === assignment.subject_id)
          return (
            <div key={assignment._id} className={`card ${assignment.status === 'completed' ? 'opacity-60' : ''}`}>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <button onClick={() => toggleStatus(assignment._id, assignment.status)}>
                      <CheckCircle className={`h-6 w-6 ${assignment.status === 'completed' ? 'text-green-600' : 'text-gray-400'}`} />
                    </button>
                    <div>
                      <h3 className={`font-bold text-lg ${assignment.status === 'completed' ? 'line-through' : ''}`}>{assignment.title}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">{subject?.name}</p>
                    </div>
                  </div>
                  {assignment.description && <p className="text-gray-600 dark:text-gray-400 ml-9">{assignment.description}</p>}
                </div>
                <div className="text-right">
                  <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                    <Clock className="h-4 w-4" />
                    <span>{new Date(assignment.deadline).toLocaleDateString()}</span>
                  </div>
                  <span className={`inline-block px-2 py-1 text-xs rounded mt-2 ${assignment.priority === 'high' ? 'bg-red-100 text-red-800' : assignment.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}`}>
                    {assignment.priority}
                  </span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default Assignments

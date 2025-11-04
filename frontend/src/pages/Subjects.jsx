import { useState, useEffect } from 'react'
import api from '../utils/api'
import { Plus, Edit2, Trash2, BookOpen } from 'lucide-react'

const Subjects = () => {
  const [subjects, setSubjects] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ name: '', code: '', credits: 3, professor: '', color: '#3B82F6' })
  const [editingId, setEditingId] = useState(null)

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
      if (editingId) {
        await api.put(`/subjects/${editingId}`, formData)
      } else {
        await api.post('/subjects', formData)
      }
      setFormData({ name: '', code: '', credits: 3, professor: '', color: '#3B82F6' })
      setShowForm(false)
      setEditingId(null)
      fetchSubjects()
    } catch (error) {
      console.error('Error saving subject:', error)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this subject?')) {
      try {
        await api.delete(`/subjects/${id}`)
        fetchSubjects()
      } catch (error) {
        console.error('Error deleting subject:', error)
      }
    }
  }

  const handleEdit = (subject) => {
    setFormData({ name: subject.name, code: subject.code, credits: subject.credits, professor: subject.professor || '', color: subject.color || '#3B82F6' })
    setEditingId(subject._id)
    setShowForm(true)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Subjects & Marks</h1>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary flex items-center space-x-2">
          <Plus className="h-5 w-5" />
          <span>Add Subject</span>
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">
            {editingId ? 'Edit Subject' : 'New Subject'}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Subject Name"
                className="input-field"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
              <input
                type="text"
                placeholder="Subject Code"
                className="input-field"
                value={formData.code}
                onChange={(e) => setFormData({ ...formData, code: e.target.value })}
                required
              />
              <input
                type="number"
                placeholder="Credits"
                className="input-field"
                value={formData.credits}
                onChange={(e) => setFormData({ ...formData, credits: parseInt(e.target.value) })}
                required
              />
              <input
                type="text"
                placeholder="Professor Name"
                className="input-field"
                value={formData.professor}
                onChange={(e) => setFormData({ ...formData, professor: e.target.value })}
              />
            </div>
            <div className="flex items-center space-x-4">
              <label className="text-gray-700 dark:text-gray-300">Color:</label>
              <input
                type="color"
                className="h-10 w-20 rounded cursor-pointer"
                value={formData.color}
                onChange={(e) => setFormData({ ...formData, color: e.target.value })}
              />
            </div>
            <div className="flex space-x-3">
              <button type="submit" className="btn-primary">
                {editingId ? 'Update' : 'Add'} Subject
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowForm(false)
                  setEditingId(null)
                  setFormData({ name: '', code: '', credits: 3, professor: '', color: '#3B82F6' })
                }}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {subjects.map((subject) => (
          <div key={subject._id} className="card" style={{ borderLeft: `4px solid ${subject.color}` }}>
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-3">
                <div className="p-2 rounded-lg" style={{ backgroundColor: `${subject.color}20` }}>
                  <BookOpen className="h-6 w-6" style={{ color: subject.color }} />
                </div>
                <div>
                  <h3 className="font-bold text-lg text-gray-900 dark:text-white">{subject.name}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{subject.code}</p>
                </div>
              </div>
              <div className="flex space-x-2">
                <button onClick={() => handleEdit(subject)} className="text-blue-600 hover:text-blue-700">
                  <Edit2 className="h-4 w-4" />
                </button>
                <button onClick={() => handleDelete(subject._id)} className="text-red-600 hover:text-red-700">
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
            <div className="space-y-2 text-sm">
              <p className="text-gray-600 dark:text-gray-400">Credits: {subject.credits}</p>
              {subject.professor && <p className="text-gray-600 dark:text-gray-400">Professor: {subject.professor}</p>}
            </div>
          </div>
        ))}
      </div>

      {subjects.length === 0 && !showForm && (
        <div className="text-center py-12">
          <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">No subjects added yet. Click "Add Subject" to get started!</p>
        </div>
      )}
    </div>
  )
}

export default Subjects

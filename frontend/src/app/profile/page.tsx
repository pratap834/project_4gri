'use client'

import { useState, useEffect } from 'react'
import { useUser } from '@clerk/nextjs'
import { useRouter } from 'next/navigation'

interface UserProfileData {
  name: string
  email: string
  phone: string
  address: {
    street: string
    city: string
    state: string
    pincode: string
    country: string
  }
  farmDetails: {
    farmName: string
    totalArea: number
    areaUnit: string
    soilType: string
    irrigationType: string[]
  }
  preferences: {
    smsNotifications: boolean
    emailNotifications: boolean
    language: string
  }
}

const SOIL_TYPES = ['Alluvial', 'Black', 'Red', 'Laterite', 'Desert', 'Mountain', 'Clay', 'Sandy', 'Loamy', 'Other']
const IRRIGATION_TYPES = ['Drip', 'Sprinkler', 'Flood', 'Rain-fed', 'Canal', 'Tube-well', 'Other']
const INDIAN_STATES = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat',
  'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
  'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
  'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
  'Uttarakhand', 'West Bengal'
]

export default function UserProfilePage() {
  const { user, isLoaded } = useUser()
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)
  
  const [formData, setFormData] = useState<UserProfileData>({
    name: '',
    email: '',
    phone: '',
    address: {
      street: '',
      city: '',
      state: '',
      pincode: '',
      country: 'India'
    },
    farmDetails: {
      farmName: '',
      totalArea: 0,
      areaUnit: 'acre',
      soilType: '',
      irrigationType: []
    },
    preferences: {
      smsNotifications: true,
      emailNotifications: true,
      language: 'en'
    }
  })

  useEffect(() => {
    if (isLoaded && user) {
      fetchProfile()
    }
  }, [isLoaded, user])

  const fetchProfile = async () => {
    try {
      const response = await fetch('/api/user/profile')
      
      if (response.status === 404) {
        // Profile doesn't exist, initialize with Clerk data
        setFormData(prev => ({
          ...prev,
          name: user?.fullName || '',
          email: user?.primaryEmailAddress?.emailAddress || ''
        }))
        setLoading(false)
        return
      }

      if (!response.ok) throw new Error('Failed to fetch profile')

      const data = await response.json()
      if (data.success) {
        setFormData(data.data)
      }
    } catch (error) {
      console.error('Error fetching profile:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setMessage(null)

    try {
      // Try to update first
      let response = await fetch('/api/user/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      // If profile doesn't exist, create it
      if (response.status === 404) {
        response = await fetch('/api/user/profile', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        })
      }

      const data = await response.json()

      if (data.success) {
        setMessage({ type: 'success', text: 'Profile saved successfully!' })
        
        // Update local state with saved data to prevent reset
        if (data.data) {
          setFormData(data.data)
        } else if (data.profile) {
          setFormData(data.profile)
        }
        
        // Optionally refetch from server to ensure sync
        await fetchProfile()
        
        setTimeout(() => setMessage(null), 3000)
      } else {
        throw new Error(data.error || 'Failed to save profile')
      }
    } catch (error: any) {
      setMessage({ type: 'error', text: error.message || 'Failed to save profile' })
    } finally {
      setSaving(false)
    }
  }

  const handleInputChange = (path: string, value: any) => {
    setFormData(prev => {
      const keys = path.split('.')
      const updated = { ...prev }
      let current: any = updated

      for (let i = 0; i < keys.length - 1; i++) {
        current[keys[i]] = { ...current[keys[i]] }
        current = current[keys[i]]
      }

      current[keys[keys.length - 1]] = value
      return updated
    })
  }

  const toggleIrrigationType = (type: string) => {
    setFormData(prev => ({
      ...prev,
      farmDetails: {
        ...prev.farmDetails,
        irrigationType: prev.farmDetails.irrigationType.includes(type)
          ? prev.farmDetails.irrigationType.filter(t => t !== type)
          : [...prev.farmDetails.irrigationType, type]
      }
    }))
  }

  if (!isLoaded || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#2d5016]"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#f5f5dc] to-[#e8f5e8] py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => router.back()}
            className="flex items-center text-[#2d5016] hover:text-[#4a7c59] mb-4"
          >
            <i className="fas fa-arrow-left mr-2"></i> Back
          </button>
          <h1 className="text-4xl font-bold text-[#2d5016] mb-2">
            <i className="fas fa-user-circle mr-3"></i>User Profile
          </h1>
          <p className="text-gray-600">Manage your personal and farm information</p>
        </div>

        {/* Message Alert */}
        {message && (
          <div className={`mb-6 p-4 rounded-lg ${
            message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            <i className={`fas fa-${message.type === 'success' ? 'check-circle' : 'exclamation-circle'} mr-2`}></i>
            {message.text}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Personal Information */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-[#2d5016] mb-4">
              <i className="fas fa-id-card mr-2"></i>Personal Information
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email *
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number (for SMS alerts)
                </label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => handleInputChange('phone', e.target.value)}
                  placeholder="+91 9876543210"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                />
              </div>
            </div>
          </div>

          {/* Address Information */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-[#2d5016] mb-4">
              <i className="fas fa-map-marker-alt mr-2"></i>Address
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Street Address
                </label>
                <input
                  type="text"
                  value={formData.address.street}
                  onChange={(e) => handleInputChange('address.street', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  City
                </label>
                <input
                  type="text"
                  value={formData.address.city}
                  onChange={(e) => handleInputChange('address.city', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  State
                </label>
                <select
                  value={formData.address.state}
                  onChange={(e) => handleInputChange('address.state', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                >
                  <option value="">Select State</option>
                  {INDIAN_STATES.map(state => (
                    <option key={state} value={state}>{state}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Pincode
                </label>
                <input
                  type="text"
                  value={formData.address.pincode}
                  onChange={(e) => handleInputChange('address.pincode', e.target.value)}
                  maxLength={6}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Country
                </label>
                <input
                  type="text"
                  value={formData.address.country}
                  onChange={(e) => handleInputChange('address.country', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                />
              </div>
            </div>
          </div>

          {/* Farm Details */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-[#2d5016] mb-4">
              <i className="fas fa-tractor mr-2"></i>Farm Details
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Farm Name
                </label>
                <input
                  type="text"
                  value={formData.farmDetails.farmName}
                  onChange={(e) => handleInputChange('farmDetails.farmName', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Total Area
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.farmDetails.totalArea}
                  onChange={(e) => handleInputChange('farmDetails.totalArea', parseFloat(e.target.value))}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Area Unit
                </label>
                <select
                  value={formData.farmDetails.areaUnit}
                  onChange={(e) => handleInputChange('farmDetails.areaUnit', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                >
                  <option value="acre">Acre</option>
                  <option value="hectare">Hectare</option>
                  <option value="bigha">Bigha</option>
                </select>
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Soil Type
                </label>
                <select
                  value={formData.farmDetails.soilType}
                  onChange={(e) => handleInputChange('farmDetails.soilType', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                >
                  <option value="">Select Soil Type</option>
                  {SOIL_TYPES.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Irrigation Type (select all that apply)
                </label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                  {IRRIGATION_TYPES.map(type => (
                    <label key={type} className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.farmDetails.irrigationType.includes(type)}
                        onChange={() => toggleIrrigationType(type)}
                        className="w-4 h-4 text-[#4a7c59] border-gray-300 rounded focus:ring-[#4a7c59]"
                      />
                      <span className="text-sm text-gray-700">{type}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Notification Preferences */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-[#2d5016] mb-4">
              <i className="fas fa-bell mr-2"></i>Notification Preferences
            </h2>
            <div className="space-y-4">
              <label className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.preferences.smsNotifications}
                  onChange={(e) => handleInputChange('preferences.smsNotifications', e.target.checked)}
                  className="w-5 h-5 text-[#4a7c59] border-gray-300 rounded focus:ring-[#4a7c59]"
                />
                <span className="text-gray-700">
                  <i className="fas fa-sms mr-2 text-[#4a7c59]"></i>
                  Receive SMS notifications
                </span>
              </label>
              <label className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.preferences.emailNotifications}
                  onChange={(e) => handleInputChange('preferences.emailNotifications', e.target.checked)}
                  className="w-5 h-5 text-[#4a7c59] border-gray-300 rounded focus:ring-[#4a7c59]"
                />
                <span className="text-gray-700">
                  <i className="fas fa-envelope mr-2 text-[#4a7c59]"></i>
                  Receive Email notifications
                </span>
              </label>
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => router.back()}
              className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-3 bg-gradient-to-r from-[#2d5016] to-[#4a7c59] text-white rounded-lg hover:from-[#1a2f0a] hover:to-[#365a42] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {saving ? (
                <>
                  <i className="fas fa-spinner fa-spin mr-2"></i>
                  Saving...
                </>
              ) : (
                <>
                  <i className="fas fa-save mr-2"></i>
                  Save Profile
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

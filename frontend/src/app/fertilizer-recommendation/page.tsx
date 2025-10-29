'use client'

import { useState } from 'react'
import Link from 'next/link'
import { UserButton, useUser } from '@clerk/nextjs'

export default function FertilizerRecommendationPage() {
  const { user } = useUser()
  const [formData, setFormData] = useState({
    temperature: '',
    humidity: '',
    moisture: '',
    soil_type: 'Sandy',
    crop_type: 'Maize',
    nitrogen: '',
    phosphorous: '',
    potassium: '',
    prediction_date: new Date().toISOString().split('T')[0], // Today's date
    timeframe: '3 months'
  })
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [reportLoading, setReportLoading] = useState(false)
  const [detailedReport, setDetailedReport] = useState<any>(null)

  const soilTypes = ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey']
  const cropTypes = ['Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Barley', 'Wheat', 'Millets', 'Oil seeds', 'Pulses', 'Ground Nuts']
  const timeframeOptions = ['1 month', '2 months', '3 months', '6 months', '1 year']

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setDetailedReport(null)

    try {
      const response = await fetch('http://localhost:8001/api/predict-fertilizer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          temperature: parseFloat(formData.temperature),
          humidity: parseFloat(formData.humidity),
          moisture: parseFloat(formData.moisture),
          soil_type: formData.soil_type,
          crop_type: formData.crop_type,
          nitrogen: parseFloat(formData.nitrogen),
          phosphorous: parseFloat(formData.phosphorous),
          potassium: parseFloat(formData.potassium),
          userId: user?.id || 'guest_user',
          prediction_date: formData.prediction_date,
          timeframe: formData.timeframe
        })
      })

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`)
      }

      const data = await response.json()
      console.log('API Response:', data)
      setResult(data)
    } catch (error) {
      console.error('Error:', error)
      setError('Failed to get recommendation. Ensure API server is running on port 8001.')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateReport = async () => {
    if (!user?.id) {
      setError('Please sign in to generate detailed reports.')
      return
    }

    setReportLoading(true)
    setError(null)

    try {
      const response = await fetch(
        `http://localhost:8001/api/generate-detailed-report?userId=${user.id}&predictionType=fertilizer`,
        { method: 'POST' }
      )

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`)
      }

      const report = await response.json()
      console.log('Report:', report)
      setDetailedReport(report)
    } catch (error) {
      console.error('Error generating report:', error)
      setError('Failed to generate report. Please try again.')
    } finally {
      setReportLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-gradient-to-r from-[#2d5016] to-[#4a7c59] shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center py-4">
            <Link href="/" className="text-white text-3xl font-bold"> FarmWise Analytics</Link>
            <div className="flex items-center space-x-6">
              <Link href="/" className="text-white hover:text-yellow-300">Dashboard</Link>
              <Link href="/profile" className="text-white hover:text-yellow-300">Profile</Link>
              <UserButton afterSignOutUrl="/sign-in" />
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <Link href="/" className="text-[#4a7c59] hover:underline mb-4 inline-block"> Back to Dashboard</Link>
            <h1 className="text-4xl font-bold text-[#2d5016] mb-2"> Fertilizer Recommendation</h1>
            <p className="text-gray-600">Get smart fertilizer suggestions to maximize crop nutrition</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-semibold mb-6 text-[#2d5016]">Enter Field Data</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Soil Type</label>
                  <select className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.soil_type} onChange={(e) => setFormData({...formData, soil_type: e.target.value})}>
                    {soilTypes.map(type => <option key={type} value={type}>{type}</option>)}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Crop Type</label>
                  <select className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.crop_type} onChange={(e) => setFormData({...formData, crop_type: e.target.value})}>
                    {cropTypes.map(type => <option key={type} value={type}>{type}</option>)}
                  </select>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Nitrogen (N)</label>
                    <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.nitrogen} onChange={(e) => setFormData({...formData, nitrogen: e.target.value})} placeholder="37" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Phosphorous (P)</label>
                    <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.phosphorous} onChange={(e) => setFormData({...formData, phosphorous: e.target.value})} placeholder="0" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Potassium (K)</label>
                    <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.potassium} onChange={(e) => setFormData({...formData, potassium: e.target.value})} placeholder="0" />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Temperature (C)</label>
                    <input type="number" step="0.1" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.temperature} onChange={(e) => setFormData({...formData, temperature: e.target.value})} placeholder="26" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Humidity (%)</label>
                    <input type="number" step="0.1" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.humidity} onChange={(e) => setFormData({...formData, humidity: e.target.value})} placeholder="52" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Moisture (%)</label>
                    <input type="number" step="0.1" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.moisture} onChange={(e) => setFormData({...formData, moisture: e.target.value})} placeholder="38" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      📅 Test Date
                    </label>
                    <input 
                      type="date" 
                      required 
                      className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" 
                      value={formData.prediction_date} 
                      onChange={(e) => setFormData({...formData, prediction_date: e.target.value})} 
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      ⏱️ Expected Results Timeframe
                    </label>
                    <select 
                      className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" 
                      value={formData.timeframe} 
                      onChange={(e) => setFormData({...formData, timeframe: e.target.value})}
                    >
                      {timeframeOptions.map(option => <option key={option} value={option}>{option}</option>)}
                    </select>
                  </div>
                </div>

                <button type="submit" disabled={loading} className="w-full bg-gradient-to-r from-[#8b4513] to-[#a0522d] text-white py-3 px-6 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50">
                  {loading ? 'Analyzing...' : '🌱 Get Recommendation'}
                </button>
              </form>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-semibold mb-6 text-[#2d5016]">Results</h2>
              {error ? (
                <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                  <p className="text-red-700">{error}</p>
                </div>
              ) : !result ? (
                <div className="text-center text-gray-500 py-12">
                  <p className="text-lg">Fill out the form to get fertilizer recommendations</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* AI Notification */}
                  {result.notification && (
                    <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                      <div className="flex items-start">
                        <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/>
                        </svg>
                        <div>
                          <h4 className="font-semibold text-blue-800 mb-1">AI Insight</h4>
                          <p className="text-sm text-blue-700">{result.notification}</p>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="bg-amber-50 border-l-4 border-amber-500 p-6 rounded">
                    <h3 className="text-xl font-bold text-amber-800 mb-2">Recommended Fertilizer</h3>
                    <p className="text-3xl font-bold text-amber-600">{result.recommended_fertilizer}</p>
                    <div className="mt-4">
                      <p className="text-sm text-gray-600 mb-1">Confidence Level</p>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div className="bg-amber-600 h-3 rounded-full" style={{width: `${result.confidence}%`}}></div>
                      </div>
                      <p className="text-right text-sm font-semibold mt-1">{result.confidence}%</p>
                    </div>
                  </div>

                  {/* Generate Report Button */}
                  {user && (
                    <button
                      onClick={handleGenerateReport}
                      disabled={reportLoading}
                      className="w-full bg-gradient-to-r from-[#a0522d] to-[#8b4513] text-white py-3 px-6 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 flex items-center justify-center"
                    >
                      {reportLoading ? (
                        <>
                          <svg className="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                          </svg>
                          Generating Report...
                        </>
                      ) : (
                        <>
                          📄 Generate Detailed Report
                        </>
                      )}
                    </button>
                  )}
                  
                  {result.npk_values && (
                    <div className="bg-blue-50 p-4 rounded">
                      <h4 className="font-semibold mb-2">NPK Values:</h4>
                      <div className="grid grid-cols-3 gap-2 text-sm">
                        <div> N: {result.npk_values.nitrogen}</div>
                        <div> P: {result.npk_values.phosphorous}</div>
                        <div> K: {result.npk_values.potassium}</div>
                      </div>
                    </div>
                  )}

                  {result.soil_conditions && (
                    <div className="bg-green-50 p-4 rounded">
                      <h4 className="font-semibold mb-2">Field Conditions:</h4>
                      <ul className="space-y-1 text-sm">
                        <li> Soil Type: {result.soil_conditions.soil_type}</li>
                        <li> Temperature: {result.soil_conditions.temperature}C</li>
                        <li> Humidity: {result.soil_conditions.humidity}%</li>
                        <li> Moisture: {result.soil_conditions.moisture}%</li>
                        <li> Crop: {result.crop_type}</li>
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Detailed Report Section */}
          {detailedReport && detailedReport.success && (
            <div className="bg-white rounded-lg shadow-lg p-8 mt-8">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-semibold text-[#2d5016]">📊 Detailed AI Report - Soil Health Analysis</h2>
                <button
                  onClick={() => setDetailedReport(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>
              
              <div className="mb-4 p-4 bg-amber-50 rounded">
                <p className="text-sm text-gray-600">Generated: {new Date(detailedReport.generated_at).toLocaleString()}</p>
                <p className="text-sm text-gray-600">Based on {detailedReport.history_count} previous prediction(s)</p>
              </div>

              <div className="prose max-w-none">
                <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                  {detailedReport.detailed_report}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

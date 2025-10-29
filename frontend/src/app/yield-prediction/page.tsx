'use client'

import { useState } from 'react'
import Link from 'next/link'
import { UserButton, useUser } from '@clerk/nextjs'

export default function YieldPredictionPage() {
  const { user } = useUser()
  const [formData, setFormData] = useState({
    state: 'Assam',
    crop: 'Rice',
    season: 'Kharif',
    area: '',
    production: '',
    annual_rainfall: '',
    fertilizer: '',
    pesticide: '',
    prediction_date: new Date().toISOString().split('T')[0],
    timeframe: '6 months'
  })
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [reportLoading, setReportLoading] = useState(false)
  const [detailedReport, setDetailedReport] = useState<any>(null)

  const states = ['Andhra Pradesh', 'Karnataka', 'Maharashtra', 'Tamil Nadu', 'Uttar Pradesh', 'West Bengal', 'Gujarat', 'Madhya Pradesh', 'Punjab', 'Haryana', 'Assam', 'Kerala', 'Meghalaya', 'Puducherry', 'Goa', 'Odisha', 'Bihar', 'Mizoram', 'Tripura', 'Nagaland', 'Chhattisgarh', 'Uttarakhand', 'Jharkhand', 'Delhi', 'Manipur', 'Jammu and Kashmir', 'Telangana', 'Arunachal Pradesh', 'Sikkim']
  const crops = ['Rice', 'Wheat', 'Maize', 'Sugarcane', 'Cotton', 'Jute', 'Coconut', 'Arecanut', 'Bajra', 'Barley', 'Jowar', 'Ragi', 'Groundnut', 'Sunflower', 'Soyabean', 'Rapeseed', 'Moong', 'Urad', 'Arhar/Tur', 'Masoor', 'Gram', 'Horse-gram', 'Peas']
  const seasons = ['Kharif', 'Rabi', 'Whole Year', 'Autumn', 'Summer', 'Winter']
  const timeframeOptions = ['3 months', '4 months', '6 months', '9 months', '1 year']

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setDetailedReport(null)

    try {
      const response = await fetch('http://localhost:8001/api/predict-yield', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          crop: formData.crop,
          season: formData.season,
          state: formData.state,
          area: parseFloat(formData.area),
          production: parseFloat(formData.production),
          annual_rainfall: parseFloat(formData.annual_rainfall),
          fertilizer: parseFloat(formData.fertilizer),
          pesticide: parseFloat(formData.pesticide),
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
      setError('Failed to predict yield. Ensure API server is running on port 8001.')
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
        `http://localhost:8001/api/generate-detailed-report?userId=${user.id}&predictionType=yield`,
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
            <h1 className="text-4xl font-bold text-[#2d5016] mb-2"> Yield Prediction</h1>
            <p className="text-gray-600">Forecast your crop yield with AI-powered analytics</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-semibold mb-6 text-[#2d5016]">Enter Cultivation Details</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">State</label>
                  <select className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.state} onChange={(e) => setFormData({...formData, state: e.target.value})}>
                    {states.map(state => <option key={state} value={state}>{state}</option>)}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Crop</label>
                  <select className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.crop} onChange={(e) => setFormData({...formData, crop: e.target.value})}>
                    {crops.map(crop => <option key={crop} value={crop}>{crop}</option>)}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Season</label>
                  <select className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.season} onChange={(e) => setFormData({...formData, season: e.target.value})}>
                    {seasons.map(season => <option key={season} value={season}>{season}</option>)}
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Area (hectares)</label>
                    <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.area} onChange={(e) => setFormData({...formData, area: e.target.value})} placeholder="100" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Previous Production (tons)</label>
                    <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.production} onChange={(e) => setFormData({...formData, production: e.target.value})} placeholder="200" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Annual Rainfall (mm)</label>
                    <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.annual_rainfall} onChange={(e) => setFormData({...formData, annual_rainfall: e.target.value})} placeholder="1200" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Fertilizer (kg/ha)</label>
                    <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.fertilizer} onChange={(e) => setFormData({...formData, fertilizer: e.target.value})} placeholder="150" />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Pesticide (kg/ha)</label>
                  <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.pesticide} onChange={(e) => setFormData({...formData, pesticide: e.target.value})} placeholder="50" />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      📅 Prediction Date
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
                      ⏱️ Expected Harvest Timeframe
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

                <button type="submit" disabled={loading} className="w-full bg-gradient-to-r from-[#2d5016] to-[#4a7c59] text-white py-3 px-6 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50">
                  {loading ? 'Calculating...' : '🌾 Predict Yield'}
                </button>
              </form>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-semibold mb-6 text-[#2d5016]">Prediction Results</h2>
              {error ? (
                <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                  <p className="text-red-700">{error}</p>
                </div>
              ) : !result ? (
                <div className="text-center text-gray-500 py-12">
                  <p className="text-lg">Fill out the form to predict crop yield</p>
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

                  <div className="bg-green-50 border-l-4 border-green-500 p-6 rounded">
                    <h3 className="text-xl font-bold text-green-800 mb-2">Predicted Yield</h3>
                    <p className="text-5xl font-bold text-green-600">{result.predicted_yield}</p>
                    <p className="text-gray-600 mt-2">{result.yield_unit || 'tonnes per hectare'}</p>
                  </div>

                  {/* Generate Report Button */}
                  {user && (
                    <button
                      onClick={handleGenerateReport}
                      disabled={reportLoading}
                      className="w-full bg-gradient-to-r from-[#4a7c59] to-[#2d5016] text-white py-3 px-6 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 flex items-center justify-center"
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
                  
                  {result.confidence_interval && (
                    <div className="bg-blue-50 p-4 rounded">
                      <h4 className="font-semibold mb-2">Confidence Interval:</h4>
                      <div className="flex justify-between text-sm">
                        <span>Lower: {result.confidence_interval.lower} t/ha</span>
                        <span>Upper: {result.confidence_interval.upper} t/ha</span>
                      </div>
                    </div>
                  )}

                  {result.input_parameters && (
                    <div className="bg-yellow-50 p-4 rounded">
                      <h4 className="font-semibold mb-2">Cultivation Summary:</h4>
                      <ul className="space-y-1 text-sm text-gray-700">
                        <li> <strong>Crop:</strong> {result.input_parameters.crop}</li>
                        <li> <strong>State:</strong> {result.input_parameters.state}</li>
                        <li> <strong>Season:</strong> {result.input_parameters.season}</li>
                        <li> <strong>Area:</strong> {result.input_parameters.area} hectares</li>
                        <li> <strong>Rainfall:</strong> {result.input_parameters.annual_rainfall} mm</li>
                        <li> <strong>Fertilizer:</strong> {result.input_parameters.fertilizer} kg/ha</li>
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
                <h2 className="text-2xl font-semibold text-[#2d5016]">📊 Detailed AI Report - Yield Analysis</h2>
                <button
                  onClick={() => setDetailedReport(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>
              
              <div className="mb-4 p-4 bg-green-50 rounded">
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

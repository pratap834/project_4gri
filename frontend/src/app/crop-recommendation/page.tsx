'use client'

import { useState } from 'react'
import Link from 'next/link'
import { UserButton, useUser } from '@clerk/nextjs'

export default function CropRecommendationPage() {
  const { user } = useUser()
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: ''
  })
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [reportLoading, setReportLoading] = useState(false)
  const [detailedReport, setDetailedReport] = useState<any>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setDetailedReport(null)

    try {
      const response = await fetch('http://localhost:8001/api/predict-crop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          N: parseFloat(formData.N),
          P: parseFloat(formData.P),
          K: parseFloat(formData.K),
          temperature: parseFloat(formData.temperature),
          humidity: parseFloat(formData.humidity),
          ph: parseFloat(formData.ph),
          rainfall: parseFloat(formData.rainfall),
          userId: user?.id || 'guest_user'
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
        `http://localhost:8001/api/generate-detailed-report?userId=${user.id}&predictionType=crop`,
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
            <h1 className="text-4xl font-bold text-[#2d5016] mb-2"> Crop Recommendation</h1>
            <p className="text-gray-600">Get AI-powered crop suggestions based on soil and climate conditions</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-semibold mb-6 text-[#2d5016]">Soil & Climate Data</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Nitrogen (N)</label>
                    <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.N} onChange={(e) => setFormData({...formData, N: e.target.value})} placeholder="90" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Phosphorus (P)</label>
                    <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.P} onChange={(e) => setFormData({...formData, P: e.target.value})} placeholder="42" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Potassium (K)</label>
                    <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.K} onChange={(e) => setFormData({...formData, K: e.target.value})} placeholder="43" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Temperature (C)</label>
                    <input type="number" step="0.1" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.temperature} onChange={(e) => setFormData({...formData, temperature: e.target.value})} placeholder="20.8" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Humidity (%)</label>
                    <input type="number" step="0.1" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.humidity} onChange={(e) => setFormData({...formData, humidity: e.target.value})} placeholder="82" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">pH Level</label>
                    <input type="number" step="0.1" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.ph} onChange={(e) => setFormData({...formData, ph: e.target.value})} placeholder="6.5" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Rainfall (mm)</label>
                    <input type="number" step="0.1" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-[#4a7c59]" value={formData.rainfall} onChange={(e) => setFormData({...formData, rainfall: e.target.value})} placeholder="202.9" />
                  </div>
                </div>

                <button type="submit" disabled={loading} className="w-full bg-gradient-to-r from-[#2d5016] to-[#4a7c59] text-white py-3 px-6 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50">
                  {loading ? 'Analyzing...' : ' Get Recommendation'}
                </button>
              </form>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-semibold mb-6 text-[#2d5016]">Recommended Crop</h2>
              {error ? (
                <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                  <p className="text-red-700">{error}</p>
                </div>
              ) : !result ? (
                <div className="text-center text-gray-500 py-12">
                  <p className="text-lg">Fill out the form to get crop recommendations</p>
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
                    <h3 className="text-xl font-bold text-green-800 mb-2">Best Crop for Your Field</h3>
                    <p className="text-4xl font-bold text-green-600 capitalize">{result.recommended_crop}</p>
                    <div className="mt-4">
                      <p className="text-sm text-gray-600 mb-1">Confidence Level</p>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div className="bg-green-600 h-3 rounded-full" style={{width: `${result.confidence}%`}}></div>
                      </div>
                      <p className="text-right text-sm font-semibold mt-1">{result.confidence}%</p>
                    </div>
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

                  {result.alternatives && result.alternatives.length > 0 && (
                    <div className="bg-blue-50 p-4 rounded">
                      <h4 className="font-semibold mb-3">Alternative Recommendations:</h4>
                      <div className="space-y-2">
                        {result.alternatives.map((alt: any, i: number) => (
                          <div key={i} className="flex justify-between items-center">
                            <span className="capitalize">{alt.crop}</span>
                            <span className="text-sm font-semibold text-blue-600">{alt.confidence}%</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {result.soil_analysis && (
                    <div className="bg-amber-50 p-4 rounded">
                      <h4 className="font-semibold mb-2">Soil Analysis:</h4>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div> Nitrogen: {result.soil_analysis.nitrogen}</div>
                        <div> Phosphorus: {result.soil_analysis.phosphorus}</div>
                        <div> Potassium: {result.soil_analysis.potassium}</div>
                        <div> pH: {result.soil_analysis.ph}</div>
                      </div>
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
                <h2 className="text-2xl font-semibold text-[#2d5016]">📊 Detailed AI Report</h2>
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

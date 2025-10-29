'use client'

import { useState } from 'react'
import Link from 'next/link'
import { UserButton, useUser } from '@clerk/nextjs'

export default function DiseaseDetectionPage() {
  const { user } = useUser()
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [predictionDate, setPredictionDate] = useState(new Date().toISOString().split('T')[0])
  const [timeframe, setTimeframe] = useState('1 week')
  const [showReportModal, setShowReportModal] = useState(false)
  const [detailedReport, setDetailedReport] = useState<string>('')
  const [loadingReport, setLoadingReport] = useState(false)

  const timeframeOptions = ['1 week', '2 weeks', '1 month', '2 months']

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      const reader = new FileReader()
      reader.onloadend = () => setPreview(reader.result as string)
      reader.readAsDataURL(file)
      setResult(null)
      setError(null)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedFile) {
      setError('Please select an image first')
      return
    }

    setLoading(true)
    setError(null)
    const formData = new FormData()
    formData.append('file', selectedFile)
    formData.append('userId', user?.id || '')
    formData.append('prediction_date', predictionDate)
    formData.append('timeframe', timeframe)

    try {
      const response = await fetch('http://localhost:8002/api/detect-disease', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`)
      }

      const data = await response.json()
      console.log('API Response:', data)
      setResult(data)
    } catch (error) {
      console.error('Error:', error)
      setError('Failed to detect disease. Ensure Disease Detection API is running on port 8002 (start_disease_service.bat).')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateReport = async () => {
    if (!result || !user?.id) return
    
    setLoadingReport(true)
    try {
      const response = await fetch('http://localhost:8001/api/generate-detailed-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: user.id,
          prediction_type: 'disease'
        })
      })

      if (!response.ok) {
        throw new Error(`Report API Error: ${response.status}`)
      }

      const data = await response.json()
      if (data.success) {
        setDetailedReport(data.report)
        setShowReportModal(true)
      }
    } catch (error) {
      console.error('Report Error:', error)
      setError('Failed to generate detailed report')
    } finally {
      setLoadingReport(false)
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
            <h1 className="text-4xl font-bold text-[#2d5016] mb-2"> Disease Detection</h1>
            <p className="text-gray-600">Identify plant diseases using AI-powered image analysis</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-semibold mb-6 text-[#2d5016]">Upload Plant Image</h2>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="prediction_date" className="block text-sm font-medium text-gray-700 mb-2">
                      📅 Detection Date
                    </label>
                    <input
                      type="date"
                      id="prediction_date"
                      value={predictionDate}
                      onChange={(e) => setPredictionDate(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                      required
                    />
                  </div>
                  <div>
                    <label htmlFor="timeframe" className="block text-sm font-medium text-gray-700 mb-2">
                      ⏱️ Follow-up Timeframe
                    </label>
                    <select
                      id="timeframe"
                      value={timeframe}
                      onChange={(e) => setTimeframe(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4a7c59] focus:border-transparent"
                      required
                    >
                      {timeframeOptions.map((option) => (
                        <option key={option} value={option}>{option}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-[#4a7c59] transition-colors">
                  {preview ? (
                    <div className="space-y-4">
                      <img src={preview} alt="Preview" className="max-h-64 mx-auto rounded-lg shadow-md" />
                      <p className="text-sm text-gray-600">{selectedFile?.name}</p>
                    </div>
                  ) : (
                    <div className="py-8">
                      <svg className="mx-auto h-16 w-16 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                      <p className="mt-4 text-sm text-gray-600">Click to upload or drag and drop</p>
                      <p className="text-xs text-gray-500">PNG, JPG up to 10MB</p>
                    </div>
                  )}
                  <input type="file" accept="image/*" onChange={handleFileChange} className="hidden" id="file-upload" />
                  <label htmlFor="file-upload" className="mt-4 inline-block bg-white border border-gray-300 rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 cursor-pointer">
                    {preview ? 'Change Image' : 'Select Image'}
                  </label>
                </div>

                {error && (
                  <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                    <p className="text-red-700 text-sm">{error}</p>
                  </div>
                )}

                <button type="submit" disabled={loading || !selectedFile} className="w-full bg-gradient-to-r from-red-600 to-red-700 text-white py-3 px-6 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50">
                  {loading ? 'Analyzing...' : ' Detect Disease'}
                </button>
              </form>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-semibold mb-6 text-[#2d5016]">Detection Results</h2>
              {!result ? (
                <div className="text-center text-gray-500 py-12">
                  <p className="text-lg">Upload an image to detect diseases</p>
                  <p className="text-sm mt-2">Supported plants: Apple, Corn, Grape, Potato, Rice, Tomato, Wheat</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {result.notification && (
                    <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                      <div className="flex items-start">
                        <div className="flex-shrink-0">
                          <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                          </svg>
                        </div>
                        <div className="ml-3 flex-1">
                          <p className="text-sm text-blue-700 font-medium">AI Analysis</p>
                          <p className="text-sm text-blue-600 mt-1 whitespace-pre-line">{result.notification}</p>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className={`border-l-4 p-6 rounded ${result.is_healthy ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'}`}>
                    <h3 className={`text-xl font-bold mb-2 ${result.is_healthy ? 'text-green-800' : 'text-red-800'}`}>
                      {result.is_healthy ? ' Plant is Healthy!' : ' Disease Detected'}
                    </h3>
                    <p className="text-sm text-gray-600 mb-1">Plant Type:</p>
                    <p className="text-2xl font-bold text-gray-800 mb-3">{result.plant}</p>
                    
                    <p className="text-sm text-gray-600 mb-1">Condition:</p>
                    <p className={`text-3xl font-bold ${result.is_healthy ? 'text-green-600' : 'text-red-600'}`}>
                      {result.disease}
                    </p>
                    
                    <div className="mt-4">
                      <p className="text-sm text-gray-600 mb-1">Confidence Level:</p>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div className={`h-2 rounded-full ${result.is_healthy ? 'bg-green-600' : 'bg-red-600'}`} style={{width: `${result.confidence}%`}}></div>
                      </div>
                      <p className="text-right text-sm font-semibold mt-1">{result.confidence}%</p>
                    </div>

                    {result.severity && result.severity !== 'None' && (
                      <div className="mt-3">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${result.severity === 'High' ? 'bg-red-200 text-red-800' : result.severity === 'Moderate' ? 'bg-yellow-200 text-yellow-800' : 'bg-orange-200 text-orange-800'}`}>
                          Severity: {result.severity}
                        </span>
                      </div>
                    )}
                  </div>

                  {result.top_predictions && result.top_predictions.length > 0 && (
                    <div className="bg-blue-50 p-4 rounded">
                      <h4 className="font-semibold mb-2">Top Predictions:</h4>
                      <div className="space-y-2">
                        {result.top_predictions.map((pred: any, i: number) => (
                          <div key={i} className="flex justify-between text-sm">
                            <span>{pred.plant} - {pred.disease}</span>
                            <span className="font-semibold text-blue-600">{pred.confidence}%</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {result.recommendations && (
                    <div className="bg-yellow-50 p-4 rounded">
                      <h4 className="font-semibold mb-2"> Treatment Recommendations:</h4>
                      {result.recommendations.treatment && (
                        <div className="mb-3">
                          <p className="text-sm font-semibold text-gray-700">Treatment:</p>
                          <p className="text-sm text-gray-600">{result.recommendations.treatment}</p>
                        </div>
                      )}
                      {result.recommendations.prevention && result.recommendations.prevention.length > 0 && (
                        <div className="mb-3">
                          <p className="text-sm font-semibold text-gray-700">Prevention:</p>
                          <ul className="text-sm text-gray-600 space-y-1">
                            {result.recommendations.prevention.map((tip: string, i: number) => (
                              <li key={i}> {tip}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {result.recommendations.pesticides && result.recommendations.pesticides.length > 0 && (
                        <div>
                          <p className="text-sm font-semibold text-gray-700">Recommended Pesticides:</p>
                          <p className="text-sm text-gray-600">{result.recommendations.pesticides.join(', ')}</p>
                        </div>
                      )}
                    </div>
                  )}

                  <button
                    onClick={handleGenerateReport}
                    disabled={loadingReport}
                    className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 px-6 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50"
                  >
                    {loadingReport ? 'Generating Report...' : '📊 Generate Detailed Disease Report'}
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {showReportModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" onClick={() => setShowReportModal(false)}>
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
              <h3 className="text-2xl font-bold text-[#2d5016]">📊 Detailed Disease Analysis Report</h3>
              <button onClick={() => setShowReportModal(false)} className="text-gray-400 hover:text-gray-600">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="px-6 py-4">
              <div className="prose max-w-none">
                <div className="whitespace-pre-line text-gray-700 leading-relaxed">{detailedReport}</div>
              </div>
            </div>
            <div className="sticky bottom-0 bg-gray-50 px-6 py-4 border-t border-gray-200">
              <button onClick={() => setShowReportModal(false)} className="w-full bg-[#2d5016] text-white py-2 px-4 rounded-lg hover:bg-[#4a7c59] transition-colors">
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

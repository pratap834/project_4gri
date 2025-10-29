'use client'

import { UserButton } from '@clerk/nextjs'
import Link from 'next/link'

const Dashboard = () => {
  return (
    <>
      {/* Navigation */}
      <nav className="bg-gradient-to-r from-[#2d5016] to-[#4a7c59] shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center py-4">
            <Link href="/" className="text-white text-3xl font-bold">
              <i className="fas fa-seedling mr-2"></i>FarmWise Analytics
            </Link>
            <div className="flex items-center space-x-6">
              <Link
                href="/profile"
                className="text-white hover:text-[#daa520] transition-colors flex items-center"      
              >
                <i className="fas fa-user mr-2"></i>
                Profile
              </Link>
              <Link
                href="/crops"
                className="text-white hover:text-[#daa520] transition-colors flex items-center"      
              >
                <i className="fas fa-seedling mr-2"></i>
                My Crops
              </Link>
              <Link
                href="/resources"
                className="text-white hover:text-[#daa520] transition-colors flex items-center"      
              >
                <i className="fas fa-box mr-2"></i>
                Resources
              </Link>
              <Link
                href="/schemes"
                className="text-white hover:text-[#daa520] transition-colors flex items-center"      
              >
                <i className="fas fa-landmark mr-2"></i>
                Schemes
              </Link>
              <UserButton
                appearance={{
                  elements: {
                    avatarBox: 'w-8 h-8'
                  }
                }}
                afterSignOutUrl="/sign-in"
              />
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-[#2d5016cc] to-[#4a7c59cc] text-white py-16 text-center relative">
        <div
          className="absolute inset-0 opacity-30"
          style={{
            backgroundImage: `url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 600'><path d='M0,300 Q300,200 600,300 T1200,300 L1200,600 L0,600 Z' fill='%23a8d5ba' opacity='0.3'/></svg>")`,
            backgroundSize: 'cover'
          }}
        ></div>
        <div className="container mx-auto px-4 relative z-10">
          <h1 className="text-6xl font-bold mb-4 drop-shadow-lg">Smart Agriculture Solutions</h1>    
          <p className="text-xl mb-8 opacity-90">Empowering farmers with data-driven insights for sustainable and profitable farming</p>
        </div>
      </section>

      {/* Statistics */}
      <div className="container mx-auto px-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 -mt-8 relative z-20 max-w-4xl mx-auto">   
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center p-4">
              <span className="block text-4xl font-bold text-[#2d5016] mb-2">98.8%</span>
              <span className="text-gray-600 text-sm uppercase tracking-wider">Disease Detection Accuracy</span>
            </div>
            <div className="text-center p-4">
              <span className="block text-4xl font-bold text-[#2d5016] mb-2">90.9%</span>
              <span className="text-gray-600 text-sm uppercase tracking-wider">Fertilizer Prediction</span>
            </div>
            <div className="text-center p-4">
              <span className="block text-4xl font-bold text-[#2d5016] mb-2">89.5%</span>
              <span className="text-gray-600 text-sm uppercase tracking-wider">Crop Recommendation</span>
            </div>
            <div className="text-center p-4">
              <span className="block text-4xl font-bold text-[#2d5016] mb-2">38+</span>
              <span className="text-gray-600 text-sm uppercase tracking-wider">Plant Diseases Detected</span>
            </div>
          </div>
        </div>
      </div>

      {/* Services Section */}
      <div className="container mx-auto px-4 py-20">
        <h2 className="text-5xl font-bold text-center text-[#2d5016] mb-16 relative">
          Agricultural Intelligence Services
          <div className="absolute bottom-[-10px] left-1/2 transform -translate-x-1/2 w-20 h-1 bg-gradient-to-r from-[#daa520] to-[#d4691a] rounded"></div>
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          {/* Crop Recommendation */}
          <div className="group">
            <div className="bg-white rounded-3xl p-10 text-center transition-all duration-400 shadow-lg hover:shadow-2xl transform hover:-translate-y-3 h-full relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#daa520] to-[#d4691a] transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
              <i className="fas fa-seedling text-6xl text-[#4a7c59] mb-6 block"></i>
              <h3 className="text-2xl font-semibold text-[#2d5016] mb-4">Smart Crop Planning</h3>    
              <p className="text-gray-600 text-base leading-relaxed mb-8">
                Get personalized crop recommendations based on soil conditions, weather patterns, and nutrient analysis for optimal yield.
              </p>
              <Link
                href="/crop-recommendation"
                className="inline-block bg-gradient-to-r from-[#4a7c59] to-[#5db36a] text-white py-3 px-8 rounded-full font-medium uppercase tracking-wider transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
              >
                Plan Crops
              </Link>
            </div>
          </div>

          {/* Fertilizer Optimization */}
          <div className="group">
            <div className="bg-white rounded-3xl p-10 text-center transition-all duration-400 shadow-lg hover:shadow-2xl transform hover:-translate-y-3 h-full relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#daa520] to-[#d4691a] transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
              <i className="fas fa-flask text-6xl text-[#8b4513] mb-6 block"></i>
              <h3 className="text-2xl font-semibold text-[#2d5016] mb-4">Fertilizer Optimization</h3>
              <p className="text-gray-600 text-base leading-relaxed mb-8">
                Maximize crop nutrition while minimizing costs with our intelligent fertilizer recommendation system.
              </p>
              <Link
                href="/fertilizer-recommendation"
                className="inline-block bg-gradient-to-r from-[#8b4513] to-[#a0522d] text-white py-3 px-8 rounded-full font-medium uppercase tracking-wider transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
              >
                Optimize Nutrition
              </Link>
            </div>
          </div>

          {/* Yield Forecasting */}
          <div className="group">
            <div className="bg-white rounded-3xl p-10 text-center transition-all duration-400 shadow-lg hover:shadow-2xl transform hover:-translate-y-3 h-full relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#daa520] to-[#d4691a] transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
              <i className="fas fa-chart-line text-6xl text-[#daa520] mb-6 block"></i>
              <h3 className="text-2xl font-semibold text-[#2d5016] mb-4">Yield Forecasting</h3>      
              <p className="text-gray-600 text-base leading-relaxed mb-8">
                Predict harvest outcomes and plan your farming operations with accurate yield predictions and market insights.
              </p>
              <Link
                href="/yield-prediction"
                className="inline-block bg-gradient-to-r from-[#daa520] to-[#ffd700] text-[#2d5016] py-3 px-8 rounded-full font-medium uppercase tracking-wider transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
              >
                Forecast Yield
              </Link>
            </div>
          </div>

          {/* Plant Health Monitor */}
          <div className="group">
            <div className="bg-white rounded-3xl p-10 text-center transition-all duration-400 shadow-lg hover:shadow-2xl transform hover:-translate-y-3 h-full relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#daa520] to-[#d4691a] transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
              <i className="fas fa-leaf text-6xl text-[#d4691a] mb-6 block"></i>
              <h3 className="text-2xl font-semibold text-[#2d5016] mb-4">Plant Health Monitor</h3>   
              <p className="text-gray-600 text-base leading-relaxed mb-8">
                Early detection of plant diseases using advanced image analysis to protect your crops and prevent losses.
              </p>
              <Link
                href="/disease-detection"
                className="inline-block bg-gradient-to-r from-[#d4691a] to-[#ff7f50] text-white py-3 px-8 rounded-full font-medium uppercase tracking-wider transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
              >
                Check Plant Health
              </Link>
            </div>
          </div>

          {/* Government Schemes */}
          <div className="group">
            <div className="bg-white rounded-3xl p-10 text-center transition-all duration-400 shadow-lg hover:shadow-2xl transform hover:-translate-y-3 h-full relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#daa520] to-[#d4691a] transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
              <i className="fas fa-landmark text-6xl text-[#0066cc] mb-6 block"></i>
              <h3 className="text-2xl font-semibold text-[#2d5016] mb-4">Government Schemes</h3>
              <p className="text-gray-600 text-base leading-relaxed mb-8">
                Explore agricultural schemes and subsidies available for farmers. Find financial assistance and support programs.
              </p>
              <Link
                href="/schemes"
                className="inline-block bg-gradient-to-r from-[#0066cc] to-[#0052a3] text-white py-3 px-8 rounded-full font-medium uppercase tracking-wider transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
              >
                View Schemes
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-[#2d5016] text-white py-12 mt-20">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <h3 className="text-2xl font-semibold mb-4">
              <i className="fas fa-seedling mr-2"></i>FarmWise Analytics
            </h3>
            <p className="mb-4">Transforming agriculture through intelligent data analysis and machine learning</p>
            <p className="mt-8">&copy; 2025 FarmWise Analytics. Cultivating the future of farming.</p>
          </div>
        </div>
      </footer>
    </>
  )
}

export default Dashboard

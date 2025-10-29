import { SignIn } from '@clerk/nextjs'

export default function SignInPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl mx-auto">
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden flex">
          {/* Left Side - Branding */}
          <div className="hidden lg:flex flex-1 bg-gradient-to-br from-primary-600 to-secondary-600 p-12 flex-col justify-center relative overflow-hidden">
            <div className="relative z-10">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-secondary-500 rounded-lg flex items-center justify-center mr-4">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z" clipRule="evenodd" />
                  </svg>
                </div>
                <h1 className="text-3xl font-display font-bold text-white">FarmWise Analytics</h1>
              </div>
              <p className="text-xl text-primary-100 mb-8 leading-relaxed">
                Cultivating the future of smart agriculture with AI-powered insights
              </p>
              <div className="space-y-4">
                <div className="flex items-center text-primary-100">
                  <svg className="w-6 h-6 mr-3 text-secondary-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  Advanced AI crop recommendations
                </div>
                <div className="flex items-center text-primary-100">
                  <svg className="w-6 h-6 mr-3 text-secondary-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  Smart fertilizer optimization
                </div>
                <div className="flex items-center text-primary-100">
                  <svg className="w-6 h-6 mr-3 text-secondary-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  Accurate yield predictions
                </div>
                <div className="flex items-center text-primary-100">
                  <svg className="w-6 h-6 mr-3 text-secondary-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  Plant disease detection (98.8% accuracy)
                </div>
              </div>
            </div>
            <div className="absolute inset-0 bg-pattern opacity-20"></div>
          </div>

          {/* Right Side - Sign In Form */}
          <div className="flex-1 p-12 flex items-center justify-center">
            <div className="w-full max-w-md">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-display font-bold text-primary-800 mb-2">Welcome Back</h2>
                <p className="text-gray-600">Sign in to access your agricultural dashboard</p>
              </div>
              
              <SignIn 
                appearance={{
                  elements: {
                    formButtonPrimary: 'bg-primary-600 hover:bg-primary-700 text-white',
                    card: 'shadow-none',
                    headerTitle: 'text-primary-800 font-display',
                    headerSubtitle: 'text-gray-600',
                    socialButtonsIconButton: 'border-gray-300 hover:bg-gray-50',
                    formFieldInput: 'border-gray-300 focus:border-primary-500 focus:ring-primary-500',
                    footerActionLink: 'text-primary-600 hover:text-primary-700',
                    // Hide phone number field
                    formFieldInputPhoneNumber: 'display: none !important',
                    phoneNumberField: 'display: none !important',
                    formFieldPhoneNumber: 'display: none !important'
                  }
                }}
                routing="path"
                path="/sign-in"
                redirectUrl="/"
                signUpUrl="/sign-up"
              />
            </div>
          </div>
        </div>
      </div>
      
      {/* Client-side script to remove phone number fields */}
      <script
        dangerouslySetInnerHTML={{
          __html: `
            // Function to remove phone number fields
            function removePhoneFields() {
              const phoneSelectors = [
                '[data-clerk-field="phoneNumber"]',
                '[data-testid="phone-number-field"]',
                '.cl-phoneNumber',
                '.cl-phoneNumberField',
                '.cl-formFieldPhoneNumber',
                'input[name="phoneNumber"]',
                'input[placeholder*="phone"]',
                'input[placeholder*="Phone"]',
                'label[for*="phone"]',
                'div[class*="phone"]',
                '[name="phoneNumber"]'
              ];
              
              phoneSelectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(element => {
                  if (element) {
                    element.style.display = 'none';
                    element.style.visibility = 'hidden';
                    element.style.height = '0px';
                    element.style.margin = '0px';
                    element.style.padding = '0px';
                    // Also remove parent container if it exists
                    const parent = element.closest('.cl-formField');
                    if (parent) {
                      parent.style.display = 'none';
                    }
                  }
                });
              });
            }
            
            // Run immediately and after DOM changes
            removePhoneFields();
            
            // Use MutationObserver to catch dynamically added elements
            const observer = new MutationObserver(function(mutations) {
              mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length > 0) {
                  removePhoneFields();
                }
              });
            });
            
            // Start observing
            observer.observe(document.body, {
              childList: true,
              subtree: true
            });
            
            // Also run after a delay to catch late-loading elements
            setTimeout(removePhoneFields, 1000);
            setTimeout(removePhoneFields, 2000);
          `
        }}
      />
    </div>
  )
}
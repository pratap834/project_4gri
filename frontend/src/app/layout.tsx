import { ClerkProvider } from '@clerk/nextjs'
import { Inter, Poppins } from 'next/font/google'
import './globals.css'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-poppins',
})

export const metadata = {
  title: 'FarmWise Analytics - Smart Agriculture Dashboard',
  description: 'Empowering farmers with data-driven insights for sustainable and profitable farming',
  keywords: 'agriculture, AI, crop recommendation, fertilizer, yield prediction, disease detection',
  authors: [{ name: 'FarmWise Analytics Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en" className={`${inter.variable} ${poppins.variable}`}>
        <head>
          <link rel="icon" href="/favicon.ico" />
          <meta name="theme-color" content="#2d5016" />
          <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" />
        </head>
        <body className="font-sans antialiased">
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}

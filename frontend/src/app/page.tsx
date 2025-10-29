import { auth } from '@clerk/nextjs'
import { redirect } from 'next/navigation'
import Dashboard from '@/components/Dashboard'

export default async function HomePage() {
  const { userId } = auth()

  if (!userId) {
    redirect('/sign-in')
  }

  return (
    <main className="min-h-screen">
      <Dashboard />
    </main>
  )
}

import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@clerk/nextjs'
import { sendSMS, SMSTemplates } from '@/lib/sms'
import connectDB from '@/lib/mongodb'
import UserProfile from '@/models/UserProfile'

// POST - Send SMS notification
export async function POST(request: NextRequest) {
  try {
    const { userId } = auth()

    if (!userId) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    const body = await request.json()
    const { type, data, customMessage } = body

    await connectDB()

    // Get user profile to check SMS preferences
    const profile = await UserProfile.findOne({ clerkId: userId })

    if (!profile) {
      return NextResponse.json(
        { error: 'User profile not found' },
        { status: 404 }
      )
    }

    if (!profile.preferences?.smsNotifications) {
      return NextResponse.json(
        { error: 'SMS notifications are disabled for this user' },
        { status: 403 }
      )
    }

    if (!profile.phone) {
      return NextResponse.json(
        { error: 'Phone number not configured' },
        { status: 400 }
      )
    }

    // Generate message based on type
    let message: string

    if (customMessage) {
      message = SMSTemplates.general(customMessage)
    } else {
      switch (type) {
        case 'cropReminder':
          message = SMSTemplates.cropReminder(data.cropName, data.daysUntilHarvest)
          break
        case 'weatherAlert':
          message = SMSTemplates.weatherAlert(data.type, data.severity)
          break
        case 'resourceLow':
          message = SMSTemplates.resourceLow(data.resourceName)
          break
        case 'diseaseDetection':
          message = SMSTemplates.diseaseDetection(data.cropName, data.diseaseName)
          break
        case 'marketPrice':
          message = SMSTemplates.marketPrice(data.cropName, data.price)
          break
        default:
          return NextResponse.json(
            { error: 'Invalid SMS type' },
            { status: 400 }
          )
      }
    }

    // Send SMS
    const result = await sendSMS({
      to: profile.phone,
      message,
    })

    return NextResponse.json({
      success: true,
      message: 'SMS sent successfully',
      data: result,
    })
  } catch (error: any) {
    console.error('Error sending SMS:', error)
    return NextResponse.json(
      { error: 'Failed to send SMS', details: error.message },
      { status: 500 }
    )
  }
}

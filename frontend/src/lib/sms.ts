import twilio from 'twilio'

const accountSid = process.env.TWILIO_ACCOUNT_SID
const authToken = process.env.TWILIO_AUTH_TOKEN
const twilioPhoneNumber = process.env.TWILIO_PHONE_NUMBER

if (!accountSid || !authToken || !twilioPhoneNumber) {
  console.warn('⚠️ Twilio credentials not configured. SMS features will be disabled.')
}

const client = accountSid && authToken ? twilio(accountSid, authToken) : null

export interface SMSOptions {
  to: string
  message: string
}

export async function sendSMS({ to, message }: SMSOptions) {
  if (!client || !twilioPhoneNumber) {
    console.error('❌ Twilio client not initialized')
    throw new Error('SMS service not configured')
  }

  try {
    // Format phone number (add +91 for India if not present)
    let formattedNumber = to.trim()
    if (!formattedNumber.startsWith('+')) {
      formattedNumber = `+91${formattedNumber.replace(/\D/g, '')}`
    }

    const result = await client.messages.create({
      body: message,
      from: twilioPhoneNumber,
      to: formattedNumber,
    })

    console.log('✅ SMS sent successfully:', result.sid)
    return {
      success: true,
      messageId: result.sid,
      status: result.status,
    }
  } catch (error: any) {
    console.error('❌ Error sending SMS:', error)
    throw new Error(`Failed to send SMS: ${error.message}`)
  }
}

export async function sendBulkSMS(recipients: { to: string; message: string }[]) {
  if (!client || !twilioPhoneNumber) {
    throw new Error('SMS service not configured')
  }

  const results = await Promise.allSettled(
    recipients.map((recipient) => sendSMS(recipient))
  )

  return results
}

// Predefined SMS templates
export const SMSTemplates = {
  cropReminder: (cropName: string, daysUntilHarvest: number) =>
    `🌾 FarmWise Alert: Your ${cropName} is ${daysUntilHarvest} days away from harvest. Prepare for harvesting!`,

  weatherAlert: (type: string, severity: string) =>
    `⚠️ FarmWise Weather Alert: ${type} warning (${severity}). Take necessary precautions for your crops.`,

  resourceLow: (resourceName: string) =>
    `📦 FarmWise Inventory: Your ${resourceName} stock is running low. Consider restocking soon.`,

  diseaseDetection: (cropName: string, diseaseName: string) =>
    `🔬 FarmWise Alert: ${diseaseName} detected in your ${cropName}. Check your dashboard for treatment recommendations.`,

  marketPrice: (cropName: string, price: number) =>
    `💰 FarmWise Market Update: ${cropName} current price is ₹${price}/quintal. Good time to sell!`,

  general: (message: string) =>
    `🌱 FarmWise: ${message}`,
}

export default { sendSMS, sendBulkSMS, SMSTemplates }

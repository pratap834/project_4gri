import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@clerk/nextjs'
import connectDB from '@/lib/mongodb'
import CropLog from '@/models/CropLog'

// GET - Fetch all crops for the user
export async function GET(request: NextRequest) {
  try {
    const { userId } = auth()

    if (!userId) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    const { searchParams } = new URL(request.url)
    const status = searchParams.get('status')
    const season = searchParams.get('season')
    const limit = parseInt(searchParams.get('limit') || '50')
    const skip = parseInt(searchParams.get('skip') || '0')

    await connectDB()

    const query: any = { clerkId: userId }
    
    if (status) query.status = status
    if (season) query.season = season

    const crops = await CropLog.find(query)
      .sort({ plantingDate: -1 })
      .limit(limit)
      .skip(skip)

    const total = await CropLog.countDocuments(query)

    return NextResponse.json({
      success: true,
      data: crops,
      pagination: {
        total,
        limit,
        skip,
        hasMore: skip + crops.length < total,
      },
    })
  } catch (error: any) {
    console.error('Error fetching crops:', error)
    return NextResponse.json(
      { error: 'Failed to fetch crops', details: error.message },
      { status: 500 }
    )
  }
}

// POST - Create a new crop log
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

    await connectDB()

    const crop = await CropLog.create({
      clerkId: userId,
      userId,
      ...body,
    })

    return NextResponse.json({
      success: true,
      message: 'Crop log created successfully',
      data: crop,
    }, { status: 201 })
  } catch (error: any) {
    console.error('Error creating crop log:', error)
    return NextResponse.json(
      { error: 'Failed to create crop log', details: error.message },
      { status: 500 }
    )
  }
}

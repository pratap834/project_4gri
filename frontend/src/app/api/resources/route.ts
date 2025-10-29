import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@clerk/nextjs'
import connectDB from '@/lib/mongodb'
import ResourceLog from '@/models/ResourceLog'

// GET - Fetch all resources for the user
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
    const resourceType = searchParams.get('resourceType')
    const cropReference = searchParams.get('cropReference')
    const startDate = searchParams.get('startDate')
    const endDate = searchParams.get('endDate')
    const limit = parseInt(searchParams.get('limit') || '50')
    const skip = parseInt(searchParams.get('skip') || '0')

    await connectDB()

    const query: any = { clerkId: userId }
    
    if (resourceType) query.resourceType = resourceType
    if (cropReference) query.cropReference = cropReference
    if (startDate || endDate) {
      query.transactionDate = {}
      if (startDate) query.transactionDate.$gte = new Date(startDate)
      if (endDate) query.transactionDate.$lte = new Date(endDate)
    }

    const resources = await ResourceLog.find(query)
      .sort({ transactionDate: -1 })
      .limit(limit)
      .skip(skip)
      .populate('cropReference', 'cropName plantingDate')

    const total = await ResourceLog.countDocuments(query)

    // Calculate summary statistics
    const summary = await ResourceLog.aggregate([
      { $match: query },
      {
        $group: {
          _id: '$resourceType',
          totalCost: { $sum: '$totalCost' },
          count: { $sum: 1 },
        },
      },
    ])

    return NextResponse.json({
      success: true,
      data: resources,
      summary,
      pagination: {
        total,
        limit,
        skip,
        hasMore: skip + resources.length < total,
      },
    })
  } catch (error: any) {
    console.error('Error fetching resources:', error)
    return NextResponse.json(
      { error: 'Failed to fetch resources', details: error.message },
      { status: 500 }
    )
  }
}

// POST - Create a new resource log
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

    const resource = await ResourceLog.create({
      clerkId: userId,
      userId,
      ...body,
    })

    return NextResponse.json({
      success: true,
      message: 'Resource log created successfully',
      data: resource,
    }, { status: 201 })
  } catch (error: any) {
    console.error('Error creating resource log:', error)
    return NextResponse.json(
      { error: 'Failed to create resource log', details: error.message },
      { status: 500 }
    )
  }
}

import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@clerk/nextjs'
import connectDB from '@/lib/mongodb'
import ResourceLog from '@/models/ResourceLog'

// GET - Fetch a specific resource
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { userId } = auth()

    if (!userId) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    await connectDB()

    const resource = await ResourceLog.findOne({
      _id: params.id,
      clerkId: userId,
    }).populate('cropReference', 'cropName plantingDate')

    if (!resource) {
      return NextResponse.json(
        { error: 'Resource not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      data: resource,
    })
  } catch (error: any) {
    console.error('Error fetching resource:', error)
    return NextResponse.json(
      { error: 'Failed to fetch resource', details: error.message },
      { status: 500 }
    )
  }
}

// PUT - Update a specific resource
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
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

    const resource = await ResourceLog.findOneAndUpdate(
      { _id: params.id, clerkId: userId },
      { $set: body },
      { new: true, runValidators: true }
    )

    if (!resource) {
      return NextResponse.json(
        { error: 'Resource not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      message: 'Resource updated successfully',
      data: resource,
    })
  } catch (error: any) {
    console.error('Error updating resource:', error)
    return NextResponse.json(
      { error: 'Failed to update resource', details: error.message },
      { status: 500 }
    )
  }
}

// DELETE - Delete a specific resource
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { userId } = auth()

    if (!userId) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    await connectDB()

    const resource = await ResourceLog.findOneAndDelete({
      _id: params.id,
      clerkId: userId,
    })

    if (!resource) {
      return NextResponse.json(
        { error: 'Resource not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      message: 'Resource deleted successfully',
    })
  } catch (error: any) {
    console.error('Error deleting resource:', error)
    return NextResponse.json(
      { error: 'Failed to delete resource', details: error.message },
      { status: 500 }
    )
  }
}

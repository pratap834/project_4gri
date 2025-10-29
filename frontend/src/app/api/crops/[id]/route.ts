import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@clerk/nextjs'
import connectDB from '@/lib/mongodb'
import CropLog from '@/models/CropLog'

// GET - Fetch a specific crop
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

    const crop = await CropLog.findOne({
      _id: params.id,
      clerkId: userId,
    })

    if (!crop) {
      return NextResponse.json(
        { error: 'Crop not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      data: crop,
    })
  } catch (error: any) {
    console.error('Error fetching crop:', error)
    return NextResponse.json(
      { error: 'Failed to fetch crop', details: error.message },
      { status: 500 }
    )
  }
}

// PUT - Update a specific crop
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

    const crop = await CropLog.findOneAndUpdate(
      { _id: params.id, clerkId: userId },
      { $set: body },
      { new: true, runValidators: true }
    )

    if (!crop) {
      return NextResponse.json(
        { error: 'Crop not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      message: 'Crop updated successfully',
      data: crop,
    })
  } catch (error: any) {
    console.error('Error updating crop:', error)
    return NextResponse.json(
      { error: 'Failed to update crop', details: error.message },
      { status: 500 }
    )
  }
}

// DELETE - Delete a specific crop
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

    const crop = await CropLog.findOneAndDelete({
      _id: params.id,
      clerkId: userId,
    })

    if (!crop) {
      return NextResponse.json(
        { error: 'Crop not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      message: 'Crop deleted successfully',
    })
  } catch (error: any) {
    console.error('Error deleting crop:', error)
    return NextResponse.json(
      { error: 'Failed to delete crop', details: error.message },
      { status: 500 }
    )
  }
}

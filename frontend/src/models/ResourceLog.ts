import mongoose, { Schema, Document, Model } from 'mongoose'

export interface IResourceLog extends Document {
  userId: string
  clerkId: string
  resourceType: 'Seed' | 'Fertilizer' | 'Pesticide' | 'Equipment' | 'Labor' | 'Water' | 'Fuel' | 'Other'
  resourceName: string
  category?: string
  quantity: number
  unit: string
  costPerUnit: number
  totalCost: number
  currency: string
  transactionDate: Date
  supplier?: {
    name?: string
    contact?: string
    address?: string
  }
  cropReference?: string // Reference to CropLog ID
  purpose?: string
  notes?: string
  invoice?: {
    number?: string
    imageUrl?: string
  }
  paymentStatus: 'Paid' | 'Pending' | 'Partial'
  createdAt: Date
  updatedAt: Date
}

const ResourceLogSchema: Schema = new Schema(
  {
    userId: {
      type: String,
      required: true,
      index: true,
    },
    clerkId: {
      type: String,
      required: true,
      index: true,
    },
    resourceType: {
      type: String,
      required: true,
      enum: ['Seed', 'Fertilizer', 'Pesticide', 'Equipment', 'Labor', 'Water', 'Fuel', 'Other'],
    },
    resourceName: {
      type: String,
      required: true,
      trim: true,
    },
    category: {
      type: String,
      trim: true,
    },
    quantity: {
      type: Number,
      required: true,
      min: 0,
    },
    unit: {
      type: String,
      required: true,
      trim: true,
    },
    costPerUnit: {
      type: Number,
      required: true,
      min: 0,
    },
    totalCost: {
      type: Number,
      required: true,
      min: 0,
    },
    currency: {
      type: String,
      required: true,
      default: 'INR',
      uppercase: true,
    },
    transactionDate: {
      type: Date,
      required: true,
      index: true,
    },
    supplier: {
      name: { type: String, trim: true },
      contact: { type: String, trim: true },
      address: { type: String, trim: true },
    },
    cropReference: {
      type: Schema.Types.ObjectId,
      ref: 'CropLog',
    },
    purpose: {
      type: String,
      trim: true,
      maxlength: 500,
    },
    notes: {
      type: String,
      maxlength: 1000,
    },
    invoice: {
      number: { type: String, trim: true },
      imageUrl: { type: String, trim: true },
    },
    paymentStatus: {
      type: String,
      required: true,
      enum: ['Paid', 'Pending', 'Partial'],
      default: 'Paid',
    },
  },
  {
    timestamps: true,
  }
)

// Indexes for better query performance
ResourceLogSchema.index({ userId: 1, transactionDate: -1 })
ResourceLogSchema.index({ clerkId: 1, resourceType: 1 })
ResourceLogSchema.index({ resourceType: 1, transactionDate: -1 })
ResourceLogSchema.index({ cropReference: 1 })

// Calculate total cost before saving
ResourceLogSchema.pre<IResourceLog>('save', function (next) {
  this.totalCost = this.quantity * this.costPerUnit
  next()
})

const ResourceLog: Model<IResourceLog> =
  mongoose.models.ResourceLog || mongoose.model<IResourceLog>('ResourceLog', ResourceLogSchema)

export default ResourceLog

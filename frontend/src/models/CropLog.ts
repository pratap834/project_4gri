import mongoose, { Schema, Document, Model } from 'mongoose'

export interface ICropLog extends Document {
  userId: string
  clerkId: string
  cropName: string
  cropType: 'Cereal' | 'Pulse' | 'Vegetable' | 'Fruit' | 'Cash Crop' | 'Other'
  variety?: string
  plantingDate: Date
  expectedHarvestDate: Date
  actualHarvestDate?: Date
  area: number
  areaUnit: 'acre' | 'hectare' | 'bigha'
  status: 'Planned' | 'Planted' | 'Growing' | 'Harvested' | 'Failed'
  season: 'Kharif' | 'Rabi' | 'Zaid' | 'Perennial'
  yieldExpected?: number
  yieldActual?: number
  yieldUnit: 'kg' | 'quintal' | 'ton'
  location?: {
    fieldName?: string
    coordinates?: {
      latitude: number
      longitude: number
    }
  }
  soilData?: {
    nitrogen: number
    phosphorus: number
    potassium: number
    pH: number
  }
  weatherData?: {
    avgTemperature?: number
    avgRainfall?: number
    avgHumidity?: number
  }
  notes?: string
  images?: string[]
  createdAt: Date
  updatedAt: Date
}

const CropLogSchema: Schema = new Schema(
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
    cropName: {
      type: String,
      required: true,
      trim: true,
    },
    cropType: {
      type: String,
      required: true,
      enum: ['Cereal', 'Pulse', 'Vegetable', 'Fruit', 'Cash Crop', 'Other'],
    },
    variety: {
      type: String,
      trim: true,
    },
    plantingDate: {
      type: Date,
      required: true,
    },
    expectedHarvestDate: {
      type: Date,
      required: true,
    },
    actualHarvestDate: {
      type: Date,
    },
    area: {
      type: Number,
      required: true,
      min: 0,
    },
    areaUnit: {
      type: String,
      required: true,
      enum: ['acre', 'hectare', 'bigha'],
      default: 'acre',
    },
    status: {
      type: String,
      required: true,
      enum: ['Planned', 'Planted', 'Growing', 'Harvested', 'Failed'],
      default: 'Planned',
    },
    season: {
      type: String,
      required: true,
      enum: ['Kharif', 'Rabi', 'Zaid', 'Perennial'],
    },
    yieldExpected: {
      type: Number,
      min: 0,
    },
    yieldActual: {
      type: Number,
      min: 0,
    },
    yieldUnit: {
      type: String,
      enum: ['kg', 'quintal', 'ton'],
      default: 'quintal',
    },
    location: {
      fieldName: { type: String, trim: true },
      coordinates: {
        latitude: { type: Number },
        longitude: { type: Number },
      },
    },
    soilData: {
      nitrogen: { type: Number, min: 0 },
      phosphorus: { type: Number, min: 0 },
      potassium: { type: Number, min: 0 },
      pH: { type: Number, min: 0, max: 14 },
    },
    weatherData: {
      avgTemperature: { type: Number },
      avgRainfall: { type: Number, min: 0 },
      avgHumidity: { type: Number, min: 0, max: 100 },
    },
    notes: {
      type: String,
      maxlength: 1000,
    },
    images: {
      type: [String],
    },
  },
  {
    timestamps: true,
  }
)

// Indexes for better query performance
CropLogSchema.index({ userId: 1, plantingDate: -1 })
CropLogSchema.index({ clerkId: 1, status: 1 })
CropLogSchema.index({ cropName: 1 })
CropLogSchema.index({ season: 1 })

const CropLog: Model<ICropLog> =
  mongoose.models.CropLog || mongoose.model<ICropLog>('CropLog', CropLogSchema)

export default CropLog

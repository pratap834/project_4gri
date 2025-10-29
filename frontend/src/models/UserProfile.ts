import mongoose, { Schema, Document, Model } from 'mongoose'

export interface IUserProfile extends Document {
  clerkId: string
  email: string
  name: string
  phone?: string
  address?: {
    street?: string
    city?: string
    state?: string
    pincode?: string
    country?: string
  }
  farmDetails?: {
    farmName?: string
    totalArea?: number
    areaUnit?: 'acre' | 'hectare' | 'bigha'
    soilType?: string
    irrigationType?: string[]
  }
  preferences?: {
    smsNotifications: boolean
    emailNotifications: boolean
    language: string
    timezone: string
  }
  createdAt: Date
  updatedAt: Date
}

const UserProfileSchema: Schema = new Schema(
  {
    clerkId: {
      type: String,
      required: true,
      unique: true,
      index: true,
    },
    email: {
      type: String,
      required: true,
      lowercase: true,
      trim: true,
    },
    name: {
      type: String,
      required: true,
      trim: true,
    },
    phone: {
      type: String,
      trim: true,
      validate: {
        validator: function (v: string) {
          return !v || /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im.test(v)
        },
        message: (props: any) => `${props.value} is not a valid phone number!`,
      },
    },
    address: {
      street: { type: String, trim: true },
      city: { type: String, trim: true },
      state: { type: String, trim: true },
      pincode: { type: String, trim: true },
      country: { type: String, trim: true, default: 'India' },
    },
    farmDetails: {
      farmName: { type: String, trim: true },
      totalArea: { type: Number, min: 0 },
      areaUnit: {
        type: String,
        enum: ['acre', 'hectare', 'bigha'],
        default: 'acre',
      },
      soilType: {
        type: String,
        enum: ['Alluvial', 'Black', 'Red', 'Laterite', 'Desert', 'Mountain', 'Clay', 'Sandy', 'Loamy', 'Other'],
      },
      irrigationType: {
        type: [String],
        enum: ['Drip', 'Sprinkler', 'Flood', 'Rain-fed', 'Canal', 'Tube-well', 'Other'],
      },
    },
    preferences: {
      smsNotifications: { type: Boolean, default: true },
      emailNotifications: { type: Boolean, default: true },
      language: { type: String, default: 'en' },
      timezone: { type: String, default: 'Asia/Kolkata' },
    },
  },
  {
    timestamps: true,
  }
)

// Indexes for better query performance
UserProfileSchema.index({ email: 1 })
UserProfileSchema.index({ phone: 1 })

const UserProfile: Model<IUserProfile> =
  mongoose.models.UserProfile || mongoose.model<IUserProfile>('UserProfile', UserProfileSchema)

export default UserProfile

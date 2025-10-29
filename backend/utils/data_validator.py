#!/usr/bin/env python3
"""
Agricultural AI Dashboard - Data Validation & Preprocessing
==========================================================
Clean and validate all datasets for training
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class DataValidator:
    def __init__(self):
        self.data_dir = Path("extracted_datasets")
        self.output_dir = Path("cleaned_datasets")
        self.output_dir.mkdir(exist_ok=True)
        
    def validate_crop_recommendation_data(self):
        """Clean and validate crop recommendation dataset"""
        print("🌾 Validating Crop Recommendation Dataset...")
        
        # Load data
        df = pd.read_csv(self.data_dir / "Crop_recommendation.csv")
        print(f"   Original shape: {df.shape}")
        
        # Check for missing values
        missing = df.isnull().sum()
        print(f"   Missing values: {missing.sum()}")
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Check for outliers (using IQR method)
        numeric_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower) & (df[col] <= upper)]
        
        # Standardize crop names
        df['label'] = df['label'].str.strip().str.title()
        
        # Only keep crops with sufficient samples (>= 50)
        crop_counts = df['label'].value_counts()
        valid_crops = crop_counts[crop_counts >= 50].index
        df = df[df['label'].isin(valid_crops)]
        
        print(f"   After cleaning: {df.shape}")
        print(f"   Unique crops: {df['label'].nunique()}")
        print(f"   Crops: {sorted(df['label'].unique())}")
        
        # Save cleaned data
        df.to_csv(self.output_dir / "crop_recommendation_clean.csv", index=False)
        return df
    
    def validate_fertilizer_data(self):
        """Clean and validate fertilizer recommendation dataset"""
        print("🧪 Validating Fertilizer Recommendation Dataset...")
        
        # Load data
        df = pd.read_csv(self.data_dir / "Crop and fertilizer dataset.csv")
        print(f"   Original shape: {df.shape}")
        
        # Check for missing values
        missing = df.isnull().sum()
        print(f"   Missing values: {missing.sum()}")
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Standardize crop and fertilizer names
        df['Crop'] = df['Crop'].str.strip().str.title()
        df['Fertilizer'] = df['Fertilizer'].str.strip().str.title()
        
        # Remove outliers for numeric columns
        numeric_cols = ['Nitrogen', 'Phosphorus', 'Potassium']
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower) & (df[col] <= upper)]
        
        # Only keep crops and fertilizers with sufficient samples
        crop_counts = df['Crop'].value_counts()
        valid_crops = crop_counts[crop_counts >= 20].index
        df = df[df['Crop'].isin(valid_crops)]
        
        print(f"   After cleaning: {df.shape}")
        print(f"   Unique crops: {df['Crop'].nunique()}")
        print(f"   Unique fertilizers: {df['Fertilizer'].nunique()}")
        
        # Save cleaned data
        df.to_csv(self.output_dir / "fertilizer_recommendation_clean.csv", index=False)
        return df
    
    def validate_crop_yield_data(self):
        """Clean and validate crop yield dataset"""
        print("📊 Validating Crop Yield Dataset...")
        
        # Load data
        df = pd.read_csv(self.data_dir / "crop_yield.csv")
        print(f"   Original shape: {df.shape}")
        
        # Check for missing values
        missing = df.isnull().sum()
        print(f"   Missing values: {missing.sum()}")
        
        # Remove rows with missing critical values
        df = df.dropna(subset=['Crop', 'State', 'Area', 'Production', 'Yield'])
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Standardize names
        df['Crop'] = df['Crop'].str.strip().str.title()
        df['State'] = df['State'].str.strip().str.title()
        df['Season'] = df['Season'].str.strip().str.title()
        
        # Remove outliers
        numeric_cols = ['Area', 'Production', 'Annual_Rainfall', 'Fertilizer', 'Pesticide', 'Yield']
        for col in numeric_cols:
            Q1 = df[col].quantile(0.05)  # More lenient for agricultural data
            Q3 = df[col].quantile(0.95)
            df = df[(df[col] >= Q1) & (df[col] <= Q3)]
        
        # Only keep crops with sufficient samples (>= 100)
        crop_counts = df['Crop'].value_counts()
        valid_crops = crop_counts[crop_counts >= 100].index
        df = df[df['Crop'].isin(valid_crops)]
        
        # Only keep states with sufficient data
        state_counts = df['State'].value_counts()
        valid_states = state_counts[state_counts >= 50].index
        df = df[df['State'].isin(valid_states)]
        
        print(f"   After cleaning: {df.shape}")
        print(f"   Unique crops: {df['Crop'].nunique()}")
        print(f"   Unique states: {df['State'].nunique()}")
        
        # Save cleaned data
        df.to_csv(self.output_dir / "crop_yield_clean.csv", index=False)
        return df
    
    def validate_disease_data(self):
        """Validate plant disease dataset structure"""
        print("🔬 Validating Plant Disease Dataset...")
        
        disease_dir = Path("extracted_datasets/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)")
        
        if not disease_dir.exists():
            print("   ❌ Disease dataset not found")
            return None
        
        # Count training and validation images
        train_dir = disease_dir / "train"
        valid_dir = disease_dir / "valid"
        
        if not train_dir.exists() or not valid_dir.exists():
            print("   ❌ Train/Valid directories not found")
            return None
        
        # Count classes and images
        train_classes = list(train_dir.iterdir())
        valid_classes = list(valid_dir.iterdir())
        
        train_counts = {}
        valid_counts = {}
        
        for class_dir in train_classes:
            if class_dir.is_dir():
                count = len(list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png")))
                train_counts[class_dir.name] = count
        
        for class_dir in valid_classes:
            if class_dir.is_dir():
                count = len(list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png")))
                valid_counts[class_dir.name] = count
        
        # Filter classes with sufficient data (>= 1000 training images)
        valid_classes_names = [cls for cls, count in train_counts.items() if count >= 1000]
        
        total_train = sum(train_counts.values())
        total_valid = sum(valid_counts.values())
        
        print(f"   Training images: {total_train:,}")
        print(f"   Validation images: {total_valid:,}")
        print(f"   Total classes: {len(train_counts)}")
        print(f"   Valid classes (>=1000 samples): {len(valid_classes_names)}")
        
        # Save class information
        class_info = {
            'valid_classes': valid_classes_names,
            'train_counts': train_counts,
            'valid_counts': valid_counts,
            'total_train': total_train,
            'total_valid': total_valid
        }
        
        import json
        with open(self.output_dir / "disease_classes_info.json", 'w') as f:
            json.dump(class_info, f, indent=2)
        
        return class_info
    
    def generate_summary_report(self):
        """Generate comprehensive validation report"""
        print("\n" + "="*60)
        print("📋 DATASET VALIDATION SUMMARY")
        print("="*60)
        
        # Validate all datasets
        crop_df = self.validate_crop_recommendation_data()
        fertilizer_df = self.validate_fertilizer_data()
        yield_df = self.validate_crop_yield_data()
        disease_info = self.validate_disease_data()
        
        print(f"\n✅ All datasets validated and cleaned!")
        print(f"📁 Cleaned datasets saved to: {self.output_dir}")
        
        # Create summary
        summary = {
            'crop_recommendation': {
                'shape': crop_df.shape,
                'unique_crops': crop_df['label'].nunique(),
                'crops': sorted(crop_df['label'].unique())
            },
            'fertilizer_recommendation': {
                'shape': fertilizer_df.shape,
                'unique_crops': fertilizer_df['Crop'].nunique(),
                'unique_fertilizers': fertilizer_df['Fertilizer'].nunique()
            },
            'crop_yield': {
                'shape': yield_df.shape,
                'unique_crops': yield_df['Crop'].nunique(),
                'unique_states': yield_df['State'].nunique()
            },
            'disease_detection': disease_info if disease_info else {}
        }
        
        # Save summary
        import json
        with open(self.output_dir / "validation_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        return summary

if __name__ == "__main__":
    validator = DataValidator()
    summary = validator.generate_summary_report()
    print(f"\n🎉 Data validation complete!")
"""
Gemini AI Service for generating prediction analysis, suggestions, and reports
Integrates with MongoDB to fetch prediction history and generate contextual insights
"""
import os
import google.generativeai as genai
from typing import List, Dict, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
else:
    model = None
    print("⚠ Warning: GEMINI_API_KEY not found in environment variables")


def generate_crop_notification(current_prediction: Dict, previous_predictions: List[Dict]) -> str:
    """
    Generate a brief notification message for crop recommendation
    """
    if not model:
        return "Crop recommendation completed. Enable Gemini API for intelligent insights."
    
    try:
        # Prepare context
        current_crop = current_prediction['result']['recommended_crop']
        current_conditions = current_prediction['input']
        
        history_summary = ""
        if previous_predictions and len(previous_predictions) > 0:
            prev_crop = previous_predictions[0]['result']['recommended_crop']
            history_summary = f"Previous recommendation: {prev_crop}. "
        
        prompt = f"""You are an agricultural AI assistant. Generate a brief, friendly notification message (max 2 sentences) for a farmer.

Current Recommendation: {current_crop}
Soil NPK: N={current_conditions['N']}, P={current_conditions['P']}, K={current_conditions['K']}
pH: {current_conditions['ph']}, Temperature: {current_conditions['temperature']}°C
{history_summary}

Create a short, actionable notification that highlights the key insight. Be encouraging and professional."""

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating crop notification: {e}")
        return f"✓ Crop recommendation: {current_crop}. Detailed analysis available."


def generate_fertilizer_notification(current_prediction: Dict, previous_predictions: List[Dict]) -> str:
    """
    Generate a brief notification message for fertilizer recommendation with temporal analysis
    """
    if not model:
        return "Fertilizer recommendation completed. Enable Gemini API for intelligent insights."
    
    try:
        # Prepare context
        current_fertilizer = current_prediction['result']['recommended_fertilizer']
        current_input = current_prediction['input']
        npk = current_prediction['result']['npk_values']
        current_date = current_prediction.get('prediction_date', 'today')
        timeframe = current_prediction.get('timeframe', 'Not specified')
        
        history_context = ""
        if previous_predictions and len(previous_predictions) > 0:
            prev_pred = previous_predictions[0]
            prev_npk = prev_pred['result']['npk_values']
            prev_date = prev_pred.get('prediction_date', 'previously')
            
            # Calculate NPK changes
            n_change = npk['nitrogen'] - prev_npk['nitrogen']
            p_change = npk['phosphorous'] - prev_npk['phosphorous']
            k_change = npk['potassium'] - prev_npk['potassium']
            
            history_context = f"""Previous Test ({prev_date}): N={prev_npk['nitrogen']}, P={prev_npk['phosphorous']}, K={prev_npk['potassium']}
Changes: N{'+' if n_change >= 0 else ''}{n_change:.1f}, P{'+' if p_change >= 0 else ''}{p_change:.1f}, K{'+' if k_change >= 0 else ''}{k_change:.1f}. """
        
        prompt = f"""You are an agricultural AI assistant. Generate a brief notification (max 2-3 sentences) for a farmer about fertilizer recommendation.

Test Date: {current_date}
Expected Results Timeframe: {timeframe}
Recommended Fertilizer: {current_fertilizer}
Current NPK Levels: N={npk['nitrogen']}, P={npk['phosphorous']}, K={npk['potassium']}
Soil Type: {current_input['soil_type']}, Crop: {current_input['crop_type']}
{history_context}

Task: Explain what happened to the soil since the last test (if available). Mention if NPK levels improved, declined, or stayed stable. Provide brief guidance.

Create a short, actionable notification. Be professional and encouraging."""

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating fertilizer notification: {e}")
        return f"✓ Fertilizer recommendation: {current_fertilizer}. Detailed analysis available."


def generate_yield_notification(current_prediction: Dict, previous_predictions: List[Dict]) -> str:
    """
    Generate a brief notification message for yield prediction with temporal trends
    """
    if not model:
        return "Yield prediction completed. Enable Gemini API for intelligent insights."
    
    try:
        # Prepare context
        predicted_yield = current_prediction['result']['predicted_yield']
        current_input = current_prediction['input']
        current_date = current_prediction.get('prediction_date', 'today')
        timeframe = current_prediction.get('timeframe', 'Not specified')
        
        history_context = ""
        if previous_predictions and len(previous_predictions) > 0:
            prev_pred = previous_predictions[0]
            prev_yield = prev_pred['result']['predicted_yield']
            prev_date = prev_pred.get('prediction_date', 'previously')
            yield_change = predicted_yield - prev_yield
            yield_change_pct = (yield_change / prev_yield * 100) if prev_yield > 0 else 0
            
            history_context = f"""Previous Prediction ({prev_date}): {prev_yield} t/ha
Change: {'+' if yield_change >= 0 else ''}{yield_change:.2f} t/ha ({'+' if yield_change_pct >= 0 else ''}{yield_change_pct:.1f}%). """
        
        prompt = f"""You are an agricultural AI assistant. Generate a brief notification (max 2-3 sentences) for a farmer about yield prediction.

Prediction Date: {current_date}
Expected Harvest Timeframe: {timeframe}
Predicted Yield: {predicted_yield} tonnes/hectare
Crop: {current_input['crop']}, Season: {current_input['season']}, State: {current_input['state']}
{history_context}

Task: Analyze the yield trend. If it's improving, congratulate and explain why. If declining, provide brief guidance. Mention the timeframe.

Create a short, actionable notification. Be professional and encouraging."""

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating yield notification: {e}")
        return f"✓ Predicted yield: {predicted_yield} t/ha. Detailed analysis available."


def generate_crop_detailed_report(current_prediction: Dict, previous_predictions: List[Dict]) -> Dict:
    """
    Generate a comprehensive report for crop recommendation with historical analysis
    """
    if not model:
        return {
            "success": False,
            "message": "Gemini API not configured. Please set GEMINI_API_KEY.",
            "report": None
        }
    
    try:
        current_crop = current_prediction['result']['recommended_crop']
        current_conditions = current_prediction['input']
        confidence = current_prediction['result'].get('confidence', 0)
        
        # Build history context
        history_text = ""
        if previous_predictions and len(previous_predictions) > 0:
            history_text = "\n\nPREVIOUS PREDICTIONS:\n"
            for i, pred in enumerate(previous_predictions[:5], 1):
                timestamp = pred.get('timestamp', 'Unknown')
                prev_crop = pred['result']['recommended_crop']
                prev_input = pred['input']
                history_text += f"\n{i}. Date: {timestamp}\n"
                history_text += f"   Crop: {prev_crop}\n"
                history_text += f"   NPK: N={prev_input['N']}, P={prev_input['P']}, K={prev_input['K']}\n"
                history_text += f"   pH: {prev_input['ph']}, Temp: {prev_input['temperature']}°C\n"
        
        prompt = f"""You are an expert agricultural consultant AI. Generate a comprehensive, professional report for a farmer about their crop recommendation.

CURRENT RECOMMENDATION:
- Recommended Crop: {current_crop}
- Confidence: {confidence}%
- Soil NPK Values: N={current_conditions['N']}, P={current_conditions['P']}, K={current_conditions['K']}
- pH Level: {current_conditions['ph']}
- Temperature: {current_conditions['temperature']}°C
- Humidity: {current_conditions['humidity']}%
- Rainfall: {current_conditions['rainfall']}mm
{history_text}

Generate a detailed report with the following sections:

1. EXECUTIVE SUMMARY (2-3 sentences)
2. SOIL HEALTH ANALYSIS
   - Compare current NPK levels with previous predictions (if available)
   - Analyze pH trends and soil condition improvements/deteriorations
3. CROP RECOMMENDATION RATIONALE
   - Why this specific crop is recommended
   - Expected benefits and considerations
4. COMPARISON WITH PREVIOUS RECOMMENDATIONS
   - Changes from past recommendations
   - Progress in soil conditions
5. ACTIONABLE STEPS
   - List 4-5 specific, practical steps the farmer should take
6. PROFESSIONAL ADVICE
   - Best practices for the recommended crop
   - Risk mitigation strategies
   - Expected timeline

Format the report in a professional, farmer-friendly manner. Use bullet points and clear sections."""

        response = model.generate_content(prompt)
        report_text = response.text.strip()
        
        return {
            "success": True,
            "report_type": "crop_recommendation",
            "generated_at": datetime.utcnow().isoformat(),
            "prediction_summary": {
                "recommended_crop": current_crop,
                "confidence": confidence,
                "soil_conditions": current_conditions
            },
            "detailed_report": report_text,
            "history_count": len(previous_predictions) if previous_predictions else 0
        }
    
    except Exception as e:
        print(f"Error generating crop detailed report: {e}")
        return {
            "success": False,
            "message": f"Error generating report: {str(e)}",
            "report": None
        }


def generate_fertilizer_detailed_report(current_prediction: Dict, previous_predictions: List[Dict]) -> Dict:
    """
    Generate a comprehensive report for fertilizer recommendation with soil improvement analysis
    """
    if not model:
        return {
            "success": False,
            "message": "Gemini API not configured. Please set GEMINI_API_KEY.",
            "report": None
        }
    
    try:
        current_fertilizer = current_prediction['result']['recommended_fertilizer']
        current_input = current_prediction['input']
        npk = current_prediction['result']['npk_values']
        confidence = current_prediction['result'].get('confidence', 0)
        current_date = current_prediction.get('prediction_date', 'Current date')
        timeframe = current_prediction.get('timeframe', 'Not specified')
        
        # Build history context for soil improvement analysis
        history_text = ""
        soil_changes = ""
        time_between_tests = ""
        if previous_predictions and len(previous_predictions) > 0:
            history_text = "\n\nPREVIOUS FERTILIZER APPLICATIONS:\n"
            for i, pred in enumerate(previous_predictions[:5], 1):
                pred_date = pred.get('prediction_date', pred.get('timestamp', 'Unknown'))
                pred_timeframe = pred.get('timeframe', 'N/A')
                prev_fert = pred['result']['recommended_fertilizer']
                prev_npk = pred['result']['npk_values']
                history_text += f"\n{i}. Test Date: {pred_date} (Timeframe: {pred_timeframe})\n"
                history_text += f"   Fertilizer: {prev_fert}\n"
                history_text += f"   NPK: N={prev_npk['nitrogen']}, P={prev_npk['phosphorous']}, K={prev_npk['potassium']}\n"
            
            # Calculate NPK changes
            prev_npk = previous_predictions[0]['result']['npk_values']
            prev_date = previous_predictions[0].get('prediction_date', 'Previous test')
            n_change = npk['nitrogen'] - prev_npk['nitrogen']
            p_change = npk['phosphorous'] - prev_npk['phosphorous']
            k_change = npk['potassium'] - prev_npk['potassium']
            
            time_between_tests = f"\nTime Between Tests: {prev_date} to {current_date}"
            soil_changes = f"\n\nSOIL NUTRIENT CHANGES (Since {prev_date}):\n"
            soil_changes += f"- Nitrogen: {'+' if n_change > 0 else ''}{n_change:.2f} ({'improved' if n_change > 0 else 'depleted' if n_change < 0 else 'stable'})\n"
            soil_changes += f"- Phosphorous: {'+' if p_change > 0 else ''}{p_change:.2f} ({'improved' if p_change > 0 else 'depleted' if p_change < 0 else 'stable'})\n"
            soil_changes += f"- Potassium: {'+' if k_change > 0 else ''}{k_change:.2f} ({'improved' if k_change > 0 else 'depleted' if k_change < 0 else 'stable'})\n"
        
        prompt = f"""You are an expert soil scientist and agricultural consultant. Generate a comprehensive report about fertilizer recommendation and soil health.

CURRENT RECOMMENDATION:
- Test Date: {current_date}
- Expected Results Timeframe: {timeframe}
- Recommended Fertilizer: {current_fertilizer}
- Confidence: {confidence}%
- Current NPK Levels: N={npk['nitrogen']}, P={npk['phosphorous']}, K={npk['potassium']}
- Soil Type: {current_input['soil_type']}
- Crop Type: {current_input['crop_type']}
- Temperature: {current_input['temperature']}°C
- Humidity: {current_input['humidity']}%
- Moisture: {current_input['moisture']}%
{time_between_tests}
{soil_changes}
{history_text}

Generate a detailed report with the following sections:

1. EXECUTIVE SUMMARY (2-3 sentences)
2. SOIL HEALTH ASSESSMENT
   - Current NPK status and what it means
   - Soil type characteristics and their impact
3. WHAT HAPPENED TO THE SOIL SINCE LAST APPLICATION
   - Analyze nutrient changes from previous prediction
   - Identify improvements or depletions
   - Explain causes of changes
4. CURRENT SOIL IMPROVEMENT ANALYSIS
   - How the soil has improved or changed
   - Impact of previous fertilizer applications
   - Current soil fertility status
5. FERTILIZER RECOMMENDATION RATIONALE
   - Why this specific fertilizer is recommended
   - Expected benefits and outcomes
6. APPLICATION GUIDELINES
   - Timing and dosage recommendations
   - Application method
   - Precautions
7. ACTIONABLE STEPS
   - 4-5 specific steps for the farmer
8. PROFESSIONAL ADVICE
   - Best practices for soil management
   - Long-term soil health strategies

Format professionally with clear sections and bullet points."""

        response = model.generate_content(prompt)
        report_text = response.text.strip()
        
        return {
            "success": True,
            "report_type": "fertilizer_recommendation",
            "generated_at": datetime.utcnow().isoformat(),
            "prediction_summary": {
                "recommended_fertilizer": current_fertilizer,
                "confidence": confidence,
                "npk_values": npk,
                "soil_type": current_input['soil_type'],
                "crop_type": current_input['crop_type']
            },
            "detailed_report": report_text,
            "history_count": len(previous_predictions) if previous_predictions else 0
        }
    
    except Exception as e:
        print(f"Error generating fertilizer detailed report: {e}")
        return {
            "success": False,
            "message": f"Error generating report: {str(e)}",
            "report": None
        }


def generate_yield_detailed_report(current_prediction: Dict, previous_predictions: List[Dict]) -> Dict:
    """
    Generate a comprehensive report for yield prediction with historical comparison
    """
    if not model:
        return {
            "success": False,
            "message": "Gemini API not configured. Please set GEMINI_API_KEY.",
            "report": None
        }
    
    try:
        predicted_yield = current_prediction['result']['predicted_yield']
        current_input = current_prediction['input']
        current_date = current_prediction.get('prediction_date', 'Current date')
        timeframe = current_prediction.get('timeframe', 'Not specified')
        
        # Build history context
        history_text = ""
        yield_trend = ""
        time_analysis = ""
        if previous_predictions and len(previous_predictions) > 0:
            history_text = "\n\nPREVIOUS YIELD PREDICTIONS:\n"
            for i, pred in enumerate(previous_predictions[:5], 1):
                pred_date = pred.get('prediction_date', pred.get('timestamp', 'Unknown'))
                pred_timeframe = pred.get('timeframe', 'N/A')
                prev_yield = pred['result']['predicted_yield']
                prev_input = pred['input']
                history_text += f"\n{i}. Prediction Date: {pred_date} (Harvest Timeframe: {pred_timeframe})\n"
                history_text += f"   Predicted Yield: {prev_yield} t/ha\n"
                history_text += f"   Crop: {prev_input['crop']}, Season: {prev_input['season']}\n"
                history_text += f"   Fertilizer: {prev_input['fertilizer']} kg/ha, Pesticide: {prev_input['pesticide']} kg/ha\n"
            
            # Calculate yield change
            prev_pred = previous_predictions[0]
            prev_yield = prev_pred['result']['predicted_yield']
            prev_date = prev_pred.get('prediction_date', 'Previous prediction')
            yield_change = predicted_yield - prev_yield
            yield_change_pct = (yield_change / prev_yield * 100) if prev_yield > 0 else 0
            
            time_analysis = f"\nTime Between Predictions: {prev_date} to {current_date}"
            yield_trend = f"\n\nYIELD TREND ANALYSIS:\n"
            yield_trend += f"- Previous Prediction ({prev_date}): {prev_yield} t/ha\n"
            yield_trend += f"- Current Prediction ({current_date}): {predicted_yield} t/ha\n"
            yield_trend += f"- Change: {'+' if yield_change > 0 else ''}{yield_change:.2f} t/ha ({'+' if yield_change_pct > 0 else ''}{yield_change_pct:.1f}%)\n"
            yield_trend += f"- Trend: {'Improving ✓' if yield_change > 0 else 'Declining ⚠' if yield_change < 0 else 'Stable →'}\n"
        
        prompt = f"""You are an expert agricultural economist and crop yield specialist. Generate a comprehensive yield prediction report.

CURRENT PREDICTION:
- Prediction Date: {current_date}
- Expected Harvest Timeframe: {timeframe}
- Predicted Yield: {predicted_yield} tonnes per hectare
- Crop: {current_input['crop']}
- Season: {current_input['season']}
- State: {current_input['state']}
- Cultivation Area: {current_input['area']} hectares
- Annual Rainfall: {current_input['annual_rainfall']} mm
- Fertilizer Usage: {current_input['fertilizer']} kg/ha
- Pesticide Usage: {current_input['pesticide']} kg/ha
{time_analysis}
{yield_trend}
{history_text}

Generate a detailed report with the following sections:

1. EXECUTIVE SUMMARY (2-3 sentences)
2. YIELD PREDICTION ANALYSIS
   - What the predicted yield means
   - Comparison with typical yields for this crop
3. COMPARISON WITH PREVIOUS PREDICTIONS
   - How yield has changed from previous predictions
   - Factors contributing to improvement or decline
   - Impact of input changes (fertilizer, pesticide)
4. FACTORS INFLUENCING YIELD
   - Rainfall impact
   - Fertilizer effectiveness
   - Regional considerations
5. OPTIMIZATION OPPORTUNITIES
   - How to potentially improve yield
   - Input adjustment recommendations
6. ACTIONABLE STEPS
   - 4-5 specific steps to achieve or exceed predicted yield
7. PROFESSIONAL ADVICE
   - Best practices for yield maximization
   - Risk management strategies
   - Market considerations
8. FINANCIAL PROJECTION
   - Expected production volume
   - Considerations for planning

Format professionally with clear sections and actionable insights."""

        response = model.generate_content(prompt)
        report_text = response.text.strip()
        
        return {
            "success": True,
            "report_type": "yield_prediction",
            "generated_at": datetime.utcnow().isoformat(),
            "prediction_summary": {
                "predicted_yield": predicted_yield,
                "crop": current_input['crop'],
                "season": current_input['season'],
                "area": current_input['area']
            },
            "detailed_report": report_text,
            "history_count": len(previous_predictions) if previous_predictions else 0
        }
    
    except Exception as e:
        print(f"Error generating yield detailed report: {e}")
        return {
            "success": False,
            "message": f"Error generating report: {str(e)}",
            "report": None
        }


def generate_disease_notification(current_prediction: Dict, previous_predictions: List[Dict]) -> str:
    """
    Generate a brief notification message for disease detection with progress tracking
    """
    if not model:
        return "Disease detection completed. Enable Gemini API for intelligent insights."
    
    try:
        # Extract current prediction data
        current_result = current_prediction['result']
        plant = current_result['plant']
        disease = current_result['disease']
        confidence = current_result['confidence']
        is_healthy = current_result['is_healthy']
        current_date = current_prediction.get('prediction_date', 'today')
        
        # Build history context with dates
        history_context = ""
        if previous_predictions and len(previous_predictions) > 0:
            prev_pred = previous_predictions[0]
            prev_result = prev_pred['result']
            prev_date = prev_pred.get('prediction_date', 'previously')
            prev_disease = prev_result['disease']
            prev_is_healthy = prev_result['is_healthy']
            
            history_context = f"""
Previous Detection ({prev_date}): {prev_result['plant']} - {prev_disease}
Previous Health Status: {'Healthy' if prev_is_healthy else 'Diseased'}
"""
        
        prompt = f"""You are a plant pathology AI assistant. Generate a brief notification (max 2-3 sentences) for a farmer.

Current Detection ({current_date}):
- Plant: {plant}
- Disease: {disease}
- Health Status: {'Healthy' if is_healthy else 'Diseased'}
- Confidence: {confidence}%
{history_context}

Task: If there's previous data, ACKNOWLEDGE THE PROGRESS or DETERIORATION of the disease compared to the previous prediction. 
If the plant was diseased before and is now healthy, congratulate the farmer on recovery. 
If it's getting worse, provide urgent advice. 
If it's a new detection, give a brief assessment.

Create a short, actionable notification. Be professional and empathetic."""

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating disease notification: {e}")
        return f"✓ Detection: {disease}. Confidence: {confidence}%. Detailed analysis available."


def generate_disease_detailed_report(current_prediction: Dict, previous_predictions: List[Dict]) -> Dict:
    """
    Generate a comprehensive report for disease detection with progress tracking over time
    """
    if not model:
        return {
            "success": False,
            "message": "Gemini API not configured. Please set GEMINI_API_KEY.",
            "report": None
        }
    
    try:
        current_result = current_prediction['result']
        plant = current_result['plant']
        disease = current_result['disease']
        confidence = current_result['confidence']
        is_healthy = current_result['is_healthy']
        severity = current_result['severity']
        top_predictions = current_result['top_predictions']
        recommendations = current_result['recommendations']
        current_date = current_prediction.get('prediction_date', 'Current date')
        timeframe = current_prediction.get('timeframe', 'Not specified')
        
        # Build comprehensive history with dates
        history_text = ""
        progress_analysis = ""
        if previous_predictions and len(previous_predictions) > 0:
            history_text = "\n\nPREVIOUS DISEASE DETECTIONS:\n"
            for i, pred in enumerate(previous_predictions[:5], 1):
                pred_result = pred['result']
                pred_date = pred.get('prediction_date', 'Date unknown')
                pred_timeframe = pred.get('timeframe', 'N/A')
                history_text += f"\n{i}. Detection Date: {pred_date} (Timeframe: {pred_timeframe})\n"
                history_text += f"   Plant: {pred_result['plant']}\n"
                history_text += f"   Disease: {pred_result['disease']}\n"
                history_text += f"   Health Status: {'Healthy' if pred_result['is_healthy'] else 'Diseased'}\n"
                history_text += f"   Confidence: {pred_result['confidence']}%\n"
                history_text += f"   Severity: {pred_result['severity']}\n"
            
            # Analyze disease progression
            prev_result = previous_predictions[0]['result']
            prev_date = previous_predictions[0].get('prediction_date', 'Previous date')
            
            if prev_result['is_healthy'] and not is_healthy:
                progress_analysis = f"\n\nDISEASE PROGRESSION:\n⚠ ALERT: Plant was healthy on {prev_date} but now shows {disease}. Early stage disease detected."
            elif not prev_result['is_healthy'] and is_healthy:
                progress_analysis = f"\n\nDISEASE PROGRESSION:\n✓ RECOVERY: Plant was affected by {prev_result['disease']} on {prev_date}. Now showing healthy status - treatment successful!"
            elif not prev_result['is_healthy'] and not is_healthy:
                if prev_result['disease'] == disease:
                    progress_analysis = f"\n\nDISEASE PROGRESSION:\n→ ONGOING: Same disease ({disease}) detected on {prev_date} and {current_date}. Continue treatment."
                else:
                    progress_analysis = f"\n\nDISEASE PROGRESSION:\n⚠ CHANGED: Previous disease was {prev_result['disease']} ({prev_date}). Now showing {disease} ({current_date})."
        
        prompt = f"""You are an expert plant pathologist and agricultural consultant. Generate a comprehensive disease detection report for a farmer.

CURRENT DETECTION:
- Detection Date: {current_date}
- Expected Timeframe: {timeframe}
- Plant: {plant}
- Disease: {disease}
- Health Status: {'Healthy' if is_healthy else 'Diseased'}
- Confidence: {confidence}%
- Severity: {severity}

TOP PREDICTIONS:
{chr(10).join([f"  {i+1}. {p['plant']} - {p['disease']} ({p['confidence']}%)" for i, p in enumerate(top_predictions)])}

CURRENT RECOMMENDATIONS:
Treatment: {recommendations.get('treatment', 'N/A')}
Prevention: {', '.join(recommendations.get('prevention', []))}
Pesticides: {', '.join(recommendations.get('pesticides', []))}
{progress_analysis}
{history_text}

Generate a detailed report with the following sections:

1. EXECUTIVE SUMMARY (2-3 sentences)
   - Current health status and main finding

2. DISEASE PROGRESSION ANALYSIS (CRITICAL SECTION)
   - Compare current detection with previous detections (dates mentioned)
   - Analyze if disease is NEW, ONGOING, RECOVERING, or WORSENING
   - Calculate time between detections and disease development speed
   - Acknowledge farmer's efforts if improvement is seen

3. CURRENT DISEASE ASSESSMENT
   - Detailed analysis of the detected disease
   - Severity level and risk factors
   - Expected impact if untreated

4. COMPARISON WITH PREVIOUS DETECTIONS
   - Timeline of disease history
   - Pattern analysis (recurring, seasonal, etc.)
   - Success or failure of previous treatments

5. TREATMENT RECOMMENDATIONS
   - Immediate actions required
   - Recommended pesticides and application method
   - Treatment timeline based on timeframe

6. PREVENTION STRATEGIES
   - Steps to prevent recurrence
   - Long-term plant health management
   - Environmental factors to monitor

7. ACTIONABLE STEPS (4-6 specific steps)
   - Prioritized action items with timeline

8. PROFESSIONAL ADVICE
   - Expert guidance for this specific situation
   - When to seek additional help
   - Expected recovery timeline

Format professionally with clear sections, bullet points, and empathetic language. If the plant is recovering, congratulate the farmer. If disease is worsening, provide urgent guidance."""

        response = model.generate_content(prompt)
        report_text = response.text.strip()
        
        return {
            "success": True,
            "report_type": "disease_detection",
            "generated_at": datetime.utcnow().isoformat(),
            "prediction_summary": {
                "plant": plant,
                "disease": disease,
                "is_healthy": is_healthy,
                "confidence": confidence,
                "severity": severity,
                "detection_date": current_date
            },
            "detailed_report": report_text,
            "history_count": len(previous_predictions) if previous_predictions else 0
        }
    
    except Exception as e:
        print(f"Error generating disease detailed report: {e}")
        return {
            "success": False,
            "message": f"Error generating report: {str(e)}",
            "report": None
        }

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load the trained model and encoders
try:
    with open('best_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
    
    print("Model and encoders loaded successfully!")
    print(f"Model type: {type(model)}")
    print(f"Available encoders: {list(encoders.keys())}")
    
except Exception as e:
    print(f"Error loading model or encoders: {e}")
    model = None
    encoders = None

# Define the questions for the AQ-10 screening test
AQ10_QUESTIONS = [
    {
        "id": "A1_Score",
        "question": "I often notice small sounds when others do not",
        "description": "Do you notice subtle sounds that others might miss?"
    },
    {
        "id": "A2_Score", 
        "question": "I usually concentrate more on the whole picture, rather than the small details",
        "description": "Do you focus on the overall picture rather than details?"
    },
    {
        "id": "A3_Score",
        "question": "I find it easy to do more than one thing at once",
        "description": "Can you easily multitask or handle multiple activities?"
    },
    {
        "id": "A4_Score",
        "question": "If there is an interruption, I can switch back to what I was doing very quickly",
        "description": "Can you quickly return to tasks after being interrupted?"
    },
    {
        "id": "A5_Score",
        "question": "I find it easy to 'read between the lines' when someone is talking to me",
        "description": "Do you easily understand implied meanings in conversations?"
    },
    {
        "id": "A6_Score",
        "question": "I know how to tell if someone listening to me is getting bored",
        "description": "Can you recognize when someone is losing interest?"
    },
    {
        "id": "A7_Score",
        "question": "When I'm reading a story I find it difficult to work out the characters' intentions",
        "description": "Do you have difficulty understanding characters' motivations?"
    },
    {
        "id": "A8_Score",
        "question": "I like to collect information about categories of things",
        "description": "Do you enjoy collecting detailed information about specific topics?"
    },
    {
        "id": "A9_Score",
        "question": "I find it easy to work out what someone is thinking or feeling by looking at their face",
        "description": "Can you easily read emotions from facial expressions?"
    },
    {
        "id": "A10_Score",
        "question": "I find it difficult to work out people's intentions",
        "description": "Do you have trouble understanding what people really mean?"
    }
]

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html', questions=AQ10_QUESTIONS)

@app.route('/api/questions')
def get_questions():
    """API endpoint to get AQ-10 questions"""
    return jsonify(AQ10_QUESTIONS)

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for autism prediction"""
    try:
        if model is None or encoders is None:
            return jsonify({
                'error': 'Model or encoders not loaded properly',
                'success': False
            }), 500
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'success': False
            }), 400
        
        # Validate required fields
        required_fields = [
            'A1_Score', 'A2_Score', 'A3_Score', 'A4_Score', 'A5_Score',
            'A6_Score', 'A7_Score', 'A8_Score', 'A9_Score', 'A10_Score',
            'age', 'gender', 'ethnicity', 'jaundice', 'austim',
            'contry_of_res', 'used_app_before', 'relation'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}',
                'success': False
            }), 400
        
        # Create DataFrame with the input data
        input_df = pd.DataFrame([data])
        
        # Calculate result score (sum of A1-A10 scores)
        aq_scores = [f'A{i}_Score' for i in range(1, 11)]
        input_df['result'] = input_df[aq_scores].sum(axis=1)
        
        # Apply label encoding to categorical columns
        categorical_columns = ['gender', 'ethnicity', 'jaundice', 'austim', 'contry_of_res', 'used_app_before', 'relation']
        
        for column in categorical_columns:
            if column in encoders:
                try:
                    # Handle unknown categories
                    unique_values = list(encoders[column].classes_)
                    if input_df[column].iloc[0] not in unique_values:
                        # If unknown category, use the most common one (usually 'Others' or first category)
                        input_df[column] = unique_values[0] if unique_values else 0
                    
                    input_df[column] = encoders[column].transform(input_df[column])
                except Exception as e:
                    print(f"Error encoding {column}: {e}")
                    # Fallback to 0 if encoding fails
                    input_df[column] = 0
        
        # Ensure all columns are in the correct order and type
        feature_columns = [
            'A1_Score', 'A2_Score', 'A3_Score', 'A4_Score', 'A5_Score',
            'A6_Score', 'A7_Score', 'A8_Score', 'A9_Score', 'A10_Score',
            'age', 'gender', 'ethnicity', 'jaundice', 'austim',
            'contry_of_res', 'used_app_before', 'result', 'relation'
        ]
        
        # Reorder columns to match training data
        input_df = input_df[feature_columns]
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]
        
        # Debug output
        print(f"DEBUG: Input features shape: {input_df.shape}")
        print(f"DEBUG: Input features: {input_df.iloc[0].to_dict()}")
        print(f"DEBUG: Model prediction: {prediction}")
        print(f"DEBUG: Prediction probabilities: {prediction_proba}")
        print(f"DEBUG: AQ total score: {sum(data[f'A{i}_Score'] for i in range(1, 11))}")
        
        # Get confidence score
        confidence = float(max(prediction_proba))
        
        # Determine risk level
        if confidence >= 0.8:
            risk_level = "High"
        elif confidence >= 0.6:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        # Calculate AQ-10 total score
        aq_total = sum(data[f'A{i}_Score'] for i in range(1, 11))
        
        # Generate explanation
        explanation = generate_explanation(prediction, confidence, aq_total, data)
        
        # Prepare response
        response = {
            'success': True,
            'prediction': 'YES' if prediction == 1 else 'NO',
            'confidence': round(confidence * 100, 1),
            'risk_level': risk_level,
            'aq_total_score': aq_total,
            'explanation': explanation,
            'recommendations': get_recommendations(prediction, aq_total, confidence)
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'success': False
        }), 500

def generate_explanation(prediction, confidence, aq_total, data):
    """Generate a detailed explanation of the prediction"""
    
    pred_text = "suggests autism traits" if prediction == 1 else "does not suggest autism traits"
    confidence_text = f"{confidence*100:.1f}%"
    
    explanation = f"Based on the assessment, the model {pred_text} with {confidence_text} confidence. "
    
    # AQ-10 score interpretation
    if aq_total >= 6:
        explanation += f"Your AQ-10 total score is {aq_total}/10, which is above the typical threshold (6+) "
        explanation += "that suggests further evaluation may be beneficial. "
    else:
        explanation += f"Your AQ-10 total score is {aq_total}/10, which is below the typical threshold. "
    
    # Add demographic context
    age = data.get('age', 'Unknown')
    gender = data.get('gender', 'Unknown')
    explanation += f"This assessment considers your age ({age}) and gender ({gender}) "
    explanation += "along with your responses to the AQ-10 screening questions. "
    
    # Add confidence interpretation
    if confidence >= 0.8:
        explanation += "The high confidence level indicates strong alignment with the training data patterns."
    elif confidence >= 0.6:
        explanation += "The moderate confidence level suggests some uncertainty in the prediction."
    else:
        explanation += "The lower confidence level indicates significant uncertainty in the prediction."
    
    return explanation

def get_recommendations(prediction, aq_total, confidence):
    """Generate recommendations based on the prediction"""
    
    recommendations = []
    
    if prediction == 1 or aq_total >= 6:
        recommendations.extend([
            "Consider consulting with a qualified healthcare professional or psychologist who specializes in autism assessment",
            "Keep a journal of your experiences and challenges to discuss with a professional",
            "Research local autism support groups and resources in your area",
            "Remember that this is a screening tool and not a diagnostic instrument"
        ])
    else:
        recommendations.extend([
            "Your responses suggest lower likelihood of autism traits",
            "If you still have concerns, consider speaking with a healthcare professional",
            "Continue to trust your own experiences and seek support if needed",
            "This screening tool is just one data point - your experiences matter most"
        ])
    
    # Add general recommendations
    recommendations.extend([
        "This assessment is for educational purposes only and should not replace professional evaluation",
        "Autism presents differently in each individual, and formal diagnosis requires comprehensive assessment",
        "Consider exploring neurodiversity resources regardless of the screening results"
    ])
    
    return recommendations

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'encoders_loaded': encoders is not None
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

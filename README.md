# Autism Prediction Web Application

A full-stack web application that uses machine learning to predict autism spectrum traits based on the AQ-10 screening questionnaire.

## Features

🧠 **Machine Learning Model**: Random Forest classifier trained on autism screening data
📊 **AQ-10 Assessment**: Standard 10-question autism screening questionnaire  
🎨 **Modern UI**: Responsive design with progress tracking
📈 **Real-time Results**: Instant prediction with confidence scores
🔬 **Data Analysis**: Comprehensive explanation of results

## Quick Start (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/vishalsb1/final_project.git
cd final_project
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

### 4. Open in Browser
Go to: `http://localhost:5000`

### 5. Share with Friends on Same Network
Find your computer's IP address and share: `http://YOUR_IP_ADDRESS:5000`

## For Your Friends to Use:

### Windows Users:
1. Download Python from https://python.org
2. Open Command Prompt and run the commands above

### Mac Users:
1. Install Python: `brew install python` (if Homebrew is installed)
2. Open Terminal and run the commands above

### Linux Users:
1. Install Python: `sudo apt install python3 python3-pip`
2. Open Terminal and run the commands above

### For Positive Autism Prediction:
- Select **"Definitely Agree"** for all 10 AQ-10 questions
- Set **Family History of Autism** to "Yes"
- Expected result: "Autism Traits Detected" with 89% confidence

### For Negative Autism Prediction:
- Select **"Definitely Disagree"** for all 10 AQ-10 questions  
- Set **Family History of Autism** to "No"
- Expected result: "No Autism Traits Detected"
- Confidence scores and detailed explanations
- Professional presentation of results

## Technology Stack

### Backend
- **Flask**: Python web framework
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation
- **pickle**: Model serialization
- **CORS**: Cross-origin resource sharing

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript**: Interactive functionality
- **Responsive Design**: Mobile-friendly interface

### Machine Learning
- **Random Forest Classifier**: Primary prediction model
- **SMOTE**: Synthetic minority oversampling technique
- **Label Encoding**: Categorical data preprocessing
- **Cross-validation**: Model evaluation

## Project Structure

```
├── app.py                 # Flask backend API
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
├── templates/
│   └── index.html        # Main webpage
├── models/
│   ├── best_model.pkl    # Trained ML model
│   └── encoders.pkl      # Data encoders
└── requirements.txt      # Python dependencies
```

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd autism-prediction-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## API Endpoints

### POST /predict
Predicts autism likelihood based on input features.

**Request Body:**
```json
{
  "A1_Score": 1,
  "A2_Score": 1,
  "A3_Score": 0,
  ...
  "gender": "m",
  "ethnicity": "White-European",
  "jaundice": "no",
  "austim": "no",
  "contry_of_res": "United States",
  "used_app_before": "no",
  "relation": "Self"
}
```

**Response:**
```json
{
  "prediction": "YES",
  "confidence": 0.87,
  "risk_level": "High",
  "explanation": "Based on the assessment scores and demographic information..."
}
```

## Model Performance

- **Algorithm**: Random Forest Classifier
- **Cross-validation Accuracy**: 93%
- **Features**: 17 input variables including AQ-10 scores and demographics
- **Training Data**: Balanced dataset using SMOTE technique

## Usage

1. **Complete the Assessment**: Fill out the AQ-10 questionnaire and provide demographic information
2. **Submit for Analysis**: Click "Predict Autism Risk" to get results
3. **Review Results**: Get prediction, confidence score, and detailed explanation
4. **Consult Professional**: Use results as guidance for seeking professional evaluation

## Disclaimer

This tool is for educational and screening purposes only. It should not replace professional medical diagnosis. Always consult with qualified healthcare providers for proper autism assessment and diagnosis.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for improvements.

## License
This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for autism awareness and accessibility**

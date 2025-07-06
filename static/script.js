// Autism Assessment Tool - Frontend JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('assessmentForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultsSection = document.getElementById('resultsSection');
    const loader = document.querySelector('.btn-loader');
    
    // Progress tracking
    let totalQuestions = 10; // AQ-10 questions
    let totalFields = 8; // Age, gender, ethnicity, country, jaundice, autism, app, relation
    let totalFormFields = totalQuestions + totalFields;
    
    // Initialize form validation
    initializeFormValidation();
    
    // Form submission handler
    form.addEventListener('submit', handleFormSubmission);
    
    function initializeFormValidation() {
        // Add event listeners to all form inputs
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('change', updateFormProgress);
            input.addEventListener('input', updateFormProgress);
        });
        
        // Initial validation check
        updateFormProgress();
    }
    
    function updateFormProgress() {
        const filledFields = countFilledFields();
        const progress = (filledFields / totalFormFields) * 100;
        
        // Update progress bar if exists
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }
        
        // Update submit button state
        updateSubmitButton(progress === 100);
        
        // Update progress text if exists
        const progressText = document.querySelector('.progress-text');
        if (progressText) {
            progressText.textContent = `${filledFields}/${totalFormFields} fields completed`;
        }
    }
    
    function countFilledFields() {
        let count = 0;
        
        // Count AQ-10 questions (radio buttons)
        for (let i = 1; i <= 10; i++) {
            const questionName = `A${i}_Score`;
            const selectedOption = form.querySelector(`input[name="${questionName}"]:checked`);
            if (selectedOption) {
                count++;
            }
        }
        
        // Count demographic fields
        const demographicFields = ['age', 'gender', 'ethnicity', 'contry_of_res', 'jaundice', 'austim', 'used_app_before', 'relation'];
        demographicFields.forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field && field.value.trim() !== '') {
                count++;
            }
        });
        
        return count;
    }
    
    function updateSubmitButton(isFormComplete) {
        if (isFormComplete) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('disabled');
            submitBtn.style.opacity = '1';
        } else {
            submitBtn.disabled = true;
            submitBtn.classList.add('disabled');
            submitBtn.style.opacity = '0.6';
        }
    }
    
    async function handleFormSubmission(e) {
        e.preventDefault();
        
        // Show loading state
        showLoadingState();
        
        try {
            // Collect form data
            const formData = collectFormData();
            
            // Send prediction request
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                displayResults(result);
            } else {
                displayError(result.error || 'An error occurred during prediction');
            }
            
        } catch (error) {
            console.error('Error:', error);
            displayError('Network error. Please try again.');
        } finally {
            hideLoadingState();
        }
    }
    
    function collectFormData() {
        const data = {};
        
        // Collect AQ-10 scores
        for (let i = 1; i <= 10; i++) {
            const questionName = `A${i}_Score`;
            const selectedOption = form.querySelector(`input[name="${questionName}"]:checked`);
            data[questionName] = selectedOption ? parseInt(selectedOption.value) : 0;
        }
        
        // Collect demographic data
        const demographicFields = ['age', 'gender', 'ethnicity', 'contry_of_res', 'jaundice', 'austim', 'used_app_before', 'relation'];
        demographicFields.forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                data[fieldName] = field.value;
            }
        });
        
        return data;
    }
    
    function showLoadingState() {
        submitBtn.disabled = true;
        submitBtn.querySelector('span').style.display = 'none';
        loader.classList.remove('hidden');
    }
    
    function hideLoadingState() {
        submitBtn.disabled = false;
        submitBtn.querySelector('span').style.display = 'inline';
        loader.classList.add('hidden');
    }
    
    function displayResults(result) {
        console.log('DEBUG: Received result:', result);
        
        // Hide form section
        document.querySelector('.assessment-section').style.display = 'none';
        
        // Show results section
        resultsSection.classList.remove('hidden');
        
        // Update prediction result
        const predictionResult = document.getElementById('predictionResult');
        const predictionSubtitle = document.getElementById('predictionSubtitle');
        
        console.log('DEBUG: Prediction value:', result.prediction);
        
        if (result.prediction === 'YES') {
            predictionResult.textContent = 'Autism Traits Detected';
            predictionResult.className = 'result-value positive';
            predictionSubtitle.textContent = 'The assessment suggests autism spectrum traits may be present';
            console.log('DEBUG: Set to positive result');
        } else {
            predictionResult.textContent = 'No Autism Traits Detected';
            predictionResult.className = 'result-value negative';
            predictionSubtitle.textContent = 'The assessment suggests autism spectrum traits are unlikely';
            console.log('DEBUG: Set to negative result');
        }
        
        // Update confidence level
        const confidenceValue = document.getElementById('confidenceValue');
        const confidence = result.confidence;
        confidenceValue.textContent = confidence + '%';
        
        // Update AQ-10 score
        const aqScore = document.getElementById('aqScore');
        const scoreInterpretation = document.getElementById('scoreInterpretation');
        aqScore.textContent = result.aq_total_score;
        
        if (result.aq_total_score >= 6) {
            scoreInterpretation.textContent = 'Score indicates possible autism spectrum traits';
            scoreInterpretation.className = 'score-interpretation high';
        } else if (result.aq_total_score >= 4) {
            scoreInterpretation.textContent = 'Score indicates some autism spectrum traits';
            scoreInterpretation.className = 'score-interpretation medium';
        } else {
            scoreInterpretation.textContent = 'Score indicates few autism spectrum traits';
            scoreInterpretation.className = 'score-interpretation low';
        }
        
        // Update risk level
        const riskLevel = document.getElementById('riskLevel');
        if (result.prediction === 'YES') {
            riskLevel.textContent = 'Higher Risk';
            riskLevel.className = 'risk-indicator high';
        } else {
            riskLevel.textContent = 'Lower Risk';
            riskLevel.className = 'risk-indicator low';
        }
        
        // Update explanation
        const explanationText = document.getElementById('explanationText');
        explanationText.innerHTML = `<p>${result.explanation}</p>`;
        
        // Update recommendations
        const recommendationsList = document.getElementById('recommendationsList');
        if (result.recommendations && result.recommendations.length > 0) {
            recommendationsList.innerHTML = result.recommendations.map(rec => `<li>${rec}</li>`).join('');
        } else {
            // Fallback recommendations
            const recommendations = [];
            
            if (result.prediction === 'YES') {
                recommendations.push('Consider consulting with a qualified healthcare professional for comprehensive evaluation');
                recommendations.push('Explore resources about autism spectrum conditions');
                recommendations.push('Connect with autism support communities if helpful');
            } else {
                recommendations.push('This screening suggests lower likelihood of autism spectrum traits');
                recommendations.push('If you still have concerns, consider speaking with a healthcare professional');
                recommendations.push('Remember that this is a screening tool, not a diagnostic assessment');
            }
            
            recommendations.push('This assessment should not replace professional medical evaluation');
            
            recommendationsList.innerHTML = recommendations.map(rec => `<li>${rec}</li>`).join('');
        }
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    function displayError(message) {
        alert('Error: ' + message);
    }
    
    // Global functions for buttons
    window.resetAssessment = function() {
        // Reset form
        form.reset();
        
        // Hide results section
        resultsSection.classList.add('hidden');
        
        // Show form section
        document.querySelector('.assessment-section').style.display = 'block';
        
        // Reset form validation
        updateFormProgress();
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };
    
    window.printResults = function() {
        window.print();
    };
    
    // Initialize the form
    console.log('Autism Assessment Tool initialized');
});

"""
Financial Advisor - Main Flask Application
This module handles all the routing and API endpoints for the application.
"""

from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime
from ai_analyzer import analyze_finances, chat_with_ai
from data_processor import process_manual_data, process_csv_data, calculate_financial_health

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Home/Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Input Page (Manual or CSV)
@app.route('/input')
def input_page():
    return render_template('input.html')

# Process Manual Data
@app.route('/process-manual', methods=['POST'])
def process_manual():
    try:
        data = request.json
        
        # Process the data
        processed_data = process_manual_data(data)
        
        # Store in session for dashboard
        session['financial_data'] = processed_data
        
        return jsonify({
            'success': True,
            'message': 'Data processed successfully!',
            'data': processed_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing data: {str(e)}'
        }), 400

# Process CSV Upload
@app.route('/process-csv', methods=['POST'])
def process_csv():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process CSV
            processed_data = process_csv_data(filepath)
            
            # Store in session
            session['financial_data'] = processed_data
            
            return jsonify({
                'success': True,
                'message': 'CSV processed successfully!',
                'data': processed_data
            })
        else:
            return jsonify({'success': False, 'message': 'Please upload a CSV file'}), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing CSV: {str(e)}'
        }), 400

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    financial_data = session.get('financial_data')
    
    if not financial_data:
        return render_template('input.html', error='Please enter your financial data first')
    
    return render_template('dashboard.html', data=financial_data)

# AI Analysis Endpoint
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        financial_data = session.get('financial_data')
        
        if not financial_data:
            return jsonify({
                'success': False,
                'message': 'No financial data found. Please enter data first.'
            }), 400
        
        # Get AI analysis
        analysis = analyze_finances(financial_data)
        
        # Calculate financial health score
        health_score = calculate_financial_health(financial_data)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'health_score': health_score
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error analyzing data: {str(e)}'
        }), 400

# AI Chat Endpoint
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        financial_data = session.get('financial_data', {})
        
        # Get AI response
        response = chat_with_ai(user_message, financial_data)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error in chat: {str(e)}'
        }), 400

# Chat Page
@app.route('/chat-page')
def chat_page():
    financial_data = session.get('financial_data')
    
    if not financial_data:
        return render_template('input.html', error='Please enter your financial data first')
    
    return render_template('chat.html', data=financial_data)

if __name__ == '__main__':
    app.run()
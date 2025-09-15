# Quick Start Guide

## Quick Installation

1. Install Python packages:
   python install.py

## Web Applications

### Basic Web App
python -m streamlit run web_app.py
Access at: http://localhost:8501

### Secure Web App (Recommended)
python run_secure_app.py
Access at: http://localhost:8501
Default password: admin123

### Windows Users
Double-click: start_secure_app.bat

## Desktop Application
python density_temperature_app.py

## Sample Data
- Use the included sample_data.xlsx for testing
- Or download sample data from the web app

## Security
- Change default password in secure_web_app.py
- Sessions expire after 1 hour
- File upload limit: 10MB

## Full Documentation
See README.md and DEPLOYMENT.md for complete instructions.

## Support
- Check the documentation files
- Ensure all requirements are installed
- Verify Python version (3.7+)

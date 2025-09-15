# Density-Temperature Lookup Application

A Python application (both desktop GUI and web-based) that allows users to upload Excel files containing density and temperature data, and perform lookups to find corresponding density values.

## 🌐 Web Version (Recommended)

The web version provides a modern, interactive interface accessible from any browser with a simple link.

### Quick Start (Web Version)
1. **Run the web app locally**:
   ```bash
   pip install -r requirements.txt
   streamlit run web_app.py
   ```
2. **Open your browser** to `http://localhost:8501`
3. **Upload your Excel file** and start using the app!

### Deploy to Web (Share with Others)
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to:
- **Streamlit Cloud** (Free, recommended)
- **Heroku**
- **Local network sharing**
- **Docker**

## 🖥️ Desktop Version

The original desktop GUI application using tkinter.

## Features

### Web Version Features
- **🌐 Browser-based Interface**: Access from any device with a web browser
- **📊 Interactive Visualizations**: Plotly charts showing data relationships
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **⬇️ Sample Data Download**: Built-in sample data generator
- **🎯 Real-time Results**: Instant lookup with visual feedback
- **📈 Data Visualization**: Interactive scatter plots with your input highlighted

### Both Versions Include
- **Excel File Upload**: Upload Excel files (.xlsx, .xls) containing your data
- **Data Validation**: Ensures the uploaded file has the required columns
- **Interactive Lookup**: Enter measured density and observed temperature to find corresponding density
- **Data Preview**: View uploaded data in a table format
- **Error Handling**: Comprehensive error handling for invalid inputs and file issues

## Required Excel Format

Your Excel file must contain exactly these three columns:
- `Measured Density`
- `Observed Temperature` 
- `Corresponding Density`

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python density_temperature_app.py
```

2. **Upload Data**:
   - Click "Upload Excel File" button
   - Select your Excel file with the required columns
   - The data will be displayed in the preview table

3. **Perform Lookup**:
   - Enter a value for "Measured Density"
   - Enter a value for "Observed Temperature"
   - Click "Find Corresponding Density"
   - The result will be displayed with the closest matching corresponding density

## How It Works

The application uses a distance-based matching algorithm:
- It calculates the Euclidean distance between your input values and all rows in the dataset
- Returns the corresponding density from the row with the smallest distance
- Also shows the calculated distance for reference

## Sample Data

A sample Excel file (`sample_data.xlsx`) is included with 50 rows of test data. You can use this to test the application functionality.

## Requirements

- Python 3.7+
- pandas
- openpyxl
- numpy
- tkinter (usually included with Python)

## File Structure

```
├── web_app.py                   # 🌐 Web application (Streamlit)
├── density_temperature_app.py   # 🖥️ Desktop application (tkinter)
├── requirements.txt             # Python dependencies
├── create_sample_data.py        # Script to generate sample data
├── sample_data.xlsx            # Sample data file
├── DEPLOYMENT.md               # Deployment instructions
└── README.md                   # This file
```

## Quick Deployment to Share with Others

### Option 1: Streamlit Cloud (Easiest)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy with one click
5. Share the generated link!

### Option 2: Local Network Sharing
```bash
streamlit run web_app.py --server.address 0.0.0.0
```
Then share: `http://YOUR_IP:8501`

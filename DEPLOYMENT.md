# Deployment Guide for Density-Temperature Lookup Web App

This guide explains how to deploy the Streamlit web application so others can access it via a web link.

## 🔒 Security Features

The secure version includes:
- **Password Protection**: Login required to access the application
- **Session Timeout**: Automatic logout after 1 hour
- **File Size Limits**: Maximum 10MB file upload
- **XSRF Protection**: Cross-site request forgery protection
- **CORS Disabled**: Enhanced security for local deployment
- **Input Validation**: Comprehensive data validation

## Option 1: Streamlit Cloud (Recommended - Free)

### Steps:
1. **Push to GitHub**:
   - Create a GitHub repository
   - Upload all files to the repository
   - Ensure `requirements.txt` is in the root directory

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set main file path to `web_app.py`
   - Click "Deploy"

3. **Access Your App**:
   - Your app will be available at: `https://your-app-name.streamlit.app`
   - Share this link with users

## Option 2: Heroku

### Steps:
1. **Create Procfile**:
   ```
   web: streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create runtime.txt**:
   ```
   python-3.11.0
   ```

3. **Deploy**:
   - Install Heroku CLI
   - Run: `heroku create your-app-name`
   - Run: `git push heroku main`

## Option 3: Secure Local Network Sharing

### For secure local network deployment:
1. **Run the secure application**:
   ```bash
   python run_secure_app.py
   ```
   Or use the batch file on Windows:
   ```bash
   start_secure_app.bat
   ```

2. **Access the application**:
   - Local: `http://localhost:8501`
   - Network: `http://YOUR_IP:8501`
   - Default password: `admin123`

3. **Security Configuration**:
   - Change the default password in `secure_web_app.py`
   - Sessions expire after 1 hour
   - File uploads limited to 10MB
   - XSRF protection enabled

### Manual secure deployment:
```bash
streamlit run secure_web_app.py --server.address 0.0.0.0 --server.port 8501
```

## Option 4: Docker Deployment

### Create Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "web_app.py", "--server.address", "0.0.0.0"]
```

### Deploy:
```bash
docker build -t density-app .
docker run -p 8501:8501 density-app
```

## Environment Variables (Optional)

Create `.streamlit/config.toml` for custom configuration:
```toml
[server]
port = 8501
address = "0.0.0.0"

[theme]
primaryColor = "#3498db"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## Security Considerations

1. **File Upload Limits**: Streamlit has built-in file size limits
2. **Data Privacy**: Consider data handling policies for uploaded files
3. **Access Control**: Add authentication if needed for production use

## Troubleshooting

### Common Issues:
1. **Port already in use**: Change port with `--server.port 8502`
2. **File upload errors**: Check file size and format
3. **Memory issues**: Optimize data processing for large files

### Performance Tips:
1. **Caching**: Use `@st.cache_data` for expensive operations
2. **Data limits**: Consider limiting dataset size for web deployment
3. **Session state**: Use `st.session_state` for better performance

## Monitoring

- **Streamlit Cloud**: Built-in analytics and usage stats
- **Heroku**: Use Heroku metrics dashboard
- **Custom**: Add logging and monitoring as needed

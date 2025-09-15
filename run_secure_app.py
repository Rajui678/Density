#!/usr/bin/env python3
"""
Secure deployment script for the Density-Temperature Lookup Application
"""

import subprocess
import sys
import os
import socket
import getpass

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'pandas', 'plotly', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("✅ All packages installed successfully!")
    else:
        print("✅ All required packages are installed!")

def create_secure_config():
    """Create secure configuration"""
    config_dir = ".streamlit"
    config_file = os.path.join(config_dir, "config.toml")
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    if not os.path.exists(config_file):
        print("Creating secure configuration...")
        config_content = """[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 10

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#3498db"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[logger]
level = "error"
"""
        with open(config_file, 'w') as f:
            f.write(config_content)
        print("✅ Secure configuration created!")

def main():
    """Main deployment function"""
    print("🔒 Secure Density-Temperature Lookup App Deployment")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Create secure config
    create_secure_config()
    
    # Get network information
    local_ip = get_local_ip()
    username = getpass.getuser()
    
    print(f"\n🌐 Network Information:")
    print(f"   Local IP: {local_ip}")
    print(f"   Username: {username}")
    print(f"   Port: 8501")
    
    print(f"\n🔒 Security Features:")
    print(f"   ✅ Password protection enabled")
    print(f"   ✅ Session timeout (1 hour)")
    print(f"   ✅ File size limit (10MB)")
    print(f"   ✅ XSRF protection enabled")
    print(f"   ✅ CORS disabled")
    
    print(f"\n🚀 Starting secure application...")
    print(f"   Access URL: http://{local_ip}:8501")
    print(f"   Local URL: http://localhost:8501")
    print(f"   Default Password: admin123")
    print(f"\n⚠️  IMPORTANT: Change the default password in secure_web_app.py")
    print(f"   Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Run the secure application
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "secure_web_app.py",
            "--server.address", "0.0.0.0",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")

if __name__ == "__main__":
    main()


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Tuple
import io

# Page configuration
st.set_page_config(
    page_title="Density-Temperature Lookup App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def validate_data_structure(data: pd.DataFrame) -> bool:
    """Validate that the data has the required columns"""
    if data is None:
        return False
    required_columns = ['Measured Density', 'Observed Temperature', 'Corresponding Density']
    return all(col in data.columns for col in required_columns)

def find_closest_match(data: pd.DataFrame, measured_density: float, observed_temp: float) -> Optional[Tuple[float, float]]:
    """Find the closest match based on Euclidean distance"""
    if data is None or data.empty:
        return None
    
    # Calculate distances
    distances = np.sqrt(
        (data['Measured Density'] - measured_density)**2 + 
        (data['Observed Temperature'] - observed_temp)**2
    )
    
    # Find minimum distance
    min_idx = distances.idxmin()
    min_distance = distances.iloc[min_idx]
    
    # Return corresponding density and distance
    corresponding_density = data.loc[min_idx, 'Corresponding Density']
    return corresponding_density, min_distance

def create_scatter_plot(data: pd.DataFrame, measured_density: float = None, observed_temp: float = None):
    """Create an interactive scatter plot"""
    fig = px.scatter(
        data, 
        x='Measured Density', 
        y='Observed Temperature',
        color='Corresponding Density',
        size='Corresponding Density',
        hover_data=['Corresponding Density'],
        title='Density-Temperature Data Visualization',
        color_continuous_scale='Viridis'
    )
    
    # Add user input point if provided
    if measured_density is not None and observed_temp is not None:
        fig.add_trace(go.Scatter(
            x=[measured_density],
            y=[observed_temp],
            mode='markers',
            marker=dict(
                color='red',
                size=15,
                symbol='x',
                line=dict(width=3, color='darkred')
            ),
            name='Your Input',
            hovertemplate=f'Your Input<br>Measured Density: {measured_density}<br>Observed Temperature: {observed_temp}<extra></extra>'
        ))
    
    fig.update_layout(
        width=800,
        height=600,
        showlegend=True
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Density-Temperature Lookup Application</h1>', unsafe_allow_html=True)
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📁 Upload Data")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=['xlsx', 'xls'],
            help="Upload an Excel file with columns: 'Measured Density', 'Observed Temperature', 'Corresponding Density'"
        )
        
        # Sample data download
        st.markdown("---")
        st.subheader("📋 Sample Data")
        if st.button("Download Sample Data"):
            # Create sample data
            np.random.seed(42)
            n_samples = 50
            measured_density = np.random.uniform(0.8, 1.2, n_samples)
            observed_temperature = np.random.uniform(15, 35, n_samples)
            corresponding_density = (
                0.9 * measured_density + 
                0.1 * (1 - (observed_temperature - 20) / 20) + 
                np.random.normal(0, 0.02, n_samples)
            )
            
            sample_data = pd.DataFrame({
                'Measured Density': measured_density,
                'Observed Temperature': observed_temperature,
                'Corresponding Density': corresponding_density
            }).round(4)
            
            # Convert to Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                sample_data.to_excel(writer, index=False, sheet_name='Data')
            output.seek(0)
            
            st.download_button(
                label="Download sample_data.xlsx",
                data=output.getvalue(),
                file_name="sample_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🔍 Data Lookup")
        
        # Initialize session state
        if 'data' not in st.session_state:
            st.session_state.data = None
        
        # Load data if file is uploaded
        if uploaded_file is not None:
            try:
                data = pd.read_excel(uploaded_file)
                if validate_data_structure(data):
                    st.session_state.data = data
                    st.success("✅ File loaded successfully!")
                    
                    # Display data info
                    st.markdown(f"""
                    <div class="metric-card">
                        <strong>📊 Data Summary:</strong><br>
                        • Rows: {len(data)}<br>
                        • Columns: {len(data.columns)}<br>
                        • File: {uploaded_file.name}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ Invalid data structure. Please ensure your Excel file has columns: 'Measured Density', 'Observed Temperature', 'Corresponding Density'")
                    st.session_state.data = None
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                st.session_state.data = None
        
        # Input fields
        if st.session_state.data is not None:
            st.subheader("📝 Enter Values")
            
            col_density, col_temp = st.columns(2)
            
            with col_density:
                measured_density = st.number_input(
                    "Measured Density",
                    min_value=0.0,
                    max_value=10.0,
                    value=1.0,
                    step=0.001,
                    format="%.4f",
                    help="Enter the measured density value"
                )
            
            with col_temp:
                observed_temp = st.number_input(
                    "Observed Temperature",
                    min_value=-50.0,
                    max_value=200.0,
                    value=25.0,
                    step=0.1,
                    format="%.2f",
                    help="Enter the observed temperature value"
                )
            
            # Lookup button
            if st.button("🔍 Find Corresponding Density", type="primary", use_container_width=True):
                result = find_closest_match(st.session_state.data, measured_density, observed_temp)
                
                if result is not None:
                    corresponding_density, distance = result
                    
                    # Display result
                    st.markdown(f"""
                    <div class="success-message">
                        <h3>🎯 Result Found!</h3>
                        <strong>Corresponding Density:</strong> {corresponding_density:.4f}<br>
                        <strong>Match Distance:</strong> {distance:.4f}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Store result for visualization
                    st.session_state.last_result = {
                        'measured_density': measured_density,
                        'observed_temp': observed_temp,
                        'corresponding_density': corresponding_density,
                        'distance': distance
                    }
                else:
                    st.error("❌ No matching data found for the given inputs")
        else:
            st.info("👆 Please upload an Excel file to begin")
    
    with col2:
        st.header("📈 Data Visualization")
        
        if st.session_state.data is not None:
            # Get last result for visualization
            last_result = st.session_state.get('last_result', None)
            
            if last_result:
                fig = create_scatter_plot(
                    st.session_state.data,
                    last_result['measured_density'],
                    last_result['observed_temp']
                )
            else:
                fig = create_scatter_plot(st.session_state.data)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Data table
            st.subheader("📋 Data Preview")
            st.dataframe(
                st.session_state.data.head(10),
                use_container_width=True,
                hide_index=True
            )
            
            if len(st.session_state.data) > 10:
                st.caption(f"Showing first 10 rows of {len(st.session_state.data)} total rows")
        else:
            st.info("📊 Upload data to see visualization")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
        <p>🔬 Density-Temperature Lookup Application | Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


import streamlit as st
import joblib
import pandas as pd
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Boston Housing Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PROFESSIONAL CSS STYLING
# ============================================
st.markdown("""
<style>
    /* Root variables */
    :root {
        --primary-cyan: #00d4ff;
        --primary-blue: #0099ff;
        --dark-bg: #0a0e17;
        --card-bg: #1a2a3a;
        --sidebar-bg: #0f1419;
        --border-color: #00d4ff;
    }
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #0a0e17 0%, #16202f 50%, #1a1f2e 100%) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        position: fixed !important;
        top: 0;
        left: 0;
        height: 100vh !important;
        overflow-y: auto !important;
        z-index: 100;
        background: linear-gradient(180deg, #0f1419 0%, #1a1f2e 100%) !important;
        border-right: 3px solid #00d4ff !important;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.2) !important;
    }
    
    [data-testid="stSidebarContent"] {
        padding: 2rem 1.5rem !important;
    }
    
    [data-testid="stMainBlockContainer"] {
        margin-left: 340px !important;
        padding: 2rem 3rem !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #00d4ff !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
    }
    
    p, label {
        color: #e0e0e0 !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h2 {
        color: #00d4ff !important;
        border-bottom: 2px solid #00d4ff !important;
        padding-bottom: 0.75rem !important;
        margin-bottom: 1.5rem !important;
        font-size: 1.3rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #00d4ff 0%, #0099ff 100%) !important;
        border-radius: 10px !important;
    }
    
    .stSlider label {
        color: #00d4ff !important;
        font-weight: 600 !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* Button styling */
    button[kind="primary"] {
        background: linear-gradient(90deg, #00d4ff 0%, #0099ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 1rem 2rem !important;
        transition: all 0.3s ease !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.3) !important;
    }
    
    button[kind="primary"]:hover {
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.6) !important;
        transform: translateY(-3px) !important;
    }
    
    button[kind="primary"]:active {
        transform: translateY(-1px) !important;
    }
    
    /* Container cards */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: linear-gradient(135deg, #1a2a3a 0%, #0f1f2e 100%) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1) !important;
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a2a3a 0%, #0f1f2e 100%) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 15px !important;
        padding: 2rem 1.5rem !important;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.15) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="metric-container"]:hover {
        box-shadow: 0 12px 48px rgba(0, 212, 255, 0.25) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Info box */
    .stInfo {
        background: linear-gradient(135deg, #0f3a4a 0%, #1a2535 100%) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.15) !important;
        color: #e0e0e0 !important;
    }
    
    /* Data frame styling */
    [data-testid="stDataFrame"] {
        border: 2px solid #00d4ff !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1) !important;
    }
    
    /* Divider */
    hr {
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        margin: 2rem 0 !important;
    }
    
    /* Form styling */
    .stForm {
        border: none !important;
        padding: 0 !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f1419;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00d4ff 0%, #0099ff 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #0099ff 0%, #0066ff 100%);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# MODEL LOADING
# ============================================
MODEL_PATH = Path(__file__).resolve().parent / "boston_extra_trees_model.pkl"

@st.cache_resource
def load_model():
    """Load the trained model with error handling"""
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except FileNotFoundError:
        st.error(f"❌ Model file not found at: {MODEL_PATH}")
        st.error("Make sure 'boston_extra_trees_model.pkl' is in the same directory.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

model = load_model()

# ============================================
# MAIN CONTENT
# ============================================
if model is not None:
    # Header section
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.title("🏠 Boston Housing Price Predictor")
        st.markdown("### Predict median home values using Machine Learning")
    
    with col2:
        st.markdown("""
        <div style='text-align: right; padding-top: 1rem;'>
        <p style='color: #00d4ff; font-size: 0.9rem; font-weight: 600;'>
        📊 Powered by Extra Trees Regressor
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Introduction section
    with st.container():
        st.markdown("""
        **Welcome!** Adjust the three key features below to predict Boston residential property values.
        
        The model considers:
        - **RM**: Average number of rooms (affects property size and value)
        - **LSTAT**: % of lower status population (affects neighborhood quality)
        - **PTRATIO**: Pupil-teacher ratio (indicates school quality)
        """)
    
    st.markdown("---")
    
    # ============================================
    # SIDEBAR FORM (prevents re-run on slider movement)
    # ============================================
    with st.sidebar:
        st.header("Input Features")
        st.markdown("Adjust the values below to make a prediction")
        
        with st.form("prediction_form"):
            # Create input sliders
            rm = st.slider(
                "RM - Average number of rooms",
                min_value=3.0,
                max_value=9.0,
                value=6.5,
                step=0.1,
                help="Range: 3-9 rooms per dwelling"
            )
            
            lstat = st.slider(
                "LSTAT - Lower status population %",
                min_value=1.0,
                max_value=37.0,
                value=12.0,
                step=0.1,
                help="Range: 1-37% of population"
            )
            
            ptratio = st.slider(
                "PTRATIO - Pupil-teacher ratio",
                min_value=12.0,
                max_value=22.0,
                value=15.3,
                step=0.1,
                help="Range: 12-22 students per teacher"
            )
            
            st.markdown("---")
            
            # Submit button
            submit_button = st.form_submit_button(
                "🔮 PREDICT PRICE",
                use_container_width=True
            )
    
    # ============================================
    # RESERVED SPACE FOR RESULTS (prevents layout shift)
    # ============================================
    results_container = st.container()
    
    # Example data section (stays in place)
    st.markdown("---")
    st.subheader("📊 Data Range Reference")
    
    example_data = pd.DataFrame({
        'Feature': ['RM', 'LSTAT', 'PTRATIO', 'MEDV (Target)'],
        'Min': [3.56, 1.73, 12.6, 5.0],
        'Max': [8.78, 37.97, 22.0, 50.0],
        'Mean': [6.28, 12.65, 18.46, 22.53],
        'Current Input': [f"{rm:.2f}", f"{lstat:.2f}", f"{ptratio:.2f}", "..."]
    })
    
    st.dataframe(
        example_data,
        use_container_width=True,
        hide_index=True
    )
    
    # ============================================
    # DISPLAY RESULTS IN RESERVED CONTAINER
    # ============================================
    if submit_button:
        with results_container:
            st.subheader("✨ Prediction Results")
            
            # Create input DataFrame
            input_features = pd.DataFrame(
                [[rm, lstat, ptratio]],
                columns=['RM', 'LSTAT', 'PTRATIO']
            )
            
            # Make prediction
            prediction = model.predict(input_features)[0]
            
            # Display metrics in columns
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.metric(
                    label="RM (Rooms)",
                    value=f"{rm:.1f}",
                    delta="Rooms per dwelling"
                )
            
            with metric_col2:
                st.metric(
                    label="LSTAT (%)",
                    value=f"{lstat:.1f}",
                    delta="Lower status population"
                )
            
            with metric_col3:
                st.metric(
                    label="PTRATIO",
                    value=f"{ptratio:.1f}",
                    delta="Students per teacher"
                )
            
            st.divider()
            
            # Price prediction display
            predicted_price = prediction * 1000
            
            col_price1, col_price2 = st.columns([0.6, 0.4])
            
            with col_price1:
                st.markdown(f"""
                ### 💰 Predicted Home Value
                ## ${predicted_price:,.0f}
                
                *Based on your input parameters*
                """)
            
            with col_price2:
                st.info(f"""
                **Raw Model Output:** ${prediction:.2f}k
                
                **Confidence Level:** High
                **Model:** Extra Trees (100 trees)
                """)
            
            # Detailed interpretation
            st.markdown("---")
            st.markdown("### 📋 Prediction Details")
            
            interpretation = f"""
            Based on the input parameters:
            
            - **{rm} rooms** indicates a {'larger' if rm > 6.5 else 'smaller'} property
            - **{lstat:.1f}% lower status population** suggests a {'lower-income' if lstat > 15 else 'higher-income'} neighborhood
            - **{ptratio:.1f} pupil-teacher ratio** indicates {'better' if ptratio < 18 else 'lower'} school quality
            
            The model predicts a median home value of **${predicted_price:,.0f}** in 1990 dollars.
            """
            
            st.markdown(interpretation)
            
            # Success message
            st.success("✅ Prediction completed successfully!")
    else:
        # Show placeholder when no prediction yet
        with results_container:
            st.info("👆 Adjust the sliders and click 'PREDICT PRICE' to see results here")

else:
    st.error("❌ Unable to load the model. Please check the installation.")
    st.stop()
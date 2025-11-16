import streamlit as st
from PIL import Image
import numpy as np
import random
import time

# --- MOCK CLASSIFICATION LOGIC (Replace with your actual model) ---
def classify_endometrium(thickness_mm):
    """
    Simulates the model's classification based on thickness.
    
    In a real application:
    1. A segmentation model identifies the endometrium.
    2. Image processing measures the thickness (e.g., max distance).
    3. The classification is based on the measured thickness and possibly texture/pattern.
    """
    
    if thickness_mm is None:
        return "N/A", "Please run the analysis first."

    # Standard IVF/IUI Thresholds for demonstration:
    if thickness_mm >= 9.0 and thickness_mm <= 15.0:
        classification = "Receptive (9-15 mm)"
        color = "green"
    elif thickness_mm > 7.0 and thickness_mm < 9.0:
        classification = "Pre-Receptive (7-9 mm)"
        color = "orange"
    else: # thickness_mm < 7.0 or > 15.0
        classification = "Non-Receptive (<7 mm or >15 mm)"
        color = "red"
        
    return classification, color

# --- UI Setup and App Logic ---

# Set a dark, clean page config to match the user's screenshots
# This must be the first Streamlit command.
st.set_page_config(
    page_title="Endometrium Classifier",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply a custom dark theme to match the images
st.markdown("""
<style>
    /* Main background color (Dark Slate Gray/Navy) */
    .stApp {
        background-color: #0b1121; 
    }
    /* Main content container */
    .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    /* Title style */
    h1 {
        color: #e0f2f1; /* Light cyan */
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 0.5em;
    }
    /* Subheaders/Markdown */
    h2, .stMarkdown {
        color: #cccccc; /* Light gray for text */
    }
    /* Divider */
    hr {
        border-top: 1px solid #334155; /* Dark gray line */
    }
    /* File uploader background */
    .stFileUploader {
        background-color: #1e293b; /* Darker background for upload area */
        border-radius: 0.5rem;
        padding: 1rem;
        border: 2px dashed #475569; /* Dashed border */
    }
    /* Primary button color */
    .stButton>button {
        background-color: #6ee7b7; /* Light green/teal */
        color: #0b1121; /* Dark text */
        font-weight: bold;
        border: none;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #34d399; /* Slightly darker green on hover */
    }
</style>
""", unsafe_allow_html=True)


st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: #6ee7b7; font-size: 2.2em;">
            🩺 Endometrium Thickness & Receptivity Classifier
        </h1>
        <p style="color: #94a3b8; font-size: 1.1em;">
            Upload a transvaginal ultrasound image to estimate endometrial thickness and predict receptivity phase.
        </p>
    </div>
    <hr>
    """, unsafe_allow_html=True
)

# --- State Variables ---
if 'thickness' not in st.session_state:
    st.session_state['thickness'] = None
if 'processed_image' not in st.session_state:
    st.session_state['processed_image'] = None

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload an Ultrasound Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the file
    try:
        image = Image.open(uploaded_file)
        
        # Display uploaded image centered (simulating the top image in the screenshots)
        st.markdown("<h3 style='color:#a3e635; text-align: center;'>Uploaded Image</h3>", unsafe_allow_html=True)
        st.image(image, use_column_width=True)
        
        # --- Analysis Button ---
        if st.button("Analyze Endometrium", type="primary"):
            with st.spinner('Running segmentation and thickness measurement...'):
                time.sleep(2) # Simulate processing time

                # 1. MOCK MEASUREMENT (Replace this with your model output)
                # Generate a plausible thickness based on the Receptive/Pre-Receptive range from screenshots
                mock_thickness = round(random.uniform(6.5, 12.5), 2)
                
                st.session_state['thickness'] = mock_thickness
                
                # 2. MOCK PROCESSED IMAGE (Simulate the segmentation output)
                # Create a placeholder image to simulate segmentation output
                processed_array = np.array(image.convert("RGB"))
                
                # Simple darkening and central red box to mimic the segmentation mask
                processed_array = (processed_array * 0.7).astype(np.uint8) 
                
                # Dynamic mask area calculation (relative to image size)
                h, w, _ = processed_array.shape
                # Define a central ellipse-like area for the mask
                center_h, center_w = h // 2, w // 2
                mask_h = h // 6
                mask_w = w // 5
                
                processed_array[center_h - mask_h:center_h + mask_h, center_w - mask_w:center_w + mask_w] = [255, 50, 50] # Bright red color
                
                st.session_state['processed_image'] = Image.fromarray(processed_array)

            st.success("Analysis complete!")
            # Use st.rerun() to immediately display results after the button press
            st.rerun() 

    except Exception as e:
        st.error(f"Error loading or processing image: {e}")
        st.session_state['thickness'] = None
        st.session_state['processed_image'] = None


# --- Results Section ---
if st.session_state['thickness'] is not None and st.session_state['processed_image'] is not None:
    
    thickness = st.session_state['thickness']
    classification, color = classify_endometrium(thickness)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("## Analysis Results")
    
    # Use st.container for better visual grouping of the results
    with st.container(border=True):

        # Display the metrics first
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Estimated Endometrial Thickness", 
                value=f"{thickness:.2f} mm"
            )
        with col2:
            # Custom HTML for Classification metric to control text color
            st.markdown(
                f"""
                <div style="
                    padding: 10px; 
                    border-radius: 8px; 
                    border: 2px solid #475569; 
                    background-color: #1e293b;
                    height: 98px; /* Ensure equal height with st.metric */
                ">
                    <p style="
                        font-size: 1em; 
                        margin: 0; 
                        color: #94a3b8;
                    ">Classification</p>
                    <p style="
                        font-size: 1.5em; 
                        font-weight: bold; 
                        margin-top: 5px; 
                        color: {color};
                    ">{classification}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Display the processed image with simulated segmentation mask
        st.markdown(
            """
            <br>
            <h3 style='color:#a3e635; text-align: center; font-size: 1.3em;'>
                Segmented Endometrium (Model Output)
            </h3>
            """, unsafe_allow_html=True)
            
        st.image(st.session_state['processed_image'], caption="Simulated Segmentation and Thickness Measurement", use_column_width=True)
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F


# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AmITheAsshole?",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CUSTOM CSS STYLING ---
custom_css = """
<style>
    /* --- Global Theme Overrides (Forcing Dark Mode look) --- */
    [data-testid="stAppViewContainer"] {
        background-color: #121212; /* Very dark background for whole page */
        color: #E0E0E0; /* Light gray text usually */
    }
    [data-testid="stHeader"] {
        background-color: transparent; /* Hide the default Streamlit header bar */
    }
    /* Change standard label colors to light gray */
    .st-emotion-cache-1631y5f p, label, .st-emotion-cache-1631y5f {
         color: #B0B0B0 !important;
    }
    /* Main Titles H1 and H2 color to white */
    h1, h2, h3 {
        color: white !important;
    }

    /* --- The "Confessional" Card Container --- */
    /* We will wrap our form in a div with this class */
    .confessional-card {
        background-color: #1E1E1E; /* Slightly lighter dark gray for card */
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
        margin-top: 20px;
        border: 1px solid #333;
    }
    .card-header {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        color: white;
    }

    /* --- Styling Inputs (Text Input and Text Area) --- */
    /* We target the internal divs of Streamlit inputs to change their color */
    div[data-baseweb="input"] > div, textarea {
        background-color: #2D2D2D !important; /* Dark input background */
        border: 1px solid #444444 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    /* Placeholder text color */
    ::placeholder {
        color: #757575 !important;
    }
    /* Character count text color */
    .st-emotion-cache-1ae4d78 {
        color: #757575 !important;
    }

    /* --- The "DELIVER THE VERDICT" Button --- */
    /* Target the button to make it orange, big, and full width */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF4500 0%, #FF2E00 100%); /* Vibrant Orange gradient */
        color: white !important;
        font-weight: 800; /* Extra Bold */
        font-size: 20px !important;
        text-transform: uppercase;
        border: none;
        border-radius: 8px;
        padding-top: 18px !important;
        padding-bottom: 18px !important;
        margin-top: 20px;
        box-shadow: 0px 5px 15px rgba(255, 69, 0, 0.3);
        transition: all 0.3s ease;
    }
    /* Hover effect for the button */
    div.stButton > button:hover {
        box-shadow: 0px 8px 20px rgba(255, 69, 0, 0.5);
        transform: translateY(-2px);
    }
</style>
"""
# Inject the CSS
st.markdown(custom_css, unsafe_allow_html=True)

# --- 3. LOAD REAL MODEL ---
@st.cache_resource
def load_model():
    # 1. Point to the folder where you put model.safetensors AND config.json
    model_path = "./my_model" 
    
    try:
        # Load Tokenizer (Converts text to numbers)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        # Load Model (The safetensors weights)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        
        return tokenizer, model
    except OSError:
        st.error(f" Could not find model files in '{model_path}'. Make sure model.safetensors AND config.json are there.")
        return None, None

tokenizer, model = load_model()

# --- 4. APP LAYOUT ---

# Header Section (Gavel icon and titles)
col1, col2 = st.columns([1, 7])
with col1:
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>⚖️</h1>", unsafe_allow_html=True)
with col2:
    st.markdown("""
        <h2 style='margin-bottom: 0px;'>Are you the asshole?</h2>
    """, unsafe_allow_html=True)

# Input 1: Headline
headline = st.text_input(
    "The Conflict Headline (Keep it punchy)",
    placeholder="e.g., AITA for eating my roommate's food without asking?",
    max_chars=300,
    key="heading_input"
)

# Input 2: Story (Text Area)
story = st.text_area(
    "The Evidence (Give us all the details)",
    placeholder="Start typing your story here. Context is necessary...",
    height=250,
    max_chars=5000,
    key="body_input"
)

# Logic Button
if st.button("DELIVER THE VERDICT"):
    if not headline or not story:
        st.warning("Please provide both a headline and the evidence.")
    elif model is None:
        st.error("Model files not found. Check your 'my_model' folder.")
    else:
        with st.spinner("The Jury is deliberating..."):
            # Prepare text
            full_text = f"{headline} {story}"
            inputs = tokenizer(full_text, return_tensors="pt", truncation=True, max_length=512)
            
            # Predict
            with torch.no_grad():
                outputs = model(**inputs)
            
            # Math: Convert raw numbers to Probabilities (0 to 1)
            probabilities = F.softmax(outputs.logits, dim=-1)
            
            # Get the top label and its score
            top_score, top_label_id = torch.max(probabilities, dim=-1)
            score_value = top_score.item()
            label_id = top_label_id.item()

            # --- SMART LOGIC ---
            
            if score_value < 0.60:
                # Case 3: Ambiguous / Not Enough Info
                st.warning("### ⚠️ Verdict: Not Enough Information")
                st.write(f"The AI is conflicted (Confidence: {score_value:.1%}). Please add more details.")
            elif label_id == 1:
                # Case 1: YTA
                st.error(f"### 🛑 Verdict: You're The Asshole (YTA)")
                st.write(f"Confidence: {score_value:.1%}")
            else:
                # Case 2: NTA (label_id == 0)
                st.success(f"### ✅ Verdict: Not The Asshole (NTA)")
                st.write(f"Confidence: {score_value:.1%}")
# We close the custom HTML div
st.markdown('</div>', unsafe_allow_html=True)


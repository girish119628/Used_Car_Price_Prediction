'''
import streamlit as st
import joblib
import pandas as pd

# Load trained ML pipeline
pipeline = joblib.load("models/car_price_pipeline.pkl")

# Page title
st.title("Used Car Price Prediction")

# User inputs
brand = st.text_input("Enter Brand")

vehicle_age = st.number_input(
    "Vehicle Age",
    min_value=0,
    max_value=30,
    value=5
)

km_driven = st.number_input(
    "Kilometers Driven",
    min_value=0,
    value=50000
)

seller_type = st.text_input("Seller Type")

fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])

transmission_type = st.selectbox("Transmission Type", ["Manual", "Automatic"])

mileage = st.number_input(
    "Mileage",
    min_value=0.0,
    value=20.0
)

engine = st.number_input(
    "Engine (CC)",
    min_value=0.0,
    value=1200.0
)

max_power = st.number_input(
    "Max Power (bhp)",
    min_value=0.0,
    value=80.0
)

seats = st.number_input(
    "Number of Seats",
    min_value=1,
    max_value=10,
    value=5
)

if st.button("Predict Price"):

    input_data = pd.DataFrame({
        "brand": [brand],
        "vehicle_age": [vehicle_age],
        "km_driven": [km_driven],
        "seller_type": [seller_type],
        "fuel_type": [fuel_type],
        "transmission_type": [transmission_type],
        "mileage": [mileage],
        "engine": [engine],
        "max_power": [max_power],
        "seats": [seats]
    })

    prediction = pipeline.predict(input_data)

    st.success(
        f"Predicted Selling Price: ₹{prediction[0]:,.2f}"
    )
'''
'''
import streamlit as st
import joblib
import pandas as pd
from pathlib import Path
import base64
import textwrap

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AutoValue | Used Car Price Prediction",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "car_price_pipeline.pkl"

DATA_PATH = (
    BASE_DIR
    / "data"
    / "cleaned_data"
    / "cleaned_cars.csv"
)

BACKGROUND_IMAGE = (
    BASE_DIR
    / "assets"
    / "car_background.jpg"
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    return joblib.load(MODEL_PATH)


pipeline = load_model()


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(DATA_PATH)


df = load_data()


# ============================================================
# GET CATEGORIES FROM DATASET
# ============================================================

brands = sorted(
    df["brand"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

seller_types = sorted(
    df["seller_type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

fuel_types = sorted(
    df["fuel_type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

transmission_types = sorted(
    df["transmission_type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


# ============================================================
# SESSION STATE
# ============================================================

if "theme" not in st.session_state:

    st.session_state.theme = "dark"


if "prediction" not in st.session_state:

    st.session_state.prediction = None


# ============================================================
# THEME
# ============================================================

theme = st.session_state.theme

if theme == "dark":

    background = "#07111f"
    card_background = "rgba(10, 23, 40, 0.90)"
    input_background = "#111f32"
    text_color = "#f5f7fb"
    secondary_text = "#9ba8bb"
    border_color = "#263850"
    accent = "#4f7cff"
    accent_2 = "#7b2cff"

else:

    background = "#f5f8fc"
    card_background = "rgba(255, 255, 255, 0.94)"
    input_background = "#ffffff"
    text_color = "#172033"
    secondary_text = "#657086"
    border_color = "#dce3ed"
    accent = "#2867f0"
    accent_2 = "#6246ea"


# ============================================================
# CUSTOM CSS
# ============================================================

background_style = ""

if BACKGROUND_IMAGE.exists():

    background_style = f"""
    .stApp {{
        background:
            linear-gradient(
                90deg,
                rgba(7, 17, 31, 0.98) 0%,
                rgba(7, 17, 31, 0.92) 48%,
                rgba(7, 17, 31, 0.35) 100%
            ),
            url("file:///{BACKGROUND_IMAGE.as_posix()}");
            # url("{BACKGROUND_IMAGE}");


        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    """

else:

    background_style = f"""
    .stApp {{
        background: {background};
    }}
    """


st.markdown(
    f"""
    <style>

    {background_style}

    /* =========================
       GLOBAL
       ========================= */

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }}

    h1, h2, h3, h4, p, label {{
        color: {text_color} !important;
    }}

    /* =========================
       SIDEBAR
       ========================= */

    [data-testid="stSidebar"] {{

        background:
            linear-gradient(
                180deg,
                rgba(5, 14, 27, 0.98),
                rgba(9, 21, 37, 0.98)
            );

        border-right: 1px solid {border_color};
    }}

    .brand-logo {{

        font-size: 28px;
        font-weight: 800;
        line-height: 1.0;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }}

    .brand-logo span {{
        color: #4f7cff;
    }}

    .brand-tagline {{

        color: #9ba8bb;
        font-size: 13px;
        line-height: 1.5;
        margin-bottom: 35px;
    }}

    .sidebar-section {{

        color: #9ba8bb;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 25px;
        margin-bottom: 12px;
    }}

    /* =========================
       PAGE HEADER
       ========================= */

    .page-title {{

        font-size: 46px;
        font-weight: 800;
        letter-spacing: -2px;
        line-height: 1.1;
        margin-bottom: 5px;
    }}

    .page-subtitle {{

        color: #4f7cff;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .page-description {{

        color: {secondary_text};
        font-size: 15px;
        margin-bottom: 25px;
    }}

    /* =========================
       CARDS
       ========================= */

    .custom-card {{

        background: {card_background};

        border: 1px solid {border_color};

        border-radius: 18px;

        padding: 28px;

        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.15);

        backdrop-filter: blur(12px);
    }}

    .section-title {{

        font-size: 17px;
        font-weight: 700;

        color: #4f7cff !important;

        margin-bottom: 18px;
    }}

    /* =========================
       INPUTS
       ========================= */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {{

        background-color: {input_background} !important;

        border-color: {border_color} !important;

        border-radius: 9px !important;
    }}

    input {{

        color: {text_color} !important;
    }}

    /* =========================
       BUTTON
       ========================= */

    .stButton > button {{

        border: none !important;

        border-radius: 9px !important;

        min-height: 48px;

        font-weight: 700;

        background:
            linear-gradient(
                90deg,
                {accent},
                {accent_2}
            ) !important;

        color: white !important;

        transition: all 0.2s ease;
    }}

    .stButton > button:hover {{

        transform: translateY(-2px);

        box-shadow:
            0 8px 25px rgba(79, 124, 255, 0.30);
    }}

    /* =========================
       RESULT CARD
       ========================= */

    .result-card {{

        background: {card_background};

        border: 1px solid {border_color};

        border-radius: 18px;

        padding: 32px;

        text-align: center;

        min-height: 420px;

        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.18);

        backdrop-filter: blur(12px);
    }}

    .result-label {{

        color: #32d583;

        font-size: 13px;

        font-weight: 800;

        letter-spacing: 1px;

        text-transform: uppercase;
    }}

    .result-price {{

        color: #32d583;

        font-size: 42px;

        font-weight: 800;

        margin-top: 12px;

        margin-bottom: 5px;
    }}

    .result-caption {{

        color: {secondary_text};

        font-size: 13px;

        margin-bottom: 28px;
    }}

    .metric-box {{

        border-top: 1px solid {border_color};

        padding: 16px 0;

        display: flex;

        justify-content: space-between;

        color: {secondary_text};
    }}

    .metric-value {{

        color: {text_color};

        font-weight: 700;
    }}

    .disclaimer {{

        color: {secondary_text};

        font-size: 11px;

        text-align: center;

        margin-top: 20px;

        line-height: 1.5;
    }}

    /* =========================
       MOBILE
       ========================= */

    @media (max-width: 900px) {{

        .page-title {{
            font-size: 34px;
        }}

        .result-price {{
            font-size: 34px;
        }}

    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-logo">
            AUTO <span>VALUE</span>
        </div>

        <div class="brand-tagline">
            Smart Pricing.<br>
            Better Decisions.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">Navigation</div>',
        unsafe_allow_html=True
    )

    st.markdown("**Price Prediction**")

    st.markdown("**About Model**")

    st.markdown("**How It Works**")

    st.markdown("**Disclaimer**")

    st.markdown("---")

    st.markdown(
        """
        <div style="
            border:1px solid #263850;
            border-radius:12px;
            padding:16px;
            margin-top:25px;
        ">

        <div style="
            color:#7b6cff;
            font-weight:700;
            font-size:13px;
        ">
        AI-Powered
        </div>

        <div style="
            color:#9ba8bb;
            font-size:11px;
            margin-top:5px;
        ">
        Accurate • Fast • Reliable
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TOP HEADER + THEME SWITCH
# ============================================================

header_col, theme_col = st.columns([7, 1])

with header_col:

    st.markdown(
        """
        <div class="page-title">
            Used Car Price Prediction
        </div>

        <div class="page-subtitle">
            AI-Powered Price Estimation
        </div>

        <div class="page-description">
            Estimate the market value of your used car using
            machine learning in seconds.
        </div>
        """,
        unsafe_allow_html=True
    )


with theme_col:

    st.write("")

    if theme == "dark":

        if st.button("☀️ Light", use_container_width=True):

            st.session_state.theme = "light"

            st.rerun()

    else:

        if st.button("🌙 Dark", use_container_width=True):

            st.session_state.theme = "dark"

            st.rerun()


# ============================================================
# MAIN LAYOUT
# ============================================================

input_col, result_col = st.columns(
    [1.45, 0.85],
    gap="large"
)


# ============================================================
# INPUT SECTION
# ============================================================

with input_col:

    st.markdown(
        """
        <div class="custom-card">

        <div class="section-title">
            CAR DETAILS
        </div>

        """,
        unsafe_allow_html=True
    )

    # -----------------------------
    # ROW 1
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        brand_options = brands + ["Other / Custom Brand"]

        selected_brand = st.selectbox(
            "Brand",
            brand_options,
            index=0
        )

        if selected_brand == "Other / Custom Brand":

            brand = st.text_input(
                "Enter Brand",
                placeholder="Enter brand name"
            )

        else:

            brand = selected_brand

    with col2:

        vehicle_age = st.number_input(
            "Vehicle Age (Years)",
            min_value=0,
            max_value=30,
            value=3,
            step=1
        )

    # -----------------------------
    # ROW 2
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        km_driven = st.number_input(
            "Kilometers Driven",
            min_value=0,
            value=50000,
            step=1000
        )

    with col2:

        seller_type = st.selectbox(
            "Seller Type",
            seller_types
        )

    # -----------------------------
    # ROW 3
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        fuel_type = st.selectbox(
            "Fuel Type",
            fuel_types
        )

    with col2:

        transmission_type = st.selectbox(
            "Transmission",
            transmission_types
        )

    # -----------------------------
    # ROW 4
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        mileage = st.number_input(
            "Mileage (km/l)",
            min_value=0.0,
            value=20.0,
            step=0.1
        )

    with col2:

        engine = st.number_input(
            "Engine (CC)",
            min_value=0.0,
            value=1200.0,
            step=100.0
        )

    # -----------------------------
    # ROW 5
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        max_power = st.number_input(
            "Max Power (bhp)",
            min_value=0.0,
            value=80.0,
            step=1.0
        )

    with col2:

        seats = st.number_input(
            "Number of Seats",
            min_value=1,
            max_value=10,
            value=5,
            step=1
        )

    st.write("")

    predict_button = st.button(
        "Estimate Price  →",
        use_container_width=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# PREDICTION
# ============================================================

if predict_button:

    if not brand.strip():

        st.error("Please enter a brand.")

    else:

        input_data = pd.DataFrame({

            "brand": [brand],

            "vehicle_age": [vehicle_age],

            "km_driven": [km_driven],

            "seller_type": [seller_type],

            "fuel_type": [fuel_type],

            "transmission_type": [transmission_type],

            "mileage": [mileage],

            "engine": [engine],

            "max_power": [max_power],

            "seats": [seats]
        })

        prediction = pipeline.predict(input_data)

        st.session_state.prediction = float(
            prediction[0]
        )


# ============================================================
# RESULT SECTION
# ============================================================

with result_col:

    prediction = st.session_state.prediction

    if prediction is None:

        st.markdown(
            """
            <div class="result-card">

                <div class="result-label">
                    ESTIMATED SELLING PRICE
                </div>

                <div style="
                    font-size:22px;
                    font-weight:700;
                    margin-top:35px;
                    color:#9ba8bb;
                ">
                    Enter vehicle details
                </div>

                <div class="result-caption">
                    Your estimated market value
                    will appear here.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        # Indicative range only.
        # This is NOT a model confidence interval.
        lower_price = prediction * 0.90
        upper_price = prediction * 1.10

        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-label">
                    ESTIMATED SELLING PRICE
                </div>

                <div class="result-price">
                    ₹{prediction:,.0f}
                </div>

                <div class="result-caption">
                    Machine-learning based price estimate
                </div>

                <div class="metric-box">

                    <span>
                        Indicative Price Range
                    </span>

                    <span class="metric-value">
                        ₹{lower_price:,.0f}
                        -
                        ₹{upper_price:,.0f}
                    </span>

                </div>

                <div class="metric-box">

                    <span>
                        Vehicle Age
                    </span>

                    <span class="metric-value">
                        {vehicle_age} years
                    </span>

                </div>

                <div class="metric-box">

                    <span>
                        Kilometers Driven
                    </span>

                    <span class="metric-value">
                        {km_driven:,} km
                    </span>

                </div>

                <div class="metric-box">

                    <span>
                        Fuel / Transmission
                    </span>

                    <span class="metric-value">
                        {fuel_type} / {transmission_type}
                    </span>

                </div>

                <div class="disclaimer">

                    * The price range shown above is an
                    indicative ±10% range around the model
                    prediction, not a statistical confidence
                    interval. Actual market prices may vary.

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )'''

import streamlit as st
import joblib
import pandas as pd
from pathlib import Path
import base64
import textwrap


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AutoValue | Used Car Price Prediction",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "car_price_pipeline.pkl"

DATA_PATH = (
    BASE_DIR
    / "data"
    / "cleaned_data"
    / "cleaned_cars.csv"
)

ASSETS_DIR = BASE_DIR / "assets"


# ============================================================
# FIND BACKGROUND IMAGE
# ============================================================

background_image = None

for extension in [".png", ".jpg", ".jpeg", ".webp"]:

    possible_image = ASSETS_DIR / f"car_background{extension}"

    if possible_image.exists():

        background_image = possible_image

        break


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    return joblib.load(MODEL_PATH)


pipeline = load_model()


# ============================================================
# LOAD CLEANED DATA
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(DATA_PATH)


df = load_data()


# ============================================================
# GET CATEGORIES FROM DATASET
# ============================================================

brands = sorted(
    df["brand"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


seller_types = sorted(
    df["seller_type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


fuel_types = sorted(
    df["fuel_type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


transmission_types = sorted(
    df["transmission_type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


# ============================================================
# SESSION STATE
# ============================================================

if "theme" not in st.session_state:

    st.session_state.theme = "dark"


if "prediction" not in st.session_state:

    st.session_state.prediction = None


if "prediction_details" not in st.session_state:

    st.session_state.prediction_details = None


# ============================================================
# THEME SETTINGS
# ============================================================

if st.session_state.theme == "dark":

    background_color = "#07111f"

    card_background = "rgba(8, 22, 39, 0.92)"

    input_background = "#151a25"

    text_color = "#f5f7fb"

    secondary_text = "#9ba8bb"

    border_color = "#263850"

    accent = "#4f7cff"

    accent_secondary = "#7b2cff"

else:

    background_color = "#f4f7fb"

    card_background = "rgba(255, 255, 255, 0.94)"

    input_background = "#ffffff"

    text_color = "#172033"

    secondary_text = "#667085"

    border_color = "#dce3ed"

    accent = "#2867f0"

    accent_secondary = "#6246ea"


# ============================================================
# BACKGROUND IMAGE
# ============================================================

if background_image is not None:

    with open(background_image, "rb") as image_file:

        image_base64 = base64.b64encode(
            image_file.read()
        ).decode()

    image_type = background_image.suffix.lower().replace(".", "")

    if image_type == "jpg":
        image_type = "jpeg"

    background_style = f"""
    .stApp {{
        background-image:
            linear-gradient(
                90deg,
                rgba(7, 17, 31, 0.98) 0%,
                rgba(7, 17, 31, 0.93) 35%,
                rgba(7, 17, 31, 0.72) 60%,
                rgba(7, 17, 31, 0.30) 100%
            ),
            url("data:image/{image_type};base64,{image_base64}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    """

else:

    background_style = f"""
    .stApp {{
        background: {background_color};
    }}
    """


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    {background_style}


    /* ========================================================
       GLOBAL
       ======================================================== */

    .block-container {{

        padding-top: 2rem;
        padding-bottom: 3rem;

        max-width: 1450px;
    }}


    h1, h2, h3, h4, h5, h6 {{

        color: {text_color} !important;
    }}


    p, label {{

        color: {text_color} !important;
    }}


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {{

        background:
            linear-gradient(
                180deg,
                rgba(5, 14, 27, 0.99),
                rgba(7, 18, 32, 0.99)
            );

        border-right:
            1px solid {border_color};
    }}


    .brand-name {{

        font-size: 28px;

        font-weight: 800;

        letter-spacing: -1.2px;

        margin-top: 5px;

        margin-bottom: 5px;

        color: #ffffff;
    }}


    .brand-name span {{

        color: #4f7cff;
    }}


    .brand-tagline {{

        color: #9ba8bb;

        font-size: 13px;

        line-height: 1.6;

        margin-bottom: 38px;
    }}


    .sidebar-heading {{

        color: #7f8da3;

        font-size: 11px;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 1.4px;

        margin-bottom: 16px;
    }}


    .sidebar-item {{

        color: #f5f7fb;

        font-size: 14px;

        font-weight: 600;

        padding: 10px 0;
    }}


    .sidebar-divider {{

        border: none;

        border-top: 1px solid #263850;

        margin: 28px 0;
    }}


    .sidebar-info {{

        border:
            1px solid #263850;

        border-radius: 12px;

        padding: 16px;

        margin-top: 20px;

        background:
            rgba(10, 23, 40, 0.55);
    }}


    .sidebar-info-title {{

        color: #7b6cff;

        font-weight: 700;

        font-size: 13px;

        margin-bottom: 5px;
    }}


    .sidebar-info-text {{

        color: #9ba8bb;

        font-size: 11px;

        line-height: 1.5;
    }}


    /* ========================================================
       PAGE HEADER
       ======================================================== */

    .page-title {{

        color: {text_color};

        font-size: 46px;

        font-weight: 800;

        letter-spacing: -2.3px;

        line-height: 1.08;

        margin-bottom: 8px;
    }}


    .page-subtitle {{

        color: #4f7cff;

        font-size: 14px;

        font-weight: 800;

        letter-spacing: 1.8px;

        text-transform: uppercase;

        margin-bottom: 9px;
    }}


    .page-description {{

        color: {secondary_text};

        font-size: 15px;

        line-height: 1.6;

        margin-bottom: 25px;
    }}


    /* ========================================================
       THEME BUTTON
       ======================================================== */

    .theme-button > button {{

        min-height: 46px !important;

        border-radius: 10px !important;

        border: 1px solid {border_color} !important;

        background:
            linear-gradient(
                90deg,
                {accent},
                {accent_secondary}
            ) !important;

        color: #ffffff !important;

        font-weight: 700 !important;
    }}


    /* ========================================================
       MAIN CARDS
       ======================================================== */

    .custom-card {{

        background: {card_background};

        border:
            1px solid {border_color};

        border-radius: 18px;

        padding: 28px;

        box-shadow:
            0 18px 50px rgba(0, 0, 0, 0.18);

        backdrop-filter: blur(14px);
    }}


    .section-title {{

        color: #4f7cff !important;

        font-size: 16px;

        font-weight: 800;

        letter-spacing: 0.8px;

        text-transform: uppercase;

        margin-bottom: 22px;
    }}


    /* ========================================================
       STREAMLIT INPUTS
       ======================================================== */

    div[data-baseweb="input"] > div {{

        background-color:
            {input_background} !important;

        border-color:
            {border_color} !important;

        border-radius:
            9px !important;
    }}


    div[data-baseweb="select"] > div {{

        background-color:
            {input_background} !important;

        border-color:
            {border_color} !important;

        border-radius:
            9px !important;
    }}


    input {{

        color: {text_color} !important;
    }}


    [data-baseweb="select"] * {{

        color: {text_color} !important;
    }}


    /* ========================================================
       BUTTON
       ======================================================== */

    .predict-button > button {{

        min-height: 50px !important;

        border: none !important;

        border-radius: 10px !important;

        background:
            linear-gradient(
                90deg,
                {accent},
                {accent_secondary}
            ) !important;

        color: #ffffff !important;

        font-size: 15px !important;

        font-weight: 800 !important;

        letter-spacing: 0.2px;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }}


    .predict-button > button:hover {{

        transform: translateY(-2px);

        box-shadow:
            0 10px 30px rgba(79, 124, 255, 0.35);
    }}


    /* ========================================================
       RESULT CARD
       ======================================================== */

    .result-card {{

        background: {card_background};

        border:
            1px solid {border_color};

        border-radius: 18px;

        padding: 30px;

        min-height: 455px;

        box-shadow:
            0 18px 50px rgba(0, 0, 0, 0.18);

        backdrop-filter: blur(14px);
    }}


    .result-label {{

        color: #32d583;

        font-size: 12px;

        font-weight: 800;

        letter-spacing: 1.3px;

        text-transform: uppercase;

        text-align: center;
    }}


    .result-price {{

        color: #32d583;

        font-size: 42px;

        font-weight: 800;

        letter-spacing: -1.5px;

        text-align: center;

        margin-top: 13px;

        margin-bottom: 5px;
    }}


    .result-placeholder {{

        color: {secondary_text};

        font-size: 21px;

        font-weight: 700;

        text-align: center;

        margin-top: 55px;

        margin-bottom: 8px;
    }}


    .result-caption {{

        color: {secondary_text};

        font-size: 12px;

        line-height: 1.5;

        text-align: center;

        margin-bottom: 25px;
    }}


    .metric-box {{

        border-top:
            1px solid {border_color};

        padding:
            15px 0;

        display:
            flex;

        justify-content:
            space-between;

        gap: 15px;

        font-size: 12px;

        color: {secondary_text};
    }}


    .metric-value {{

        color: {text_color};

        font-weight: 700;

        text-align: right;
    }}


    .disclaimer {{

        color: {secondary_text};

        font-size: 10px;

        line-height: 1.5;

        text-align: center;

        margin-top: 17px;
    }}


    /* ========================================================
       ERROR / WARNING
       ======================================================== */

    .warning-box {{

        border:
            1px solid #8a6d1d;

        background:
            rgba(138, 109, 29, 0.12);

        border-radius: 10px;

        padding: 12px;

        color: #d6bd68;

        font-size: 12px;

        margin-top: 12px;
    }}


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 900px) {{

        .page-title {{

            font-size: 34px;

            letter-spacing: -1.5px;
        }}

        .result-price {{

            font-size: 34px;
        }}

    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-name">
            AUTO <span>VALUE</span>
        </div>

        <div class="brand-tagline">
            Smart Pricing.<br>
            Better Decisions.
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sidebar-heading">Navigation</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sidebar-item">Price Prediction</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sidebar-item">About Model</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sidebar-item">How It Works</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sidebar-item">Disclaimer</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<hr class="sidebar-divider">',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="sidebar-info">

            <div class="sidebar-info-title">
                Machine Learning
            </div>

            <div class="sidebar-info-text">
                Fast estimation based on
                vehicle specifications and
                historical pricing data.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

header_col, theme_col = st.columns(
    [7, 1],
    gap="large"
)


with header_col:

    st.markdown(
        """
        <div class="page-title">
            Used Car Price Prediction
        </div>

        <div class="page-subtitle">
            AI-Powered Price Estimation
        </div>

        <div class="page-description">
            Estimate the market value of a used vehicle
            using a machine learning model trained on
            historical vehicle data.
        </div>
        """,
        unsafe_allow_html=True
    )


with theme_col:

    st.write("")

    if st.session_state.theme == "dark":

        st.markdown(
            '<div class="theme-button">',
            unsafe_allow_html=True
        )

        if st.button(
            "Light Mode",
            use_container_width=True
        ):

            st.session_state.theme = "light"

            st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="theme-button">',
            unsafe_allow_html=True
        )

        if st.button(
            "Dark Mode",
            use_container_width=True
        ):

            st.session_state.theme = "dark"

            st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ============================================================
# MAIN LAYOUT
# ============================================================

input_col, result_col = st.columns(
    [1.45, 0.85],
    gap="large"
)


# ============================================================
# INPUT CARD
# ============================================================

with input_col:

    st.markdown(
        textwrap.dedent(
            """
            <div class="custom-card">

                <div class="section-title">
                    Car Details
                </div>

            """
        ),
        unsafe_allow_html=True
    )


    # ========================================================
    # ROW 1
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        brand_options = brands + [
            "Other / Custom Brand"
        ]

        selected_brand = st.selectbox(
            "Brand",
            brand_options,
            index=0
        )


        if selected_brand == "Other / Custom Brand":

            brand = st.text_input(
                "Enter Brand",
                placeholder="Enter brand name"
            )

        else:

            brand = selected_brand


    with col2:

        vehicle_age = st.number_input(
            "Vehicle Age (Years)",
            min_value=0,
            max_value=30,
            value=3,
            step=1
        )


    # ========================================================
    # ROW 2
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        km_driven = st.number_input(
            "Kilometers Driven",
            min_value=0,
            value=50000,
            step=1000
        )


    with col2:

        seller_type = st.selectbox(
            "Seller Type",
            seller_types
        )


    # ========================================================
    # ROW 3
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        fuel_type = st.selectbox(
            "Fuel Type",
            fuel_types
        )


    with col2:

        transmission_type = st.selectbox(
            "Transmission",
            transmission_types
        )


    # ========================================================
    # ROW 4
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        mileage = st.number_input(
            "Mileage (km/l)",
            min_value=0.0,
            value=20.0,
            step=0.1,
            format="%.1f"
        )


    with col2:

        engine = st.number_input(
            "Engine (CC)",
            min_value=0.0,
            value=1200.0,
            step=100.0,
            format="%.0f"
        )


    # ========================================================
    # ROW 5
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        max_power = st.number_input(
            "Max Power (bhp)",
            min_value=0.0,
            value=80.0,
            step=1.0,
            format="%.0f"
        )


    with col2:

        seats = st.number_input(
            "Number of Seats",
            min_value=1,
            max_value=10,
            value=5,
            step=1
        )


    st.write("")


    # ========================================================
    # PREDICT BUTTON
    # ========================================================

    st.markdown(
        '<div class="predict-button">',
        unsafe_allow_html=True
    )


    predict_button = st.button(
        "Estimate Selling Price",
        use_container_width=True
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# PREDICTION
# ============================================================

if predict_button:

    if not brand.strip():

        st.session_state.prediction = None

        st.session_state.prediction_details = None

        st.error(
            "Please enter a valid brand."
        )

    else:

        input_data = pd.DataFrame({

            "brand": [brand],

            "vehicle_age": [vehicle_age],

            "km_driven": [km_driven],

            "seller_type": [seller_type],

            "fuel_type": [fuel_type],

            "transmission_type": [transmission_type],

            "mileage": [mileage],

            "engine": [engine],

            "max_power": [max_power],

            "seats": [seats]
        })


        try:

            prediction = pipeline.predict(
                input_data
            )


            predicted_price = float(
                prediction[0]
            )


            st.session_state.prediction = (
                predicted_price
            )


            st.session_state.prediction_details = {

                "vehicle_age": vehicle_age,

                "km_driven": km_driven,

                "fuel_type": fuel_type,

                "transmission_type":
                    transmission_type
            }


        except Exception as error:

            st.session_state.prediction = None

            st.session_state.prediction_details = None

            st.error(
                "The model could not process this input."
            )

            st.warning(
                "If you entered a custom brand, the saved "
                "model may not support unseen brands. "
                "Check that the OneHotEncoder used during "
                "training has handle_unknown='ignore'."
            )


# ============================================================
# RESULT CARD
# ============================================================

with result_col:

    prediction = st.session_state.prediction


    # ========================================================
    # BEFORE PREDICTION
    # ========================================================

    if prediction is None:

        result_html = """
        <div class="result-card">

            <div class="result-label">
                Estimated Selling Price
            </div>

            <div class="result-placeholder">
                Enter vehicle details
            </div>

            <div class="result-caption">
                Your machine-learning based
                market estimate will appear here.
            </div>

        </div>
        """


        st.markdown(
            textwrap.dedent(result_html),
            unsafe_allow_html=True
        )


    # ========================================================
    # AFTER PREDICTION
    # ========================================================

    else:

        details = (
            st.session_state.prediction_details
        )


        # ----------------------------------------------------
        # INDICATIVE PRICE RANGE
        # ----------------------------------------------------
        #
        # IMPORTANT:
        # This is NOT a statistical confidence interval.
        # It is simply an indicative range around prediction.
        #

        lower_price = prediction * 0.90

        upper_price = prediction * 1.10


        result_html = f"""
        <div class="result-card">

            <div class="result-label">
                Estimated Selling Price
            </div>

            <div class="result-price">
                ₹{prediction:,.0f}
            </div>

            <div class="result-caption">
                Machine-learning based price estimate
            </div>


            <div class="metric-box">

                <span>
                    Indicative Price Range
                </span>

                <span class="metric-value">
                    ₹{lower_price:,.0f}
                    -
                    ₹{upper_price:,.0f}
                </span>

            </div>


            <div class="metric-box">

                <span>
                    Vehicle Age
                </span>

                <span class="metric-value">
                    {details["vehicle_age"]} years
                </span>

            </div>


            <div class="metric-box">

                <span>
                    Kilometers Driven
                </span>

                <span class="metric-value">
                    {details["km_driven"]:,} km
                </span>

            </div>


            <div class="metric-box">

                <span>
                    Fuel Type
                </span>

                <span class="metric-value">
                    {details["fuel_type"]}
                </span>

            </div>


            <div class="metric-box">

                <span>
                    Transmission
                </span>

                <span class="metric-value">
                    {details["transmission_type"]}
                </span>

            </div>


            <div class="disclaimer">

                The displayed range is an indicative
                ±10% range around the model prediction.
                It is not a statistical confidence interval.
                Actual market prices may vary.

            </div>

        </div>
        """


        st.markdown(
            textwrap.dedent(result_html),
            unsafe_allow_html=True
        )        
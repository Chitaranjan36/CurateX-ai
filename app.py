import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit.components.v1 as components
from io import BytesIO
import time
import random

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="CurateX AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SYSTEM ANNOUNCER
# =========================================================

def announce(message):

    components.html(f"""

    <script>

    const msg = new SpeechSynthesisUtterance();

    msg.text = "{message}";
    msg.rate = 1;
    msg.pitch = 0.9;
    msg.volume = 1;

    window.speechSynthesis.speak(msg);

    </script>

    """, height=0)

# =========================================================
# RUBY CUBE VIDEO LOADER
# =========================================================

loading = st.empty()

loading.markdown("""

<div id="ruby-loader">

<!-- Background Video -->

<video autoplay muted loop playsinline id="bg-video">
    <source src="https://cdn.pixabay.com/vimeo/328940142/digital-23315.mp4?width=1280&hash=4a8a5b6c4f1fcb2f8dfecfcf7f0d8cbf5f9c3c48" type="video/mp4">
</video>

<!-- Dark Overlay -->

<div class="overlay"></div>

<!-- Main Content -->

<div class="content">

<div class="scene">

<div class="cube">

<div class="face front"></div>
<div class="face back"></div>
<div class="face right"></div>
<div class="face left"></div>
<div class="face top"></div>
<div class="face bottom"></div>

</div>

</div>

<h1 class="loading-title">
🌐CurateX AI
</h1>

<p class="loading-sub">
INITIALIZING AI ...
</p>

</div>

</div>

<style>

/* Main Loader */

#ruby-loader{

position:fixed;
top:0;
left:0;

width:100%;
height:100%;

overflow:hidden;

z-index:999999;
}

/* Background Video */

#bg-video{

position:absolute;
top:0;
left:0;

width:100%;
height:100%;

object-fit:cover;

z-index:-3;
}

/* Overlay */

.overlay{

position:absolute;
top:0;
left:0;

width:100%;
height:100%;

background:
linear-gradient(
135deg,
rgba(0,0,0,0.82),
rgba(20,0,20,0.75),
rgba(0,0,0,0.9)
);

backdrop-filter:blur(3px);

z-index:-2;
}

/* Content */

.content{

position:relative;

width:100%;
height:100%;

display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
}

/* 3D Scene */

.scene{

width:160px;
height:160px;

perspective:900px;

margin-bottom:40px;
}

/* Cube */

.cube{

width:100%;
height:100%;

position:relative;

transform-style:preserve-3d;

animation:rotateCube 6s infinite linear;
}

/* Faces */

.face{

position:absolute;

width:160px;
height:160px;

background:rgba(255,0,90,0.10);

border:2px solid #ff0055;

box-shadow:
0 0 25px #ff0055,
inset 0 0 25px #ff0055;
}

/* Cube Sides */

.front{
transform:rotateY(0deg) translateZ(80px);
}

.back{
transform:rotateY(180deg) translateZ(80px);
}

.right{
transform:rotateY(90deg) translateZ(80px);
}

.left{
transform:rotateY(-90deg) translateZ(80px);
}

.top{
transform:rotateX(90deg) translateZ(80px);
}

.bottom{
transform:rotateX(-90deg) translateZ(80px);
}

/* Rotation */

@keyframes rotateCube{

0%{
transform:rotateX(0deg) rotateY(0deg);
}

100%{
transform:rotateX(360deg) rotateY(360deg);
}
}

/* Title */

.loading-title{

font-size:54px;
font-weight:900;

letter-spacing:4px;

color:#ff0055;

margin:0;

text-shadow:
0 0 10px #ff0055,
0 0 25px #ff0055,
0 0 50px #ff0055;

animation:pulseText 2s infinite;
}

/* Subtitle */

.loading-sub{

margin-top:18px;

font-size:18px;

font-family:monospace;

letter-spacing:6px;

color:white;

opacity:0.95;
}

/* Pulse */

@keyframes pulseText{

0%{
opacity:0.5;
transform:scale(1);
}

50%{
opacity:1;
transform:scale(1.05);
}

100%{
opacity:0.5;
transform:scale(1);
}
}

/* Mobile */

@media(max-width:768px){

.loading-title{
font-size:30px;
text-align:center;
}

.loading-sub{
font-size:13px;
letter-spacing:3px;
}

.scene{
width:120px;
height:120px;
}

.face{
width:120px;
height:120px;
}

.front{
transform:rotateY(0deg) translateZ(60px);
}

.back{
transform:rotateY(180deg) translateZ(60px);
}

.right{
transform:rotateY(90deg) translateZ(60px);
}

.left{
transform:rotateY(-90deg) translateZ(60px);
}

.top{
transform:rotateX(90deg) translateZ(60px);
}

.bottom{
transform:rotateX(-90deg) translateZ(60px);
}

}

</style>

""", unsafe_allow_html=True)

time.sleep(5)

loading.empty()
# =========================================================
# SOUND EFFECTS
# =========================================================

components.html("""

<!-- STARTUP SOUND -->
<audio id="startupSound" autoplay>
    <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mp3">
</audio>

<!-- SUCCESS SOUND -->
<audio id="successSound">
    <source src="https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3" type="audio/mp3">
</audio>

<!-- WARNING SOUND -->
<audio id="warningSound">
    <source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mp3">
</audio>

<!-- HOVER SOUND -->
<audio id="hoverSound">
    <source src="https://assets.mixkit.co/active_storage/sfx/1114/1114-preview.mp3" type="audio/mp3">
</audio>

<script>

// ======================================
// STARTUP SOUND
// ======================================

window.addEventListener('load', () => {

    const startup =
    document.getElementById("startupSound");

    startup.volume = 0.4;

   startup.play().catch(function(error){});

});

// ======================================
// BUTTON HOVER SOUND
// ======================================

setTimeout(() => {

    const buttons =
    parent.document.querySelectorAll("button");

    buttons.forEach(btn => {

        btn.addEventListener("mouseenter", () => {

            const hover =
            document.getElementById("hoverSound");

            hover.volume = 0.15;

            hover.currentTime = 0;

            hover.play();

        });

    });

}, 2000);

// ======================================
// GLOBAL FUNCTIONS
// ======================================

window.playSuccess = function(){

    const s =
    document.getElementById("successSound");

    s.volume = 0.4;

    s.currentTime = 0;

    s.play();
}

window.playWarning = function(){

    const w =
    document.getElementById("warningSound");

    w.volume = 0.5;

    w.currentTime = 0;

    w.play();
}

</script>

""", height=0)
# =========================================================
# AI LOGO
# =========================================================

st.markdown("""
<div style="
display:flex;
align-items:center;
gap:18px;
margin-bottom:20px;
">

<div style="
width:80px;
height:80px;
border-radius:20px;
background:linear-gradient(135deg,#00FFA3,#00c3ff);
display:flex;
align-items:center;
justify-content:center;
font-size:40px;
font-weight:bold;
color:black;
box-shadow:0 0 30px #00FFA3;
animation:pulseLogo 2s infinite;
">
⚡
</div>

<div>

<h1 style="
margin:0;
font-size:42px;
font-weight:900;
color:white;
">
🌐CurateX AI
</h1>

<p style="
margin:0;
color:#00FFA3;
letter-spacing:3px;
">
Created by Moirangthem Chitaranjan Singh
</p>

</div>

</div>

<style>

@keyframes pulseLogo{
0%{transform:scale(1);}
50%{transform:scale(1.08);}
100%{transform:scale(1);}
}

</style>
""", unsafe_allow_html=True)
st.markdown(f"""
<div class="glass float">

<h2 class="neon">🚀 CurateX AI Enterprise System</h2>

<p>
Advanced Artificial Intelligence Data Intelligence Platform
</p>

</div>
""", unsafe_allow_html=True)
# =========================================================
# DATA CLEANING FUNCTIONS
# =========================================================

def remove_duplicates(df):
    return df.drop_duplicates()

def fill_missing(df):

    numeric = df.select_dtypes(include='number').columns

    for col in numeric:
        df[col] = df[col].fillna(df[col].median())

    return df

def smart_fill(df):

    df_copy = df.copy()

    numeric_cols = df_copy.select_dtypes(include='number').columns

    for col in numeric_cols:

        if df_copy[col].isnull().sum() > 0:

            train = df_copy[df_copy[col].notnull()]
            test = df_copy[df_copy[col].isnull()]

            if len(train) < 2:
                continue

            X_train = train[numeric_cols].drop(columns=[col], errors='ignore')
            y_train = train[col]

            X_test = test[numeric_cols].drop(columns=[col], errors='ignore')

            X_train = X_train.fillna(0)
            X_test = X_test.fillna(0)

            if X_train.shape[1] == 0:
                continue

            model = LinearRegression()

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            df_copy.loc[df_copy[col].isnull(), col] = predictions

    return df_copy

def remove_outliers(df):

    numeric_cols = df.select_dtypes(include='number').columns

    for col in numeric_cols:

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df = df[
            (df[col] >= lower) &
            (df[col] <= upper)
        ]

    return df

def encode_categorical(df):

    encoder = LabelEncoder()

    cat_cols = df.select_dtypes(include='object').columns

    for col in cat_cols:

        df[col] = encoder.fit_transform(df[col].astype(str))

    return df

def data_quality_score(df):

    total = df.size

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    score = 100 - ((missing + duplicates) / total * 100)

    return max(0, round(score, 2))

# =========================================================
# MATRIX BACKGROUND
# =========================================================

components.html("""

<canvas id="matrix"></canvas>

<style>

#matrix{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
z-index:-1;
pointer-events:none;
opacity:0.12;
}

</style>

<script>

const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

canvas.height = window.innerHeight;
canvas.width = window.innerWidth;

const letters = "01アイウエオカキクケコABCDEFGHIJKLMNOPQRSTUVWXYZ";
const fontSize = 14;
const columns = canvas.width/fontSize;

const drops = [];

for(let i=0;i<columns;i++){
drops[i]=1;
}

function draw(){

ctx.fillStyle = "rgba(0,0,0,0.05)";
ctx.fillRect(0,0,canvas.width,canvas.height);

ctx.fillStyle="#00FFA3";
ctx.font=fontSize+"px monospace";

for(let i=0;i<drops.length;i++){

const text = letters[Math.floor(Math.random()*letters.length)];

ctx.fillText(text,i*fontSize,drops[i]*fontSize);

if(drops[i]*fontSize>canvas.height && Math.random()>0.975){
drops[i]=0;
}

drops[i]++;
}
}

setInterval(draw,33);

</script>

""", height=0)

# =========================================================
# SCANLINE EFFECT
# =========================================================

st.markdown("""
<style>

.scanline{

position:fixed;
top:0;
left:0;
width:100%;
height:6px;

background:linear-gradient(
90deg,
transparent,
#00FFA3,
transparent
);

z-index:9999;

animation:scanMove 4s linear infinite;
}

@keyframes scanMove{

0%{
top:0%;
}

100%{
top:100%;
}
}

</style>

<div class="scanline"></div>
""", unsafe_allow_html=True)

## =========================================================
# ULTRA FUTURISTIC UI
# =========================================================

st.markdown("""
<style>

/* =======================================================
GLOBAL
======================================================= */

html, body, [class*="css"]  {

    font-family: 'Segoe UI', sans-serif;
}

/* Main App */

.stApp {

    background:
    linear-gradient(
        135deg,
        #020617,
        #071426,
        #000000
    );

    color: white;
}

/* =======================================================
HEADINGS
======================================================= */

h1,h2,h3,h4,h5,h6 {

    color: white !important;
    font-weight: 800 !important;
}

/* =======================================================
SIDEBAR
======================================================= */

[data-testid="stSidebar"] {

    background: rgba(5,10,20,0.85);

    backdrop-filter: blur(20px);

    border-right: 1px solid rgba(255,255,255,0.08);
}

/* =======================================================
BUTTONS
======================================================= */

.stButton > button {

    width: 100%;

    border-radius: 18px;

    border: none;

    padding: 14px;

    font-size: 15px;

    font-weight: bold;

    color: black;

    background: linear-gradient(
        90deg,
        #00FFA3,
        #00c3ff
    );

    transition: 0.4s ease;
}

.stButton > button:hover {

    transform: scale(1.03);

    box-shadow:
    0 0 20px #00FFA3,
    0 0 50px #00c3ff;
}

/* =======================================================
DOWNLOAD BUTTON
======================================================= */

.stDownloadButton > button {

    width: 100%;

    border-radius: 18px;

    border: none;

    padding: 14px;

    font-weight: bold;

    color: black;

    background: linear-gradient(
        90deg,
        #00FFA3,
        #00c3ff
    );
}

/* =======================================================
INPUTS
======================================================= */

.stTextInput input,
.stNumberInput input,
.stSelectbox div {

    background-color: rgba(255,255,255,0.05) !important;

    color: white !important;

    border-radius: 12px !important;
}

/* =======================================================
DATAFRAME
======================================================= */

[data-testid="stDataFrame"] {

    border-radius: 20px;

    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
    0 0 20px rgba(0,255,163,0.1);
}

/* =======================================================
METRIC CARDS
======================================================= */

[data-testid="metric-container"] {

    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(255,255,255,0.08);

    padding: 15px;

    border-radius: 20px;

    backdrop-filter: blur(20px);

    box-shadow:
    0 0 25px rgba(0,255,163,0.12);

    transition: 0.3s;
}

[data-testid="metric-container"]:hover {

    transform: translateY(-5px);

    box-shadow:
    0 0 30px #00FFA3;
}

/* =======================================================
PLOTLY CHARTS
======================================================= */

.js-plotly-plot {

    border-radius: 20px;

    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
    0 0 20px rgba(0,255,163,0.12);
}

/* =======================================================
SCROLLBAR
======================================================= */

::-webkit-scrollbar {

    width: 10px;
}

::-webkit-scrollbar-thumb {

    background: #00FFA3;

    border-radius: 20px;
}

/* =======================================================
GLASS CARD
======================================================= */

.glass {

    background: rgba(255,255,255,0.05);

    backdrop-filter: blur(20px);

    border-radius: 24px;

    padding: 25px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
    0 0 30px rgba(0,255,163,0.12);

    margin-bottom: 20px;
}

/* =======================================================
NEON TITLE
======================================================= */

.neon {

    color: #00FFA3;

    text-shadow:
    0 0 10px #00FFA3,
    0 0 20px #00FFA3,
    0 0 40px #00FFA3;
}

/* =======================================================
FLOAT ANIMATION
======================================================= */

.float {

    animation: floating 4s ease-in-out infinite;
}

@keyframes floating {

    0% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-10px);
    }

    100% {
        transform: translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)
# =========================================================
# TYPING EFFECT
# =========================================================

components.html("""

<div id="typing"></div>

<script>

const text =
"BOSS I AM Waiting for Your Command";

let i = 0;

function type(){

if(i < text.length){

document.getElementById("typing").innerHTML += text.charAt(i);

i++;

setTimeout(type,50);

}
}

type();

</script>

<style>

#typing{

font-size:22px;
color:#00FFA3;
text-align:center;
font-family:monospace;
margin-bottom:20px;
letter-spacing:2px;
}

</style>

""", height=60)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
<div style="
background:linear-gradient(135deg,#00FFA3,#00c3ff);
padding:18px;
border-radius:18px;
text-align:center;
font-size:20px;
font-weight:bold;
color:black;
box-shadow:0 0 25px #00FFA3;
">
⚡ AI DATA CLEANER
</div>
""", unsafe_allow_html=True)

st.sidebar.success("🟢 KYANG MCS ONLINE")
# =========================================================
# THEME SWITCHER
# =========================================================
# =========================================================
# THEME SWITCHER
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🎨 THEME")

theme = st.sidebar.radio(
    "Select Theme",
    [
        "Cyberpunk",
        "Ocean",
        "Midnight"
    ]
)

if theme == "Ocean":

    st.markdown("""
    <style>

    .stApp{
        background:
        linear-gradient(
            135deg,
            #021B79,
            #0575E6
        );
    }

    </style>
    """, unsafe_allow_html=True)

elif theme == "Midnight":

    st.markdown("""
    <style>

    .stApp{
        background:
        linear-gradient(
            135deg,
            #000000,
            #434343
        );
    }

    </style>
    """, unsafe_allow_html=True)
# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload Dataset",
    type=["csv","xlsx"]
)

if uploaded_file:

    with st.spinner("🧠 AI analyzing dataset patterns..."):
        time.sleep(2)

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    status = "✅ Dataset Uploaded"

    announce("Dataset uploaded successfully Sir")

else:

    df = pd.read_csv("Data/sample_data.csv")

    status = "⚠ Using Sample Dataset"

original_df = df.copy()

st.sidebar.success(status)

# =========================================================
# AI HEALTH
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🧠 AI HEALTH")

health = random.randint(85,100)

st.sidebar.metric(
    "AI Stability",
    f"{health}%"
)

st.sidebar.success(
    "Neural Systems Operational"
)

# =========================================================
# SYSTEM STATUS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🖥 SYSTEM STATUS")

cpu = random.randint(20,90)
ram = random.randint(30,95)
gpu = random.randint(15,100)

st.sidebar.progress(cpu/100)
st.sidebar.write(f"⚡ CPU : {cpu}%")

st.sidebar.progress(ram/100)
st.sidebar.write(f"🧠 RAM : {ram}%")

st.sidebar.progress(gpu/100)
st.sidebar.write(f"🔥 GPU : {gpu}%")

# =========================================================
# CLEANING TOOLS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🧹 CLEANING TOOLS")

if st.sidebar.button("🚀 AUTO CLEAN"):

    announce("Auto cleaning initialized")

    df = remove_duplicates(df)
    df = fill_missing(df)

    announce("Dataset cleaned successfully")

if st.sidebar.button("🤖 SMART AI FILL"):

    announce("Artificial intelligence filling missing values")

    df = smart_fill(df)

    announce("AI fill completed")

if st.sidebar.button("⚡ ENCODE CATEGORIES"):

    announce("Encoding categorical values")

    df = encode_categorical(df)

    announce("Encoding completed")

if st.sidebar.button("🔥 REMOVE OUTLIERS"):

    announce("Removing outliers from dataset")

    df = remove_outliers(df)

    announce("Outlier removal completed")

# =========================================================
# METRICS
# =========================================================

st.markdown("## 📊 DATASET OVERVIEW")

c1,c2,c3,c4 = st.columns(4)

c1.metric("ROWS", df.shape[0])
c2.metric("COLUMNS", df.shape[1])
c3.metric("MISSING", df.isnull().sum().sum())
c4.metric("DUPLICATES", df.duplicated().sum())

# =========================================================
# QUALITY SCORE
# =========================================================

score = data_quality_score(df)

st.markdown("## 🎯 AI QUALITY SCORE")

st.progress(score/100)

# =========================================================
# AI INSIGHTS
# =========================================================

numeric_cols = df.select_dtypes(include=np.number).columns

st.markdown("## 🤖 AI INSIGHTS ENGINE")

missing = df.isnull().sum().sum()
duplicates = df.duplicated().sum()

insights = []

if missing > 0:
    insights.append(
        f"⚠ Dataset contains {missing} missing values."
    )

if duplicates > 0:
    insights.append(
        f"⚠ Dataset contains {duplicates} duplicate rows."
    )

if score > 90:
    insights.append(
        "✅ Excellent dataset quality detected."
    )

if len(numeric_cols) > 3:
    insights.append(
        "📊 Multiple numeric features available for AI analytics."
    )

for item in insights:
    st.info(item)

# =========================================================
# AI RECOMMENDATION ENGINE
# =========================================================

st.markdown("## 🤖 AI RECOMMENDATIONS")

recommendations = []

missing_percent = (
    df.isnull().sum().sum() / df.size
) * 100

if missing_percent > 10:
    recommendations.append(
        "⚠ High missing values detected. Use SMART AI FILL."
    )

if duplicates > 0:
    recommendations.append(
        "🧹 Duplicate rows found. Use AUTO CLEAN."
    )

if len(numeric_cols) > 5:
    recommendations.append(
        "📊 Large numeric dataset detected. Use correlation analytics."
    )

if score < 70:
    recommendations.append(
        "🚨 Dataset quality is low. AI optimization recommended."
    )

if len(recommendations) == 0:
    recommendations.append(
        "✅ Dataset looks highly optimized."
    )

for rec in recommendations:
    st.success(rec)

# =========================================================
# BEFORE / AFTER
# =========================================================

st.markdown("## 🔍 DATA TRANSFORMATION")

col1,col2 = st.columns(2)

with col1:
    st.markdown("### BEFORE CLEANING")
    st.dataframe(original_df, use_container_width=True)

with col2:
    st.markdown("### AFTER CLEANING")
    st.dataframe(df, use_container_width=True)

# =========================================================
# VISUALIZATION
# =========================================================

if len(numeric_cols) > 0:

    st.markdown("## 📊 DISTRIBUTION ANALYSIS")

    hist_col = st.selectbox(
        "SELECT NUMERIC COLUMN",
        numeric_cols
    )

    fig = px.histogram(
        df,
        x=hist_col,
        nbins=40,
        title="AI Distribution Analysis",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# HEATMAP
# =========================================================

if len(numeric_cols) > 1:

    st.markdown("## 🔥 CORRELATION HEATMAP")

    corr = df.corr(numeric_only=True)

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# ANOMALY DETECTION
# =========================================================

st.markdown("## 🚨 AI ANOMALY DETECTION")

for col in numeric_cols:

    mean = df[col].mean()
    std = df[col].std()

    anomalies = df[
        (df[col] > mean + 2*std) |
        (df[col] < mean - 2*std)
    ]

    st.write(
        f"{col} → {len(anomalies)} anomalies detected"
    )

# =========================================================
# AI PREDICTION MODEL
# =========================================================
# =========================================================
# AI PREDICTION MODEL
# =========================================================

if uploaded_file is not None:

    if len(numeric_cols) >= 2:

        st.markdown("## 🧠 AI PREDICTION ENGINE")

        target = st.selectbox(
            "SELECT TARGET COLUMN",
            numeric_cols
        )

        features = [c for c in numeric_cols if c != target]

        if len(features) > 0:

            if st.button("🚀 TRAIN AI MODEL"):

                announce("Training artificial intelligence model")

                X = df[features].fillna(0)
                y = df[target].fillna(0)

                model = RandomForestRegressor()

                model.fit(X, y)

                prediction = model.predict(X[:5])

                st.success("AI MODEL TRAINED SUCCESSFULLY")

                announce(
                    "Artificial intelligence model trained successfully"
                )

                pred_df = pd.DataFrame({
                    "Actual": y[:5].values,
                    "Predicted": prediction
                })

                st.dataframe(pred_df)

else:

    st.info(
        "📂 Upload dataset to enable AI prediction engine."
    )

# =========================================================
# LIVE STREAM
# =========================================================

st.markdown("## 📡 LIVE AI STREAM")

stream_data = pd.DataFrame(
    np.random.randn(30,3),
    columns=["AI SIGNAL","NETWORK","SECURITY"]
)

st.line_chart(stream_data)

#

# =========================================================
# DOWNLOAD
# =========================================================

st.markdown("## 🧹 DOWNLOAD CURATED DATASET")

csv = df.to_csv(index=False).encode("utf-8")

if st.download_button(
    "⬇ DOWNLOAD CSV",
    csv,
    "curated_dataset.csv",
    "text/csv"
):
    announce("CSV download started")

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        index=False,
        sheet_name="CuratedData"
    )

excel_data = excel_buffer.getvalue()

if st.download_button(
    "📥 DOWNLOAD EXCEL",
    excel_data,
    "curated_dataset.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
):
    announce("Excel download started")

# =========================================================
# FLOATING ORB
# =========================================================

components.html("""

<div id="orb"></div>

<style>

#orb{

position:fixed;

bottom:30px;
right:30px;

width:90px;
height:90px;

border-radius:50%;

background:radial-gradient(
circle,
#00FFA3,
#00c3ff
);

box-shadow:
0 0 30px #00FFA3,
0 0 60px #00c3ff;

animation:floatOrb 4s ease-in-out infinite;

z-index:999;
}

@keyframes floatOrb{

0%{
transform:translateY(0px);
}

50%{
transform:translateY(-20px);
}

100%{
transform:translateY(0px);
}
}

</style>

""", height=0)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
---
<center>

⚡ KYANG MCS  
One of the best Data Curation Platform

</center>
""", unsafe_allow_html=True)
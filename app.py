import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from tensorflow.keras.models import load_model

def load_data():

    events_cleaned = pd.read_csv("Cleaned/events_cleaned.csv", parse_dates = ["timestamp"])
    df_items = pd.read_csv("df_items.csv")

    # Create visitor and item maps
    visitor_map = {v: i for i, v in enumerate(events_cleaned["visitorid"].unique())}
    item_map = {i: j for j, i in enumerate(df_items["itemid"].unique())}
    

    return events_cleaned, df_items, visitor_map, item_map

events_cleaned, df_items, visitor_map, item_map = load_data()

# --- Load trained model ---
def load_trained_model():
    model = load_model("hybrid_model.h5")
    return model

model = load_trained_model()

st.title("Hybrid Recommendation System")

selected_user = st.number_input(
    "Enter Visitor ID:",
    value = int(events_cleaned["visitorid"].iloc[0])
)
selected_item = st.number_input(
    "Enter Item ID:",
    value = int(df_items["itemid"].iloc[0])
)


# Map visitorid/itemid to model indices
user_idx = visitor_map.get(selected_user)
item_idx = item_map.get(selected_item)

if user_idx is None or item_idx is None:
    st.warning("Visitor ID or Item ID not found in dataset.")
else:
    # Predict interaction score
    predicted_score = model.predict([np.array([user_idx]), np.array([item_idx])])
    st.write(f"Predicted interaction score: {predicted_score[0][0]:.3f}")


# Display top items for user

if st.checkbox("Show top 5 recommended items for this user"):
    # Generate scores for all items
    all_item_indices = np.array(list(item_map.values()))
    user_array = np.array([user_idx] * len(all_item_indices))
    
    scores = model.predict([user_array, all_item_indices]).flatten()
    top_indices = scores.argsort()[-5:][::-1]  # Top 5
    top_items = [list(item_map.keys())[i] for i in top_indices]

    
    st.write("Top 5 recommended items:", top_items)
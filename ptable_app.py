import streamlit as st
import pandas as pd

# Set page title and icon
st.set_page_config(page_title="Interactive Periodic Table", page_icon="🔬")

# Load the dataset
df = pd.read_csv('elements.csv')

# Convert 'Group' to numeric and drop rows where 'Group' is missing or cannot be converted
df['Group'] = pd.to_numeric(df['Group'], errors='coerce')
df = df.dropna(subset=['Group'])
# Ensure 'Group' is integer for safe indexing
df['Group'] = df['Group'].astype(int)

# Sort the dataframe by 'Atomic_Number'
df_sorted = df.sort_values('Atomic_Number')

# Display the title
st.title('Interactive Periodic Table')

# Custom CSS to inject for styling the buttons and sidebar
st.markdown("""
<style>
.element-button {
    border: 2px solid #4CAF50;
    border-radius: 10px;
    color: white;
    padding: 10px;
    text-align: center;
    display: inline-block;
    font-size: 16px;
    margin: 4px;
    cursor: pointer;
}

/* Example colors for categories - customize as needed */
.nonmetal { background-color: #8ebf87; }
.noble-gas { background-color: #f0c75e; }
.alkali-metal { background-color: #ff6666; }
.alkaline-earth-metal { background-color: #f4b183; }
.transition-metal { background-color: #b4c7e7; }
/* Add more categories with colors here */

.sidebar .sidebar-content {
    background-color: #f1f1f1;
}
</style>
""", unsafe_allow_html=True)

# Create a dynamic layout based on the number of elements
columns = st.columns(18)

# Display elements in a grid-like layout
for index, element in df_sorted.iterrows():
    group = element['Group']  # Access 'Group' value directly
    if not 1 <= group <= 18:
        st.warning(f"Skipping element {element['Name']} due to invalid 'Group' value.")
        continue

    col_index = group - 1
    col = columns[col_index]
    with col:
        # Access 'Phase' value directly and handle missing values
        phase = element['Phase'] if pd.notnull(element['Phase']) else 'unknown'
        phase_class = phase.lower().replace(" ", "-")
        button_html = f"<button class='element-button {phase_class}' onclick='alert(\"{element['Name']}\")'>{element['Symbol']}</button>"
        st.markdown(button_html, unsafe_allow_html=True)

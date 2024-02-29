import streamlit as st
import pandas as pd

# Set page title and icon
st.set_page_config(page_title="Interactive Periodic Table", page_icon="🔬")

# Load the dataset
df = pd.read_csv('elements.csv')
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
    # Safely get the Group value and ensure it's within the expected range
    group = element.get('Group')
    if group is None or not 1 <= group <= 18:
        st.warning(f"Skipping element {element['Name']} due to invalid or missing 'Group' value.")
        continue

    col_index = group - 1
    if col_index >= len(columns):
        st.error(f"Group index out of range for element {element['Name']}.")
        continue

    col = columns[col_index]
    with col:
        phase = element.get('Phase', 'unknown').lower().replace(" ", "-")
        button_html = f"<button class='element-button {phase}' onclick='alert(\"{element['Name']}\")'>{element['Symbol']}</button>"
        st.markdown(button_html, unsafe_allow_html=True)

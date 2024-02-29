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

# Custom CSS to inject for styling the buttons
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

# Function to display element details
def display_element_details(symbol):
    element = df[df['Symbol'] == symbol].iloc[0]
    st.sidebar.header(f"{element['Name']} ({element['Symbol']})")
    st.sidebar.write(f"**Atomic Number:** {element['Atomic_Number']}")
    st.sidebar.write(f"**Atomic Weight:** {element['Atomic_Weight']}")
    st.sidebar.write(f"**Density:** {element['Density']} g/cm³")
    st.sidebar.write(f"**Phase at STP:** {element['Phase']}")
    st.sidebar.write(f"**Group:** {element['Group']}")
    st.sidebar.write(f"**Period:** {element['Period']}")
    st.sidebar.write(f"**Block:** {element['Block']}")
    if pd.notnull(element['Melting_Point']):
        st.sidebar.write(f"**Melting Point:** {element['Melting_Point']} K")
    if pd.notnull(element['Boiling_Point']):
        st.sidebar.write(f"**Boiling Point:** {element['Boiling_Point']} K")

# Create a dynamic layout based on the number of elements
columns = st.columns(18)

# Display elements in a grid-like layout
for index, element in df_sorted.iterrows():
    group = element['Group']  # Access 'Group' value directly
    if not 1 <= group <= 18:
        continue

    col_index = group - 1
    col = columns[col_index]
    with col:
        phase_class = element['Phase'].lower().replace(" ", "-") if pd.notnull(element['Phase']) else 'unknown'
        # Use a button with a custom class for each element
        button_id = f"button_{element['Symbol']}"
        button_html = f"<button id='{button_id}' class='element-button {phase_class}' onclick='if (typeof(Storage) !== \"undefined\") {{localStorage.setItem(\"selectedElement\", \"{element['Symbol']}\"); location.reload();}}'>{element['Symbol']}</button>"
        st.markdown(button_html, unsafe_allow_html=True)
        # Check if this element was clicked
        if st.session_state.get(button_id):
            display_element_details(element['Symbol'])

# Check local storage for selected element
selected_element = st.experimental_get_query_params().get("selectedElement")
if selected_element:
    display_element_details(selected_element[0])

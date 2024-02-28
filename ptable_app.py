import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv('elements.csv')

# Display the periodic table (interactive version)
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

# Sort elements by their atomic number for a logical display
df_sorted = df.sort_values('Atomic_Number')

# Create a dynamic layout based on the number of elements
max_columns = 18  # Maximum number of groups in the periodic table
columns = st.columns(max_columns)

# Helper function to display element properties
def display_element_properties(element):
    st.sidebar.header(f"{element['Name']} ({element['Symbol']})")
    properties = ['Atomic_Number', 'Atomic_Weight', 'Density', 'Melting_Point',
                  'Boiling_Point', 'Phase', 'Valence', 'Electronegativity',
                  'ElectronAffinity', 'Block', 'Group', 'Period', 'Electron_Configuration']
    for prop in properties:
        st.sidebar.write(f"**{prop.replace('_', ' ')}:** {element[prop]}")

# Display elements in a grid-like layout
for index, element in df_sorted.iterrows():
    with columns[element['Group'] - 1]:  # Adjust column based on the element's group
        # Assign a CSS class based on the element's category (or other property)
        category_class = element['Phase'].lower().replace(" ", "-")  # Example: Convert "Noble Gas" to "noble-gas"
        button_html = f"<button class='element-button {category_class}' onclick='alert(\"{element['Name']}\")'>{element['Symbol']}</button>"
        st.markdown(button_html, unsafe_allow_html=True)

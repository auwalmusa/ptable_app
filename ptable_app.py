import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category20

# Set page configuration
st.set_page_config(page_title="Interactive Periodic Table", page_icon="🔬")

# Load the dataset
df = pd.read_csv('elements.csv')

# Preprocess the data
df['Group'] = pd.to_numeric(df['Group'], errors='coerce')
df.dropna(subset=['Group'], inplace=True)
df['Group'] = df['Group'].astype(int)
df['Period'] = df['Period'].astype(int)
df['group_str'] = df['Group'].astype(str)
df['period_str'] = df['Period'].astype(str)

# Create a ColumnDataSource
source = ColumnDataSource(df)

# Define color mapper using 'Group'
group_palette = Category20[20]  # Use a color palette with 20 distinct colors
df['color'] = df['Group'] % 20  # Map group number to color index
df['color'] = df['color'].apply(lambda x: group_palette[x])  # Apply color mapping

# Bokeh figure with corrected y_range for the traditional layout
p = figure(title="Periodic Table", x_range=(1, max(df['Group'])), y_range=(1, max(df['Period'])),
           tools="", toolbar_location=None, width=1200, height=600)

# Add rectangles for each element
p.rect("Group", "Period", width=0.95, height=0.95, source=source,
       fill_color='color', line_color='black')

# Add hover tool
hover = HoverTool()
hover.tooltips = """
    <div>
        <h3>@Name (@Symbol)</h3>
        <div><strong>Atomic Number:</strong> @Atomic_Number</div>
        <div><strong>Atomic Weight:</strong> @Atomic_Weight</div>
        <div><strong>Density:</strong> @Density</div>
        <div><strong>Electron Configuration:</strong> @Electron_Configuration</div>
        <div><strong>Valence:</strong> @Valence</div>
        <div><strong>Electronegativity:</strong> @Electronegativity</div>
        <div><strong>Electron Affinity:</strong> @Electron_Affinity</div>
    </div>
"""
p.add_tools(hover)

# Customizing plot aesthetics
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None
p.background_fill_color = '#f0f0f0'

# Display the title
st.title('Interactive Periodic Table')

# Bokeh chart in Streamlit
st.bokeh_chart(p, use_container_width=True)

# Sidebar for element details
st.sidebar.header("Element Details")
selected_symbol = st.sidebar.text_input("Enter an element symbol to see details:", "")

if selected_symbol:
    element_df = df[df['Symbol'].str.upper() == selected_symbol.upper()]
    if not element_df.empty:
        element = element_df.iloc[0]
        # Check for the existence of the 'Electron_Affinity' column
        electron_affinity = element['Electron_Affinity'] if 'Electron_Affinity' in df.columns else "N/A"
        st.sidebar.write(f"**Name:** {element['Name']}")
        st.sidebar.write(f"**Symbol:** {element['Symbol']}")
        st.sidebar.write(f"**Atomic Number:** {element['Atomic_Number']}")
        st.sidebar.write(f"**Atomic Weight:** {element['Atomic_Weight']}")
        st.sidebar.write(f"**Density:** {element['Density']} g/cm³")
        st.sidebar.write(f"**Electron Configuration:** {element['Electron_Configuration']}")
        st.sidebar.write(f"**Valence:** {element['Valence']}")
        st.sidebar.write(f"**Electronegativity:** {element['Electronegativity']}")
        st.sidebar.write(f"**Electron Affinity:** {element['Electron_Affinity']} kJ/mol")
    else:
        st.sidebar.write("Element not found. Please enter a valid symbol.")

# Instructions for user
st.write("Hover over an element to see its details.")

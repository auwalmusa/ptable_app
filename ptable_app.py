import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category20

# Set page configuration
st.set_page_config(page_title="Interactive Periodic Table", page_icon="🔬")

# Load the dataset
df = pd.read_csv('elements.csv')

# Function to map element blocks to colors
def map_color(block):
    color_mapping = {
        's': '#FF6666',  # light red
        'p': '#F0E442',  # light yellow
        'd': '#66FF66',  # light green
        'f': '#6666FF',  # light blue
    }
    return color_mapping.get(block, '#FFFFFF')  # default to white if block is not found

# Apply color mapping to the dataframe
df['color'] = df['Block'].apply(map_color)

# Create a ColumnDataSource
source = ColumnDataSource(df)

# Bokeh figure with corrected orientation and axis ranges
p = figure(title="Periodic Table", x_range=(0, 19), y_range=(0, 8),
           tools="", toolbar_location=None, plot_width=1200, plot_height=600)

# Add rectangles for each element, using 'Group' for the x-coordinate and 'Period' for the y-coordinate
p.rect("Group", "Period", width=0.95, height=0.95, source=source,
       fill_color='color', line_color='black')

# Add hover tool
hover = HoverTool()
hover.tooltips = """
    <div>
        <h3>@Name (@Symbol)</h3>
        <div><strong>Atomic Number:</strong> @Atomic_Number</div>
        <div><strong>Atomic Weight:</strong> @Atomic_Weight</div>
        <div><strong>Density:</strong> @Density g/cm³</div>
        <div><strong>Melting Point:</strong> @Melting_Point K</div>
        <div><strong>Boiling Point:</strong> @Boiling_Point K</div>
        <div><strong>Phase:</strong> @Phase</div>
        <div><strong>Valence:</strong> @Valence</div>
        <div><strong>Electronegativity:</strong> @Electronegativity</div>
        <div><strong>Electron Affinity:</strong> @ElectronAffinity kJ/mol</div>
        <div><strong>Group:</strong> @Group</div>
        <div><strong>Period:</strong> @Period</div>
    </div>
"""
p.add_tools(hover)

# Customizing plot aesthetics to improve readability
p.axis.visible = True
p.grid.visible = True
p.axis.axis_label_standoff = 12
p.xaxis.axis_label = "Group"
p.yaxis.axis_label = "Period"
p.xaxis.major_label_orientation = "horizontal"
p.yaxis.major_label_orientation = "horizontal"
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
        # Display element details
        st.sidebar.write(f"**Name:** {element['Name']}")
        st.sidebar.write(f"**Symbol:** {element['Symbol']}")
        st.sidebar.write(f"**Atomic Number:** {element['Atomic_Number']}")
        st.sidebar.write(f"**Atomic Weight:** {element['Atomic_Weight']}")
        st.sidebar.write(f"**Density:** {element['Density']} g/cm³")
        st.sidebar.write(f"**Melting Point:** {element['Melting_Point']} K")
        st.sidebar.write(f"**Boiling Point:** {element['Boiling_Point']} K")
        st.sidebar.write(f"**Phase:** {element['Phase']}")
        st.sidebar.write(f"**Valence:** {element['Valence']}")
        st.sidebar.write(f"**Electronegativity:** {element['Electronegativity']}")
        st.sidebar.write(f"**Electron Affinity:** {element['ElectronAffinity']} kJ/mol")
    else:
        st.sidebar.write("Element not found. Please enter a valid symbol.")

# Instructions for user
st.write("Hover over an element to see its details.")

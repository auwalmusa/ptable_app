import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import transform
from bokeh.palettes import Category20

# Set page configuration
st.set_page_config(page_title="Interactive Periodic Table", page_icon="🔬")

# Load the dataset
df = pd.read_csv('elements.csv')

# Preprocess the data
df['Group'] = pd.to_numeric(df['Group'], errors='coerce')
df.dropna(subset=['Group'], inplace=True)
df['Group'] = df['Group'].astype(int)
df['period_str'] = df['Period'].astype(str)
df['group_str'] = df['Group'].astype(str)

# Create a ColumnDataSource
source = ColumnDataSource(df)

# Define a categorical color mapper
group_count = df['group_str'].nunique()
color_mapper = Category20[group_count] if group_count <= 20 else Category20[20] + df['group_str'].unique()[20:].tolist()

# Bokeh figure
p = figure(title="Periodic Table", x_range=df['group_str'].unique(), y_range=list(reversed(df['period_str'].unique())),
           tools="", toolbar_location=None, width=1200, height=600)

# Add rectangles for each element
p.rect("group_str", "period_str", width=0.95, height=0.95, source=source,
       fill_color=transform('group_str', factor_cmap('group_str', palette=color_mapper, factors=df['group_str'].unique())),
       line_color='white', line_width=0.5)

# Add hover tool
hover = HoverTool()
hover.tooltips = """
    <div>
        <h3>@Name (@Symbol)</h3>
        <div><strong>Atomic Number:</strong> @Atomic_Number</div>
        <div><strong>Atomic Weight:</strong> @Atomic_Weight</div>
        <div><strong>Density:</strong> @Density g/cm³</div>
        <div><strong>Electron Configuration:</strong> @Electron_Configuration</div>
        <div><strong>Valence:</strong> @Valence</div>
        <div><strong>Electronegativity:</strong> @Electronegativity</div>
        <div><strong>Electron Affinity:</strong> @Electron_Affinity kJ/mol</div>
    </div>
"""
p.add_tools(hover)

# Customizing plot aesthetics
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None
p.background_fill_color = '#f0f0f0'  # Light grey background for better contrast

# Display the title
st.title('Interactive Periodic Table')

# Bokeh chart in Streamlit
st.bokeh_chart(p, use_container_width=True)

# Sidebar for element details
st.sidebar.header("Element Details")
selected_symbol = st.sidebar.text_input("Enter an element symbol to see details:", "")

if selected_symbol:
    if selected_symbol.upper() in df['Symbol'].values:
        element = df[df['Symbol'].str.upper() == selected_symbol.upper()].iloc[0]
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

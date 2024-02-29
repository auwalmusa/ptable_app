import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Viridis256

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

# Define color mapper using 'Group', ensure there are enough colors
colors = Viridis256[:len(df['Group'].unique())]

# Bokeh figure
p = figure(title="Periodic Table", x_range=df['group_str'].unique(), y_range=list(reversed(df['period_str'].unique())),
           tools="", toolbar_location=None)

# Add rectangles for each element
p.rect("group_str", "period_str", width=0.95, height=0.95, source=source,
       fill_color=factor_cmap('group_str', palette=colors, factors=df['group_str'].unique()), line_color=None)

# Add hover tool
hover = HoverTool()
hover.tooltips = """
    <div>
        <h3>@Name</h3>
        <div><strong>Symbol:</strong> @Symbol</div>
        <div><strong>Atomic Number:</strong> @Atomic_Number</div>
        <div><strong>Atomic Weight:</strong> @Atomic_Weight g/mol</div>
        <div><strong>Density:</strong> @Density g/cm³</div>
        <div><strong>Electron Configuration:</strong> @Electron_Configuration</div>
        <div><strong>Valence:</strong> @Valence</div>
        <div><strong>Electronegativity:</strong> @Electronegativity</div>
        <div><strong>Electron Affinity:</strong> @Electron_Affinity kJ/mol</div>
    </div>
"""
p.add_tools(hover)

# Add element symbols as text labels
p.text(x='group_str', y='period_str', text='Symbol', source=source,
       text_align='center', text_baseline='middle', text_font_size='10pt')

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
    element = df[df['Symbol'].str.upper() == selected_symbol.upper()].iloc[0] if not df[df['Symbol'].str.upper() == selected_symbol.upper()].empty else None
    if element is None:
        st.sidebar.write("No details available. Please enter a valid symbol.")
    else:
        st.sidebar.write(f"**Name:** {element['Name']}")
        st.sidebar.write(f"**Symbol:** {element['Symbol']}")
        st.sidebar.write(f"**Atomic Number:** {element['Atomic_Number']}")
        st.sidebar.write(f"**Atomic Weight:** {element['Atomic_Weight']}")
        st.sidebar.write(f"**Density:** {element['Density']} g/cm³")
        st.sidebar.write(f"**Electron Configuration:** {element['Electron_Configuration']}")
        st.sidebar.write(f"**Valence:** {element['Valence']}")
        st.sidebar.write(f"**Electronegativity:** {element['Electronegativity']}")
        st.sidebar.write(f"**Electron Affinity:** {element['Electron_Affinity']} kJ/mol")

# Instructions for user
st.write("Hover over an element to see its details.")

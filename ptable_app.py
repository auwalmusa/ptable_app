import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import factor_cmap
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

# Define color mapper using 'Group', ensure there are enough colors
max_groups = 20  # Typically, there are 18 groups in the periodic table but we're using 20 for the color palette
colors = Category20[max_groups]

# Bokeh figure
p = figure(title="Periodic Table", x_range=[str(x) for x in range(1, 19)], y_range=[str(y) for y in reversed(range(1, 8))],
           tools="", toolbar_location=None, width=1200, height=450)

# Add rectangles for each element
p.rect("group_str", "period_str", width=0.95, height=0.95, source=source,
       fill_color=factor_cmap('group_str', palette=colors, factors=sorted(df['group_str'].unique())), line_color=None)

# Add hover tool
hover = HoverTool()
hover.tooltips = """
    <div>
        <h3>@Name</h3>
        <div><strong>Symbol:</strong> @Symbol</div>
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

# Add element symbols as text labels
p.text(x='group_str', y='period_str', text='Symbol', source=source,
       text_align='center', text_baseline='middle', text_font_size='9pt', text_color="white")

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

def safe_column_access(column_name):
    """Return the column data if it exists, or a placeholder if not."""
    if column_name in df.columns:
        return df[column_name]
    else:
        st.sidebar.write(f"The column '{column_name}' does not exist in the dataset.")
        return "Data not available"

if selected_symbol:
    element_data = df[df['Symbol'].str.upper() == selected_symbol.upper()].iloc[0] if not df[df['Symbol'].str.upper() == selected_symbol.upper()].empty else None
    if element_data is None:
        st.sidebar.write("No details available. Please enter a valid symbol.")
    else:
        # Use the safe_column_access function to retrieve data
        st.sidebar.write(f"**Name:** {safe_column_access('Name')}")
        st.sidebar.write(f"**Symbol:** {safe_column_access('Symbol')}")
        st.sidebar.write(f"**Atomic Number:** {safe_column_access('Atomic_Number')}")
        st.sidebar.write(f"**Atomic Weight:** {safe_column_access('Atomic_Weight')}")
        st.sidebar.write(f"**Density:** {safe_column_access('Density')}") g/cm³")
        st.sidebar.write(f"**Electron Configuration:** {safe_column_access('Electron_Configuration')}")
        st.sidebar.write(f"**Valence:** {safe_column_access('Valence')}")
        st.sidebar.write(f"**Electronegativity:** {safe_column_access('Electronegativity')}")
        st.sidebar.write(f"**Electron Affinity:** {safe_column_access('Electron_Affinity')}") kJ/mol")

# Instructions for user
st.write("Hover over an element to see its details.")

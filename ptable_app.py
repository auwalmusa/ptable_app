import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Turbo256

# Set page title and icon
st.set_page_config(page_title="Interactive Periodic Table", page_icon="🔬")

# Assuming 'elements.csv' is in the same directory as your Streamlit app
df = pd.read_csv('elements.csv')

# Preprocess the data
df['Group'] = pd.to_numeric(df['Group'], errors='coerce')
df.dropna(subset=['Group'], inplace=True)
df['Group'] = df['Group'].astype(int)
df_sorted = df.sort_values('Atomic_Number')
df_sorted['period_str'] = df_sorted['Period'].astype(str)
df_sorted['group_str'] = df_sorted['Group'].astype(str)

# Create a ColumnDataSource
source = ColumnDataSource(df_sorted)

# Define color mapper - assuming 'Type' or similar column for color mapping
# Adjust the 'field_name' to match your DataFrame's column name for element types/categories
field_name = 'Type'  # Example column name for element types
colors = Turbo256[:len(df_sorted[field_name].unique())]
color_mapper = factor_cmap(field_name, palette=colors, factors=df_sorted[field_name].unique())

# Bokeh figure
p = figure(title="Periodic Table", x_range=df_sorted['group_str'].unique(), y_range=list(reversed(df_sorted['period_str'].unique())),
           tools="", toolbar_location=None, tooltips="@Name: @Symbol")

# Add rectangles for each element
p.rect("group_str", "period_str", width=0.95, height=0.95, source=source, fill_color=color_mapper, line_color=None)

# Add hover tool
hover = HoverTool()
hover.tooltips = """
    <div>
        <h3>@Name</h3>
        <div><strong>Symbol:</strong> @Symbol</div>
        <div><strong>Atomic Number:</strong> @Atomic_Number</div>
        <div><strong>Group:</strong> @Group</div>
        <div><strong>Period:</strong> @Period</div>
    </div>
"""
p.add_tools(hover)

# Display the title
st.title('Interactive Periodic Table')

# Bokeh chart in Streamlit
st.bokeh_chart(p, use_container_width=True)

# Sidebar with element details (optional, based on interaction)
st.sidebar.header("Element Details")
selected_symbol = st.sidebar.text_input("Enter an element symbol to see details:", "")

if selected_symbol:
    element = df_sorted[df_sorted['Symbol'].str.upper() == selected_symbol.upper()].iloc[0]
    if element.empty:
        st.sidebar.write("No details available. Please enter a valid symbol.")
    else:
        st.sidebar.write(f"**Name:** {element['Name']}")
        st.sidebar.write(f"**Symbol:** {element['Symbol']}")
        st.sidebar.write(f"**Atomic Number:** {element['Atomic_Number']}")
        st.sidebar.write(f"**Atomic Weight:** {element['Atomic_Weight']}")
        # Add more details as needed

import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Turbo256

# Set page title and icon
st.set_page_config(page_title="Interactive Periodic Table", page_icon="🔬")

# Assuming 'elements.csv' is in the same directory as your Streamlit app
# Load the dataset
df = pd.read_csv('elements.csv')

# Preprocess the data
df['Group'] = pd.to_numeric(df['Group'], errors='coerce')
df.dropna(subset=['Group'], inplace=True)
df['Group'] = df['Group'].astype(int)
df['period_str'] = df['Period'].astype(str)
df['group_str'] = df['Group'].astype(str)

# Ensure the 'Group' column is suitable for color mapping
max_groups = len(df['Group'].unique())
colors = Turbo256[:max(max_groups, 256)]  # Ensure there are enough colors

# Create a ColumnDataSource
source = ColumnDataSource(df)

# Define color mapper using 'Group'
color_mapper = factor_cmap('group_str', palette=colors, factors=df['group_str'].unique())

# Bokeh figure
p = figure(title="Periodic Table", x_range=df['group_str'].unique(), y_range=list(reversed(df['period_str'].unique())),
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

# Sidebar for element details (Optional)
st.sidebar.header("Element Details")
selected_symbol = st.sidebar.text_input("Enter an element symbol to see details:", "")

if selected_symbol:
    element = df[df['Symbol'].str.upper() == selected_symbol.upper()].iloc[0]
    if element.empty:
        st.sidebar.write("No details available. Please enter a valid symbol.")
    else:
        st.sidebar.write(f"**Name:** {element['Name']}")
        st.sidebar.write(f"**Symbol:** {element['Symbol']}")
        st.sidebar.write(f"**Atomic Number:** {element['Atomic_Number']}")
        st.sidebar.write(f"**Atomic Weight:** {element['Atomic_Weight']}")
        # Add more details as needed

import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category20
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.resources import CDN
from bokeh.embed import file_html

# Apply the color mapping function to the 'Block' column in the dataframe
df['color'] = df['Block'].apply(map_color)

# Create a ColumnDataSource from the dataframe
source = ColumnDataSource(df)

# Define the Bokeh figure with the correct orientation
p = figure(title="Periodic Table", x_range=(0, 19), y_range=(0, 8),
           tools="", toolbar_location=None, plot_width=1344, plot_height=497)

# Add rectangles for each element with the specified colors and a black line border
p.rect("Group", "Period", width=0.95, height=0.95, source=source,
       fill_color='color', line_color='black')

# Define the hover tool with the appropriate HTML for tooltips
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

# Customize the plot to show axes and grid
p.axis.visible = True
p.grid.visible = True
p.axis.axis_label_standoff = 12
p.xaxis.axis_label = "Group"
p.yaxis.axis_label = "Period"
p.xaxis.major_label_orientation = "horizontal"
p.yaxis.major_label_orientation = "horizontal"
p.background_fill_color = '#f0f0f0'

# Generate the HTML components to embed the Bokeh figure
html = file_html(p, CDN, "Periodic Table")

# Save the HTML to a file to be shared with the user
html_file_path = '/mnt/data/periodic_table.html'
with open(html_file_path, 'w') as f:
    f.write(html)

# Return the path to the generated HTML file
html_file_path

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

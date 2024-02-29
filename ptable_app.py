import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category20c  # Using a categorical palette with 20 colors

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

# Assuming 'Category' is a column in your dataset that categorizes elements
# If not, you would need to create such a categorization
# For the sake of demonstration, I'll categorize elements by their group number
df['Category'] = df['Group'] % len(Category20c)  # Simple categorization by group number

# Define color mapper using 'Category'
category_palette = Category20c[20]  # Use a color palette with 20 distinct colors
df['color'] = df['Category'].apply(lambda x: category_palette[x])  # Apply color mapping

# Bokeh figure
p = figure(title="Periodic Table", x_range=(-1, 18), y_range=(-1, 10),
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

# Add text labels for symbols
p.text(x='Group', y='Period', text='Symbol', source=source,
       text_align='center', text_baseline='middle', text_font_size='10pt', text_color="black")

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

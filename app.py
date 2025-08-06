import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u

def aitoff_projection_plot(selected_df):
    """
    Creates an AITOFF projection plot for the selected sources.
    """
    fig = plt.figure(figsize=(10, 5))
    plt.style.use('dark_background')
    ax = fig.add_subplot(111, projection="aitoff")
    ax.grid(True)
    
    # Set plot labels and title
    ax.set_xlabel("Right Ascension (RA)", fontsize=12)
    ax.set_ylabel("Declination (DEC)", fontsize=12)
    ax.set_title("AITOFF Projection of Selected Sources", fontsize=15)
    
    # Convert RA and DEC to radians for the AITOFF projection
    c = SkyCoord(ra=selected_df['RA'].values * u.degree, dec=selected_df['DEC'].values * u.degree, frame='icrs')
    
    # Plot the sources
    ax.plot(c.ra.wrap_at(180*u.degree).radian, c.dec.radian, '.', color='cyan', markersize=5)
    
    return fig

def main():
    """
    Main function to run the Streamlit app.
    """
    st.set_page_config(layout="wide")
    st.title('Classifying Chandra Sources: Interactive Viewer 🔭')
    
    # Load data from the CSV file
    try:
        df = pd.read_csv('df2.csv')
    except FileNotFoundError:
        st.error("Error: 'df2.csv' not found. Please make sure the data file is in the same directory.")
        return
    
    # --- Sidebar for Filters ---
    with st.sidebar:
        st.header("Filters")
        
        # Slider to filter by class probability
        probability_threshold = st.slider(
            'Minimum class Probability',
            min_value=0.0, max_value=1.0, value=0.5, step=0.01
        )
        
        # Filter sources based on probability
        filtered_df = df[df['prob'] >= probability_threshold]
        
        # Multiselect to filter by class
        unique_classes = sorted(filtered_df['class'].unique())
        selected_classes = st.multiselect(
            'Filter by class',
            options=unique_classes,
            default=unique_classes
        )
        
        # Apply class filter
        filtered_df = filtered_df[filtered_df['class'].isin(selected_classes)]

    # --- Main content area with a three-column layout ---
    col1 = st.columns([1,])

    # --- Left Panel (User Interaction & Table Display) ---
    with col1:
        st.header("Source Data Table")
        st.write("Select rows from the table below for plotting.")
        
        # Display the filtered dataframe and allow row selection
        selected_rows = st.dataframe(
            filtered_df,
            column_config={
                "CSC-ID": st.column_config.TextColumn(
                    "CSC-ID",
                    help="Unique identifier for the source."
                )
            },
            hide_index=True,
            use_container_width=True,
            selection_mode="multi-select"
        )
        
        # Create a button to trigger the plot
        # plot_button = st.button("Plot Selected Sources")

    # # --- Middle Panel (Plotting) ---
    # with col2:
    #     st.header("AITOFF Projection")
    #     if plot_button:
    #         if not selected_rows['selection']:
    #             st.info("Please select at least one source from the table to plot.")
    #         else:
    #             selected_indices = selected_rows['selection']
    #             selected_df = filtered_df.loc[selected_indices]
    #             fig = aitoff_projection_plot(selected_df)
    #             st.pyplot(fig)
    #     else:
    #         st.info("Select sources from the left panel and click 'Plot Selected Sources' to view the projection.")
            
    # # --- Right Panel (Placeholder) ---
    # with col3:
    #     st.header("SHAP Analysis")
    #     st.write("Local Explanation of Classification")

if __name__ == "__main__":
    main()
# This is the app.py file.

import streamlit as st
from modules.data_processing import process_data
from modules.streamlit_logger import StreamlitMemoryHandler
import logging
import pydeck as pdk
import numpy as np

# Set up custom logging handler
logger = logging.getLogger()
# Check if StreamlitMemoryHandler is already in logger's handlers
if not any(isinstance(h, StreamlitMemoryHandler) for h in logger.handlers):
    handler = StreamlitMemoryHandler(st.session_state)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
else:
    # If the handler is already there, clear other handlers to avoid duplicates
    logger.handlers = [
        h for h in logger.handlers if isinstance(h, StreamlitMemoryHandler)
    ]


def hex_to_rgba(hex_color):
    # Convert hex to RGB and add alpha value of 150
    return [int(hex_color[i : i + 2], 16) for i in (1, 3, 5)] + [150]


# Main App
def main():
    st.title("Supply Chain Optimization App")

    # Initialize 'logs' in session state if not already present
    if "logs" not in st.session_state:
        st.session_state.logs = []
    # Initialize 'processed_df' in session state if not already present
    if "processed_df" not in st.session_state:
        st.session_state.processed_df = None
    # Initialize 'column_names' in session state if not already present
    if "column_names" not in st.session_state:
        st.session_state.column_names = None

    # Tab-like sections using st.radio
    tab = st.radio("Go to", ["Upload Dataset", "View Logs", "Visualize Data"])

    if tab == "Upload Dataset":
        # Upload Dataset
        st.header("Upload Dataset")
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

        if uploaded_file:
            import pandas as pd

            try:
                df = pd.read_csv(uploaded_file)
                (
                    st.session_state.processed_df,
                    st.session_state.column_names,
                ) = process_data(df, uploaded_file.name)
                if st.session_state.processed_df is not None:
                    st.write(st.session_state.processed_df.head())
                else:
                    st.error(
                        "The uploaded dataset couldn't be processed correctly. Please check the logs for more details."
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")
                logger.error(f"Failed to process the uploaded file: {e}")
        elif st.session_state.processed_df is not None:
            st.write(st.session_state.processed_df.head())
            with open('st.session_state.processed_df.csv') as f:
                st.download_button('Download CSV', f)

    elif tab == "View Logs":
        # Display Logs
        st.header("Logs")
        # Display logs from session state
        if "logs" in st.session_state:
            # Concatenate logs and display in a text area
            st.text_area(
                "Logs", "\n".join(st.session_state.logs), height=800, max_chars=None
            )

            # Provide a button to download the logs as a .log file
            log_content = "\n".join(st.session_state.logs)
            st.download_button(
                label="Download Logs",
                data=log_content,
                file_name="logs.log",
                mime="text/plain",
            )

    elif tab == "Visualize Data":
        st.header("Visualize Data on Map")

        if st.session_state.processed_df is not None:
            # Sidebar settings
            st.sidebar.header("Map Settings")

            supply_color = hex_to_rgba(
                st.sidebar.color_picker("Choose Supply Color", "#FF0000")
            )
            demand_color = hex_to_rgba(
                st.sidebar.color_picker("Choose Demand Color", "#0000FF")
            )

            # Map background style selection
            map_styles = {
                "Light": "mapbox://styles/mapbox/light-v10",
                "Dark": "mapbox://styles/mapbox/dark-v10",
                "Satellite": "mapbox://styles/mapbox/satellite-v9",
                "Satellite Streets": "mapbox://styles/mapbox/satellite-streets-v11",
            }
            map_style = st.sidebar.selectbox(
                "Choose Map Style", list(map_styles.keys()), index=0
            )

            # Use detect_and_validate_columns to get column names
            lat_col, long_col, volume_col, type_col = st.session_state.column_names

            # Convert columns to appropriate types
            lats = st.session_state.processed_df[lat_col].astype(float).tolist()
            longs = st.session_state.processed_df[long_col].astype(float).tolist()
            volumes = st.session_state.processed_df[volume_col].astype(float).tolist()
            types = st.session_state.processed_df[type_col].tolist()

            # Compute circle radii based on logarithm of volume
            radii = [np.log(volume + 1) * 10000 for volume in volumes]
            # Create data for pydeck chart
            data = []
            for lat, long, volume, point_type, radius in zip(
                lats, longs, volumes, types, radii
            ):
                color = supply_color if point_type == "supply" else demand_color
                data.append(
                    {
                        "latitude": lat,
                        "longitude": long,
                        "volume": volume,
                        "type": point_type,
                        "radius": radius,
                        "color": color,
                    }
                )

            # Pydeck chart
            view_state = pdk.ViewState(
                latitude=np.mean(lats), longitude=np.mean(longs), zoom=2
            )
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=data,
                get_position=["longitude", "latitude"],
                get_radius="radius",
                get_fill_color="color",  # RGBA
                pickable=True,
                auto_highlight=True,
            )
            tooltip = {
                "text": "Type: {type}, Latitude: {latitude}, Longitude: {longitude}, Volume: {volume}"
            }
            st.pydeck_chart(
                pdk.Deck(
                    map_style=map_styles[map_style],
                    layers=[layer],
                    initial_view_state=view_state,
                    tooltip=tooltip,
                )
            )
        else:
            st.warning(
                "Please upload and process a dataset first to visualize it on the map."
            )


if __name__ == "__main__":
    main()

import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI usage

import io
import base64
import matplotlib.pyplot as plt
import mplstereonet

def create_stereonet_image(plot_data, file_format="png"):
    """
    Create a stereonet plot based on the lines and planes stored in plot_data.
    Supports output formats: PNG, PDF, SVG.
    """
    # Create a stereonet figure and axis
    fig, ax = plt.subplots(subplot_kw={'projection': 'stereonet'})

    # Plot each line stored in plot_data['lines']
    for trend, plunge in plot_data['lines']:
        ax.line(trend, plunge, 'bo', markersize=8)  # Blue circles for lines

    # Plot each plane stored in plot_data['planes']
    for strike, dip_direction, dip_angle in plot_data['planes']:
        ax.plane(strike, dip_angle, 'r-', linewidth=2)  # Red lines for planes

    # Add grid to the stereonet
    ax.grid()

    # Save the plot to a buffer in the specified format
    buf = io.BytesIO()
    plt.savefig(buf, format=file_format, dpi=300)
    buf.seek(0)  # Move the pointer to the start of the buffer

    # For PNG, encode the image to base64; for others, return raw bytes
    if file_format == "png":
        plot_data_encoded = base64.b64encode(buf.read()).decode("utf-8")
        result = {"plot_data": plot_data_encoded}
    else:
        result = buf.read()  # Return raw bytes for non-PNG formats

    plt.close(fig)  # Close the figure to free resources
    return result
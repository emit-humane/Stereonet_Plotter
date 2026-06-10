from flask import Flask, render_template, request, jsonify, session, send_file
from stereonet_calculations import create_stereonet_image
import io

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Home route
@app.route('/')
def index():
    if 'plot_data' not in session:
        session['plot_data'] = {"lines": [], "planes": []}
    return render_template('index.html')

# Route for plotting lines and planes
@app.route('/plot', methods=['POST'])
def plot():
    data = request.get_json()
    plot_type = data.get('type')
    trend = data.get('trend')
    plunge = data.get('plunge')
    strike = data.get('strike')
    dip_direction = data.get('dip_direction')
    dip_angle = data.get('dip_angle')

    if plot_type == 'line' and trend is not None and plunge is not None:
        session['plot_data']['lines'].append((trend, plunge))
    elif plot_type == 'plane' and strike is not None and dip_direction is not None and dip_angle is not None:
        session['plot_data']['planes'].append((strike, dip_direction, dip_angle))

    session.modified = True
    plot_data = create_stereonet_image(session['plot_data'])
    return jsonify(plot_data)

# Route for exporting plots
@app.route('/export_plot', methods=['GET'])
def export_plot():
    file_format = request.args.get('format', 'png').lower()
    plot_data = session.get('plot_data', {"lines": [], "planes": []})
    plot_image = create_stereonet_image(plot_data, file_format)

    if file_format == 'png':
        return jsonify(plot_image)
    else:
        filename = f"stereonet_plot.{file_format}"
        return send_file(io.BytesIO(plot_image), mimetype=f"image/{file_format}", as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)
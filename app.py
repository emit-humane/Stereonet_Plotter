from flask import Flask, render_template, request, jsonify, session, send_file
from stereonet_calculations import create_stereonet_image
import io

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/')
def index():
    session.pop('plot_data', None)  # Clear session data on page load
    return render_template('index.html')

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
        session.setdefault('plot_data', {'lines': [], 'planes': []})
        session['plot_data']['lines'].append((trend, plunge))
    elif plot_type == 'plane' and strike is not None and dip_direction is not None and dip_angle is not None:
        session.setdefault('plot_data', {'lines': [], 'planes': []})
        session['plot_data']['planes'].append((strike, dip_direction, dip_angle))

    session.modified = True
    plot_data = create_stereonet_image(session['plot_data'])
    return jsonify(plot_data)

@app.route('/get_plot_data', methods=['GET'])
def get_plot_data():
    return jsonify(session.get('plot_data', {"lines": [], "planes": []}))

@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    plot_type = data.get('type')
    index = data.get('index')

    if plot_type == 'line' and 'plot_data' in session and index < len(session['plot_data']['lines']):
        session['plot_data']['lines'].pop(index)
    elif plot_type == 'plane' and 'plot_data' in session and index < len(session['plot_data']['planes']):
        session['plot_data']['planes'].pop(index)

    session.modified = True
    plot_data = create_stereonet_image(session['plot_data'])
    return jsonify(plot_data)

@app.route('/export_plot', methods=['GET'])
def export_plot():
    file_format = request.args.get('format', 'png').lower()
    plot_data = session.get('plot_data', {"lines": [], "planes": []})
    plot_image = create_stereonet_image(plot_data, file_format)

    if file_format == 'png':
        # Return JSON with base64-encoded image data for PNG
        return jsonify({'plot_data': plot_image})
    elif file_format in ['pdf', 'svg']:
        # Return the file as a blob with appropriate MIME type
        filename = f"stereonet_plot.{file_format}"
        mime_type = f"application/{file_format}" if file_format != 'svg' else "image/svg+xml"
        return send_file(io.BytesIO(plot_image), mimetype=mime_type, as_attachment=True, download_name=filename)
    else:
        return jsonify({"error": "Invalid format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
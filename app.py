"""
Flask web application for SPC Chart generation.
Provides a simple web interface for creating interactive control charts.
"""

from flask import Flask, render_template_string, request, jsonify
from spcchart.plotly_chart import PlotlySpcChart
from spcchart.spc import CHART_X_MR_X, CHART_X_BAR_R_X, CHART_P, CHART_C

app = Flask(__name__)

# HTML template for the main page
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPC Chart Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        .content {
            padding: 40px;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
            font-size: 0.95em;
        }
        input[type="text"],
        textarea,
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus,
        textarea:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        textarea {
            min-height: 120px;
            resize: vertical;
            font-family: monospace;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 5px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        .btn:active {
            transform: translateY(0);
        }
        #chart-output {
            margin-top: 30px;
        }
        .example {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 0.9em;
        }
        .example code {
            font-family: monospace;
            background: #e0e0e0;
            padding: 2px 6px;
            border-radius: 3px;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        .loading.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 SPC Chart Generator</h1>
            <p>Statistical Process Control Charts For Humans</p>
        </div>

        <div class="content">
            <form id="chart-form">
                <div class="form-group">
                    <label for="title">Chart Title</label>
                    <input type="text" id="title" name="title" placeholder="e.g., Widget Quality Measurements" required>
                </div>

                <div class="form-group">
                    <label for="data">Data Points (comma-separated numbers)</label>
                    <textarea id="data" name="data" placeholder="e.g., 1,2,3,4,5,6,7,8,9,8,7,6,5,5,5,4,4,3,3,2,2,2,3,4,5,5,5" required></textarea>
                    <div class="example">
                        <strong>Example:</strong> <code>98.6, 98.7, 98.5, 98.8, 98.6, 98.7, 98.6, 98.5, 98.9, 98.7</code>
                    </div>
                </div>

                <div class="form-group">
                    <label for="chart-type">Chart Type</label>
                    <select id="chart-type" name="chart_type">
                        <option value="X mR - X">X-mR (Individual and Moving Range)</option>
                        <option value="Xbar R - X">X-bar R (Subgroup Mean)</option>
                        <option value="p">p-chart (Proportion Defective)</option>
                        <option value="c">c-chart (Count of Defects)</option>
                    </select>
                </div>

                <button type="submit" class="btn">Generate Chart</button>
            </form>

            <div class="loading" id="loading">
                <h3>Generating chart...</h3>
            </div>

            <div id="chart-output"></div>
        </div>
    </div>

    <script>
        document.getElementById('chart-form').addEventListener('submit', async (e) => {
            e.preventDefault();

            const loading = document.getElementById('loading');
            const output = document.getElementById('chart-output');

            loading.classList.add('show');
            output.innerHTML = '';

            const formData = new FormData(e.target);
            const data = {
                title: formData.get('title'),
                data: formData.get('data'),
                chart_type: formData.get('chart_type')
            };

            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (result.error) {
                    output.innerHTML = `<div style="color: red; padding: 20px; background: #ffe0e0; border-radius: 5px;">${result.error}</div>`;
                } else {
                    output.innerHTML = result.html;
                }
            } catch (error) {
                output.innerHTML = `<div style="color: red; padding: 20px; background: #ffe0e0; border-radius: 5px;">Error: ${error.message}</div>`;
            } finally {
                loading.classList.remove('show');
            }
        });
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Main page with chart generation form."""
    return render_template_string(MAIN_TEMPLATE)


@app.route('/api/generate', methods=['POST'])
def generate_chart():
    """API endpoint to generate SPC chart."""
    try:
        data_dict = request.get_json()

        # Parse input data
        title = data_dict.get('title', 'SPC Chart')
        data_str = data_dict.get('data', '')
        chart_type = data_dict.get('chart_type', CHART_X_MR_X)

        # Convert comma-separated string to list of floats
        data = [float(x.strip()) for x in data_str.split(',') if x.strip()]

        if not data:
            return jsonify({'error': 'No valid data provided'}), 400

        if len(data) < 2:
            return jsonify({'error': 'At least 2 data points are required'}), 400

        # Create chart
        chart = PlotlySpcChart(data, title=title, chart_type=chart_type)
        html = chart.render_to_html(include_plotlyjs='cdn')

        # Get statistics
        center, lcl, ucl = chart.center, chart.lcl, chart.ucl
        violations = chart.violations

        stats_html = f"""
        <div style="background: #f0f0f0; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
            <h3>Statistics</h3>
            <p><strong>Center Line:</strong> {center:.4f}</p>
            <p><strong>Lower Control Limit (LCL):</strong> {f'{lcl:.4f}' if lcl is not None else 'N/A'}</p>
            <p><strong>Upper Control Limit (UCL):</strong> {f'{ucl:.4f}' if ucl is not None else 'N/A'}</p>
            {f'<p style="color: orange;"><strong>Violations detected:</strong> {len(violations)} rule(s)</p>' if violations else '<p style="color: green;"><strong>No violations detected</strong></p>'}
        </div>
        """

        return jsonify({'html': stats_html + html})

    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error generating chart: {str(e)}'}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

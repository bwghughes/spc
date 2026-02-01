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
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Generate Statistical Process Control charts with ease. Create X-mR, X-bar R, p-charts, and c-charts interactively.">
    <title>SPC Chart Generator | Statistical Process Control Charts</title>
    <style>
        :root {
            --color-primary: #6366f1;
            --color-primary-dark: #4f46e5;
            --color-primary-light: #818cf8;
            --color-success: #10b981;
            --color-warning: #f59e0b;
            --color-error: #ef4444;
            --color-bg: #f8fafc;
            --color-bg-alt: #f1f5f9;
            --color-surface: #ffffff;
            --color-surface-alt: #f8fafc;
            --color-text: #1e293b;
            --color-text-muted: #64748b;
            --color-border: #e2e8f0;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
            --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
            --radius-sm: 0.375rem;
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
            --radius-xl: 1rem;
            --transition: 0.2s ease;
        }

        [data-theme="dark"] {
            --color-bg: #0f172a;
            --color-bg-alt: #1e293b;
            --color-surface: #1e293b;
            --color-surface-alt: #334155;
            --color-text: #f1f5f9;
            --color-text-muted: #94a3b8;
            --color-border: #334155;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--color-bg);
            color: var(--color-text);
            min-height: 100vh;
            line-height: 1.6;
            transition: background var(--transition), color var(--transition);
        }

        .app {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        /* Header */
        .header {
            background: var(--color-surface);
            border-bottom: 1px solid var(--color-border);
            padding: 1rem 1.5rem;
            position: sticky;
            top: 0;
            z-index: 100;
            transition: background var(--transition), border-color var(--transition);
        }

        .header-content {
            max-width: 1280px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: var(--color-text);
        }

        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
        }

        .logo-text {
            font-weight: 700;
            font-size: 1.25rem;
            letter-spacing: -0.025em;
        }

        .logo-text span {
            color: var(--color-primary);
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .theme-toggle {
            width: 40px;
            height: 40px;
            border-radius: var(--radius-md);
            border: 1px solid var(--color-border);
            background: var(--color-surface-alt);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            transition: all var(--transition);
        }

        .theme-toggle:hover {
            border-color: var(--color-primary);
            background: var(--color-bg-alt);
        }

        .github-link {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: var(--radius-md);
            border: 1px solid var(--color-border);
            background: var(--color-surface-alt);
            color: var(--color-text);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all var(--transition);
        }

        .github-link:hover {
            border-color: var(--color-primary);
            background: var(--color-bg-alt);
        }

        /* Main Content */
        .main {
            flex: 1;
            max-width: 1280px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
            width: 100%;
        }

        .hero {
            text-align: center;
            margin-bottom: 3rem;
        }

        .hero h1 {
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 800;
            letter-spacing: -0.025em;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero p {
            font-size: 1.125rem;
            color: var(--color-text-muted);
            max-width: 600px;
            margin: 0 auto;
        }

        /* Grid Layout */
        .grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 2rem;
        }

        @media (min-width: 1024px) {
            .grid {
                grid-template-columns: 400px 1fr;
            }
        }

        /* Card */
        .card {
            background: var(--color-surface);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-xl);
            overflow: hidden;
            transition: background var(--transition), border-color var(--transition);
        }

        .card-header {
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--color-border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .card-title {
            font-size: 1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .card-body {
            padding: 1.5rem;
        }

        /* Form */
        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-group:last-child {
            margin-bottom: 0;
        }

        .form-label {
            display: block;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--color-text);
        }

        .form-hint {
            font-size: 0.75rem;
            color: var(--color-text-muted);
            margin-top: 0.375rem;
        }

        .form-input,
        .form-textarea,
        .form-select {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 1px solid var(--color-border);
            border-radius: var(--radius-md);
            font-size: 0.9375rem;
            background: var(--color-surface);
            color: var(--color-text);
            transition: all var(--transition);
        }

        .form-input:focus,
        .form-textarea:focus,
        .form-select:focus {
            outline: none;
            border-color: var(--color-primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
        }

        .form-textarea {
            min-height: 100px;
            resize: vertical;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
            font-size: 0.875rem;
            line-height: 1.5;
        }

        .form-select {
            cursor: pointer;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2364748b'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 0.75rem center;
            background-size: 1.25rem;
            padding-right: 2.5rem;
        }

        /* Sample Data Presets */
        .presets {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.75rem;
        }

        .preset-btn {
            padding: 0.375rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 500;
            border: 1px solid var(--color-border);
            border-radius: var(--radius-sm);
            background: var(--color-surface-alt);
            color: var(--color-text-muted);
            cursor: pointer;
            transition: all var(--transition);
        }

        .preset-btn:hover {
            border-color: var(--color-primary);
            color: var(--color-primary);
            background: rgba(99, 102, 241, 0.1);
        }

        /* Button */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 0.875rem 1.5rem;
            font-size: 0.9375rem;
            font-weight: 600;
            border: none;
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: all var(--transition);
            text-decoration: none;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            color: white;
            width: 100%;
        }

        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: var(--shadow-lg);
        }

        .btn-primary:active {
            transform: translateY(0);
        }

        .btn-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        /* Loading */
        .loading-spinner {
            width: 1.25rem;
            height: 1.25rem;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Chart Output */
        .output-area {
            min-height: 400px;
            display: flex;
            flex-direction: column;
        }

        .output-placeholder {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: var(--color-text-muted);
            padding: 3rem;
        }

        .output-placeholder-icon {
            width: 80px;
            height: 80px;
            background: var(--color-bg-alt);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin-bottom: 1.5rem;
        }

        .output-placeholder h3 {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--color-text);
            margin-bottom: 0.5rem;
        }

        /* Statistics Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .stat-card {
            padding: 1rem;
            background: var(--color-bg-alt);
            border-radius: var(--radius-md);
            text-align: center;
        }

        .stat-label {
            font-size: 0.75rem;
            font-weight: 500;
            color: var(--color-text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.375rem;
        }

        .stat-value {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--color-text);
            font-family: 'SF Mono', Monaco, monospace;
        }

        .stat-card.success .stat-value {
            color: var(--color-success);
        }

        .stat-card.warning .stat-value {
            color: var(--color-warning);
        }

        /* Alert */
        .alert {
            padding: 1rem 1.25rem;
            border-radius: var(--radius-md);
            font-size: 0.9375rem;
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
        }

        .alert-error {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: var(--color-error);
        }

        .alert-icon {
            flex-shrink: 0;
            font-size: 1.25rem;
        }

        /* Chart Container */
        .chart-container {
            border-radius: var(--radius-md);
            overflow: hidden;
            background: var(--color-surface);
        }

        /* Footer */
        .footer {
            background: var(--color-surface);
            border-top: 1px solid var(--color-border);
            padding: 1.5rem;
            text-align: center;
            transition: background var(--transition), border-color var(--transition);
        }

        .footer p {
            font-size: 0.875rem;
            color: var(--color-text-muted);
        }

        .footer a {
            color: var(--color-primary);
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        /* Responsive */
        @media (max-width: 640px) {
            .header-content {
                flex-wrap: wrap;
                gap: 1rem;
            }

            .github-link span {
                display: none;
            }

            .main {
                padding: 1.5rem 1rem;
            }

            .card-body {
                padding: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="app">
        <header class="header">
            <div class="header-content">
                <a href="/" class="logo">
                    <div class="logo-icon">📊</div>
                    <div class="logo-text">SPC<span>Chart</span></div>
                </a>
                <div class="header-actions">
                    <button class="theme-toggle" id="theme-toggle" aria-label="Toggle dark mode" title="Toggle dark mode">
                        <span id="theme-icon">🌙</span>
                    </button>
                    <a href="https://github.com/bwghughes/spc" class="github-link" target="_blank" rel="noopener">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                        </svg>
                        <span>GitHub</span>
                    </a>
                </div>
            </div>
        </header>

        <main class="main">
            <div class="hero">
                <h1>Statistical Process Control Charts</h1>
                <p>Create interactive control charts to monitor your processes. Detect variations and ensure quality with powerful SPC analysis.</p>
            </div>

            <div class="grid">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">
                            <span>⚙️</span> Configuration
                        </h2>
                    </div>
                    <div class="card-body">
                        <form id="chart-form">
                            <div class="form-group">
                                <label class="form-label" for="title">Chart Title</label>
                                <input type="text" class="form-input" id="title" name="title" placeholder="e.g., Production Line Quality" required>
                            </div>

                            <div class="form-group">
                                <label class="form-label" for="chart-type">Chart Type</label>
                                <select class="form-select" id="chart-type" name="chart_type">
                                    <option value="X mR - X">X-mR (Individual and Moving Range)</option>
                                    <option value="Xbar R - X">X-bar R (Subgroup Mean)</option>
                                    <option value="p">p-chart (Proportion Defective)</option>
                                    <option value="c">c-chart (Count of Defects)</option>
                                </select>
                                <p class="form-hint">Select the type of control chart for your data</p>
                            </div>

                            <div class="form-group">
                                <label class="form-label" for="data">Data Points</label>
                                <textarea class="form-textarea" id="data" name="data" placeholder="Enter comma-separated values..." required></textarea>
                                <p class="form-hint">Enter your measurements as comma-separated numbers</p>
                                <div class="presets">
                                    <button type="button" class="preset-btn" data-preset="temperature">Temperature</button>
                                    <button type="button" class="preset-btn" data-preset="quality">Quality Score</button>
                                    <button type="button" class="preset-btn" data-preset="defects">Defect Count</button>
                                    <button type="button" class="preset-btn" data-preset="production">Production</button>
                                </div>
                            </div>

                            <button type="submit" class="btn btn-primary" id="submit-btn">
                                <span id="btn-text">Generate Chart</span>
                                <div class="loading-spinner" id="btn-spinner" style="display: none;"></div>
                            </button>
                        </form>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">
                            <span>📈</span> Chart Output
                        </h2>
                    </div>
                    <div class="card-body output-area" id="chart-output">
                        <div class="output-placeholder">
                            <div class="output-placeholder-icon">📊</div>
                            <h3>No Chart Generated</h3>
                            <p>Configure your settings and click "Generate Chart" to create an interactive SPC chart.</p>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <footer class="footer">
            <p>Built with <a href="https://github.com/bwghughes/spc">SPCChart</a> — Statistical Process Control Charts For Humans</p>
        </footer>
    </div>

    <script>
        // Sample data presets
        const presets = {
            temperature: {
                title: 'Temperature Monitoring',
                data: '98.6, 98.7, 98.5, 98.8, 98.6, 98.7, 98.6, 98.5, 98.9, 98.7, 98.6, 98.8, 98.5, 98.7, 98.6, 98.8, 98.7, 98.5, 98.6, 98.7'
            },
            quality: {
                title: 'Widget Quality Measurements',
                data: '1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 5, 5, 4, 4, 3, 3, 2, 2, 2, 3, 4, 5, 5, 5'
            },
            defects: {
                title: 'Daily Defect Count',
                data: '3, 2, 4, 1, 5, 2, 3, 4, 2, 1, 3, 2, 4, 3, 2, 1, 2, 3, 4, 2'
            },
            production: {
                title: 'Production Output',
                data: '102, 98, 101, 99, 103, 97, 100, 101, 99, 102, 98, 100, 101, 99, 103, 98, 100, 102, 99, 101'
            }
        };

        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        const themeIcon = document.getElementById('theme-icon');
        const html = document.documentElement;

        // Check for saved theme preference or system preference
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light');

        html.setAttribute('data-theme', initialTheme);
        themeIcon.textContent = initialTheme === 'dark' ? '☀️' : '🌙';

        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            themeIcon.textContent = newTheme === 'dark' ? '☀️' : '🌙';
        });

        // Preset buttons
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const preset = presets[btn.dataset.preset];
                if (preset) {
                    document.getElementById('title').value = preset.title;
                    document.getElementById('data').value = preset.data;
                }
            });
        });

        // Form submission
        document.getElementById('chart-form').addEventListener('submit', async (e) => {
            e.preventDefault();

            const submitBtn = document.getElementById('submit-btn');
            const btnText = document.getElementById('btn-text');
            const btnSpinner = document.getElementById('btn-spinner');
            const output = document.getElementById('chart-output');

            // Show loading state
            submitBtn.disabled = true;
            btnText.textContent = 'Generating...';
            btnSpinner.style.display = 'block';

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
                    output.innerHTML = `
                        <div class="alert alert-error">
                            <span class="alert-icon">⚠️</span>
                            <div>${result.error}</div>
                        </div>
                    `;
                } else {
                    output.innerHTML = result.html;
                }
            } catch (error) {
                output.innerHTML = `
                    <div class="alert alert-error">
                        <span class="alert-icon">⚠️</span>
                        <div>Connection error: ${error.message}</div>
                    </div>
                `;
            } finally {
                submitBtn.disabled = false;
                btnText.textContent = 'Generate Chart';
                btnSpinner.style.display = 'none';
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

        # Determine violation status class
        violation_class = 'warning' if violations else 'success'
        violation_text = f'{len(violations)} detected' if violations else 'None'

        stats_html = f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Center Line</div>
                <div class="stat-value">{center:.4f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">LCL</div>
                <div class="stat-value">{f'{lcl:.4f}' if lcl is not None else 'N/A'}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">UCL</div>
                <div class="stat-value">{f'{ucl:.4f}' if ucl is not None else 'N/A'}</div>
            </div>
            <div class="stat-card {violation_class}">
                <div class="stat-label">Violations</div>
                <div class="stat-value">{violation_text}</div>
            </div>
        </div>
        <div class="chart-container">
        """

        chart_end_html = "</div>"

        return jsonify({'html': stats_html + html + chart_end_html})

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

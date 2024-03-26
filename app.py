from flask import Flask, render_template, request, redirect, url_for
import random
import string

app = Flask(__name__)

# Dictionary to store long URL - short URL mapping and analytics data
url_mapping = {}

# Function to generate a random short code
def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

# Route to render the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle URL shortening
@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    short_code = generate_short_code()
    short_url = request.host_url + short_code
    url_mapping[short_code] = {'long_url': long_url, 'visits': 0}
    return render_template('shortened.html', short_url=short_url)

# Route to redirect short URLs to their original long URLs
@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    if short_code in url_mapping:
        url_mapping[short_code]['visits'] += 1
        return redirect(url_mapping[short_code]['long_url'])
    else:
        return render_template('404.html'), 404

# Route to display analytics data
@app.route('/analytics')
def analytics():
    return render_template('analytics.html', url_mapping=url_mapping)

if __name__ == '__main__':
    app.run(debug=True)

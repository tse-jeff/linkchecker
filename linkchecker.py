from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to check links
def check_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    results = []

    for link in links:
        link_url = link['href']
        if not link_url.startswith('http'):
            link_url = requests.compat.urljoin(url, link_url)

        try:
            link_response = requests.get(link_url)
            if link_response.status_code == 200:
                results.append({"url": link_url, "status": "works"})
            else:
                results.append({"url": link_url, "status": f"broken - Status Code: {link_response.status_code}"})
        
        except requests.exceptions.RequestException as e:
            results.append({"url": link_url, "status": f"Failed - Error: {e}"})

    return results

# Define the route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    if request.method == 'POST':
        url = request.form.get('website_url')
        if url:
            results = check_links(url)
    return render_template('test.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

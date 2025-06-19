from flask import Flask, render_template_string, request, redirect
import requests
import os

app = Flask(__name__)
backend_url = os.getenv("BACKEND_URL", "http://backend:8080")

HTML = """
<!DOCTYPE html>
<html>
<head><title>Vote</title></head>
<body>
  <h1>Vote for your favorite candidate</h1>
  <form method="post" action="/vote">
    <input type="radio" name="candidate" value="Alice" required> Alice<br>
    <input type="radio" name="candidate" value="Bob" required> Bob<br>
    <input type="radio" name="candidate" value="Charlie" required> Charlie<br><br>
    <input type="submit" value="Vote">
  </form>
  <h2>Current Results</h2>
  <ul>
    {% for candidate, votes in results.items() %}
      <li>{{candidate}}: {{votes}}</li>
    {% endfor %}
  </ul>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    try:
        resp = requests.get(f"{backend_url}/results")
        results = resp.json()
    except:
        results = {}
    return render_template_string(HTML, results=results)

@app.route('/vote', methods=['POST'])
def vote():
    candidate = request.form.get('candidate')
    if candidate:
        requests.post(f"{backend_url}/vote", json={"candidate": candidate})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

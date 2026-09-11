import string
import random
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

url_database = {}

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dynamic URL Shortener</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            /* عکس پیش‌فرض (شب) */
            background-image: url('{{ night_bg }}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            transition: background-image 1s ease-in-out; /* افکت تغییر نرم پس‌زمینه */
        }
        .container {
            background: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
            text-align: center;
            width: 350px;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 6px;
            box-sizing: border-box;
            margin-bottom: 15px;
        }
        button {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #218838;
        }
        .result {
            margin-top: 20px;
            font-size: 16px;
            word-break: break-all;
        }
        a {
            color: #007bff;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body id="page-body">
    <div class="container">
        <h2>URL Shortener</h2>
        <form method="POST" onsubmit="changeBackground()">
            <input type="text" name="long_url" placeholder="Enter long URL here..." required>
            <button type="submit">Shorten Link</button>
        </form>
        {% if short_url %}
        <div class="result">
            <p>Shortened Link:</p>
            <a href="{{ short_url }}" target="_blank">{{ short_url }}</a>
        </div>
        <script>
            // تغییر پس‌زمینه به حالت روز بعد از کوتاه شدن لینک
            document.getElementById('page-body').style.backgroundImage = "url('{{ day_bg }}')";
        </script>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    # لینک عکس شب که فرستادی به همراه یک عکس روز باکیفیت و هماهنگ
    night_bg = "https://miro.medium.com/v2/resize:fit:12032/1*tUfdYNHPIEAg2ZWExDDm_Q.jpeg"
    day_bg = "https://images.unsplash.com/photo-1506744038136-46273834b3fb"
    
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        code = generate_short_code()
        url_database[code] = long_url
        short_url = request.host_url + code
        
    return render_template_string(HTML_PAGE, short_url=short_url, night_bg=night_bg, day_bg=day_bg)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    long_url = url_database.get(short_code)
    if long_url:
        return redirect(long_url)
    return "URL not found!", 404

if __name__ == '__main__':
    app.run(debug=True)
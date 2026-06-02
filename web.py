from flask import Flask, request, redirect, session
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "queen_secret_key"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

manager_img = None
gallery = []

ADMIN_USERNAME = "Queen"
ADMIN_PASSWORD = "Queen@1986"

OWNER_EMAIL = "shudufhadzomulangaphuma@gmail.com"
EMAIL_PASSWORD = "xnixlpygrvprggaw"


# ================= EMAIL =================
def send_email(name, phone, service, date, time):

    msg = MIMEText(f"""
👑 NEW BOOKING 👑

Name: {name}
Phone: {phone}
Service: {service}
Date: {date}
Time: {time}

Queen's Crown Beauty Studio
""")

    msg["Subject"] = "New Booking"
    msg["From"] = OWNER_EMAIL
    msg["To"] = OWNER_EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(OWNER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(OWNER_EMAIL, OWNER_EMAIL, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email error:", e)


# ================= GLOBAL STYLE =================
STYLE = """
<style>
body {
    margin:0;
    font-family:Arial;
    color:white;
    background:url('https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?auto=format&fit=crop&w=1950&q=80') center/cover fixed;
}

body::before {
    content:"";
    position:fixed;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.65);
    z-index:-1;
}

h1,h2,h3,p,li {
    color:white;
}

a {
    color:white;
    text-decoration:none;
    font-weight:bold;
}

.container {
    text-align:center;
    padding:30px;
}

.card {
    background:rgba(255,255,255,0.12);
    padding:20px;
    margin:10px;
    border-radius:15px;
    display:inline-block;
    width:260px;
}
</style>
"""


# ================= HOME =================
@app.route("/")
def home():

    manager_html = f"<img src='/static/uploads/{manager_img}' width='180'>" if manager_img else ""

    gallery_html = "".join([
        f"<img src='/static/uploads/{img}' width='90' style='margin:5px;border-radius:8px;'>"
        for img in gallery
    ])

    return f"""
<html>
<head>
<title>Queen's Crown Beauty Studio</title>
{STYLE}
</head>

<body>

<header class="container">
<h1>👑 QUEEN'S CROWN BEAUTY STUDIO</h1>
<p>Where every queen is crowned in beauty 💅💇</p>
</header>

<nav class="container">
<a href="/">Home</a> |
<a href="/services">Services</a> |
<a href="/booking">Book</a> |
<a href="/gallery">Gallery</a> |
<a href="/admin">Admin</a>
</nav>

<div class="container">

<div class="card">
<h3>👩‍💼 Manager</h3>
{manager_html}
</div>

<div class="card">
<h3>💅 Gallery</h3>
{gallery_html}
</div>

</div>

</body>
</html>
"""


# ================= SERVICES =================
@app.route("/services")
def services():
    return f"""
<html>
<head>
<title>Services</title>
{STYLE}
</head>

<body>

<div class="container">

<h1>💇 Our Services</h1>

<div class="card">Braiding</div>
<div class="card">Wig Installation</div>
<div class="card">Hair Treatment</div>
<div class="card">Hair Coloring</div>
<div class="card">Manicure</div>
<div class="card">Pedicure</div>
<div class="card">Gel Nails</div>
<div class="card">Acrylic Nails</div>

<br><br>
<a href="/">⬅ Back Home</a>

</div>

</body>
</html>
"""


# ================= BOOKING =================
@app.route("/booking", methods=["GET", "POST"])
def booking():

    if request.method == "POST":

        send_email(
            request.form["name"],
            request.form["phone"],
            request.form["service"],
            request.form["date"],
            request.form["time"]
        )

        return f"""
        <html>
        <head>{STYLE}</head>
        <body>
        <div class="container">
        <h2>Booking Sent Successfully 👑💅</h2>
        <a href="/">Back Home</a>
        </div>
        </body>
        </html>
        """

    return f"""
<html>
<head>
<title>Book Appointment</title>
{STYLE}
</head>

<body>

<div class="container">

<h1>📅 Book Appointment</h1>

<form method="POST">

<input name="name" placeholder="Full Name"><br><br>
<input name="phone" placeholder="Phone"><br><br>
<input name="service" placeholder="Service"><br><br>
<input type="date" name="date"><br><br>
<input type="time" name="time"><br><br>

<button>Book Now</button>

</form>

<br><a href="/">Back</a>

</div>

</body>
</html>
"""


# ================= GALLERY =================
@app.route("/gallery")
def gallery_page():

    images = "".join([
        f"<img src='/static/uploads/{img}' width='150' style='margin:5px;border-radius:10px;'>"
        for img in gallery
    ])

    return f"""
<html>
<head>
<title>Gallery</title>
{STYLE}
</head>

<body>

<div class="container">

<h1>💅 Gallery</h1>

{images}

<br><br>
<a href="/">⬅ Back Home</a>

</div>

</body>
</html>
"""


# ================= ADMIN =================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":

        username = request.form.get("admin_user")
        password = request.form.get("admin_password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/panel")

        return "<h3>Wrong login</h3><a href='/admin'>Try again</a>"

    return f"""
    <html>
    <head>
    <title>Admin Login</title>
    {STYLE}
    </head>

    <body>

    <div class="container">

    <h1>Admin Login</h1>

    <form method="POST" autocomplete="off">

    <!-- VERY IMPORTANT: fake login fields to absorb browser autofill -->
    <input type="text" name="fake_user" style="display:none" autocomplete="username">
    <input type="password" name="fake_pass" style="display:none" autocomplete="current-password">

    <!-- REAL FIELDS (renamed to avoid browser detection) -->
    <input
        name="admin_user"
        placeholder="Username"
        autocomplete="off"
        required
    ><br><br>

    <input
        type="password"
        name="admin_password"
        placeholder="Password"
        autocomplete="off"
        required
    ><br><br>

    <button type="submit">Login</button>

    </form>

    </div>

    </body>
    </html>
    """


# ================= PANEL =================
@app.route("/panel")
def panel():

    if not session.get("admin"):
        return redirect("/admin")

    return f"""
<html>
<head>{STYLE}</head>

<body>

<div class="container">

<h2>👑 Admin Panel</h2>

<form action="/upload_manager" method="POST" enctype="multipart/form-data">
<input type="file" name="manager">
<button>Upload Manager</button>
</form>

<br>

<form action="/upload_work" method="POST" enctype="multipart/form-data">
<input type="file" name="work">
<button>Upload Work</button>
</form>

<br><br>

<a href="/logout">Logout</a><br>
<a href="/">Home</a>

</div>

</body>
</html>
"""


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/admin")


# ================= UPLOADS =================
@app.route("/upload_manager", methods=["POST"])
def upload_manager():
    global manager_img

    if session.get("admin"):
        file = request.files["manager"]
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        manager_img = file.filename

    return redirect("/panel")


@app.route("/upload_work", methods=["POST"])
def upload_work():

    if session.get("admin"):
        file = request.files["work"]
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        gallery.append(file.filename)

    return redirect("/panel")


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, session
from function.auth import login, register
from function.event import tampilkan_event, tambah_event, hapus_event
from function.ticket import beli_tiket, tiket_user
import os

app = Flask(__name__)
app.secret_key = "rahasia123"

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'app.secret_key')
app.config['DEBUG'] = False

@app.route("/")
def index():
    events = tampilkan_event()
    return render_template("index.html", events=events)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        user = login(request.form["username"], request.form["password"])
        if user:
            session["user"] = user
            if user["role"] == "admin":
                return redirect("/dashboard")
            return redirect("/")
        return "Login gagal!"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        result = register(request.form["username"], request.form["password"])
        if result == "success":
            return redirect("/login")
        else:
            return result
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect("/login")
    events = tampilkan_event()
    return render_template("dashboard.html", events=events)

@app.route("/tambah_event", methods=["POST"])
def tambah_event_route():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect("/login")

    nama = request.form["nama"]
    tanggal = request.form["tanggal"]
    lokasi = request.form["lokasi"]
    harga = int(request.form["harga"])
    stok_tiket = int(request.form["stok_tiket"])

    tambah_event(nama, tanggal, lokasi, harga, stok_tiket)
    return redirect("/dashboard")

@app.route("/hapus_event/<int:event_id>", methods=["POST"])
def hapus_event_route(event_id):
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect("/login")
    hapus_event(event_id)
    return redirect("/dashboard")

@app.route("/beli_tiket/<int:event_id>", methods=["POST"])
def beli_tiket_route(event_id):
    if "user" not in session or session["user"]["role"] != "user":
        return redirect("/login")

    jumlah = int(request.form["jumlah"])
    user_id = session["user"]["id"]

    result = beli_tiket(user_id, event_id, jumlah)
    if result == "success":
        return redirect("/my_tickets")
    else:
        return result

@app.route("/my_tickets")
def my_tickets():
    if "user" not in session or session["user"]["role"] != "user":
        return redirect("/login")

    user_id = session["user"]["id"]
    data_tiket = tiket_user(user_id)
    events = tampilkan_event()

    tiket_dengan_detail = []
    for t in data_tiket:
        for e in events:
            if e["id"] == t["event_id"]:
                tiket_dengan_detail.append({
                    "event_id": e["id"],
                    "nama": e["nama"],
                    "tanggal": e["tanggal"],
                    "lokasi": e["lokasi"],
                    "harga": e["harga"],
                    "jumlah": t["jumlah"],
                    "total_harga": t["total_harga"]
                })

    return render_template("my_tickets.html", tickets=tiket_dengan_detail)

@app.route("/batalkan_tiket/<int:event_id>", methods=["POST"])
def batalkan_tiket_route(event_id):
    if "user" not in session or session["user"]["role"] != "user":
        return redirect("/login")

    user_id = session["user"]["id"]
    from function.ticket import batalkan_tiket
    result = batalkan_tiket(user_id, event_id)
    if result == "success":
        return redirect("/my_tickets")
    else:
        return "Gagal membatalkan tiket!"

if __name__ == "__main__":
    app.run(debug=True)
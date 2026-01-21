from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

# ================= APP CONFIG =================
app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload folders
UPLOAD_FILES = os.path.join(BASE_DIR, 'uploads', 'files')
UPLOAD_PREVIEWS = os.path.join(BASE_DIR, 'uploads', 'previews')
os.makedirs(UPLOAD_FILES, exist_ok=True)
os.makedirs(UPLOAD_PREVIEWS, exist_ok=True)

db = SQLAlchemy(app)

# ================= DATABASE =================
class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)   # 0 = FREE
    asset_type = db.Column(db.String(10), nullable=False)  # 2D / 3D
    filename = db.Column(db.String(200), nullable=False)
    preview_image = db.Column(db.String(200), nullable=False)

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/assets")
def assets():
    all_assets = Asset.query.order_by(Asset.id.desc()).all()
    return render_template("assets.html", assets=all_assets)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        name = request.form['name']
        category = request.form['category']
        price = int(request.form['price'])
        asset_type = request.form['asset_type']

        asset_file = request.files.get('file')
        preview_file = request.files.get('preview')

        if not asset_file or not preview_file:
            abort(400)

        asset_filename = secure_filename(asset_file.filename)
        preview_filename = secure_filename(preview_file.filename)

        asset_file.save(os.path.join(UPLOAD_FILES, asset_filename))
        preview_file.save(os.path.join(UPLOAD_PREVIEWS, preview_filename))

        new_asset = Asset(
            name=name,
            category=category,
            price=price,
            asset_type=asset_type,
            filename=asset_filename,
            preview_image=preview_filename
        )
        db.session.add(new_asset)
        db.session.commit()

        return redirect(url_for("assets"))

    return render_template("upload.html")

@app.route("/asset/<int:asset_id>")
def asset_detail(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    return render_template("asset.html", asset=asset)

# ================= PREVIEW IMAGE =================
@app.route("/preview/<filename>")
def preview_image(filename):
    return send_from_directory(UPLOAD_PREVIEWS, filename)

# ================= SECURE DOWNLOAD =================
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FILES, filename, as_attachment=True)

# ================= BUY FLOW =================
@app.route("/buy/<int:asset_id>")
def buy(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    if asset.price == 0:
        return redirect(url_for("download_file", filename=asset.filename))
    return render_template("payment_select.html", asset=asset)

# ================= RUN =================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

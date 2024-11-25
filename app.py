from flask import Flask, render_template, request, redirect, url_for
from aes_encryption import encrypt_message, decrypt_message
from PIL import Image, ImageDraw
import qrcodegen
import base64
import os

app = Flask(__name__)

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handling QR code generation
        if "generate" in request.form:
            data = request.form["data"]
            key = request.form["key"]
            encrypted_data = encrypt_message(data, key)

            qr = qrcodegen.QrCode.encode_text(
                encrypted_data, qrcodegen.QrCode.Ecc.LOW
            )
            size = qr.get_size()
            scale = 10
            border = 4
            img_size = (size + 2 * border) * scale

            img = Image.new("1", (img_size, img_size), color="white")
            draw = ImageDraw.Draw(img)

            for y in range(size):
                for x in range(size):
                    if qr.get_module(x, y):
                        draw.rectangle(
                            [
                                ((x + border) * scale, (y + border) * scale),
                                ((x + border + 1) * scale - 1, (y + border + 1) * scale - 1),
                            ],
                            fill="black",
                        )

            img = img.convert("RGB")
            img.save("static/encrypted_qrcode.png")

            return render_template(
                "index.html",
                generated=True,
                encrypted_data=encrypted_data,
                qr_code="static/encrypted_qrcode.png",
            )

        # Handling QR code decryption
        elif "decrypt" in request.form:
            key = request.form["key"]
            try:
                with open("static/encrypted_qrcode.png", "rb") as qr_file:
                    img = Image.open(qr_file)
                    encrypted_data = request.form["encrypted_data"]
                    decrypted_data = decrypt_message(encrypted_data, key)
                    return render_template(
                        "index.html",
                        decrypted=True,
                        decrypted_data=decrypted_data,
                        qr_code="static/encrypted_qrcode.png",
                    )
            except Exception as e:
                return render_template(
                    "index.html",
                    error="Decryption failed. Please check your decryption key.",
                )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

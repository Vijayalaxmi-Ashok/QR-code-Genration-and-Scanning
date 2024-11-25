from PIL import Image, ImageDraw
from pyzbar.pyzbar import decode
import cv2
from aes_encryption import encrypt_message, decrypt_message
import webbrowser
from PIL import Image, ImageDraw
import qrcodegen

def generate_qr():
    data = input("Enter the message to encode in the QR Code: ")
    encryption_key = input("Enter the encryption key: ")

    # Encrypt the message
    encrypted_data = encrypt_message(data, encryption_key)
    print("Encrypted Data: {}".format(encrypted_data))

    # Create QR Code
    qr = qrcodegen.QrCode.encode_text(
        encrypted_data, qrcodegen.QrCode.Ecc.LOW  # Use correct error correction level
    )

    size = qr.get_size()
    scale = 10
    border = 4
    img_size = (size + 2 * border) * scale

    # Create a new image for the QR code
    img = Image.new("1", (img_size, img_size), color="white")
    draw = ImageDraw.Draw(img)

    for y in range(size):
        for x in range(size):
            if qr.get_module(x, y):  # Check if the module is filled
                draw.rectangle(
                    [
                        ((x + border) * scale, (y + border) * scale),
                        ((x + border + 1) * scale - 1, (y + border + 1) * scale - 1),
                    ],
                    fill="black",
                )

    img = img.convert("RGB")
    img.save("encrypted_qrcode.png")
    print("QR Code saved as 'encrypted_qrcode.png'.")

    
# Scan and Decrypt QR Code
def scan_qr():
    image_path = input("Enter the path of the QR Code image to scan: ")
    decryption_key = input("Enter the decryption key: ")

    # Read the QR Code
    image = cv2.imread(image_path)
    decoded_objects = decode(image)

    if not decoded_objects:
        print("No QR Code detected!")
        return

    for obj in decoded_objects:
        encrypted_data = obj.data.decode('utf-8')
        print("Encrypted Data: {}".format(encrypted_data))
        
        try:
            # Decrypt the message
            decrypted_data = decrypt_message(encrypted_data, decryption_key)
            print("Decrypted Data: {}".format(decrypted_data))

            if decrypted_data == "https://www.kletech.ac.in":
                print("Opening KLE Tech website...")
                webbrowser.open(decrypted_data)
            else:
                print("The decrypted message is URL.")

        except Exception as e:
            print("Decryption failed: {}".format(e))

# Main Program
if __name__ == "__main__":
    print("1. Generate QR Code")
    print("2. Scan QR Code")
    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        generate_qr()
    elif choice == "2":
        scan_qr()
    else:
        print("Invalid choice.")

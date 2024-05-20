from flask import Flask, render_template, request
import cv2
from pyzbar.pyzbar import decode
import winsound

app = Flask(__name__)

# Define your functions here
# BarcodeReaderImage function
@app.route("/")
def index():
    return render_template("Index.html")


@app.route("/barcode_cam")
def barcode_cam():
    barcode_data = BarcodeReaderCam()
    return render_template("Result.html", barcode_data=barcode_data)


@app.route("/barcode_image", methods=["POST"])
def barcode_image():
    # Get the uploaded file
    image = request.files["image"]
    image_path = "uploaded_image.jpg"  # Save the image temporarily
    image.save(image_path)
    barcode_data = BarcodeReaderImage(image_path)
    print("Barcode Data:", barcode_data)
    print("Barcode Type:", )
    return render_template("Result.html", barcode_data=barcode_data)


def BarcodeReaderImage(image):
    img = cv2.imread(image)
    detectedBarcodes = decode(img)
    barcode_data = []

    if not detectedBarcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
    else:
        for barcode in detectedBarcodes:
            if barcode.data != "":
                barcode_data.append((barcode.data, barcode.type))
                print("Barcode Data:", barcode.data)
                print("Barcode Type:", barcode.type)

    return barcode_data


def BarcodeReaderCam():
    cap = cv2.VideoCapture(0)
    cap.set(3, 720)
    cap.set(4, 480)

    barcode_data = []

    while not barcode_data:
        success, img = cap.read()

        detectedBarcodes = decode(img)

        if detectedBarcodes:
            for barcode in detectedBarcodes:
                if barcode.data != "":
                    barcode_data.append((barcode.data, barcode.type))
                    print("Barcode Detected:", barcode.data)
                    print("Barcode Type:", barcode.type)
                    winsound.Beep(1000, 500)  # Play a beep sound
                    break  # Stop after detecting the first barcode

    cap.release()
    cv2.destroyAllWindows()

    return barcode_data


if __name__ == "__main__":
    app.run(debug=True, port=8000)  # Change port to 8000


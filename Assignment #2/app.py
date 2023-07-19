from flask import Flask, render_template, request, make_response
import pdfkit
import qrcode
from io import BytesIO
from base64 import b64encode
app = Flask(__name__)


@app.route("/")
def form():
    return render_template('index.html')


@app.route("/generateQR", methods=['POST'])
def generateQRInPdf():
    memory = BytesIO()
    data = "Full name: "+request.form['fullName'] + "\n" + "Email: " + \
        request.form['email']+"\n" + "Phone: " + str(request.form['phone'])
    img = qrcode.make(data)
    img.save(memory)
    memory.seek(0)
    base64Img = "data:image/png;base64," + \
        b64encode(memory.getvalue()).decode('ascii')

    rendered = render_template('QRCode.html', data=base64Img)

    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=QR.pdf'
    return response


if __name__ == "__main__":
    app.run(debug=True)

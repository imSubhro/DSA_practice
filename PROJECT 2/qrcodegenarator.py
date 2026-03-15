import image
import qrcode 
qr = qrcode.QRCode(
    version = 16,
    box_size = 18,
    border = 9
)

data = "https://youtube.com/channel/UCAX_WRmXTTM3hy-87tp4gXA"
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill="black",back_color= "white")
img.save('text.png')


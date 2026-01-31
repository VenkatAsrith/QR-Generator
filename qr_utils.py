import qrcode

def generate_qr_image(data, save_path):
    qr = qrcode.make(data)
    qr.save(save_path)

import qrcode

data = input("Enter your text or Url: ")
file_name = input("enter the file name: ")
qr = qrcode.make(data, box_size=10, border=4)
qr.save(f"{file_name}.png")
print(f"qrcode saved as {file_name}.png")

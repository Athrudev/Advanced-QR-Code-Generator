import segno
from urllib.request import urlopen
from pyzbar.pyzbar import decode
from PIL import Image
from cryptography.fernet import Fernet
import io


default_gif = "https://media.giphy.com/media/LpwBqCorPvZC0/giphy.gif"
default_bg = 'white'
default_qr = 'black'


light_colors = {
        1: "white",
        2: "lightblue",
        3: "lightyellow",
        4: "lightgreen",
        5: "lightpink"
    }

dark_colors = {
        1: "black",
        2: "darkblue",
        3: "darkgreen",
        4: "darkred",
        5: "purple"
    }


gif_options = {
    1: "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",  
    2: "https://media.giphy.com/media/hvS1eKlR75hMr0lYzJ/giphy.gif",
    3: "https://media.giphy.com/media/LpwBqCorPvZC0/giphy.gif",  
    4: "https://media.giphy.com/media/du3J3cXyzhj75IOgvA/giphy.gif", 
    5: "https://media.giphy.com/media/xT5LMHxhOfscxPfIfm/giphy.gif" 
}



def get_info():
    return input('🖊️  Please enter the information for your QR code: ')

def get_name():
    return input('📁 Choose a file name for your QR code: ')

def get_color(array, name, default):
    print(f'\n🎨 {name} color options:')
    for key, value in array.items():
        print(f'   {key}. {value}')
    try:
        choice = int(input(f'Select {name.lower()} color (enter the number): '))
        color = array.get(choice, default)
    except ValueError:
        print(f"⚠️  Invalid input. Using default color: {default}")
        color = default
    return color

def get_gif(array, default):
    print("\n🎭 Animated background options:")
    print("   0. Add custom GIF link")
    for key, value in array.items():
        print(f"   {key}. Animated Background {key}")
    try:
        choice = int(input('Select animated background (enter the number): '))
        if choice == 0:
            custom_link = input("Enter your custom GIF URL: ")
            return custom_link
        gif_url = array.get(choice, default)
    except ValueError:
        print(f"⚠️  Invalid input. Using default animated background.")
        gif_url = default
    return gif_url


def encrypt_data(data):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data, key

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data

def insert_logo(qr_image, logo_path, logo_size):
    logo = Image.open(logo_path)
    logo = logo.resize(logo_size)
    pos = ((qr_image.size[0] - logo.size[0]) // 2,
           (qr_image.size[1] - logo.size[1]) // 2)
    qr_image.paste(logo, pos, logo.convert('RGBA'))
    return qr_image


def read_qr_code():
    image_path = input("🖼️  Enter the path to the QR code image: ")
    try:
        image = Image.open(image_path)
        decoded = decode(image)
        if decoded:
            print(f"✅ Decoded QR code: {decoded[0].data.decode('utf-8')}")
            decrypt_choice = input("🔐 Is this data encrypted? (y/n): ").lower()
            if decrypt_choice == 'y':
                key = input("🔑 Enter the decryption key: ").encode()
                try:
                    decrypted_data = decrypt_data(decoded[0].data, key)
                    print(f"🔓 Decrypted data: {decrypted_data}")
                except Exception as e:
                    print(f"❌ Decryption failed: {str(e)}")
        else:
            print("❌ No QR code found in the image.")
    except Exception as e:
        print(f"❌ Error reading QR code: {str(e)}")


def default_qr():
    print("\n📌 Creating a default QR code...")
    info = get_info()
    name = get_name()
    
    encrypt_choice = input("🔐 Encrypt the data? (y/n): ").lower()
    if encrypt_choice == 'y':
        info, key = encrypt_data(info)
        print(f"🔑 Decryption key: {key.decode()}")  # Store this securely!
    
    qrcode = segno.make_qr(info)
    qrcode.save(f"{name}.png", scale=8, border=4)
    
    logo_choice = input("🖼️  Add a logo to the QR code? (y/n): ").lower()
    if logo_choice == 'y':
        logo_path = input("Enter path to logo image: ")
        logo_size = (50, 50)  # Adjust size as needed
        qr_image = Image.open(f"{name}.png")
        qr_with_logo = insert_logo(qr_image, logo_path, logo_size)
        qr_with_logo.save(f"{name}_with_logo.png")
        print('✅ QR code with logo generated successfully!')
    else:
        print('✅ QR code generated successfully!')

def customized_qr():
    print("\n🎨 Creating a customized QR code...")
    info = get_info()
    name = get_name()
    qr_size = int(input('🔍 Select size for QR code (8 is default): '))
    border_size = int(input('🖼️  Select border size of the QR code (4 is default): '))

    bg_color = get_color(light_colors, 'Background', default_bg)
    qr_color = get_color(dark_colors, 'QR color', default_qr)

    encrypt_choice = input("🔐 Encrypt the data? (y/n): ").lower()
    if encrypt_choice == 'y':
        info, key = encrypt_data(info)
        print(f"🔑 Decryption key: {key.decode()}")  # Store this securely!

    qrcode = segno.make_qr(info)
    qrcode.save(f"{name}.png",
                scale=qr_size,
                border=border_size,
                light=bg_color,
                dark=qr_color)

    logo_choice = input("🖼️  Add a logo to the QR code? (y/n): ").lower()
    if logo_choice == 'y':
        logo_path = input("Enter path to logo image: ")
        logo_size = (50, 50)  # Adjust size as needed
        qr_image = Image.open(f"{name}.png")
        qr_with_logo = insert_logo(qr_image, logo_path, logo_size)
        qr_with_logo.save(f"{name}_with_logo.png")
        print('✅ Customized QR code with logo generated successfully!')
    else:
        print('✅ Customized QR code generated successfully!')

def animated_qr():
    print("\n🎬 Creating an animated QR code...")
    info = get_info()
    name = get_name()
    qr_size = int(input('🔍 Select size for QR code (8 is default): '))
    bg_color = get_color(light_colors, 'Background', default_bg)
    qr_color = get_color(dark_colors, 'QR color', default_qr)
    
    print("\n🖼️  Choose GIF background:")
    print("1. Select from default options")
    print("2. Add custom GIF link")
    
    gif_choice = input("Enter your choice (1 or 2): ")
    
    if gif_choice == "1":
        gif_url = get_gif(gif_options, default_gif)
    elif gif_choice == "2":
        gif_url = input("Enter your custom GIF URL: ")
    else:
        print("⚠️  Invalid choice. Using default GIF.")
        gif_url = default_gif
    
    encrypt_choice = input("🔐 Encrypt the data? (y/n): ").lower()
    if encrypt_choice == 'y':
        info, key = encrypt_data(info)
        print(f"🔑 Decryption key: {key.decode()}")  # Store this securely!

    try:
        url = urlopen(gif_url)
        qrcode = segno.make_qr(info)
        
        qrcode.to_artistic(background=url,
                           target=f"{name}.gif",
                           scale=qr_size,
                           light=bg_color,
                           dark=qr_color)
        print('✅ Animated QR code generated successfully!')
    except Exception as e:
        print(f"❌ Error generating QR code: {str(e)}")
        print("Please check your GIF URL and try again.")

def main():
    print("🌟 Welcome to the QR Code Generator! 🌟")
    while True:
        print("\n📋 MENU")
        print('1. 📊 Default QR code')
        print('2. 🎨 Customized QR code')
        print('3. 🎬 Animated QR code')
        print('4. 📷 Read QR code')
        print('5. 🚪 Exit')

        try:
            user = int(input('Enter your choice (1-5): '))
            if user == 1:
                default_qr()
            elif user == 2:
                customized_qr()
            elif user == 3:
                animated_qr()
            elif user == 4:
                read_qr_code()
            elif user == 5:
                print("👋 Thank you for using our QR Code Generator. Have a great day!")
                break
            else:
                print('❌ Invalid choice. Please select a number between 1 and 5.')
        except ValueError:
            print('❌ Invalid input. Please enter a number.')

if __name__ == "__main__":
    main()

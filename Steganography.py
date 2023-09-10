import shutil
import hashlib
import PIL.Image
import onetimepad 
import numpy as np
from PIL import Image
from tkinter import *
from tkinter import messagebox

window = Tk()

def on_closing(exit_window):
    button1['state'] = ACTIVE
    button2['state'] = ACTIVE
    exit_window.destroy()

# Window Settings 
window.geometry("550x260")
window.title("Image Steganography")
window.resizable(False,False)
window.config(background='#666633')

# Heading Label Settings
label1 = Label(
    window,
    text='IMAGE STEGANOGRAPHY',
    font=('Arial Black', 25, 'bold'),
    bg='#666633',
    fg='#FFFDD0',
    padx=10,
    pady=10,
)

label1.pack()

# Encoding Function
def Encoder_window():

    # Encoder Window Settings 
    encode_window = Toplevel(window)
    encode_window.title('Encoder')
    encode_window.geometry('500x460')
    encode_window.resizable(False,False)
    encode_window.config(background='#666633')
    encode_window.protocol("WM_DELETE_WINDOW", lambda x=encode_window: on_closing(x))
    button1['state'] = DISABLED
    button2['state'] = DISABLED

    # Encoder Heading Label Settings
    label2 = Label(
        encode_window,
        text='Encoder',
        font=('Arial Black', 25, 'bold'),
        bg='#666633',
        fg='#FFFFFF',
        padx=10,
        pady=10,
    )

    label2.pack()

    # Filepath Label Settings
    label3 = Label(
    encode_window,
    text='Filepath',
    font=('Monaco', 15, 'underline'),
    bg='#666633',
    fg='#FFFFFF',
    padx=10,
    pady=10,
    )

    label3.place(x=30, y=80)

    # Destination Label Settings
    label4 = Label(
    encode_window,
    text='Destination',
    font=('Monaco', 15, 'underline'),
    bg='#666633',
    fg='#FFFFFF',
    padx=10,
    pady=10,
    )

    label4.place(x=30,y=160)

    # Message Label Settings
    label5 = Label(
    encode_window,
    text='Message',
    font=('Monaco', 15, 'underline'),
    bg='#666633',
    fg='#FFFFFF',
    padx=10,
    pady=10,
    )

    label5.place(x=30,y=240)

    # Message Label Settings
    label6 = Label(
    encode_window,
    text='Password',
    font=('Monaco', 15, 'underline'),
    bg='#666633',
    fg='#FFFFFF',
    padx=10,
    pady=10,
    )

    label6.place(x=30,y=320)

    # Filepath TextField Settings 
    textfield1 = Entry(
    encode_window,
    font=('Monaco', 15),
    bg='#FFFFFF',
    fg='#000000',
    )

    textfield1.place(x=200,y=90)

    # Destination TextField Settings
    textfield2 = Entry(
    encode_window,
    font=('Monaco', 15),
    bg='#FFFFFF',
    fg='#000000',
    )

    textfield2.place(x=200,y=180)

    # Message TextField Settings
    textfield3 = Entry(
    encode_window,
    font=('Monaco', 15),
    bg='#FFFFFF',
    fg='#000000',
    )

    textfield3.place(x=200,y=260)

    # Message TextField Settings
    textfield4 = Entry(
    encode_window,
    font=('Monaco', 15),
    bg='#FFFFFF',
    fg='#000000',
    )

    textfield4.place(x=200,y=340)
    
    # HexDump Encoding Button Function
    def HexDump():
        filepath = textfield1.get()
        dest_path = textfield2.get()
        msg = textfield3.get()
        pass_key = textfield4.get()
        cipher_key = str(hashlib.sha256(pass_key.encode()).digest())

        shutil.copy(filepath, dest_path)
        
        with open(dest_path, 'ab') as file:
            cipher_msg = onetimepad.encrypt(msg, cipher_key)
            hidden_msg = bytes(cipher_msg,'utf-8')
            file.write(b'' + hidden_msg)
            messagebox.showinfo("Encode","Image Encoded Successfully!")
            button1['state'] = ACTIVE
            button2['state'] = ACTIVE
            encode_window.destroy()


    # HexDump Encoding Button Settings
    button3 = Button(
    encode_window,
    text='HexDump',
    font=('Monaco', 15, 'bold'),
    fg="#003300",
    activeforeground="#003300",
    bg="#339966",
    activebackground="#339966",
    padx=2,
    pady=2,
    command=HexDump
    )

    button3.place(x=150, y=400)

    # LSB Encoding Button Function
    def LSB():
        filepath = textfield1.get()
        dest_path = textfield2.get()
        msg = textfield3.get()
        pass_key = textfield4.get()
        cipher_key = str(hashlib.sha256(pass_key.encode()).digest())
        
        image = PIL.Image.open(filepath, 'r')
        width, height = image.size
        img_array = np.array(list(image.getdata()))
        
        if image.mode == 'RGB':        
            n = 3
        elif image.mode == 'RGBA':
            n = 4
        elif image.mode == 'P':
            print("Not Supported")
            exit()
        
        total_pixels = img_array.size//n
        
        stop_indicator = "$LSB Method$"
        stop_indicator_length = len(stop_indicator)

        msg += stop_indicator
        cipher_msg = onetimepad.encrypt(msg, cipher_key)
        bits_msg = ''.join(f"{ord(c):08b}" for c in msg)
        bits = len(bits_msg)
        
        if bits > total_pixels:
            print("Not Enough Space")
        else:
            index = 0
            for i in range(total_pixels):
                for j in range(0,3):
                    if index < bits:
                        img_array[i][j] = int(bin(img_array[i][j])[2:-1] + bits_msg[index], 2)
                        index += 1

        img_array = img_array.reshape(height, width, n)
        result_img = PIL.Image.fromarray(img_array.astype('uint8'), image.mode)
        result_img.save(dest_path)
        
        messagebox.showinfo("Encode","Image Encoded Successfully!")
        button1['state'] = ACTIVE
        button2['state'] = ACTIVE
        encode_window.destroy()


    # LSB Encoding Button Settings
    button4 = Button(
    encode_window,
    text='LSB',
    font=('Monaco', 15, 'bold'),
    fg="#003300",
    activeforeground="#003300",
    bg="#339966",
    activebackground="#339966",
    padx=2,
    pady=2,
    command=LSB
    )

    button4.place(x=300, y=400)


# Decoding Function
def Decoder_window():

    # Decoder Window Settings 
    decode_window = Toplevel(window)
    decode_window.title('Decoder')
    decode_window.geometry('600x280')
    decode_window.resizable(False,False)
    decode_window.config(background='#666633')
    decode_window.protocol("WM_DELETE_WINDOW", lambda x=decode_window: on_closing(x))
    button1['state'] = DISABLED
    button2['state'] = DISABLED

    # Decoder Heading Label Settings
    label2 = Label(
        decode_window,
        text='Decoder',
        font=('Arial Black', 25, 'bold'),
        bg='#666633',
        fg='#FFFFFF',
        padx=10,
        pady=10,
    )

    label2.pack()

    # Filepath Label Settings
    label3 = Label(
    decode_window,
    text='Filepath',
    font=('Monaco', 15, 'underline'),
    bg='#666633',
    fg='#FFFFFF',
    padx=10,
    pady=10,
    )

    label3.place(x=70, y=70)

    # Filepath TextField Settings 
    textfield1 = Entry(
    decode_window,
    font=('Monaco', 15),
    bg='#FFFFFF',
    fg='#000000',
    )

    textfield1.place(x=280,y=80)

    # Filepath Label Settings
    label4 = Label(
    decode_window,
    text='Password',
    font=('Monaco', 15, 'underline'),
    bg='#666633',
    fg='#FFFFFF',
    padx=10,
    pady=10,
    )

    label4.place(x=70, y=150)

    # Filepath TextField Settings 
    textfield2 = Entry(
    decode_window,
    font=('Monaco', 15),
    bg='#FFFFFF',
    fg='#000000',
    )

    textfield2.place(x=280,y=160)

    # Decoding Button Function
    def Decode():

        filepath = textfield1.get()
        pass_key = 'Alok Mahto'
        cipher_key = str(hashlib.sha256(pass_key.encode()).digest())
        png_end_hex = b"\xae\x42\x60\x82"
        jpg_end_hex = b"\xff\xd9"

        image = PIL.Image.open(filepath,"r")
        img_array = np.array(list(image.getdata()))

        if image.mode == 'RGB':
            n = 3
        elif image.mode == 'RGBA':
            n = 4
        elif image.mode == 'P':
            print("Not Supported")
            exit()

        total_pixels = img_array.size//n
        
        encoded_bits = [bin(img_array[i][j])[-1] for i in range(total_pixels) for j in range(0,3)]
        encoded_bits = ''.join(encoded_bits)
        encoded_bits = [encoded_bits[i:i+8] for i in range(0, len(encoded_bits), 8) ]

        hidden_str = [chr(int(encoded_bits[i], 2)) for i in range(len(encoded_bits))]
        hidden_str = ''.join(hidden_str)

        stop_indicator = "$LSB Method$"
        
        if stop_indicator in hidden_str:
            messagebox.showinfo('Decode', 'Encrypted Message: ' + hidden_str[:hidden_str.index(stop_indicator)])
            button1['state'] = ACTIVE
            button2['state'] = ACTIVE
            decode_window.destroy()
            
        else:                
            with open(filepath, 'rb') as file:
                content = file.read()
                
                try:
                    offset = content.index(png_end_hex)
                    file.seek(offset + 4)
                except ValueError:
                    offset = content.index(jpg_end_hex)
                    file.seek(offset + 2)    
                
                joined_str = str(file.read(), 'utf-8')
                hidden_str = onetimepad.decrypt(joined_str, cipher_key)

                if len(hidden_str) != 0:
                    messagebox.showinfo('Decode', 'Encrypted Message: ' + hidden_str)
                    button1['state'] = ACTIVE
                    button2['state'] = ACTIVE
                    decode_window.destroy()
                else:
                    messagebox.showerror('Decode', 'No Message Found')
                    button1['state'] = ACTIVE
                    button2['state'] = ACTIVE
                    decode_window.destroy()


    # Decoding Button Settings
    button5 = Button(
    decode_window,
    text='Decode',
    font=('Monaco', 15, 'bold'),
    fg="#003300",
    activeforeground="#003300",
    bg="#339966",
    activebackground="#339966",
    padx=2,
    pady=2,
    command=Decode
    )

    button5.place(x=240, y=220)


# Encoding Button Settings
button1 = Button(
    window,
    text='Encoder',
    font=('Monaco', 15, 'bold'),
    fg="#003300",
    activeforeground="#003300",
    bg="#339966",
    activebackground="#339966",
    padx=2,
    pady=2,
    command=Encoder_window
)

button1.place(x=120, y=120)

# Decoding Button Settings
button2 = Button(
    window,
    text='Decoder',
    font=('Monaco', 15, 'bold'),
    fg="#003300",
    activeforeground="#003300",
    bg="#339966",
    activebackground="#339966",
    padx=2,
    pady=2,
    command=Decoder_window
)

button2.place(x=320, y=120)

window.mainloop()
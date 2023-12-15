import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk
import io

# Define the main application class
class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title('QR Code Generator')
        self.generated_qr_image = None  # This will hold the generated QR code image
        
        # Initialize GUI elements
        self.setup_gui()
        
    def setup_gui(self):
        # Create layout frames
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill=tk.BOTH, expand=True)
        
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL entry
        self.url_label = tk.Label(self.top_frame, text="Enter URL:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.url_entry = tk.Entry(self.top_frame, width=40)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Color selection for QR code
        self.color_label = tk.Label(self.top_frame, text="Select QR Code Color:")
        self.color_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.color_button = tk.Button(self.top_frame, text="Choose Color", command=self.choose_qr_color)
        self.color_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Background color selection
        self.bg_color_label = tk.Label(self.top_frame, text="Select Background Color:")
        self.bg_color_label.grid(row=2, column=0, padx=5, pady=5)
        
        self.bg_color_button = tk.Button(self.top_frame, text="Choose Color", command=self.choose_bg_color)
        self.bg_color_button.grid(row=2, column=1, padx=5, pady=5)
        
        # Image insertion button
        self.image_button = tk.Button(self.top_frame, text="Insert Image", command=self.insert_image)
        self.image_button.grid(row=3, column=1, padx=5, pady=5)
        
        # Image size slider
        self.size_label = tk.Label(self.top_frame, text="Select Image Size (% of QR):")
        self.size_label.grid(row=4, column=0, padx=5, pady=5)
        
        self.size_slider = tk.Scale(self.top_frame, from_=5, to=20, orient=tk.HORIZONTAL)
        self.size_slider.set(10)  # default size
        self.size_slider.grid(row=4, column=1, padx=5, pady=5)
        
        # Error correction level dropdown
        self.error_correction_label = tk.Label(self.top_frame, text="Error Correction Level:")
        self.error_correction_label.grid(row=5, column=0, padx=5, pady=5)
        
        self.error_correction = ttk.Combobox(self.top_frame, values=['L', 'M', 'Q', 'H'], state="readonly")
        self.error_correction.grid(row=5, column=1, padx=5, pady=5)
        self.error_correction.set('H') # Set the highest error correction by default
        
        # Generate QR code button
        self.generate_button = tk.Button(self.bottom_frame, text="Generate QR Code", command=self.generate_qr)
        self.generate_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Save QR code button
        self.save_button = tk.Button(self.bottom_frame, text="Save QR Code", command=self.save_qr)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Preview of the QR code
        self.qr_preview_label = tk.Label(self.bottom_frame, text="QR Code Preview:")
        self.qr_preview_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.qr_preview_canvas = tk.Canvas(self.bottom_frame, width=250, height=250)
        self.qr_preview_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def choose_qr_color(self):
        # Open color chooser dialog and set QR code color
        self.qr_color = colorchooser.askcolor(title ="Choose color")[1]
        
    def choose_bg_color(self):
        # Open color chooser dialog and set background color
        self.bg_color = colorchooser.askcolor(title ="Choose color")[1]
    
    def insert_image(self):
        # Open file dialog to select an image to insert in the QR code
        self.image_path = filedialog.askopenfilename()
    
    def generate_qr(self):
    # Generate the QR code with the specified URL and color
        qr = qrcode.QRCode(
            version=1,
            error_correction=getattr(qrcode.constants, 'ERROR_CORRECT_' + self.error_correction.get()),
            box_size=10,
            border=4,
        )
        qr.add_data(self.url_entry.get())
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.qr_color, back_color=self.bg_color).convert('RGB')
        
        # If an image has been selected, insert it into the QR code
        if hasattr(self, 'image_path'):
            logo = Image.open(self.image_path).convert('RGBA')
            basewidth = int((self.size_slider.get() / 100) * img.size[0])
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            
            # Calculate the position for the logo
            position = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
            img.paste(logo, position, logo)

        # Save the generated image for later use in saving
        self.generated_qr_image = img
        
        # Update the preview
        self.update_preview(img)
        
    def update_preview(self, img):
        # Convert the QR code to an image for the preview
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        preview_image = ImageTk.PhotoImage(Image.open(img_byte_arr))
        self.qr_preview_canvas.create_image(125, 125, image=preview_image)
        self.qr_preview_canvas.image = preview_image  # Keep a reference so it's not garbage collected
        
    def save_qr(self):
        # Save the generated QR code
        if self.generated_qr_image:
            file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                     filetypes=[("PNG file", '*.png'), ("JPG file", '*.jpg')])
            if file_path:
                self.generated_qr_image.save(file_path)

# Create the Tkinter window and run the app
root = tk.Tk()
app = QRCodeApp(root)
root.mainloop()
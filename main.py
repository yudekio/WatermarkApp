import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageFont, ImageDraw, ImageTk
from tkinter import filedialog

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Add")

        # Initialize image path variable
        self.image_path = None

        # Create a frame
        self.frame = tk.Frame(self.root, background='lightgray')
        self.frame.pack(padx=50, pady=50)

        # Create a label for displaying preview image
        self.preview_label = tk.Label(self.frame)
        self.preview_label.pack()

        # Label for instructions
        self.label = tk.Label(self.frame, text='Drag and drop an image here:', background='lightblue', width=50, height=10)
        self.label.pack()

        # Label for displaying selected image path
        self.info_text = tk.Label(self.root, text='Select an image')
        self.info_text.pack()

        # Entry widget for entering watermark text
        self.watermark_entry = tk.Entry(self.frame, width=40)
        self.watermark_entry.insert(0, "watermark text")  # Default watermark text
        self.watermark_entry.pack()

        # Button for applying watermark
        self.button_apply = tk.Button(self.frame, text='Apply Watermark', command=self.apply_watermark)
        self.button_apply.pack()

        # Button for saving the processed image
        self.button_save = tk.Button(self.frame, text='Save Image', command=self.save_image)
        self.button_save.pack()

        # Register drop event handler
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)

    def apply_watermark(self):
        if not self.image_path:
            return

        watermark_text = self.watermark_entry.get()

        # 1. Open the image
        image = Image.open(self.image_path)

        # 2. Create a text layer
        text_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))

        # 3. Load a font
        font = ImageFont.truetype('fonts/Montserrat-ExtraBold.ttf', 20)

        # 4. Add the watermark
        draw = ImageDraw.Draw(text_layer)
        text_color = (255, 128, 255, 200)
        stroke_color = (0, 0, 0, 200)
        draw.text((12, 8), watermark_text, fill=text_color, align='center', stroke_width=1, font=font,
                  stroke_fill=stroke_color, anchor='lt', )
        image_with_text = Image.alpha_composite(image.convert("RGBA"), text_layer)

        # Display the processed image in the preview
        self.display_processed_image(image_with_text)

    def drop(self, event):
        # Get the path of the file being dragged into the window
        file = event.data
        if file:
            self.image_path = file.strip('{}')
            self.info_text.config(text=f'Selected image: {self.image_path}')
            self.update_preview()

    def update_preview(self):
        # Update the image preview
        if self.image_path:
            preview_image = Image.open(self.image_path)
            preview_image.thumbnail((500, 500))
            preview_photo = ImageTk.PhotoImage(preview_image)
            self.preview_label.config(image=preview_photo)
            self.preview_label.image = preview_photo

    def display_processed_image(self, processed_image):
        # Display the processed image in the preview
        processed_image.thumbnail((500, 500))
        processed_photo = ImageTk.PhotoImage(processed_image)
        self.preview_label.config(image=processed_photo)
        self.preview_label.image = processed_photo

    def save_image(self):
        if not self.image_path:
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

        if save_path:
            processed_image = Image.open(self.image_path)
            watermark_text = self.watermark_entry.get()
            font = ImageFont.truetype('fonts/Montserrat-ExtraBold.ttf', 20)
            draw = ImageDraw.Draw(processed_image)
            text_color = (255, 128, 255, 200)
            stroke_color = (0, 0, 0, 200)
            draw.text((12, 8), watermark_text, fill=text_color, align='center',
                      stroke_width=1, font=font, stroke_fill=stroke_color, anchor='lt')
            processed_image.save(save_path)
            self.info_text.config(text=f'Saved as: {save_path}')
        else:
            self.info_text.config(text='Save canceled')

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = WatermarkApp(root)
    root.mainloop()

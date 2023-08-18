import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk

class ImageCollageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Collage Maker")
        self.images = []
        self.image_refs = []
        self.collage_size = (600, 600)
        self.collage_canvas = tk.Canvas(
            self.root,
            width=self.collage_size[0],
            height=self.collage_size[1],
            bg="white",
        )
        self.collage_canvas.pack()
        self.btn_add_image = tk.Button(
            self.root,
            text="Add Image",
            command=self.add_images,
            font=("Arial", 12, "bold"),
        )
        self.btn_add_image.pack(pady=10)
        self.btn_create_collage = tk.Button(
            self.root,
            text="Create Collage",
            command=self.create_collage,
            font=("Arial", 12, "bold"),
        )
        self.btn_create_collage.pack(pady=5)
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.image_positions = []
        self.collage_canvas.bind("<ButtonPress-1>", self.on_press)
        self.collage_canvas.bind("<B1-Motion>", self.on_drag)
        self.collage_canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.drag_data["item"] = self.collage_canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
    def on_drag(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        self.collage_canvas.move(self.drag_data["item"], delta_x, delta_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_release(self, event):
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        self.update_image_positions()

    def update_image_positions(self):
        self.image_positions.clear()
        for item in self.collage_canvas.find_all():
            x, y = self.collage_canvas.coords(item)
            self.image_positions.append((x, y))

    def add_images(self):
        num_images = simpledialog.askinteger(
            "Number of Images", "Enter the number of images:"
        )
        if num_images is not None:
            file_paths = filedialog.askopenfilenames(
                filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")]
            )
            if file_paths:
                for i in range(min(num_images, len(file_paths))):
                    file_path = file_paths[i]
                    image = Image.open(file_path)
                    resized_image = self.resize_image(image)
                    self.images.append(resized_image)
                    self.image_refs.append(ImageTk.PhotoImage(resized_image))
                self.update_canvas()

    def resize_image(self, image):
        img_width, img_height = image.size
        aspect_ratio = img_width / img_height
        if aspect_ratio > 1:
            new_width = self.collage_size[0] // 2
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = self.collage_size[1] // 2
            new_width = int(new_height * aspect_ratio)
        return image.resize((new_width, new_height))

    def update_canvas(self):
        self.collage_canvas.delete("all")
        rows = simpledialog.askinteger("Number of Rows", "Enter the number of rows:")
        cols = simpledialog.askinteger(
            "Number of Columns", "Enter the number of columns:"
        )
        collage_width = self.collage_size[0] * cols // 2
        collage_height = self.collage_size[1] * rows // 2
        self.collage_canvas.config(width=collage_width, height=collage_height)
        self.image_positions.clear()
        x_offset, y_offset = 0, 0
        for i, image_ref in enumerate(self.image_refs):
            self.collage_canvas.create_image(
                x_offset, y_offset, anchor=tk.NW, image=image_ref
            )
            self.image_positions.append((x_offset, y_offset))
            x_offset += self.collage_size[0] // 2
            if (i + 1) % cols == 0:
                x_offset = 0
                y_offset += self.collage_size[1] // 2

    def create_collage(self):
        if len(self.images) == 0:
            messagebox.showwarning("Warning", "Please add images first!")
            return
        collage_width = self.collage_canvas.winfo_width()
        collage_height = self.collage_canvas.winfo_height()
        background = Image.new("RGB", (collage_width, collage_height), "white")
        for idx, image in enumerate(self.images):
            x_offset, y_offset = self.image_positions[idx]
            x_offset, y_offset = int(x_offset), int(y_offset)
            paste_box = (
                x_offset,
                y_offset,
                x_offset + image.width,
                y_offset + image.height,
            )
            background.paste(image, paste_box)
        background.save("collage_with_white_background.jpg")
        background.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCollageApp(root)
    root.mainloop()

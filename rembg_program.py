import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Label
from PIL import Image, ImageTk
from rembg import remove
import os
from pathlib import Path

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Background Remover")
        self.root.geometry("800x600")
        
        # Make the window resizable
        self.root.resizable(True, True)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        
        # Configure button styles with black text
        self.style.configure('TButton', padding=5, relief="flat", background="#4CAF50", foreground="black")
        self.style.map('TButton', background=[('active', '#45a049')])
        
        # Create a specific style for the Clear button
        self.style.configure('Clear.TButton', background="#f44336", foreground="black")
        self.style.map('Clear.TButton', background=[('active', '#d32f2f')])
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Drop area with improved styling
        self.drop_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.drop_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.drop_area = tk.Label(
            self.drop_frame, 
            text="Drag & Drop Image Here\nor Click to Browse", 
            bg='#f5f5f5', fg='#555555', 
            relief=tk.GROOVE, bd=2,
            font=('Helvetica', 14, 'bold'), 
            padx=20, pady=40
        )
        self.drop_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.drop_area.bind("<Button-1>", self.browse_image)
        
        # Add some visual cues
        self.drop_icon = tk.Label(
            self.drop_area,
            text="📷",
            font=('Helvetica', 32),
            bg='#f5f5f5',
            fg='#4CAF50'
        )
        self.drop_icon.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        # Enable drag-and-drop
        self.setup_drag_and_drop()
        
        # Preview area
        self.preview_frame = ttk.Frame(self.main_frame)
        self.preview_frame.pack(fill=tk.BOTH, expand=True)
        
        self.original_label = Label(self.preview_frame, text="Original Image", bg='#f0f0f0')
        self.original_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_label = Label(self.preview_frame, text="Result (Background Removed)", bg='#f0f0f0')
        self.result_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.remove_bg_btn = ttk.Button(self.button_frame, text="Remove Background", 
                                      command=self.remove_background, state=tk.DISABLED)
        self.remove_bg_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(self.button_frame, text="Save Result", 
                                  command=self.save_result, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Use the Clear style for the clear button
        self.clear_btn = ttk.Button(self.button_frame, text="Clear", command=self.clear_all, style='Clear.TButton')
        self.clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # Initialize variables
        self.input_image_path = None
        self.original_image = None
        self.result_image = None
        self.tk_original_image = None
        self.tk_result_image = None

    def setup_drag_and_drop(self):
        """Setup drag and drop functionality with fallback"""
        try:
            # Windows-specific drag and drop
            self.root.drop_target_register(tk.DND_FILES)
            self.root.dnd_bind('<<DropEnter>>', self.on_drag_enter)
            self.root.dnd_bind('<<DropLeave>>', self.on_drag_leave)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
        except Exception:
            # Fallback for systems without DND support
            self.drop_area.config(text="Click to Browse (Drag-drop not supported)")
            self.drop_area.unbind("<DragEnter>")
            self.drop_area.unbind("<DragLeave>")
            self.drop_area.unbind("<Drop>")
        
    def browse_image(self, event=None):
        filetypes = (
            ('Image files', '*.jpg *.jpeg *.png *.bmp'),
            ('All files', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title="Open an image",
            initialdir=os.path.expanduser('~'),
            filetypes=filetypes
        )
        
        if filename:
            self.process_image(filename)
    
    def on_drag_enter(self, event):
        self.drop_area.config(bg='#e1f5fe', fg='#0277bd')
        self.drop_icon.config(bg='#e1f5fe', fg='#0277bd')
        return event.action
    
    def on_drag_leave(self, event):
        self.drop_area.config(bg='#f5f5f5', fg='#555555')
        self.drop_icon.config(bg='#f5f5f5', fg='#4CAF50')
        return event.action
    
    def on_drop(self, event):
        self.drop_area.config(bg='#f5f5f5', fg='#555555')
        self.drop_icon.config(bg='#f5f5f5', fg='#4CAF50')
        
        # Get the dropped file path
        file_path = event.data
        
        # On Windows, the path might be surrounded by {}
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        
        # Process the dropped file
        self.process_dropped_file(file_path)
        return event.action
    
    def process_dropped_file(self, file_path):
        """Process a file that was dropped or selected"""
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found")
            return
            
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ('.jpg', '.jpeg', '.png', '.bmp'):
            messagebox.showerror("Error", "Please drop an image file (JPG, PNG, BMP)")
            return
            
        self.process_image(file_path)
    
    def process_image(self, file_path):
        try:
            self.input_image_path = file_path
            self.original_image = Image.open(file_path)
            
            # Resize for display while maintaining aspect ratio
            display_size = (400, 400)
            img_for_display = self.resize_image(self.original_image, display_size)
            
            self.tk_original_image = ImageTk.PhotoImage(img_for_display)
            self.original_label.config(image=self.tk_original_image, text="")
            
            # Enable remove background button
            self.remove_bg_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.DISABLED)
            
            # Clear any previous result
            self.result_label.config(image=None, text="Result (Background Removed)")
            self.tk_result_image = None
            self.result_image = None
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {str(e)}")
    
    def resize_image(self, image, size):
        """Resize image maintaining aspect ratio"""
        original_width, original_height = image.size
        target_width, target_height = size
        
        # Calculate aspect ratios
        original_ratio = original_width / original_height
        target_ratio = target_width / target_height
        
        # Determine new dimensions
        if original_ratio > target_ratio:
            # Image is wider than target
            new_width = target_width
            new_height = int(target_width / original_ratio)
        else:
            # Image is taller than target
            new_height = target_height
            new_width = int(target_height * original_ratio)
        
        return image.resize((new_width, new_height), Image.LANCZOS)
    
    def remove_background(self):
        if not self.input_image_path or not self.original_image:
            return
            
        try:
            # Show loading message
            self.result_label.config(text="Processing...", image=None)
            self.root.update()
            
            # Remove background
            self.result_image = remove(self.original_image)
            
            # Resize for display
            display_size = (400, 400)
            img_for_display = self.resize_image(self.result_image, display_size)
            
            self.tk_result_image = ImageTk.PhotoImage(img_for_display)
            self.result_label.config(image=self.tk_result_image, text="")
            
            # Enable save button
            self.save_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove background: {str(e)}")
    
    def save_result(self):
        if not self.result_image:
            return
            
        default_filename = os.path.basename(self.input_image_path)
        default_filename = os.path.splitext(default_filename)[0] + "_no_bg.png"
        
        file_path = filedialog.asksaveasfilename(
            title="Save image without background",
            initialdir=os.path.expanduser('~'),
            initialfile=default_filename,
            defaultextension=".png",
            filetypes=(("PNG files", "*.png"), ("All files", "*.*"))
        )
        
        if file_path:
            try:
                self.result_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def clear_all(self):
        self.input_image_path = None
        self.original_image = None
        self.result_image = None
        self.tk_original_image = None
        self.tk_result_image = None
        
        self.original_label.config(image=None, text="Original Image")
        self.result_label.config(image=None, text="Result (Background Removed)")
        
        self.remove_bg_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        
        self.drop_area.config(text="Drag & Drop Image Here\nor Click to Browse", bg='#f5f5f5', fg='#555555')
        self.drop_icon.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        self.drop_icon.config(bg='#f5f5f5', fg='#4CAF50')

def main():
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
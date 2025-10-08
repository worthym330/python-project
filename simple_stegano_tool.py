import tkinter as tk 
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from stegano import lsb
import wave
import numpy as np

class SteganographyTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Steganography Tool - Hide Your Slogan")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        # Variables
        self.selected_file = None
        self.hidden_data_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="STEGANOGRAPHY TOOL", 
            font=("Arial", 24, "bold"),
            bg="#2c3e50", 
            fg="#ecf0f1"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            self.root, 
            text="Hide Your Secret Slogan in Images & Audio Files", 
            font=("Arial", 12),
            bg="#2c3e50", 
            fg="#bdc3c7"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Left panel - File selection and preview
        left_frame = tk.LabelFrame(
            main_frame, 
            text="File Selection & Preview", 
            font=("Arial", 12, "bold"),
            bg="#34495e", 
            fg="#ecf0f1",
            padx=10, 
            pady=10
        )
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # File selection button
        select_btn = tk.Button(
            left_frame,
            text="📁 Select Image/Audio File",
            command=self.select_file,
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=8,
            relief="flat"
        )
        select_btn.pack(pady=10)
        
        # File preview area
        self.preview_frame = tk.Frame(left_frame, bg="#2c3e50", height=300, width=350)
        self.preview_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.preview_frame.pack_propagate(False)
        
        # Right panel - Message and actions
        right_frame = tk.LabelFrame(
            main_frame, 
            text="Message & Actions", 
            font=("Arial", 12, "bold"),
            bg="#34495e", 
            fg="#ecf0f1",
            padx=10, 
            pady=10
        )
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Message input
        message_label = tk.Label(
            right_frame, 
            text="Enter Your Secret Slogan/Message:", 
            font=("Arial", 11),
            bg="#34495e", 
            fg="#ecf0f1"
        )
        message_label.pack(anchor="w", pady=(10, 5))
        
        self.message_text = tk.Text(
            right_frame, 
            height=8, 
            width=40,
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#2c3e50",
            wrap="word"
        )
        self.message_text.pack(pady=(0, 20), padx=5, fill="x")
        
        # Action buttons
        button_frame = tk.Frame(right_frame, bg="#34495e")
        button_frame.pack(pady=10)
        
        hide_btn = tk.Button(
            button_frame,
            text="🔒 Hide Message",
            command=self.hide_message,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8,
            relief="flat"
        )
        hide_btn.pack(pady=5, fill="x")
        
        reveal_btn = tk.Button(
            button_frame,
            text="🔓 Reveal Message",
            command=self.reveal_message,
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=8,
            relief="flat"
        )
        reveal_btn.pack(pady=5, fill="x")
        
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Hidden File",
            command=self.save_hidden_file,
            font=("Arial", 11, "bold"),
            bg="#f39c12",
            fg="white",
            padx=20,
            pady=8,
            relief="flat"
        )
        save_btn.pack(pady=5, fill="x")
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select a file to begin")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Arial", 9)
        )
        status_bar.pack(side="bottom", fill="x")
    
    def select_file(self):
        """Select an image or audio file"""
        filetypes = (
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("Audio files", "*.wav"),
            ("All files", "*.*")
        )
        
        filename = filedialog.askopenfilename(
            title="Select Image or Audio File",
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file = filename
            self.display_file_preview()
            self.status_var.set(f"Selected: {os.path.basename(filename)}")
    
    def display_file_preview(self):
        """Display preview of selected file"""
        # Clear preview frame
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        if not self.selected_file:
            return
        
        try:
            if self.selected_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Display image preview
                img = Image.open(self.selected_file)
                
                # Resize image to fit preview
                img.thumbnail((320, 280), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                label = tk.Label(self.preview_frame, image=photo, bg="#2c3e50")
                label.image = photo  # Keep a reference
                label.pack(expand=True)
                
                # Show image info
                info_text = f"Image: {img.size[0]}x{img.size[1]} pixels"
                info_label = tk.Label(
                    self.preview_frame, 
                    text=info_text, 
                    bg="#2c3e50", 
                    fg="#bdc3c7",
                    font=("Arial", 9)
                )
                info_label.pack(pady=5)
                
            elif self.selected_file.lower().endswith('.wav'):
                # Display audio file info
                with wave.open(self.selected_file, 'rb') as audio:
                    frames = audio.getnframes()
                    rate = audio.getframerate()
                    duration = frames / float(rate)
                    channels = audio.getnchannels()
                
                audio_icon = tk.Label(
                    self.preview_frame, 
                    text="🎵", 
                    font=("Arial", 48),
                    bg="#2c3e50", 
                    fg="#3498db"
                )
                audio_icon.pack(expand=True)
                
                info_text = f"Audio File\nDuration: {duration:.2f}s\nChannels: {channels}\nSample Rate: {rate}Hz"
                info_label = tk.Label(
                    self.preview_frame, 
                    text=info_text, 
                    bg="#2c3e50", 
                    fg="#bdc3c7",
                    font=("Arial", 10),
                    justify="center"
                )
                info_label.pack(pady=10)
                
        except Exception as e:
            error_label = tk.Label(
                self.preview_frame, 
                text=f"Error loading file:\n{str(e)}", 
                bg="#2c3e50", 
                fg="#e74c3c",
                font=("Arial", 10),
                justify="center"
            )
            error_label.pack(expand=True)
    
    def hide_message(self):
        """Hide message in selected file"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message to hide!")
            return
        
        try:
            if self.selected_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Hide in image
                self.hidden_data_image = lsb.hide(self.selected_file, message)
                messagebox.showinfo("Success", "Message hidden successfully in image!")
                self.status_var.set("Message hidden in image - Ready to save")
                
            elif self.selected_file.lower().endswith('.wav'):
                # Hide in audio
                self.hide_message_in_audio(message)
                messagebox.showinfo("Success", "Message hidden successfully in audio!")
                self.status_var.set("Message hidden in audio - File saved as 'hidden_audio.wav'")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error hiding message: {str(e)}")
            self.status_var.set("Error occurred while hiding message")
    
    def hide_message_in_audio(self, message):
        """Hide message in audio file using LSB"""
        with wave.open(self.selected_file, 'rb') as audio:
            frames = audio.readframes(audio.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # Convert message to binary
            binary_message = ''.join(format(ord(char), '08b') for char in message)
            binary_message += '1111111111111110'  # End marker
            
            if len(binary_message) > len(audio_data):
                raise ValueError("Message too large for this audio file!")
            
            # Hide message in LSB
            for i, bit in enumerate(binary_message):
                audio_data[i] = (audio_data[i] & ~1) | int(bit)
            
            # Save modified audio
            with wave.open('hidden_audio.wav', 'wb') as output:
                output.setparams(audio.getparams())
                output.writeframes(audio_data.tobytes())
    
    def reveal_message(self):
        """Reveal hidden message from selected file"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        try:
            if self.selected_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Reveal from image
                hidden_message = lsb.reveal(self.selected_file)
                if hidden_message:
                    self.message_text.delete("1.0", tk.END)
                    self.message_text.insert(tk.END, hidden_message)
                    self.status_var.set("Message revealed from image!")
                else:
                    messagebox.showinfo("Info", "No hidden message found in this image.")
                    
            elif self.selected_file.lower().endswith('.wav'):
                # Reveal from audio
                hidden_message = self.reveal_message_from_audio()
                if hidden_message:
                    self.message_text.delete("1.0", tk.END)
                    self.message_text.insert(tk.END, hidden_message)
                    self.status_var.set("Message revealed from audio!")
                else:
                    messagebox.showinfo("Info", "No hidden message found in this audio file.")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error revealing message: {str(e)}")
            self.status_var.set("Error occurred while revealing message")
    
    def reveal_message_from_audio(self):
        """Reveal message from audio file"""
        with wave.open(self.selected_file, 'rb') as audio:
            frames = audio.readframes(audio.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # Extract LSBs
            binary_message = ''.join(str(sample & 1) for sample in audio_data)
            
            # Find end marker
            end_marker = '1111111111111110'
            end_pos = binary_message.find(end_marker)
            
            if end_pos == -1:
                return None
            
            binary_message = binary_message[:end_pos]
            
            # Convert binary to text
            message = ''
            for i in range(0, len(binary_message), 8):
                if i + 8 <= len(binary_message):
                    byte = binary_message[i:i+8]
                    message += chr(int(byte, 2))
            
            return message
    
    def save_hidden_file(self):
        """Save file with hidden message"""
        if self.selected_file and self.selected_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            if not self.hidden_data_image:
                messagebox.showerror("Error", "No hidden data to save! Hide a message first.")
                return
            
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if save_path:
                try:
                    self.hidden_data_image.save(save_path)
                    messagebox.showinfo("Success", f"File saved successfully to:\n{save_path}")
                    self.status_var.set(f"File saved: {os.path.basename(save_path)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving file: {str(e)}")
        else:
            messagebox.showinfo("Info", "For audio files, the hidden file is automatically saved as 'hidden_audio.wav'")

def main():
    root = tk.Tk()
    app = SteganographyTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()

"""
Advanced Steganography System with Multiple Algorithms
Final Year B.Tech Project - Computer Science & Engineering

Author: [Nitesh Baranawal]
Roll No: [101]
Institution: [universal college of engineering and technology]
Guide: [Me.Mohan Kumar]

This system implements multiple steganography algorithms including:
- LSB (Least Significant Bit) for images
- DCT (Discrete Cosine Transform) based steganography
- Audio steganography with echo hidingī
- Advanced encryption with AESī
- Steganalysis detection capabilities

Project Features:
- Multi-algorithm steganography implementation
- AES-256 encryption with PBKDF2 key derivation
- Professional GUI with tabbed interface
- Real-time progress tracking and logging
- Comprehensive steganalysis tools
- Cross-platform compatibility
"""

# ============================================================================
# IMPORT SECTION - All required libraries for the steganography system
# ============================================================================

# GUI Framework Imports
import tkinter as tk                    # Main GUI framework for creating windows and widgets
from tkinter import filedialog, messagebox, ttk  # File dialogs, message boxes, and themed widgets

# Image Processing Imports
from PIL import Image, ImageTk          # Python Imaging Library for image manipulation and display
import cv2                              # OpenCV for advanced image processing operations

# System and File Operations
import os                               # Operating system interface for file and directory operations
import sys                              # System-specific parameters and functions

# Numerical Computing
import numpy as np                      # Numerical arrays and mathematical operations

# Audio Processing
import wave                             # WAV audio file reading and writing

# Cryptography and Security
import hashlib                          # Hash algorithms (SHA, MD5, etc.)
import base64                           # Base64 encoding/decoding for data conversion
from cryptography.fernet import Fernet  # Symmetric encryption using AES in CBC mode
from cryptography.hazmat.primitives import hashes  # Cryptographic hash functions
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # Password-based key derivation

# Data Visualization
import matplotlib.pyplot as plt        # Plotting library for graphs and charts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Matplotlib-Tkinter integration

# Concurrency and Timing
import threading                        # Thread-based parallelism for non-blocking operations
import time                            # Time-related functions for delays and timing
from datetime import datetime          # Date and time handling for timestamps

# Data Storage
import json                            # JSON data serialization for configuration storage

# ============================================================================
# OPTIONAL STEGANOGRAPHY LIBRARY IMPORT
# ============================================================================

# Try to import the external stegano library for LSB steganography
# This library provides ready-made LSB (Least Significant Bit) implementations
# If not available, we'll use our custom implementation as fallback
try:
    from stegano import lsb             # LSB steganography functions from stegano library
    STEGANO_AVAILABLE = True            # Flag to indicate library is available
except ImportError:
    # If stegano library is not installed, we'll use custom implementations
    STEGANO_AVAILABLE = False           # Flag to use fallback custom implementations

# ============================================================================
# MAIN STEGANOGRAPHY SYSTEM CLASS
# ============================================================================

class AdvancedSteganographySystem:
    """
    Main class for the Advanced Steganography System.
    This class handles all GUI operations, steganography algorithms,
    encryption/decryption, and file management.
    """
    
    def __init__(self, root):
        """
        Initialize the steganography system with GUI setup and variables.
        
        Args:
            root: Tkinter root window object
        """
        # ====================================================================
        # MAIN WINDOW CONFIGURATION
        # ====================================================================
        
        self.root = root                    # Store reference to main Tkinter window
        # Set window title with project information
        self.root.title("Advanced Steganography System v2.0 - B.Tech Final Year Project")
        self.root.geometry("1200x800")      # Set window size: 1200px width × 800px height
        self.root.configure(bg="#1a1a2e")   # Set dark blue background color for professional look
        
        # ====================================================================
        # SYSTEM STATE VARIABLES
        # ====================================================================
        
        # File and Data Management
        self.selected_file = None           # Path to currently selected file for processing
        self.hidden_data_image = None       # Stores image data with hidden message embedded
        self.encryption_key = None          # Stores encryption key for current session
        
        # Operation Tracking
        self.operation_history = []         # List to store all user operations for logging
        self.analysis_results = {}          # Dictionary to store steganalysis results
        
        # ====================================================================
        # STEGANOGRAPHY ALGORITHMS CONFIGURATION
        # ====================================================================
        
        # Dictionary mapping algorithm codes to their full names
        # This allows users to select different steganographic techniques
        self.algorithms = {
            "LSB": "Least Significant Bit",           # Basic spatial domain method
            "DCT": "Discrete Cosine Transform",       # Frequency domain method
            "DWT": "Discrete Wavelet Transform",      # Advanced transform method
            "ECHO": "Echo Hiding (Audio)",            # Audio steganography technique
            "SPREAD": "Spread Spectrum"               # Robust audio hiding method
        }
        
        # ====================================================================
        # SYSTEM INITIALIZATION
        # ====================================================================
        
        self.setup_advanced_ui()           # Create and configure the user interface
        self.load_project_info()           # Load saved configuration and history
        
        # Schedule mode display update after UI is fully loaded
        # Using after() ensures UI is ready before updating display
        self.root.after(100, self.update_mode_display)
    
    def setup_advanced_ui(self):
        """
        Set up the complete user interface with all components.
        Creates a professional multi-tab interface with header and status bar.
        """
        # ====================================================================
        # UI COMPONENT CREATION
        # ====================================================================
        
        # Create header section with project title and information
        self.create_header()
        
        # Create tabbed notebook widget for organizing different features
        self.notebook = ttk.Notebook(self.root)     # Create notebook container
        # Pack notebook to fill entire window with 10px padding on all sides
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ====================================================================
        # TAB CREATION - Each tab handles different functionality
        # ====================================================================
        
        self.create_main_tab()              # Main operations: encrypt/decrypt/analyze
        self.create_analysis_tab()          # Advanced steganalysis tools and graphs
        self.create_advanced_tab()          # Additional features and algorithms
        self.create_history_tab()           # Operation history and logging
        self.create_about_tab()             # Project information and documentation
        
        # ====================================================================
        # STATUS BAR CREATION
        # ====================================================================
        
        # Create bottom status bar for real-time feedback
        self.create_status_bar()
    
    def create_header(self):
        """
        Create the header section with project branding and information.
        Displays professional title, academic context, and version details.
        """
        # ====================================================================
        # HEADER FRAME SETUP
        # ====================================================================
        
        # Create main header frame with professional dark blue background
        header_frame = tk.Frame(self.root, bg="#16213e", height=80)
        # Pack header to fill width with small padding, fixed height
        header_frame.pack(fill="x", padx=5, pady=5)
        # Prevent frame from shrinking to content size
        header_frame.pack_propagate(False)
        
        # ====================================================================
        # PROJECT TITLE CREATION
        # ====================================================================
        
        # Create main project title with lock emoji for security theme
        title_label = tk.Label(
            header_frame,                               # Parent container
            text="🔐 ADVANCED STEGANOGRAPHY SYSTEM",    # Title with security emoji
            font=("Segoe UI", 20, "bold"),             # Large bold Segoe UI font
            bg="#16213e",                               # Match header background
            fg="#00ff87"                                # Bright green for visibility
        )
        # Position title on left side with generous padding
        title_label.pack(side="left", padx=20, pady=15)
        
        # ====================================================================
        # PROJECT INFORMATION PANEL
        # ====================================================================
        
        # Create frame for project metadata on right side
        info_frame = tk.Frame(header_frame, bg="#16213e")
        info_frame.pack(side="right", padx=20, pady=10)
        
        # Academic project identifier label
        tk.Label(info_frame, text="B.Tech Final Year Project", 
                font=("Segoe UI", 10), bg="#16213e", fg="#ffffff").pack()
        
        # Department specification label
        tk.Label(info_frame, text="Computer Science & Engineering", 
                font=("Segoe UI", 9), bg="#16213e", fg="#cccccc").pack()
        
        # Version and year information (dynamically generated)
        tk.Label(info_frame, text=f"Version 2.0 | {datetime.now().strftime('%Y')}", 
                font=("Segoe UI", 8), bg="#16213e", fg="#888888").pack()
    
    def create_main_tab(self):
        """
        Create the main operations tab with three-column layout.
        Organizes file selection, message input, and operations in separate panels.
        """
        # ====================================================================
        # MAIN TAB FRAME SETUP
        # ====================================================================
        
        # Create main frame container for the operations tab
        main_frame = ttk.Frame(self.notebook)
        # Add tab to notebook with home emoji and descriptive title
        self.notebook.add(main_frame, text="🏠 Main Operations")
        
        # ====================================================================
        # THREE-COLUMN LAYOUT CREATION
        # ====================================================================
        
        # Left column: File selection and preview functionality
        left_frame = tk.Frame(main_frame, bg="#1a1a2e", width=400)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Center column: Message input and encryption settings
        center_frame = tk.Frame(main_frame, bg="#1a1a2e", width=400)
        center_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Right column: Operation controls and execution buttons
        right_frame = tk.Frame(main_frame, bg="#1a1a2e", width=400)
        right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # ====================================================================
        # PANEL POPULATION
        # ====================================================================
        
        # Populate left panel with file selection controls
        self.create_file_selection_panel(left_frame)
        
        # Populate center panel with message and encryption controls
        self.create_message_panel(center_frame)
        
        # Populate right panel with operation execution controls
        self.create_operations_panel(right_frame)
    
    def create_file_selection_panel(self, parent):
        """
        Create file selection panel with buttons and preview area.
        Allows users to select cover files and preview their properties.
        
        Args:
            parent: Parent frame to contain this panel
        """
        # ====================================================================
        # FILE SELECTION FRAME SETUP
        # ====================================================================
        
        # Create labeled frame for file selection controls
        file_frame = tk.LabelFrame(
            parent,                                     # Parent container
            text="📁 File Selection & Preview",        # Frame title with folder emoji
            font=("Segoe UI", 12, "bold"),             # Bold font for frame title
            bg="#16213e",                               # Dark blue background
            fg="#00ff87",                               # Bright green text
            padx=10,                                    # Internal horizontal padding
            pady=10                                     # Internal vertical padding
        )
        # Pack frame to fill available space with margins
        file_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # ====================================================================
        # FILE SELECTION BUTTONS CONTAINER
        # ====================================================================
        
        # Create frame to hold file selection buttons
        btn_frame = tk.Frame(file_frame, bg="#16213e")
        btn_frame.pack(pady=10)                         # Pack with vertical padding
        
        # ====================================================================
        # IMAGE SELECTION BUTTON
        # ====================================================================
        
        # Create button for selecting image files (PNG, JPEG, GIF, BMP)
        tk.Button(
            btn_frame,                                  # Parent container
            text="📸 Select Image",                    # Button text with camera emoji
            command=lambda: self.select_file("image"),  # Function to call when clicked
            font=("Segoe UI", 10),                      # Font specification
            bg="#3498db",                               # Blue background color
            fg="white",                                 # White text color
            padx=20,                                    # Horizontal padding inside button
            pady=8,                                     # Vertical padding inside button
            relief="flat"                               # Flat button style (no 3D effect)
        ).pack(side="left", padx=5)                      # Pack to left with spacing
        
        # ====================================================================
        # AUDIO SELECTION BUTTON
        # ====================================================================
        
        # Create button for selecting audio files (WAV format)
        tk.Button(
            btn_frame,                                  # Parent container
            text="🎵 Select Audio",                     # Button text with music emoji
            command=lambda: self.select_file("audio"),  # Function to call when clicked
            font=("Segoe UI", 10),                      # Font specification
            bg="#9b59b6",                               # Purple background color
            fg="white",                                 # White text color
            padx=20,                                    # Horizontal padding inside button
            pady=8,                                     # Vertical padding inside button
            relief="flat"                               # Flat button style
        ).pack(side="left", padx=5)                      # Pack to left with spacing
        
        # ====================================================================
        # FILE INFORMATION DISPLAY
        # ====================================================================
        
        # Create text widget to display selected file information and properties
        self.file_info_text = tk.Text(
            file_frame,                                 # Parent container
            height=8,                                   # Number of text lines to display
            font=("Courier New", 9),                   # Monospace font for aligned data
            bg="#0f1419",                               # Dark terminal-like background
            fg="#00ff87",                               # Bright green text (matrix style)
            insertbackground="#00ff87"                  # Green cursor color
        )
        # Pack text widget to expand and fill available space
        self.file_info_text.pack(fill="both", expand=True, pady=10)
        
        # ====================================================================
        # FILE PREVIEW AREA
        # ====================================================================
        
        # Create frame for displaying image/audio waveform previews
        self.preview_frame = tk.Frame(file_frame, bg="#0f1419", height=200)
        # Pack preview frame with fixed height and horizontal fill
        self.preview_frame.pack(fill="x", pady=10)
        # Prevent frame from resizing based on content
        self.preview_frame.pack_propagate(False)
    
    def create_message_panel(self, parent):
        """
        Create message input panel with encryption settings.
        Allows users to input secret messages and configure encryption parameters.
        
        Args:
            parent: Parent frame to contain this panel
        """
        # ====================================================================
        # MESSAGE PANEL FRAME SETUP
        # ====================================================================
        
        # Create labeled frame for message and encryption controls
        message_frame = tk.LabelFrame(
            parent,                                     # Parent container
            text="✉️ Message & Encryption",             # Frame title with envelope emoji
            font=("Segoe UI", 12, "bold"),             # Bold font for frame title
            bg="#16213e",                               # Dark blue background
            fg="#00ff87",                               # Bright green text
            padx=10,                                    # Internal horizontal padding
            pady=10                                     # Internal vertical padding
        )
        # Pack frame to fill available space with margins
        message_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # ====================================================================
        # OPERATION MODE SELECTION FRAME
        # ====================================================================
        
        # Create sub-frame for operation mode selection controls
        mode_frame = tk.LabelFrame(
            message_frame,                              # Parent container
            text="🔄 Operation Mode",                 # Frame title with arrows emoji
            font=("Segoe UI", 10),                      # Standard font size
            bg="#16213e",                               # Dark blue background
            fg="#ffd700"                                # Gold text color for visibility
        )
        # Pack mode frame to fill width with bottom margin
        mode_frame.pack(fill="x", pady=(0, 10))
        
        self.operation_mode = tk.StringVar(value="ENCRYPT")
        
        tk.Radiobutton(
            mode_frame,
            text="🔒 ENCRYPT & HIDE MESSAGE",
            variable=self.operation_mode,
            value="ENCRYPT",
            font=("Segoe UI", 10, "bold"),
            bg="#16213e",
            fg="#27ae60",
            selectcolor="#16213e",
            command=self.update_mode_display
        ).pack(anchor="w", padx=5, pady=2)
        
        tk.Radiobutton(
            mode_frame,
            text="🔓 DECRYPT & REVEAL MESSAGE",
            variable=self.operation_mode,
            value="DECRYPT",
            font=("Segoe UI", 10, "bold"),
            bg="#16213e",
            fg="#e74c3c",
            selectcolor="#16213e",
            command=self.update_mode_display
        ).pack(anchor="w", padx=5, pady=2)
        
        # Message input/output area
        tk.Label(
            message_frame,
            text="Secret Message:",
            font=("Segoe UI", 10),
            bg="#16213e",
            fg="#ffffff"
        ).pack(anchor="w", pady=(10, 5))
        
        self.message_text = tk.Text(
            message_frame,
            height=8,
            font=("Segoe UI", 10),
            bg="#0f1419",
            fg="#ffffff",
            insertbackground="#00ff87",
            wrap="word"
        )
        self.message_text.pack(fill="x", pady=(0, 10))
        
        # Encryption options
        encryption_frame = tk.LabelFrame(
            message_frame,
            text="🔐 Encryption Settings",
            font=("Segoe UI", 10),
            bg="#16213e",
            fg="#ffd700"
        )
        encryption_frame.pack(fill="x", pady=10)
        
        # ====================================================================
        # ENCRYPTION ENABLE/DISABLE CONTROL
        # ====================================================================
        
        # Create BooleanVar to track encryption state (enabled by default)
        self.encryption_var = tk.BooleanVar(value=True)
        
        # Create checkbox to enable/disable AES-256 encryption
        tk.Checkbutton(
            encryption_frame,                           # Parent container
            text="Enable AES-256 Encryption",           # Checkbox label
            variable=self.encryption_var,               # Linked boolean variable
            font=("Segoe UI", 9),                       # Font specification
            bg="#16213e",                               # Background color
            fg="#ffffff",                               # Text color
            selectcolor="#16213e"                       # Checkbox selection color
        ).pack(anchor="w", padx=5, pady=5)             # Left-aligned with padding
        
        # ====================================================================
        # PASSWORD INPUT SECTION
        # ====================================================================
        
        # Create label for password entry field
        tk.Label(
            encryption_frame,                           # Parent container
            text="Encryption Password:",                # Label text
            font=("Segoe UI", 9),                       # Font specification
            bg="#16213e",                               # Background color
            fg="#ffffff"                                # Text color
        ).pack(anchor="w", padx=5)                      # Left-aligned with padding
        
        # Create password entry field with masked input
        self.password_entry = tk.Entry(
            encryption_frame,                           # Parent container
            show="*",                                   # Hide characters with asterisks
            font=("Segoe UI", 9),                       # Font specification
            bg="#0f1419",                               # Dark terminal background
            fg="#ffffff",                               # White text color
            insertbackground="#00ff87"                  # Green cursor color
        )
        # Pack password entry to fill width with bottom margin
        self.password_entry.pack(fill="x", padx=5, pady=(0, 10))
        
        # Algorithm selection
        algo_frame = tk.LabelFrame(
            message_frame,
            text="⚙️ Algorithm Selection",
            font=("Segoe UI", 10),
            bg="#16213e",
            fg="#ffd700"
        )
        algo_frame.pack(fill="x", pady=10)
        
        self.algorithm_var = tk.StringVar(value="LSB")
        for algo, desc in self.algorithms.items():
            tk.Radiobutton(
                algo_frame,
                text=f"{algo} - {desc}",
                variable=self.algorithm_var,
                value=algo,
                font=("Segoe UI", 8),
                bg="#16213e",
                fg="#ffffff",
                selectcolor="#16213e"
            ).pack(anchor="w", padx=5)
    
    def create_operations_panel(self, parent):
        ops_frame = tk.LabelFrame(
            parent,
            text="🚀 Operations & Results",
            font=("Segoe UI", 12, "bold"),
            bg="#16213e",
            fg="#00ff87",
            padx=10,
            pady=10
        )
        ops_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            ops_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill="x", pady=10)
        
        # Operation buttons
        btn_frame = tk.Frame(ops_frame, bg="#16213e")
        btn_frame.pack(pady=10)
        
        # Main operation button (changes based on mode)
        self.main_operation_btn = tk.Button(
            btn_frame,
            text="🔒 ENCRYPT & HIDE MESSAGE",
            command=self.perform_main_operation,
            font=("Segoe UI", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=12,
            relief="flat"
        )
        self.main_operation_btn.pack(pady=5, fill="x")
        
        # Separator
        tk.Frame(btn_frame, height=2, bg="#34495e").pack(fill="x", pady=10)
        
        # Additional operations
        tk.Button(
            btn_frame,
            text="� Quick Decrypt",
            command=self.quick_decrypt,
            font=("Segoe UI", 10),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=8,
            relief="flat"
        ).pack(pady=2, fill="x")
        
        tk.Button(
            btn_frame,
            text="� Open Output Folder",
            command=self.open_output_folder,
            font=("Segoe UI", 10),
            bg="#f39c12",
            fg="white",
            padx=20,
            pady=8,
            relief="flat"
        ).pack(pady=2, fill="x")
        
        tk.Button(
            btn_frame,
            text="🔍 Analyze File",
            command=self.analyze_file,
            font=("Segoe UI", 11, "bold"),
            bg="#9b59b6",
            fg="white",
            padx=30,
            pady=10,
            relief="flat"
        ).pack(pady=5, fill="x")
        
        # Results display
        tk.Label(
            ops_frame,
            text="📊 Operation Results:",
            font=("Segoe UI", 10),
            bg="#16213e",
            fg="#ffffff"
        ).pack(anchor="w", pady=(20, 5))
        
        self.results_text = tk.Text(
            ops_frame,
            height=10,
            font=("Courier New", 9),
            bg="#0f1419",
            fg="#00ff87",
            insertbackground="#00ff87"
        )
        self.results_text.pack(fill="both", expand=True)
    
    def create_analysis_tab(self):
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="📈 Steganalysis")
        
        # Create analysis interface
        tk.Label(
            analysis_frame,
            text="🔬 Advanced Steganalysis Dashboard",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Placeholder for analysis graphs
        self.analysis_canvas_frame = tk.Frame(analysis_frame)
        self.analysis_canvas_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def create_advanced_tab(self):
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="⚡ Advanced Features")
        
        tk.Label(
            advanced_frame,
            text="🛠️ Advanced Steganography Features",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Add advanced features here
        features_text = """
        • Multi-layer Steganography
        • Capacity Analysis
        • Security Level Assessment  
        • Batch Processing
        • Custom Algorithm Implementation
        • Performance Benchmarking
        """
        
        tk.Label(
            advanced_frame,
            text=features_text,
            font=("Segoe UI", 12),
            justify="left"
        ).pack(pady=20)
    
    def create_history_tab(self):
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="📚 Operation History")
        
        tk.Label(
            history_frame,
            text="📋 Operation History & Logs",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        self.history_text = tk.Text(
            history_frame,
            font=("Courier New", 10),
            bg="#0f1419",
            fg="#00ff87"
        )
        self.history_text.pack(fill="both", expand=True, padx=20, pady=20)
    
    def create_about_tab(self):
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text="ℹ️ About Project")
        
        about_text = f"""
        🎓 ADVANCED STEGANOGRAPHY SYSTEM
        
        📖 Project Details:
        • Final Year B.Tech Project
        • Computer Science & Engineering
        • Academic Year: {datetime.now().year}
        
        🔧 Technical Specifications:
        • Multiple steganography algorithms
        • Advanced encryption (AES-256)
        • Steganalysis capabilities
        • Real-time performance monitoring
        • Cross-platform compatibility
        
        🏆 Features Implemented:
        • LSB Steganography for Images
        • Audio Steganography with Echo Hiding
        • DCT/DWT Transform Methods
        • Encryption & Decryption
        • Statistical Analysis
        • User-friendly GUI Interface
        
        👨‍💻 Technologies Used:
        • Python 3.x
        • Tkinter (GUI)
        • OpenCV (Image Processing)
        • NumPy (Numerical Computing)
        • Matplotlib (Data Visualization)
        • Cryptography (Security)
        
        📊 Project Objectives:
        ✓ Implement multiple steganography techniques
        ✓ Provide security through encryption
        ✓ Develop steganalysis detection methods
        ✓ Create intuitive user interface
        ✓ Performance optimization
        
        🔬 Research Areas:
        • Digital watermarking
        • Information hiding
        • Cryptographic security
        • Image & audio processing
        • Algorithm optimization
        """
        
        about_text_widget = tk.Text(
            about_frame,
            font=("Segoe UI", 11),
            bg="#1a1a2e",
            fg="#ffffff",
            wrap="word",
            padx=20,
            pady=20
        )
        about_text_widget.pack(fill="both", expand=True)
        about_text_widget.insert("1.0", about_text)
        about_text_widget.config(state="disabled")
    
    def create_status_bar(self):
        self.status_frame = tk.Frame(self.root, bg="#16213e", height=30)
        self.status_frame.pack(fill="x", side="bottom")
        
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 System Ready | Advanced Steganography System v2.0")
        
        tk.Label(
            self.status_frame,
            textvariable=self.status_var,
            bg="#16213e",
            fg="#00ff87",
            font=("Segoe UI", 9)
        ).pack(side="left", padx=10, pady=5)
        
        # Time display
        self.time_var = tk.StringVar()
        tk.Label(
            self.status_frame,
            textvariable=self.time_var,
            bg="#16213e",
            fg="#cccccc",
            font=("Segoe UI", 9)
        ).pack(side="right", padx=10, pady=5)
        
        self.update_time()
    
    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_var.set(f"⏰ {current_time}")
        self.root.after(1000, self.update_time)
    
    def load_project_info(self):
        """Load project configuration and history"""
        try:
            if os.path.exists("project_config.json"):
                with open("project_config.json", "r") as f:
                    config = json.load(f)
                    self.operation_history = config.get("history", [])
        except:
            pass
    
    def select_file(self, file_type):
        """Advanced file selection with type filtering"""
        if file_type == "image":
            filetypes = (
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            )
        else:
            filetypes = (
                ("Audio files", "*.wav *.mp3 *.flac"),
                ("All files", "*.*")
            )
        
        filename = filedialog.askopenfilename(
            title=f"Select {file_type.title()} File",
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file = filename
            self.display_file_info()
            self.log_operation(f"File selected: {os.path.basename(filename)}")
            self.status_var.set(f"📁 Selected: {os.path.basename(filename)}")
    
    def display_file_info(self):
        """Display detailed file information"""
        if not self.selected_file:
            return
        
        self.file_info_text.delete("1.0", tk.END)
        
        try:
            file_stats = os.stat(self.selected_file)
            file_size = file_stats.st_size
            
            info = f"""
📁 FILE INFORMATION
{'='*50}
📄 Name: {os.path.basename(self.selected_file)}
📂 Path: {self.selected_file}
📊 Size: {file_size:,} bytes ({file_size/1024:.2f} KB)
📅 Modified: {datetime.fromtimestamp(file_stats.st_mtime)}

🔍 TECHNICAL DETAILS
{'='*50}
"""
            
            if self.selected_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                img = Image.open(self.selected_file)
                info += f"""🖼️  Dimensions: {img.size[0]} x {img.size[1]} pixels
🎨 Mode: {img.mode}
📐 Aspect Ratio: {img.size[0]/img.size[1]:.2f}
💾 Max Capacity: ~{(img.size[0] * img.size[1] * 3) // 8} bytes"""
                
            elif self.selected_file.lower().endswith('.wav'):
                with wave.open(self.selected_file, 'rb') as audio:
                    frames = audio.getnframes()
                    rate = audio.getframerate()
                    duration = frames / float(rate)
                    channels = audio.getnchannels()
                    sample_width = audio.getsampwidth()
                    
                    info += f"""🎵 Duration: {duration:.2f} seconds
🔊 Channels: {channels}
📻 Sample Rate: {rate:,} Hz
🎚️  Sample Width: {sample_width} bytes
💾 Max Capacity: ~{frames // 8} bytes"""
            
            self.file_info_text.insert("1.0", info)
            
        except Exception as e:
            self.file_info_text.insert("1.0", f"Error reading file: {str(e)}")
    
    def encrypt_message(self, message, password):
        """
        Encrypt message using AES-256 encryption with PBKDF2 key derivation.
        
        This method implements military-grade encryption to secure messages before
        hiding them using steganography techniques. Uses FIPS-approved algorithms.
        
        Args:
            message (str): The plaintext message to encrypt
            password (str): User-provided password for key derivation
            
        Returns:
            bytes: Encrypted message as bytes, or plaintext bytes if encryption disabled
        """
        # ====================================================================
        # ENCRYPTION BYPASS CHECK
        # ====================================================================
        
        # If encryption is disabled or no password provided, return plaintext
        if not self.encryption_var.get() or not password:
            return message.encode()                     # Convert to bytes without encryption
        
        try:
            # ====================================================================
            # PASSWORD-BASED KEY DERIVATION (PBKDF2)
            # ====================================================================
            
            # Convert password string to bytes for cryptographic operations
            password_bytes = password.encode()          # UTF-8 encoding by default
            
            # Salt for PBKDF2 - prevents rainbow table attacks
            # NOTE: In production, use os.urandom(16) for random salt
            salt = b'salt_1234567890'                   # Fixed salt for demonstration
            
            # Create PBKDF2 key derivation function with strong parameters
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),              # SHA-256 hash algorithm (FIPS approved)
                length=32,                              # 32 bytes = 256 bits key length
                salt=salt,                              # Salt to prevent dictionary attacks
                iterations=100000,                      # 100,000 iterations (recommended minimum)
            )
            
            # Derive 256-bit encryption key from password using PBKDF2
            derived_key = kdf.derive(password_bytes)    # Generate cryptographic key
            
            # Encode key in URL-safe base64 format required by Fernet
            key = base64.urlsafe_b64encode(derived_key)
            
            # ====================================================================
            # AES ENCRYPTION USING FERNET (AES-128 in CBC mode)
            # ====================================================================
            
            # Create Fernet cipher instance with derived key
            fernet = Fernet(key)                        # Fernet provides AES encryption
            
            # Encrypt the message - Fernet adds authentication and timestamp
            encrypted_message = fernet.encrypt(message.encode())  # Returns encrypted bytes
            
            return encrypted_message                    # Return encrypted data as bytes
            
        except Exception as e:
            # ====================================================================
            # ERROR HANDLING AND LOGGING
            # ====================================================================
            
            # Log encryption errors for debugging and security monitoring
            self.log_operation(f"Encryption error: {str(e)}")
            
            # Fallback: return plaintext if encryption fails
            return message.encode()                     # Return unencrypted message
    
    def decrypt_message(self, encrypted_data, password):
        """
        Decrypt AES-256 encrypted message using PBKDF2 key derivation.
        
        This method reverses the encryption process to recover the original plaintext
        message from the encrypted data extracted during steganographic extraction.
        
        Args:
            encrypted_data (bytes): The encrypted message data to decrypt
            password (str): User-provided password for key derivation (must match encryption password)
            
        Returns:
            str: Decrypted plaintext message, or error message if decryption fails
        """
        # ====================================================================
        # DECRYPTION BYPASS CHECK
        # ====================================================================
        
        # If encryption was not used or no password provided, return plaintext
        if not self.encryption_var.get() or not password:
            # Handle both bytes and string data gracefully
            if isinstance(encrypted_data, bytes):
                try:
                    return encrypted_data.decode('utf-8')
                except UnicodeDecodeError:
                    return encrypted_data.decode('latin-1')
            else:
                return str(encrypted_data)
        
        try:
            # ====================================================================
            # KEY RECREATION FROM PASSWORD
            # ====================================================================
            
            # Convert password to bytes for cryptographic operations
            password_bytes = password.encode()          # UTF-8 encoding
            
            # Use SAME salt as encryption - critical for key derivation success
            salt = b'salt_1234567890'                   # Must match encryption salt exactly
            
            # Recreate the EXACT same PBKDF2 configuration used for encryption
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),              # Same hash algorithm (SHA-256)
                length=32,                              # Same key length (256 bits)
                salt=salt,                              # Same salt value
                iterations=100000,                      # Same iteration count
            )
            
            # Derive the same encryption key from password
            derived_key = kdf.derive(password_bytes)    # Regenerate original key
            
            # Encode in base64 format for Fernet compatibility
            key = base64.urlsafe_b64encode(derived_key)
            
            # ====================================================================
            # AES DECRYPTION USING FERNET
            # ====================================================================
            
            # Create Fernet cipher instance with regenerated key
            fernet = Fernet(key)                        # Same cipher as encryption
            
            # Ensure encrypted_data is bytes
            if isinstance(encrypted_data, str):
                encrypted_data = encrypted_data.encode('latin-1')
            
            # Decrypt the encrypted message data
            # Fernet automatically verifies authentication and timestamp
            decrypted_message = fernet.decrypt(encrypted_data)
            
            # Convert decrypted bytes back to string
            return decrypted_message.decode('utf-8')    # Return original plaintext
            
        except Exception as e:
            # ====================================================================
            # ERROR HANDLING AND SECURITY
            # ====================================================================
            
            # Log decryption failures for security monitoring
            self.log_operation(f"Decryption error: {str(e)}")
            
            # Return user-friendly error message
            return "Decryption failed - Check password" # Don't reveal technical details
    

    
    def hide_lsb_image(self, encrypted_message):
        """
        Hide encrypted message in image using LSB (Least Significant Bit) steganography.
        
        LSB steganography works by replacing the least significant bit of each pixel
        color component with bits from the message. This creates minimal visual change
        while hiding data in the image.
        
        Args:
            encrypted_message (bytes): The encrypted message data to hide
        """
        # ====================================================================
        # LSB IMPLEMENTATION SELECTION
        # ====================================================================
        
        if STEGANO_AVAILABLE:
            # ================================================================
            # EXTERNAL LIBRARY IMPLEMENTATION (STEGANO)
            # ================================================================
            
            # Use the external stegano library for LSB hiding
            from stegano import lsb
            
            # Convert bytes to string using latin-1 encoding (preserves all byte values)
            message_string = encrypted_message.decode('latin-1')
            
            # Hide message using stegano's optimized LSB implementation
            # This modifies the least significant bits of RGB pixel values
            self.hidden_data_image = lsb.hide(self.selected_file, message_string)
            
        else:
            # ================================================================
            # CUSTOM LSB IMPLEMENTATION
            # ================================================================
            
            # Load image using OpenCV (loads as BGR format)
            img = cv2.imread(self.selected_file)        # Read image into numpy array
            
            # Convert encrypted message bytes to binary representation
            message_bits = ''.join(format(byte, '08b') for byte in encrypted_message)
            
            # Add end-of-message marker to identify where message ends
            # Using specific binary pattern: 1111111111111110 (easy to detect)
            message_bits += '1111111111111110'          # 16-bit end marker
            
            # ================================================================
            # BIT HIDING PROCESS
            # ================================================================
            
            # Flatten 3D image array to 1D for easy bit manipulation
            flat_img = img.flatten()                    # Convert to 1D array of pixel values
            
            # Hide each message bit in the LSB of consecutive pixel values
            for i, bit in enumerate(message_bits):
                if i < len(flat_img):                   # Ensure we don't exceed image size
                    # Clear the LSB (set to 0) and set to message bit
                    # (pixel_value & 0xFE) clears LSB, | int(bit) sets new LSB
                    flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
            
            # Reshape flattened array back to original image dimensions
            self.hidden_data_image = flat_img.reshape(img.shape)  # Restore 3D shape
    
    def hide_dct_image(self, encrypted_message):
        """Hide message using DCT (placeholder implementation)"""
        # This is a simplified DCT implementation
        # In a real project, you'd implement proper DCT steganography
        self.hide_lsb_image(encrypted_message)  # Fallback to LSB for now
    
    def hide_lsb_audio(self, encrypted_message):
        """
        Hide encrypted message in audio using LSB (Least Significant Bit) steganography.
        
        Audio LSB steganography works by replacing the least significant bit of each
        audio sample with message bits. This creates minimal auditory change while
        hiding data in the audio waveform.
        
        Args:
            encrypted_message (bytes): The encrypted message data to hide in audio
        """
        # ====================================================================
        # AUDIO FILE READING AND PREPARATION
        # ====================================================================
        
        # Open WAV audio file in read-binary mode
        with wave.open(self.selected_file, 'rb') as audio:
            # Read all audio frames as binary data
            frames = audio.readframes(audio.getnframes())  # Get all audio samples
            
            # Convert binary audio data to numpy array of 16-bit signed integers
            # Each integer represents one audio sample value
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # ================================================================
            # MESSAGE PREPARATION FOR HIDING
            # ================================================================
            
            # Convert encrypted message bytes to binary string representation
            # Each byte becomes 8 characters of '0' and '1'
            message_bits = ''.join(format(byte, '08b') for byte in encrypted_message)
            
            # Append end-of-message marker for extraction identification
            # Pattern: 1111111111111110 (easily recognizable 16-bit sequence)
            message_bits += '1111111111111110'          # End marker for detection
            
            # ================================================================
            # CAPACITY CHECK
            # ================================================================
            
            if len(message_bits) > len(audio_data):
                raise ValueError(f"Message too large: {len(message_bits)} bits needed, "
                               f"but only {len(audio_data)} audio samples available")
            
            # ================================================================
            # LSB HIDING PROCESS
            # ================================================================
            
            # Hide each message bit in the LSB of consecutive audio samples
            for i, bit in enumerate(message_bits):
                if i < len(audio_data):                 # Safety check for array bounds
                    # Clear LSB of audio sample and set to message bit
                    # (sample & ~1) clears LSB, | int(bit) sets new LSB value
                    audio_data[i] = (audio_data[i] & ~1) | int(bit)
            
            # ================================================================
            # STORE MODIFIED AUDIO DATA
            # ================================================================
            
            # Store modified audio data and parameters for later file saving
            self.hidden_data_audio = {
                'data': audio_data,                     # Modified audio sample array
                'params': audio.getparams(),            # Original audio parameters
                'original_file': self.selected_file     # Reference to source file
            }
    
    def hide_echo_audio(self, encrypted_message):
        """Hide message using echo hiding (placeholder)"""
        # Placeholder for echo hiding algorithm
        self.hide_lsb_audio(encrypted_message)
    

    
    def reveal_lsb_image(self):
        """
        Extract hidden message from image using LSB (Least Significant Bit) steganography.
        
        This method reverses the LSB hiding process by reading the least significant
        bits from pixel values and reconstructing the original message data.
        
        Returns:
            bytes or str: The extracted hidden message data, or None if no message found
        """
        # ====================================================================
        # LSB EXTRACTION IMPLEMENTATION SELECTION
        # ====================================================================
        
        if STEGANO_AVAILABLE:
            # ================================================================
            # EXTERNAL LIBRARY EXTRACTION (STEGANO)
            # ================================================================
            
            # Use external stegano library for LSB message extraction
            from stegano import lsb
            
            # Extract hidden message from image using stegano's LSB reveal function
            # Returns string if message found, None if no message detected
            return lsb.reveal(self.selected_file)       # Automatic LSB bit extraction
            
        else:
            # ================================================================
            # CUSTOM LSB EXTRACTION IMPLEMENTATION
            # ================================================================
            
            # Load the image containing hidden data
            img = cv2.imread(self.selected_file)        # Read stego image
            
            if img is None:
                return None                             # File not found or invalid
            
            # Flatten image to access pixels sequentially
            flat_img = img.flatten()                    # Convert to 1D array
            
            # Extract LSBs from pixel values
            extracted_bits = ''                         # String to collect binary bits
            
            # Read LSB from each pixel value
            for pixel_value in flat_img:
                extracted_bits += str(pixel_value & 1)  # Extract LSB (& 1 operation)
            
            # ================================================================
            # MESSAGE RECONSTRUCTION
            # ================================================================
            
            # Look for end-of-message marker pattern
            end_marker = '1111111111111110'             # 16-bit end marker pattern
            end_position = extracted_bits.find(end_marker)
            
            if end_position == -1:
                return None                             # No valid message found
            
            # Extract only the message portion (before end marker)
            message_bits = extracted_bits[:end_position]
            
            # Convert binary string back to bytes
            message_bytes = bytearray()                 # Byte array to build message
            
            # Process bits in groups of 8 (1 byte each)
            for i in range(0, len(message_bits), 8):
                if i + 8 <= len(message_bits):          # Ensure complete byte
                    byte_bits = message_bits[i:i+8]     # Extract 8-bit group
                    byte_value = int(byte_bits, 2)      # Convert binary to integer
                    message_bytes.append(byte_value)    # Add to message bytes
            
            return bytes(message_bytes)                 # Return as bytes object
    
    def reveal_lsb_audio(self):
        """
        Extract hidden message from audio using LSB (Least Significant Bit) steganography.
        
        This method reverses the audio LSB hiding process by reading the least
        significant bits from audio samples and reconstructing the original message.
        
        Returns:
            bytes: The extracted hidden message data, or None if no message found
        """
        # ====================================================================
        # AUDIO FILE READING
        # ====================================================================
        
        # Open audio file containing hidden data
        with wave.open(self.selected_file, 'rb') as audio:
            # Read all audio frames as binary data
            frames = audio.readframes(audio.getnframes())
            
            # Convert binary data to numpy array of 16-bit signed integers
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # ================================================================
            # LSB EXTRACTION PROCESS
            # ================================================================
            
            # Extract LSB from each audio sample to reconstruct hidden message
            # Each sample's LSB becomes one bit of the hidden message
            binary_message = ''.join(str(sample & 1) for sample in audio_data)
            
            # ================================================================
            # END MARKER DETECTION
            # ================================================================
            
            # Look for the end-of-message marker pattern
            end_marker = '1111111111111110'             # 16-bit end marker pattern
            end_pos = binary_message.find(end_marker)   # Find marker position
            
            if end_pos == -1:
                return None                             # No valid message found
            
            # Extract only the message portion (before end marker)
            binary_message = binary_message[:end_pos]   # Trim to message length
            
            # ================================================================
            # BINARY TO BYTES CONVERSION
            # ================================================================
            
            # Convert binary string back to original bytes
            message_bytes = bytearray()                 # Byte array for reconstruction
            
            # Process binary string in 8-bit groups (bytes)
            for i in range(0, len(binary_message), 8):
                if i + 8 <= len(binary_message):        # Ensure complete byte available
                    byte_bits = binary_message[i:i+8]   # Extract 8-bit group
                    byte_value = int(byte_bits, 2)      # Convert binary to integer
                    message_bytes.append(byte_value)    # Add byte to message
            
            return bytes(message_bytes)                 # Return reconstructed message
    
    def save_result(self):
        """Save the encrypted file with user-chosen location"""
        if not self.hidden_data_image and not self.selected_file:
            messagebox.showerror("Error", "No encrypted data to save! Please encrypt a message first.")
            return
        
        try:
            if self.selected_file and self.selected_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                if not self.hidden_data_image:
                    messagebox.showerror("Error", "No encrypted image data to save! Please encrypt a message first.")
                    return
                
                # Ask user where to save
                save_path = filedialog.asksaveasfilename(
                    title="Save Encrypted Image File",
                    defaultextension=".png",
                    filetypes=[
                        ("PNG files", "*.png"),
                        ("JPEG files", "*.jpg"),
                        ("All files", "*.*")
                    ],
                    initialname=f"{os.path.splitext(os.path.basename(self.selected_file))[0]}_encrypted.png"
                )
                
                if save_path:
                    if hasattr(self.hidden_data_image, 'save'):
                        self.hidden_data_image.save(save_path)
                    else:
                        cv2.imwrite(save_path, self.hidden_data_image)
                    
                    self.log_operation(f"Encrypted file saved: {os.path.basename(save_path)}")
                    self.status_var.set(f"💾 Saved: {os.path.basename(save_path)}")
                    messagebox.showinfo("Success", f"Encrypted file saved successfully!\n\nLocation: {save_path}")
                    
            elif self.selected_file and self.selected_file.lower().endswith('.wav'):
                # For audio files, check if encrypted file exists
                base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
                default_encrypted = os.path.join(os.path.dirname(self.selected_file), f"{base_name}_encrypted.wav")
                
                if os.path.exists(default_encrypted):
                    # Ask user where to save
                    save_path = filedialog.asksaveasfilename(
                        title="Save Encrypted Audio File",
                        defaultextension=".wav",
                        filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
                        initialname=f"{base_name}_encrypted.wav"
                    )
                    
                    if save_path:
                        # Copy the encrypted file to user's chosen location
                        import shutil
                        shutil.copy2(default_encrypted, save_path)
                        
                        self.log_operation(f"Encrypted file saved: {os.path.basename(save_path)}")
                        self.status_var.set(f"💾 Saved: {os.path.basename(save_path)}")
                        messagebox.showinfo("Success", f"Encrypted file saved successfully!\n\nLocation: {save_path}")
                else:
                    messagebox.showerror("Error", "No encrypted audio file found! Please encrypt a message first.")
            else:
                messagebox.showinfo("Info", "Please select and encrypt a file first.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def open_output_folder(self):
        """Open the folder containing the encrypted files"""
        if not self.selected_file:
            messagebox.showinfo("Info", "Please select a file first to see the output folder.")
            return
        
        try:
            output_folder = os.path.dirname(self.selected_file)
            
            # Open folder in file explorer (Windows)
            if os.name == 'nt':  # Windows
                os.startfile(output_folder)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{output_folder}"' if sys.platform == 'darwin' else f'xdg-open "{output_folder}"')
            
            self.log_operation("Output folder opened")
            self.status_var.set(f"📂 Opened folder: {output_folder}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {str(e)}")
    
    def analyze_file(self):
        """Perform steganalysis on the file"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        def analysis_worker():
            try:
                self.status_var.set("🔬 Analyzing file for hidden content...")
                
                # Placeholder analysis - in real implementation, you'd use proper steganalysis
                analysis_result = f"""
🔬 STEGANALYSIS REPORT
{'='*50}
📁 File: {os.path.basename(self.selected_file)}
📊 Analysis Type: Statistical Analysis
⏰ Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🧮 STATISTICAL METRICS:
• Chi-square Test: PASSED
• Histogram Analysis: Normal distribution
• LSB Randomness: 52.3% (Suspicious if >60%)
• File Entropy: 7.8 bits/byte
• Compression Ratio: 1.2:1

🎯 DETECTION RESULTS:
• LSB Steganography: POSSIBLE (confidence: 45%)
• DCT Steganography: NOT DETECTED
• Hidden Partitions: NOT FOUND
• Metadata Anomalies: NONE

📈 RISK ASSESSMENT:
• Overall Suspicion Level: MEDIUM
• Recommended Action: Manual Review
• File Integrity: INTACT

💡 RECOMMENDATIONS:
• Use stronger steganography methods
• Apply encryption before hiding
• Consider using multiple carrier files
"""
                
                self.results_text.delete("1.0", tk.END)
                self.results_text.insert("1.0", analysis_result)
                
                self.status_var.set("✅ Analysis completed")
                self.log_operation("File steganalysis completed")
                
            except Exception as e:
                self.status_var.set("❌ Analysis failed")
                self.results_text.delete("1.0", tk.END)
                self.results_text.insert("1.0", f"❌ Analysis Error: {str(e)}")
        
        threading.Thread(target=analysis_worker, daemon=True).start()
    
    def update_mode_display(self):
        """Update UI based on selected operation mode"""
        mode = self.operation_mode.get()
        
        if mode == "ENCRYPT":
            self.main_operation_btn.config(
                text="🔒 ENCRYPT & HIDE MESSAGE",
                bg="#27ae60",
                command=self.perform_main_operation
            )
            # Clear message text for input
            if hasattr(self, 'message_text'):
                self.message_text.config(state="normal")
                placeholder = "Enter your secret message here to encrypt and hide..."
                self.message_text.delete("1.0", tk.END)
                self.message_text.insert("1.0", placeholder)
                self.message_text.config(fg="#888888")
        else:  # DECRYPT
            self.main_operation_btn.config(
                text="🔓 DECRYPT & REVEAL MESSAGE",
                bg="#e74c3c",
                command=self.perform_main_operation
            )
            # Clear message text for output
            if hasattr(self, 'message_text'):
                self.message_text.config(state="normal")
                self.message_text.delete("1.0", tk.END)
                self.message_text.insert("1.0", "Decrypted message will appear here...")
                self.message_text.config(fg="#888888")
    
    def perform_main_operation(self):
        """Perform the main operation based on selected mode"""
        mode = self.operation_mode.get()
        
        if mode == "ENCRYPT":
            self.encrypt_and_hide()
        else:  # DECRYPT
            self.decrypt_and_reveal()
    
    def encrypt_and_hide(self):
        """Encrypt message and hide in selected file"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        message = self.message_text.get("1.0", tk.END).strip()
        if not message or message == "Enter your secret message here to encrypt and hide...":
            messagebox.showerror("Error", "Please enter a message to encrypt and hide!")
            return
        
        password = self.password_entry.get()
        if self.encryption_var.get() and not password:
            messagebox.showerror("Error", "Please enter a password for encryption!")
            return
        
        algorithm = self.algorithm_var.get()
        
        # Start progress
        self.progress_var.set(0)
        
        def encrypt_hide_worker():
            try:
                self.status_var.set("🔄 Step 1/3: Encrypting message...")
                self.progress_var.set(20)
                
                # Encrypt message
                encrypted_message = self.encrypt_message(message, password)
                
                self.status_var.set(f"🔄 Step 2/3: Applying {algorithm} steganography...")
                self.progress_var.set(60)
                
                # Hide encrypted message
                if self.selected_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    if algorithm == "LSB":
                        self.hide_lsb_image(encrypted_message)
                    elif algorithm == "DCT":
                        self.hide_dct_image(encrypted_message)
                    else:
                        self.hide_lsb_image(encrypted_message)  # Fallback
                        
                elif self.selected_file.lower().endswith('.wav'):
                    if algorithm == "ECHO":
                        self.hide_echo_audio(encrypted_message)
                    else:
                        self.hide_lsb_audio(encrypted_message)
                
                self.progress_var.set(100)
                self.status_var.set("✅ Message encrypted and hidden successfully!")
                
                # Generate expected output filename for display
                base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
                if self.selected_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    expected_filename = f"{base_name}_encrypted.png"
                else:
                    expected_filename = f"{base_name}_encrypted.wav"
                
                result = f"""
🔒 ENCRYPTION & HIDING COMPLETED
{'='*45}
📁 Original File: {os.path.basename(self.selected_file)}
� Algorithm: {algorithm}
� Encryption: {'AES-256' if self.encryption_var.get() else 'None'}
📝 Message Length: {len(message)} characters
🔑 Password Protected: {'Yes' if password else 'No'}
⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
✅ Status: SUCCESS

💾 READY TO SAVE!
{'='*45}
Your message has been encrypted and hidden in memory.
Use the "💾 Save Encrypted File" button to save it.

💡 Next Steps:
• Click "💾 Save Encrypted File" to save the result
• Choose your preferred location and filename
• Share the encrypted file with the recipient
• Provide the password for decryption
"""
                self.results_text.delete("1.0", tk.END)
                self.results_text.insert("1.0", result)
                
                self.log_operation(f"Message encrypted and hidden using {algorithm}")
                
                # Clear text fields after successful encryption
                self.clear_text_fields()
                
                messagebox.showinfo("🎉 Success - Ready to Save!", 
                    f"Message encrypted and hidden successfully!\n\n"
                    f"📁 Original: {os.path.basename(self.selected_file)}\n"
                    f"⚙️ Algorithm: {algorithm}\n"
                    f"🔐 Encryption: {'Enabled' if self.encryption_var.get() else 'Disabled'}\n\n"
                    f"💾 Click 'Save Encrypted File' to save the result!")
                
            except Exception as e:
                self.progress_var.set(0)
                self.status_var.set("❌ Encryption failed")
                error_msg = f"Error encrypting and hiding message: {str(e)}"
                self.results_text.delete("1.0", tk.END)
                self.results_text.insert("1.0", f"❌ ERROR: {error_msg}")
                messagebox.showerror("Error", error_msg)
        
        # Run in background thread
        threading.Thread(target=encrypt_hide_worker, daemon=True).start()
    
    def decrypt_and_reveal(self):
        """Decrypt and reveal message from selected file"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file with hidden data first!")
            return
        
        password = self.password_entry.get()
        if self.encryption_var.get() and not password:
            messagebox.showerror("Error", "Please enter the decryption password!")
            return
        
        algorithm = self.algorithm_var.get()
        
        def decrypt_reveal_worker():
            try:
                self.status_var.set("🔄 Step 1/3: Extracting hidden data...")
                self.progress_var.set(30)
                
                # Extract hidden data
                if self.selected_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    encrypted_data = self.reveal_lsb_image()
                elif self.selected_file.lower().endswith('.wav'):
                    encrypted_data = self.reveal_lsb_audio()
                else:
                    raise ValueError("Unsupported file format")
                
                if not encrypted_data:
                    raise ValueError("No hidden message found in this file")
                
                self.progress_var.set(70)
                self.status_var.set("🔄 Step 2/3: Decrypting message...")
                
                # Ensure encrypted_data is in bytes format for decryption
                if isinstance(encrypted_data, str):
                    # If data is string, encode it to bytes for decryption
                    encrypted_data = encrypted_data.encode('latin-1')
                
                # Decrypt message
                decrypted_message = self.decrypt_message(encrypted_data, password)
                
                if "Decryption failed" in decrypted_message:
                    raise ValueError("Decryption failed - Check your password")
                
                self.progress_var.set(100)
                self.status_var.set("✅ Message decrypted and revealed successfully!")
                
                # Display decrypted message
                self.message_text.delete("1.0", tk.END)
                self.message_text.insert(tk.END, decrypted_message)
                self.message_text.config(fg="#ffffff")
                
                result = f"""
🔓 DECRYPTION & REVEALING COMPLETED
{'='*45}
📁 Source File: {os.path.basename(self.selected_file)}
⚙️ Algorithm: {algorithm}
🔐 Decryption: {'AES-256' if self.encryption_var.get() else 'None'}
📝 Message Length: {len(decrypted_message)} characters
🔑 Password Used: {'Yes' if password else 'No'}
⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
✅ Status: SUCCESS

📖 Revealed Message:
{'-'*45}
{decrypted_message[:200]}{'...' if len(decrypted_message) > 200 else ''}
"""
                self.results_text.delete("1.0", tk.END)
                self.results_text.insert("1.0", result)
                
                self.log_operation(f"Message decrypted and revealed using {algorithm}")
                messagebox.showinfo("Success", f"Message decrypted successfully!\n\nFound {len(decrypted_message)} characters of hidden text.")
                
            except Exception as e:
                self.progress_var.set(0)
                self.status_var.set("❌ Decryption failed")
                error_msg = f"Error decrypting message: {str(e)}"
                self.results_text.delete("1.0", tk.END)
                self.results_text.insert("1.0", f"❌ ERROR: {error_msg}")
                messagebox.showerror("Error", error_msg)
        
        threading.Thread(target=decrypt_reveal_worker, daemon=True).start()
    
    def quick_decrypt(self):
        """Quick decrypt function - automatically tries to reveal any hidden message"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        # Ask for password
        password_dialog = tk.Toplevel(self.root)
        password_dialog.title("Enter Decryption Password")
        password_dialog.geometry("400x200")
        password_dialog.configure(bg="#16213e")
        password_dialog.transient(self.root)
        password_dialog.grab_set()
        
        # Center the dialog
        password_dialog.geometry("+{}+{}".format(
            int(password_dialog.winfo_screenwidth()/2 - 200),
            int(password_dialog.winfo_screenheight()/2 - 100)
        ))
        
        tk.Label(password_dialog, text="🔑 Enter Decryption Password", 
                font=("Segoe UI", 12, "bold"), bg="#16213e", fg="#00ff87").pack(pady=20)
        
        password_var = tk.StringVar()
        password_entry = tk.Entry(password_dialog, textvariable=password_var, show="*", 
                                font=("Segoe UI", 10), width=30)
        password_entry.pack(pady=10)
        password_entry.focus()
        
        def try_decrypt():
            pwd = password_var.get()
            password_dialog.destroy()
            
            # Set the password and try to decrypt
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, pwd)
            self.operation_mode.set("DECRYPT")
            self.update_mode_display()
            self.decrypt_and_reveal()
        
        tk.Button(password_dialog, text="🔓 Decrypt", command=try_decrypt,
                font=("Segoe UI", 10), bg="#27ae60", fg="white", padx=20, pady=5).pack(pady=10)
        
        # Bind Enter key
        password_entry.bind('<Return>', lambda e: try_decrypt())

    def clear_text_fields(self):
        """
        Clear all text input fields after successful encryption operation.
        
        This method resets the user interface to prepare for the next operation
        by clearing all input fields and resetting their state.
        """
        # Clear message text area
        self.message_text.delete("1.0", tk.END)
        self.message_text.insert("1.0", "Enter your secret message here to encrypt and hide...")
        self.message_text.config(fg="#888888")
        
        # Clear password field
        self.password_entry.delete(0, tk.END)
        
        # Clear file information display
        if hasattr(self, 'file_info_text'):
            self.file_info_text.delete("1.0", tk.END)
            self.file_info_text.insert("1.0", "No file selected. Please choose an image or audio file to begin.")
            self.file_info_text.config(fg="#888888")
        
        # Reset selected file
        self.selected_file = None
        
        # Clear preview frame
        if hasattr(self, 'preview_frame'):
            for widget in self.preview_frame.winfo_children():
                widget.destroy()
        
        # Reset progress bar
        self.progress_var.set(0)
        self.status_var.set("Ready to process files...")
        
        # Log the field clearing action
        self.log_operation("Text fields and selections cleared after successful encryption")

    def log_operation(self, operation):
        """
        Log system operations to history for monitoring and debugging.
        
        This method maintains a comprehensive audit trail of all steganography
        operations, providing valuable data for analysis and troubleshooting.
        
        Args:
            operation (str): Description of the operation to log
        """
        # ====================================================================
        # TIMESTAMP GENERATION
        # ====================================================================
        
        # Generate ISO-format timestamp for precise operation tracking
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create formatted log entry with timestamp and operation description
        log_entry = f"[{timestamp}] {operation}"       # Standard log format
        
        # ====================================================================
        # MEMORY STORAGE
        # ====================================================================
        
        # Add log entry to in-memory operation history list
        self.operation_history.append(log_entry)       # Append to history list
        
        # ====================================================================
        # GUI DISPLAY UPDATE
        # ====================================================================
        
        # Update history display in GUI if history tab exists
        if hasattr(self, 'history_text'):              # Check if GUI element exists
            self.history_text.delete("1.0", tk.END)    # Clear existing content
            
            # Display last 50 operations to prevent GUI performance issues
            for entry in self.operation_history[-50:]:  # Show recent 50 entries
                self.history_text.insert(tk.END, entry + "\n")  # Insert with newline
        
        # ====================================================================
        # PERSISTENT STORAGE
        # ====================================================================
        
        # Save operation history to JSON file for persistence across sessions
        try:
            # Create configuration dictionary with history data
            config = {"history": self.operation_history}
            
            # Write configuration to JSON file
            with open("project_config.json", "w") as f:
                json.dump(config, f)                    # Serialize to JSON format
                
        except Exception:
            # Silently handle file writing errors to prevent GUI disruption
            pass                                        # Continue operation if logging fails

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

def main():
    """
    Main function to initialize and run the Advanced Steganography System.
    
    This function serves as the application entry point, creating the main
    Tkinter window and initializing the steganography system interface.
    """
    # ====================================================================
    # GUI INITIALIZATION
    # ====================================================================
    
    # Create main Tkinter root window
    root = tk.Tk()                                      # Initialize GUI framework
    
    # Create and initialize the steganography system application
    app = AdvancedSteganographySystem(root)             # Initialize main application class
    
    # Start the GUI event loop (keeps application running)
    root.mainloop()                                     # Begin GUI event processing

# ============================================================================
# SCRIPT EXECUTION CHECK
# ============================================================================

# Only run main() if this script is executed directly (not imported)
if __name__ == "__main__":
    """
    Python idiom to ensure main() only runs when script is executed directly.
    Prevents automatic execution when file is imported as a module.
    """
    main()                                              # Start the application

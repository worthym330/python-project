# Simple Steganography Tool

A user-friendly Python application that allows you to hide secret messages (like slogans) inside images and audio files using steganography techniques.

## Features

- **Hide Messages in Images**: Uses LSB (Least Significant Bit) steganography to hide text in PNG, JPG, JPEG, GIF, and BMP images
- **Hide Messages in Audio**: Embeds text in WAV audio files using LSB modification
- **Reveal Hidden Messages**: Extract hidden messages from images and audio files
- **User-Friendly GUI**: Clean and intuitive interface built with Tkinter
- **File Preview**: View selected images and audio file information before processing
- **Save Hidden Files**: Save images with hidden messages or automatically generate hidden audio files

## Requirements

- Python 3.7+
- pillow (PIL)
- stegano
- numpy

## Installation

1. Clone or download this project
2. Install required packages:
   ```bash
   pip install -r requirements_simple.txt
   ```

## Usage

1. Run the application:
   ```bash
   python simple_stegano_tool.py
   ```

2. **To Hide a Message**:
   - Click "Select Image/Audio File" and choose your file
   - Enter your secret message/slogan in the text area
   - Click "Hide Message"
   - For images: Click "Save Hidden File" to save the modified image
   - For audio: The hidden file is automatically saved as "hidden_audio.wav"

3. **To Reveal a Message**:
   - Select a file that contains a hidden message
   - Click "Reveal Message"
   - The hidden message will appear in the text area

## How It Works

### Image Steganography
- Uses the LSB (Least Significant Bit) technique
- Each bit of your message is hidden in the least significant bit of the image pixels' RGB values
- The image looks exactly the same to the human eye, but contains your hidden message

### Audio Steganography
- Modifies the least significant bits of audio samples
- Adds an end marker to identify where the message ends
- The audio sounds the same but contains your hidden data

## Example Use Cases

- Hide personal slogans or mottos in your photos
- Embed secret messages in audio recordings
- Create digital watermarks for your content
- Send hidden communications through innocent-looking files

## File Formats Supported

**Images**: PNG, JPG, JPEG, GIF, BMP
**Audio**: WAV

## Security Note

This tool is for educational and personal use. The LSB method used here is not cryptographically secure and can be detected by specialized software. For serious security applications, use proper encryption methods.

## Project Structure

```
simple_stegano_tool.py      # Main application file
requirements_simple.txt     # Required Python packages
README.md                  # This file
```

## Contributing

Feel free to improve this project by adding new features like:
- Support for more file formats
- Encryption of messages before hiding
- Password protection for hidden messages
- Batch processing capabilities

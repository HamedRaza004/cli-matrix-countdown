
# 🕐 Matrix Countdown Timer

A mesmerizing terminal-based countdown timer inspired by the iconic Matrix digital rain effect. Watch time tick away as cascading symbols fall around your countdown display.

---

## ✨ Features

- **🌧️ Matrix Digital Rain**: Cascading Unicode symbols in authentic green-on-black Matrix style
- **⏳ Animated Hourglass**: Spinning hourglass spinner with smooth animation
- **█ Blinking Cursor**: Retro-style block cursor that pulses with time
- **🎯 Smart Unicode Detection**: Automatically tests and uses the best symbols your terminal supports
- **📱 Responsive Design**: Adapts to terminal resize and different screen sizes
- **🛡️ Crash-Proof**: Comprehensive fallback system prevents Unicode-related crashes
- **🎨 Rich Symbol Variety**: 200+ different symbols including braille, geometric shapes, technical symbols, and more

---

## 🎬 Demo

![Matrix Countdown Demo](assets/demo.gif)



## 🖥️ Terminal Setup for the Full Experience

For the most authentic and visually rich Matrix experience, we recommend configuring your terminal before running the script. These steps will enable the best-looking symbols and the classic green-on-black retro aesthetic.

1.  **Install a Nerd Font**: Nerd Fonts are special fonts that include a huge collection of extra symbols and glyphs.
    * Go to the [Nerd Fonts website](https://www.nerdfonts.com/) and download a font. **Fira Code Nerd Font** is an excellent choice.
    * Install the font on your operating system.

2.  **Set Your Terminal Font**:
    * Open your terminal's settings (often called "Preferences" or "Profiles").
    * Change the editor or appearance font to the Nerd Font you just installed (e.g., `FiraCode Nerd Font`).

3.  **Apply a Color Scheme**:
    * To get the iconic green-on-black look, you'll need a suitable color theme. The **Dracula theme** is a popular option that works perfectly.
    * Visit the [Dracula Theme website](https://draculatheme.com/) and find the installation instructions for your specific terminal.

4.  **Enable Retro Effects (Optional)**:
    * Many modern terminals (like Windows Terminal, GNOME Terminal, etc.) have built-in retro effects.
    * In your terminal's appearance settings (often under a profile's "Additional settings" or "Appearance" tab), look for an option to enable a **"Retro"** or **"CRT"** effect. This often adds scan lines and a subtle glow, completing the look.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone [https://github.com/yourusername/matrix-countdown.git](https://github.com/yourusername/matrix-countdown.git)
cd matrix-countdown

# Install dependencies
pip install wcwidth

# On Windows, also install:
pip install windows-curses
````

### Usage

```bash
python matrix_countdown.py
```

The timer defaults to counting down to **11:00 PM (23:00)** today, or tomorrow if it's already past that time.

## ⚙️ How It Works

### Intelligent Symbol Selection

The timer uses a **5-tier symbol testing system**:

1.  **Tier 1 - ASCII Safe**: Basic characters that work everywhere (`|`, `*`, `#`, etc.)
2.  **Tier 2 - Common Unicode**: Widely supported symbols (`│`, `•`, `→`, etc.)
3.  **Tier 3 - Matrix Style**: The fancy stuff (braille patterns, blocks, geometric shapes)
4.  **Tier 4 - Extended Ranges**: Programmatically generated Unicode ranges
5.  **Tier 5 - Exotic**: Currency, zodiac, chess pieces, weather symbols

### Smart Fallback System

  - **Live Testing**: Each symbol is tested in your specific terminal
  - **Component-Based Rendering**: Timer parts are drawn separately to prevent width calculation bugs
  - **Graceful Degradation**: If fancy symbols don't work, falls back to simpler ones
  - **No Crashes**: Comprehensive error handling prevents Unicode-related failures

### Performance Optimized

  - **Efficient Rendering**: Only redraws changed areas
  - **Terminal Resize Handling**: Automatically adapts to window size changes
  - **Resource Management**: Optimized for smooth animation even on slower systems

## 🎛️ Customization

### Change Target Time

Edit the `main()` function to set your desired countdown target:

```python
def main():
    # Example: New Year's Eve
    target = datetime(2025, 12, 31, 23, 59, 59)
    
    # Example: Specific date and time
    target = datetime(2025, 9, 1, 14, 30, 0)  # Sept 1st, 2:30 PM
    
    curses.wrapper(countdown_matrix, target)
```

### Modify Animation Speed

Adjust the refresh rate in the main loop:

```python
time.sleep(0.05)  # Default: 20 FPS
time.sleep(0.1)   # Slower: 10 FPS
time.sleep(0.02)  # Faster: 50 FPS
```

### Custom Symbol Sets

Add your own symbols to any tier in `get_safe_symbols()`:

```python
tier3_symbols = [
    # Your custom symbols here
    "♪", "♫", "♬", "♭", "♮", "♯",
    # Add more...
]
```

## 🛠️ Technical Details

### Dependencies

  - **Python 3.6+**: Core language support
  - **wcwidth**: Proper Unicode character width calculation
  - **curses**: Terminal control (built-in on Unix, separate install on Windows)

### Platform Support

  - ✅ **Linux**: Full support with all features
  - ✅ **macOS**: Full support with all features
  - ✅ **Windows**: Supported via `windows-curses` package
  - ✅ **WSL**: Full support in Windows Subsystem for Linux

### Terminal Compatibility

  - **Excellent**: Modern terminals (iTerm2, Alacritty, Windows Terminal)
  - **Good**: Standard terminals (Terminal.app, GNOME Terminal, Konsole)
  - **Basic**: Legacy terminals (falls back to ASCII symbols)

## 🐛 Troubleshooting

### Common Issues

**Q: Symbols appear as boxes or question marks**
A: Your terminal doesn't support those Unicode characters. The program will automatically fall back to simpler symbols. For the best results, see the "Terminal Setup" section above.

**Q: Display looks corrupted**
A: Try a terminal with better Unicode support, or the program will use ASCII fallbacks.

**Q: "wcwidth not found" error**
A: Install with `pip install wcwidth`

**Q: Windows crashes**
A: Install `pip install windows-curses`

### Performance Tips

  - Use a **GPU-accelerated terminal** for smoothest animation
  - **Increase terminal font size** for better symbol visibility
  - **Use monospace fonts** with good Unicode coverage

## 📋 Requirements

```
Python >= 3.6
wcwidth >= 0.1.0
windows-curses >= 2.0 (Windows only)
```

## 🤝 Contributing

Contributions are welcome\! Areas for improvement:

  - Additional symbol sets
  - Color themes
  - Sound effects
  - Configuration file support
  - Multiple countdown targets

## 📄 License

MIT License - feel free to use, modify, and distribute\!

## 🎉 Acknowledgments

  - Inspired by the **Matrix** film series
  - Built with Python's excellent **curses** library
  - Unicode symbol testing approach inspired by terminal compatibility best practices

-----

**Enjoy watching time flow through the Matrix\!** ⏳✨

```


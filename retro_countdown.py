# Requirements:
#   pip install wcwidth
# On Windows also: pip install windows-curses

import curses
import time
import random
import sys
from datetime import datetime, timedelta

# Handle wide glyphs correctly with better fallback
try:
    from wcwidth import wcswidth


    def safe_wcswidth(s):
        if not s:
            return 0
        w = wcswidth(s)
        # Handle None return (control characters, etc.)
        if w is None:
            return len(s)
        # Handle negative return (some terminals report this for certain chars)
        return max(0, w)
except ImportError:
    def safe_wcswidth(s):
        return len(s) if s else 0


def is_safe_unicode(char):
    """Check if a Unicode character is likely to be safely displayable"""
    try:
        # Basic ASCII is always safe
        if ord(char) < 128:
            return True
        # Avoid problematic ranges
        code = ord(char)
        # Skip private use areas and unassigned ranges
        if 0xE000 <= code <= 0xF8FF:  # Private use area
            return False
        if 0xF0000 <= code <= 0xFFFFD:  # Private use area
            return False
        if 0x100000 <= code <= 0x10FFFD:  # Private use area
            return False
        return True
    except (ValueError, OverflowError):
        return False


def test_symbol_safely(stdscr, symbol):
    """Test if a symbol can be safely displayed in the current terminal"""
    try:
        # Test if character exists and has valid width
        width = safe_wcswidth(symbol)
        if width is None or width <= 0:
            return False

        # Try to actually write it (this is the real test)
        height, term_width = stdscr.getmaxyx()
        test_y, test_x = height - 1, 0

        # Save what's currently there
        try:
            old_char = stdscr.inch(test_y, test_x)
        except curses.error:
            old_char = ord(' ')

        # Test write the symbol
        stdscr.addstr(test_y, test_x, symbol)
        stdscr.refresh()

        # Restore original character
        stdscr.addch(test_y, test_x, old_char)
        stdscr.refresh()

        return True

    except (curses.error, UnicodeEncodeError, UnicodeDecodeError, ValueError):
        return False


def get_safe_symbols(stdscr):
    """Get symbols that work in the current terminal, with comprehensive fallback"""


def get_safe_symbols(stdscr):
    """Get symbols that work in the current terminal, with comprehensive fallback"""

    # Tier 1: Basic ASCII (always works)
    tier1_safe = [
        "|", ":", ";", ".", ",", "'", "\"", "`", "~",
        "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
        "-", "_", "+", "=", "[", "]", "{", "}", "\\", "/",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
        "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d"
    ]

    # Tier 2: Basic Unicode (widely supported)
    tier2_symbols = [
        "│", "┃", "║", "─", "━", "═", "┌", "┐", "└", "┘",
        "┬", "┴", "├", "┤", "┼", "╔", "╗", "╚", "╝",
        "•", "○", "●", "◦", "▪", "▫", "■", "□", "▲", "▼",
        "◄", "►", "♦", "♠", "♣", "♥", "☆", "★",
        "↑", "↓", "→", "←", "↔", "↕", "⟲", "⟳"
    ]

    # Tier 3: Matrix-style symbols
    tier3_symbols = [
        # Braille patterns (the classic Matrix look)
        "⠀", "⠁", "⠂", "⠃", "⠄", "⠅", "⠆", "⠇",
        "⣀", "⣁", "⣂", "⣃", "⣄", "⣅", "⣆", "⣇",
        "⣿", "⣾", "⣽", "⣼", "⣻", "⣺", "⣹", "⣸",
        "⣷", "⣶", "⣵", "⣴", "⣳", "⣲", "⣱", "⣰",
        "⣯", "⣮", "⣭", "⣬", "⣫", "⣪", "⣩", "⣨",
        "⣟", "⣞", "⣝", "⣜", "⣛", "⣚", "⣙", "⣘",
        "⡿", "⡾", "⡽", "⡼", "⡻", "⡺", "⡹", "⡸",
        # Block elements
        "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█",
        "▉", "▊", "▋", "▌", "▍", "▎", "▏",
        "▐", "░", "▒", "▓", "▔", "▕",
        # Geometric shapes
        "◆", "◇", "◈", "◉", "◊", "○", "◌", "◍", "◎", "●",
        "◐", "◑", "◒", "◓", "◔", "◕", "◖", "◗",
        "⬟", "⬢", "⬡", "⬠", "⬣", "⬤", "⬥", "⬦",
        # Stars and sparkles
        "✦", "✧", "✩", "✪", "✫", "✬", "✭", "✮",
        "✯", "✰", "✱", "✲", "✳", "✴", "✵", "✶",
        "✷", "✸", "✹", "✺", "✻", "✼", "✽", "✾", "✿",
        "❀", "❁", "❂", "❃", "❄", "❅", "❆", "❇", "❈",
        # Technical/sci-fi symbols
        "≡", "≣", "≢", "≡", "≠", "≤", "≥", "≈", "≅",
        "⊗", "⊙", "⊚", "⊛", "⊜", "⊝", "⊞", "⊟",
        "⊠", "⊡", "⊢", "⊣", "⊤", "⊥", "⊦", "⊧",
        "⟇", "⟑", "⟒", "⟓", "⟔", "⟕", "⟖", "⟗",
        # Arrows (more variety)
        "↖", "↗", "↘", "↙", "↚", "↛", "↜", "↝",
        "⇐", "⇓", "⇑", "⇒", "⇔", "⇕", "⇖", "⇗",
        "⇘", "⇙", "⇚", "⇛", "⇜", "⇝"
    ]

    # Tier 4: Extended Unicode ranges
    tier4_symbols = []
    # More block elements
    for code in range(0x2580, 0x259F):
        tier4_symbols.append(chr(code))
    # More geometric shapes
    for code in range(0x25A0, 0x25FF):
        tier4_symbols.append(chr(code))
    # Mathematical operators
    for code in range(0x2200, 0x2230):
        tier4_symbols.append(chr(code))
    # Miscellaneous symbols
    for code in range(0x2600, 0x2670):
        tier4_symbols.append(chr(code))

    # Tier 5: Even more exotic (if terminal is really good)
    tier5_symbols = [
        # Currency and misc
        "₿", "€", "£", "¥", "₹", "₽", "₩", "₪",
        # Zodiac
        "♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏",
        "♐", "♑", "♒", "♓",
        # Chess pieces
        "♔", "♕", "♖", "♗", "♘", "♙", "♚", "♛",
        "♜", "♝", "♞", "♟",
        # Weather
        "☀", "☁", "☂", "☃", "☄", "★", "☆", "☇",
        "☈", "☉", "☊", "☋", "☌", "☍", "☎", "☔"
    ]

    # Start with Tier 1 (always works)
    working_symbols = tier1_safe[:]

    # Test and add each tier
    for symbol in tier2_symbols:
        if test_symbol_safely(stdscr, symbol):
            working_symbols.append(symbol)

    for symbol in tier3_symbols:
        if test_symbol_safely(stdscr, symbol):
            working_symbols.append(symbol)

    # Test Tier 4 in smaller batches for performance
    if len(working_symbols) > 50:  # Only if we have good base
        for symbol in tier4_symbols[::2]:  # Test every other symbol
            if test_symbol_safely(stdscr, symbol):
                working_symbols.append(symbol)

    # Test Tier 5 if terminal is really capable
    if len(working_symbols) > 100:  # Only for very capable terminals
        for symbol in tier5_symbols:
            if test_symbol_safely(stdscr, symbol):
                working_symbols.append(symbol)

    return working_symbols


def countdown_matrix(stdscr, target):
    curses.curs_set(0)

    # Initialize colors safely
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        color_pair = curses.color_pair(1) | curses.A_BOLD
    else:
        color_pair = curses.A_BOLD

    # Initialize matrix state
    height, width = stdscr.getmaxyx()
    cols = list(range(0, max(2, width - 1), 2))  # Stay within bounds
    drops = [random.randint(-height, height) for _ in cols]


def test_and_measure_chars(stdscr):
    """Test spinner and cursor chars, return working versions with measured widths"""

    # Test hourglass spinner
    hourglass_frames = ["⏳", "⌛"]
    safe_frames = []
    frame_width = 1

    for frame in hourglass_frames:
        if test_symbol_safely(stdscr, frame):
            # Measure actual display width
            measured_width = safe_wcswidth(frame)
            if measured_width and measured_width > 0:
                safe_frames.append(frame)
                frame_width = max(frame_width, measured_width)

    # Fallback if hourglass doesn't work
    if not safe_frames:
        safe_frames = ["*", "+"]
        frame_width = 1

    # Test block cursor
    block_cursor = "█"
    cursor_width = 1
    if test_symbol_safely(stdscr, block_cursor):
        cursor_width = safe_wcswidth(block_cursor) or 1
    else:
        block_cursor = "#"
        cursor_width = 1

    return safe_frames, frame_width, block_cursor, cursor_width


class Particle:
    """Represents a single spark/glitch particle"""

    def __init__(self, x, y, symbol, lifetime, dx=0, dy=0, color_variant=0):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.dx = dx  # movement in x direction
        self.dy = dy  # movement in y direction
        self.color_variant = color_variant

    def update(self):
        """Update particle position and lifetime"""
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        return self.lifetime > 0

    def get_alpha(self):
        """Get alpha value based on remaining lifetime (0.0 to 1.0)"""
        return self.lifetime / self.max_lifetime if self.max_lifetime > 0 else 0


def countdown_matrix(stdscr, target, theme):
    curses.curs_set(0)

    # Initialize colors based on selected theme
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, theme.primary, theme.background)  # Main countdown
        curses.init_pair(2, theme.secondary, theme.background)  # Matrix rain
        curses.init_pair(3, theme.accent1, theme.background)  # Spark color 1
        curses.init_pair(4, theme.accent2, theme.background)  # Spark color 2
        curses.init_pair(5, theme.urgent, theme.background)  # Urgent/glitch color
        curses.init_pair(6, theme.accent1, theme.background)  # Extra accent

        color_pair = curses.color_pair(1) | curses.A_BOLD  # Main countdown
        matrix_color = curses.color_pair(2) | curses.A_BOLD  # Matrix rain
        spark_colors = [
            curses.color_pair(3) | curses.A_BOLD,  # Accent 1
            curses.color_pair(4) | curses.A_BOLD,  # Accent 2
            curses.color_pair(5) | curses.A_BOLD,  # Urgent
            curses.color_pair(6) | curses.A_BOLD,  # Extra accent
        ]
    else:
        color_pair = curses.A_BOLD
        matrix_color = curses.A_BOLD
        spark_colors = [curses.A_BOLD, curses.A_REVERSE, curses.A_UNDERLINE]

    # Test and measure characters once at startup
    spinner_frames, frame_width, block_cursor, cursor_width = test_and_measure_chars(stdscr)

    # Get safe symbols by actually testing them in the current terminal
    symbols = get_safe_symbols(stdscr)
    if not symbols:  # Ultimate fallback
        symbols = ["|", ":", ".", "*", "#", "+", "-", "="]

    # Particle-specific symbols (sparks and glitches)
    spark_symbols = ["*", ".", "·", "°", "˚", "•", "◦", "○", "◯"]
    glitch_symbols = ["#", "@", "&", "%", "?", "!", "~", "^", "¿", "¡"]

    # Test which particle symbols work
    working_sparks = [s for s in spark_symbols if test_symbol_safely(stdscr, s)]
    working_glitches = [s for s in glitch_symbols if test_symbol_safely(stdscr, s)]

    if not working_sparks:
        working_sparks = ["*", ".", "+"]
    if not working_glitches:
        working_glitches = ["#", "@", "?"]

    # Initialize matrix state with denser rain
    height, width = stdscr.getmaxyx()
    cols = list(range(0, max(2, width - 1), 1))  # Changed from step 2 to step 1 for more columns
    drops = [random.randint(-height, height) for _ in cols]

    # Initialize particle system
    particles = []
    last_particle_spawn = time.time()

    si = 0
    cursor_visible = True
    last_toggle = time.time()
    last_resize_check = time.time()

    while True:
        current_time = time.time()

        # Check for terminal resize every 0.5 seconds
        if current_time - last_resize_check >= 0.5:
            try:
                new_height, new_width = stdscr.getmaxyx()
                if new_height != height or new_width != width:
                    height, width = new_height, new_width
                    cols = list(range(0, max(2, width - 1), 1))  # Denser columns
                    drops = [random.randint(-height, height) for _ in cols]
            except curses.error:
                pass
            last_resize_check = current_time

        now = datetime.now()
        remaining = target - now

        if remaining.total_seconds() <= 0:
            try:
                stdscr.erase()
                msg = "✓ TIME'S UP! ✓"
                msg_width = safe_wcswidth(msg)
                x = max(0, min(width - msg_width, (width - msg_width) // 2))
                y = max(0, min(height - 1, height // 2))
                stdscr.addstr(y, x, msg, color_pair)
                stdscr.refresh()
            except (curses.error, UnicodeEncodeError):
                # Fallback without checkmarks
                try:
                    msg = "TIME'S UP!"
                    msg_width = safe_wcswidth(msg)
                    x = max(0, min(width - msg_width, (width - msg_width) // 2))
                    y = max(0, min(height - 1, height // 2))
                    stdscr.addstr(y, x, msg, color_pair)
                    stdscr.refresh()
                except curses.error:
                    pass
            time.sleep(3)
            break

        # Compute time safely
        total_sec = max(0, int(remaining.total_seconds()))
        h = total_sec // 3600
        m = (total_sec % 3600) // 60
        s = total_sec % 60

        # Toggle blinking cursor
        if current_time - last_toggle >= 0.5:
            cursor_visible = not cursor_visible
            last_toggle = current_time

        # Get frame and cursor
        frame = spinner_frames[si % len(spinner_frames)]
        cursor = block_cursor if cursor_visible else " "
        si += 1

        # Build timer by DRAWING EACH PART SEPARATELY (no string concatenation)
        time_part = f"{h:02d}:{m:02d}:{s:02d}"

        # Calculate positions for each component
        time_width = 8  # "01:39:54" is always 8 chars
        total_display_width = frame_width + 1 + time_width + 1 + cursor_width

        # Center the whole thing
        start_x = max(0, (width - total_display_width) // 2)

        # Calculate each component position
        frame_x = start_x
        time_x = frame_x + frame_width + 1  # frame + space
        cursor_x = time_x + time_width + 1  # time + space

        # Ensure countdown fits on screen
        clock_y = max(0, min(height - 1, height // 2))

        # Define safe area around countdown (use actual positions)
        if total_display_width <= width - 4:
            pad_y = 1
            pad_x = 3
            safe_top = max(0, clock_y - pad_y)
            safe_bottom = min(height - 1, clock_y + pad_y)
            safe_left = max(0, start_x - pad_x)
            safe_right = min(width - 1, cursor_x + cursor_width + pad_x)
            display_timer = True

            # Spawn particles around the countdown
            current_time = time.time()
            if current_time - last_particle_spawn >= 0.1:  # Spawn every 100ms
                # Calculate intensity based on remaining time
                total_minutes = remaining.total_seconds() / 60
                if total_minutes <= 60:  # More intense in last hour
                    intensity = max(1, int(6 - (total_minutes / 10)))  # 1-6 particles
                elif total_minutes <= 300:  # Moderate in last 5 hours
                    intensity = max(1, int(3 - (total_minutes / 100)))  # 1-3 particles
                else:
                    intensity = 1  # Minimal particles for longer countdowns

                # Determine particle type based on urgency
                if total_minutes <= 5:  # Last 5 minutes - urgent glitches
                    particle_type = "urgent_glitch"
                elif total_minutes <= 30:  # Last 30 minutes - mixed
                    particle_type = random.choice(["spark", "glitch"])
                else:  # Normal sparks
                    particle_type = "spark"

                # Spawn particles around countdown area
                for _ in range(intensity):
                    # Random position around countdown (not directly on it)
                    if random.choice([True, False]):  # Spawn on sides
                        px = random.choice([
                            random.randint(max(0, safe_left - 5), safe_left),  # Left side
                            random.randint(safe_right, min(width - 1, safe_right + 5))  # Right side
                        ])
                        py = random.randint(safe_top, safe_bottom)
                    else:  # Spawn above/below
                        px = random.randint(safe_left, safe_right)
                        py = random.choice([
                            random.randint(max(0, safe_top - 3), safe_top),  # Above
                            random.randint(safe_bottom, min(height - 1, safe_bottom + 3))  # Below
                        ])

                    # Choose symbol and properties based on particle type
                    if particle_type == "urgent_glitch":
                        symbol = random.choice(working_glitches)
                        lifetime = random.randint(8, 20)  # Longer lasting
                        dx = random.choice([-1, 0, 1]) * 0.3
                        dy = random.choice([-1, 0, 1]) * 0.3
                        color_idx = random.choice([1, 2])  # Red/yellow for urgency
                    elif particle_type == "glitch":
                        symbol = random.choice(working_glitches)
                        lifetime = random.randint(5, 15)
                        dx = random.choice([-1, 0, 1]) * 0.2
                        dy = random.choice([-1, 0, 1]) * 0.2
                        color_idx = random.randint(0, len(spark_colors) - 1)
                    else:  # spark
                        symbol = random.choice(working_sparks)
                        lifetime = random.randint(3, 12)
                        dx = random.uniform(-0.5, 0.5)
                        dy = random.uniform(-0.5, 0.5)
                        color_idx = random.randint(0, len(spark_colors) - 1)

                    # Ensure particle starts in bounds
                    if 0 <= px < width - 1 and 0 <= py < height:
                        particles.append(Particle(px, py, symbol, lifetime, dx, dy, color_idx))

                last_particle_spawn = current_time
        else:
            # Timer too wide, don't display it and don't create safe area
            safe_top = safe_bottom = safe_left = safe_right = -1
            display_timer = False

        try:
            stdscr.erase()
        except curses.error:
            pass

        # Update and render particles
        active_particles = []
        for particle in particles:
            if particle.update():  # Returns True if particle is still alive
                # Calculate display position
                display_x = int(particle.x)
                display_y = int(particle.y)

                # Only render if in bounds and not overlapping countdown
                if (0 <= display_x < width - 1 and 0 <= display_y < height and
                        not (safe_left <= display_x <= safe_right and safe_top <= display_y <= safe_bottom)):

                    try:
                        # Choose color based on particle's color variant and alpha
                        alpha = particle.get_alpha()
                        if alpha > 0.7:  # Bright particles
                            color = spark_colors[particle.color_variant % len(spark_colors)]
                        elif alpha > 0.3:  # Medium particles
                            color = spark_colors[particle.color_variant % len(spark_colors)]
                        else:  # Fading particles
                            color = matrix_color  # Use theme's matrix color for fading

                        stdscr.addstr(display_y, display_x, particle.symbol, color)
                    except (curses.error, UnicodeEncodeError):
                        pass  # Skip particles that can't be drawn

                active_particles.append(particle)

        particles = active_particles  # Keep only active particles

        # Draw matrix rain with comprehensive fallback handling
        for i, col in enumerate(cols):
            if i >= len(drops):
                continue

            drop_y = drops[i]
            row = drop_y % height

            # Skip countdown safe area and check bounds
            if (not (safe_left <= col <= safe_right and safe_top <= row <= safe_bottom) and
                    0 <= row < height and 0 <= col < width - 2):  # Extra margin for wide chars

                # Try to use a random symbol with fallback chain
                for attempt in range(3):  # Try up to 3 different symbols
                    try:
                        ch = random.choice(symbols)
                        ch_width = safe_wcswidth(ch)
                        if ch_width is not None and col + ch_width <= width:
                            stdscr.addstr(row, col, ch, matrix_color)  # Use theme's matrix color
                            break  # Success, exit fallback loop
                    except (curses.error, UnicodeEncodeError):
                        if attempt == 2:  # Last attempt, use basic fallback
                            try:
                                stdscr.addstr(row, col, "|", matrix_color)  # Use theme's matrix color
                            except curses.error:
                                pass

            drops[i] = drop_y + 1
            # Make drops restart more frequently for denser effect
            if drops[i] > height + random.randint(0, height // 4):  # Changed from height//2 to height//4
                drops[i] = random.randint(-height // 4, 0)  # Shorter gaps between drops

        # Draw the countdown by placing each component separately
        if display_timer:
            try:
                # Clear the entire area first
                clear_width = cursor_x + cursor_width - frame_x
                if frame_x + clear_width <= width:
                    clear_text = " " * clear_width
                    stdscr.addstr(clock_y, frame_x, clear_text)

                # Draw each component at its exact position
                if frame_x + frame_width <= width:
                    stdscr.addstr(clock_y, frame_x, frame, color_pair)

                if time_x + time_width <= width:
                    stdscr.addstr(clock_y, time_x, time_part, color_pair)

                if cursor_x + cursor_width <= width:
                    stdscr.addstr(clock_y, cursor_x, cursor, color_pair)

            except (curses.error, UnicodeEncodeError):
                # Fallback to basic ASCII countdown
                try:
                    fallback_text = f"TIME: {h:02d}:{m:02d}:{s:02d}"
                    fallback_w = len(fallback_text)
                    fallback_x = max(0, min(width - fallback_w, (width - fallback_w) // 2))
                    if 0 <= clock_y < height and fallback_x + fallback_w <= width:
                        stdscr.addstr(clock_y, fallback_x, fallback_text, color_pair)
                except curses.error:
                    pass

        try:
            stdscr.refresh()
        except curses.error:
            pass

        time.sleep(0.05)


class ColorTheme:
    """Color theme configuration"""

    def __init__(self, name, primary, secondary, accent1, accent2, urgent, scanline=None,
                 background=curses.COLOR_BLACK):
        self.name = name
        self.primary = primary  # Main countdown color
        self.secondary = secondary  # Matrix rain color
        self.accent1 = accent1  # Spark color 1
        self.accent2 = accent2  # Spark color 2
        self.urgent = urgent  # Urgent/glitch color
        self.scanline = scanline or primary  # Scanline color (defaults to primary)
        self.background = background


def get_color_themes():
    """Define available color themes"""
    themes = {
        'matrix': ColorTheme('Matrix Green', curses.COLOR_GREEN, curses.COLOR_GREEN,
                             curses.COLOR_YELLOW, curses.COLOR_WHITE, curses.COLOR_RED,
                             scanline=curses.COLOR_GREEN),
        'retro': ColorTheme('Retro Amber', curses.COLOR_YELLOW, curses.COLOR_YELLOW,
                            curses.COLOR_RED, curses.COLOR_WHITE, curses.COLOR_RED,
                            scanline=curses.COLOR_YELLOW),
        'scifi': ColorTheme('Sci-Fi Blue', curses.COLOR_CYAN, curses.COLOR_BLUE,
                            curses.COLOR_WHITE, curses.COLOR_MAGENTA, curses.COLOR_RED,
                            scanline=curses.COLOR_CYAN),
        'urgent': ColorTheme('Urgent Red', curses.COLOR_RED, curses.COLOR_RED,
                             curses.COLOR_YELLOW, curses.COLOR_WHITE, curses.COLOR_RED,
                             scanline=curses.COLOR_RED),
        'cyberpunk': ColorTheme('Cyberpunk Purple', curses.COLOR_MAGENTA, curses.COLOR_CYAN,
                                curses.COLOR_YELLOW, curses.COLOR_RED, curses.COLOR_RED,
                                scanline=curses.COLOR_MAGENTA),
        'terminal': ColorTheme('Classic Terminal', curses.COLOR_WHITE, curses.COLOR_GREEN,
                               curses.COLOR_CYAN, curses.COLOR_YELLOW, curses.COLOR_RED,
                               scanline=curses.COLOR_WHITE)
    }
    return themes


def parse_args():
    """Parse command line arguments for time and optional theme"""
    if len(sys.argv) < 2:
        script_name = sys.argv[0]
        print(f"Usage: python {script_name} HH:MM [theme]")
        print(f"Example: python {script_name} 22:00")
        print(f"Example: python {script_name} 22:00 retro")
        print("\nAvailable themes:")
        themes = get_color_themes()
        for theme_name, theme in themes.items():
            print(f"  {theme_name} - {theme.name}")
        sys.exit(1)

    time_str = sys.argv[1]
    theme_name = sys.argv[2] if len(sys.argv) > 2 else 'matrix'

    # Parse time
    try:
        hour, minute = map(int, time_str.split(':'))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Invalid time format")

        now = datetime.now()
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target <= now:
            target += timedelta(days=1)

    except (ValueError, IndexError):
        print("Error: Please provide time in HH:MM format (24-hour)")
        print("Example: python retro_countdown.py 22:00")
        sys.exit(1)

    # Validate theme
    themes = get_color_themes()
    if theme_name not in themes:
        print(f"Error: Unknown theme '{theme_name}'")
        print("Available themes:", ", ".join(themes.keys()))
        sys.exit(1)

    return target, themes[theme_name]


def main():
    try:
        # Parse command line arguments
        target, theme = parse_args()

        print(f"Countdown target: {target.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Theme: {theme.name}")
        print("Press Ctrl+C to exit")
        time.sleep(2)  # Give user time to read

        curses.wrapper(countdown_matrix, target, theme)

    except KeyboardInterrupt:
        print("\nCountdown interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have the required packages installed:")
        print("  pip install wcwidth")
        print("  pip install windows-curses  # On Windows only")


if __name__ == "__main__":
    main()
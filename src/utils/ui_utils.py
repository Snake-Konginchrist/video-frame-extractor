import platform
import os

def get_os_specific_icon_path() -> str | None:
    """
    Determines the correct application icon path based on the operating system.

    Returns:
        str | None: The path to the icon file, or None if not found.
    """
    system = platform.system()
    if system == "Windows":
        icon_path = "assets/app.ico"
    elif system == "Darwin":  # macOS
        icon_path = "assets/app.icns"
    else:  # Linux and others
        icon_path = "assets/app.png"

    if os.path.exists(icon_path):
        return icon_path
    
    print(f"Warning: Icon not found at '{icon_path}'")
    return None

# theme.py

LIGHT = {
    "bg": "#f0f2f5",
    "card": "#ffffff",
    "text": "#2d2d2d",
    "muted": "#999999",
    "entry_bg": "#ffffff",
    "border": "#c0c0c0",
    "red": "#e05c5c",
    "blue": "#4a90d9",
}

DARK = {
    "bg": "#1e1e2e",
    "card": "#2a2a3d",
    "text": "#e0e0e0",
    "muted": "#888888",
    "entry_bg": "#2f2f45",
    "border": "#444466",
    "red": "#e05c5c",
    "blue": "#4a90d9",
}

current_theme = LIGHT

def is_dark():
    return current_theme == DARK

def get_theme():
    return current_theme

def toggle_theme():
    global current_theme
    current_theme = DARK if current_theme == LIGHT else LIGHT


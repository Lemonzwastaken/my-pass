import threading
import pystray
from PIL import Image
import os

def resource_path(relative_path):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


def setup_tray(window):
    icon_holder = [None]

    def restore_window(icon, item):
        icon.stop()
        icon_holder[0] = None
        window.deiconify()

    def quit_app(icon, item):
        icon.stop()
        window.destroy()

    def create_tray_icon():
        image = Image.open(resource_path("mypass_logo.png"))
        menu = pystray.Menu(
            pystray.MenuItem("Open", restore_window),
            pystray.MenuItem("Exit", quit_app)
        )

        icon = pystray.Icon("MyPass", image, "Mypass", menu)
        icon_holder[0] = icon
        icon.run()

    def minimize_to_tray():
        window.withdraw()
        threading.Thread(target=create_tray_icon, daemon=True).start()

    window.protocol("WM_DELETE_WINDOW", minimize_to_tray)

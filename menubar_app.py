import os
import sys
import rumps

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class FusionMenuApp(rumps.App):
    def __init__(self):
        # template=True tells macOS to render this stencil at full solid opacity
        super().__init__(
            "FusionGesture",
            icon=resource_path("icon.png"),
            template=True,
            quit_button=None
        )
        self.is_active = False  # Starts in the Off state
        self.is_running = True
        
        self.toggle_item = rumps.MenuItem("On", callback=self.toggle_active)
        
        self.menu = [
            self.toggle_item,
            None,
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]

    @rumps.clicked
    def on_icon_click(self, sender):
        """Direct click on the menu bar icon toggles state."""
        self.toggle_active(sender)

    def toggle_active(self, sender):
        self.is_active = not self.is_active
        if self.is_active:
            self.toggle_item.title = "Off"
        else:
            self.toggle_item.title = "On"

    def update_mode(self, mode):
        pass

    def quit_app(self, sender):
        self.is_running = False
        rumps.quit_application()
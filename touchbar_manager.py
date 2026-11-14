import objc
import AppKit

class TouchBarController(AppKit.NSResponder, AppKit.NSTouchBarDelegate):
    def init(self):
        self = objc.super(TouchBarController, self).init()
        if self is None:
            return None
        
        self.is_active = True
        self.current_mode = "NEUTRAL"
        self._setup_window()
        return self

    def _setup_window(self):
        # Ensure the Python script is recognized as an active foreground app
        AppKit.NSApplication.sharedApplication()
        AppKit.NSApp.activateIgnoringOtherApps_(True)

        # Create a small, subtle utility window to anchor the Touch Bar
        rect = AppKit.NSMakeRect(100, 100, 300, 100)
        self.window = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            rect,
            AppKit.NSWindowStyleMaskTitled | AppKit.NSWindowStyleMaskClosable,
            AppKit.NSBackingStoreBuffered,
            False
        )
        self.window.setTitle_("Fusion 360 Gesture Controller")
        self.window.setTouchBar_(self.makeTouchBar())
        
        # Bring the window to the front and make it key so the Touch Bar appears
        self.window.makeKeyAndOrderFront_(None)

    def makeTouchBar(self):
        touchBar = AppKit.NSTouchBar.alloc().init()
        touchBar.setDelegate_(self)
        touchBar.setDefaultItemIdentifiers_([
            "com.fusiongesture.status",
            "com.fusiongesture.mode"
        ])
        return touchBar

    def touchBar_makeItemForIdentifier_(self, touchBar, identifier):
        if identifier == "com.fusiongesture.status":
            item = AppKit.NSTouchBarItem.alloc().initWithIdentifier_(identifier)
            self.status_button = AppKit.NSButton.buttonWithTitle_target_action_(
                "Status: Active", self, "toggleActive:"
            )
            item.setView_(self.status_button)
            return item
            
        elif identifier == "com.fusiongesture.mode":
            item = AppKit.NSTouchBarItem.alloc().initWithIdentifier_(identifier)
            self.mode_button = AppKit.NSButton.buttonWithTitle_target_action_(
                "Mode: NEUTRAL", None, None
            )
            self.mode_button.setEnabled_(False)
            item.setView_(self.mode_button)
            return item
            
        return None

    def update_mode(self, mode):
        """Dynamically updates the Touch Bar mode button text."""
        self.current_mode = mode
        if hasattr(self, 'mode_button'):
            AppKit.dispatch_async_f(AppKit.dispatch_get_main_queue(), None, lambda x: self.mode_button.setTitle_(f"Mode: {mode}"))

    def toggleActive_(self, sender):
        """Toggles tracking active/paused when tapped on the Touch Bar."""
        self.is_active = not self.is_active
        title = "Status: Active" if self.is_active else "Status: Paused"
        self.status_button.setTitle_(title)
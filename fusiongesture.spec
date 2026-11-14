# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# Collect MediaPipe and OpenCV hidden imports and data files
mediapipe_imports = collect_submodules('mediapipe')
mediapipe_data = collect_data_files('mediapipe')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.png', '.')] + mediapipe_data,
    hiddenimports=['pynput.mouse._cocoa', 'rumps', 'AppKit', 'objc'] + mediapipe_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FusionGesture',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Hides the terminal window completely
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FusionGesture',
)

app = BUNDLE(
    coll,
    name='FusionGesture.app',
    icon=None,  # You can add a custom .icns file path here later if you want
    bundle_identifier='com.bilalqadri.fusiongesture',
    info_plist={
        'NSCameraUsageDescription': 'This app uses your webcam to track hand gestures for Fusion 360 navigation.',
        'NSHighResolutionCapable': 'True',
        'LSUIElement': 'True',  # Ensures it runs purely as an accessory/menu bar app with no Dock icon
    },
)
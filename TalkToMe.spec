# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/assets/AppIcon.png', 'assets'),
        ('src/assets/AppIcon.png', '.')  # Also copy to root for rumps
    ],
    hiddenimports=[
        'pyaudio',
        'whisper',
        'pynput.keyboard',
        'pynput.mouse',
        'rumps',
        'PIL',
        'PIL.Image',
        'PIL._tkinter',
        'PIL._imaging',
        'tkinter',
        'pkg_resources.py2_warn',
        'pkg_resources.markers',
        'pkg_resources._vendor.packaging.version',
        'pkg_resources._vendor.packaging.requirements',
        'pkg_resources._vendor.packaging.markers',
        'pkg_resources._vendor.packaging.specifiers'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    collect_submodules=['pynput', 'PIL']  # Ensure all submodules are collected
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TalkToMe',
    debug=True,  # Enable debug mode for better error reporting
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Enable console for debugging
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/assets/AppIcon.png'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TalkToMe'
)

app = BUNDLE(
    coll,
    name='TalkToMe.app',
    icon='src/assets/AppIcon.png',
    bundle_identifier='com.bmaddick.talktome',
    info_plist={
        'LSUIElement': True,  # Makes it a menu bar app
        'NSMicrophoneUsageDescription': 'TalkToMe needs microphone access to convert your speech to text.',
        'NSAppleEventsUsageDescription': 'TalkToMe needs accessibility access to type text into applications.',
        'CFBundleShortVersionString': '1.0.0',
        'LSBackgroundOnly': False,  # Ensure app is not background-only
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'NSSupportsAutomaticGraphicsSwitching': True,
        'CFBundleDisplayName': 'TalkToMe',  # Ensure proper display name
        'CFBundleName': 'TalkToMe',  # Ensure proper bundle name
    }
)

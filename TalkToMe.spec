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
    hiddenimports=['pyaudio', 'whisper', 'pynput', 'rumps'],
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
    name='TalkToMe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
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
    }
)

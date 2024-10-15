# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['dropper.py'],
    pathex=[],
    binaries=[],
    datas=[('encrypted_message.jpg', '.'), ('encryption_utils.py', '.'), ('file_handling.py', '.'), ('main.py', '.'), ('public_key.pem', '.'), ('requirements.txt', '.'), ('encrypted_aes_key.bin', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='dropper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)

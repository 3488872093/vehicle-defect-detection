# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[r'E:\桌面\YOLOSHOW'],
    binaries=[],
    datas=[(r'E:\桌面\YOLOSHOW\assest','assest'),
           (r'E:\桌面\YOLOSHOW\config','config'),
           (r'E:\桌面\YOLOSHOW\database','database'),
           (r'E:\桌面\YOLOSHOW\fonts','fonts'),
           (r'E:\桌面\YOLOSHOW\images','images'),
           (r'E:\桌面\YOLOSHOW\login','login'),
           (r'E:\桌面\YOLOSHOW\models','models'),
           (r'E:\桌面\YOLOSHOW\ptfiles','ptfiles'),
           (r'E:\桌面\YOLOSHOW\runs','runs'),
           (r'E:\桌面\YOLOSHOW\ui','ui'),
           (r'E:\桌面\YOLOSHOW\utils','utils'),
           (r'E:\桌面\YOLOSHOW\yolocode','yolocode'),
           (r'E:\桌面\YOLOSHOW\yoloshow','yoloshow')
           ],
    hiddenimports=['PyYAML','scipy','tqdm','protobuf','tensorboard','ipython','psutil','thop','albumentations','pycocotools','ultralytics','colorlog','Pyside6','PySide6-Fluent-Widgets[full]','together','torch','torchvision','torchaudio'],
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
    [],
    exclude_binaries=True,
    name='钢面智检',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[r'E:\桌面\YOLOSHOW\images\logo-1.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='钢面智检',
)

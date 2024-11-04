# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Go.py','Util.py','asse\\__init__.py','asse\\Btn.py','asse\\Product.py','core_func\\__init__.py','core_func\\config.py','core_func\\env_manager.py','core_func\\file_loader.py','core_func\\log_manager.py','core_func\\runner.py','entity\\__init__.py','entity\\ProductItem.py'],
    pathex=['A:\\PROJECTS\\PyCharm_Projects\\AutoDeployer'],
    binaries=[],
    datas=[('.\\static\\Icon','.\\static\\Icon'),('.\\config.yaml','.'),('.\\used.log','.')],
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
    name='AutoDeployer',
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
    icon='A:\\PROJECTS\\PyCharm_Projects\\AutoDeployer\\static\\Icon\\autodeployerLogo.ico'
)

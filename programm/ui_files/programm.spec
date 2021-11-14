# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Main\\programm.py'],
             pathex=['Main/classes.py', 'Main/CreateOlympWindwow.py', 'Main/FavoritesOlymps.py', 'Main/LoginWindwow.py', 'Main/Main_indwow.py', 'Main/ViewOlympWindow.py'],
             binaries=[],
             datas=[],
             hiddenimports=['pymysql.cursors', 'datetime', 'sys', 'pyqt5', 'webbrowser'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='programm',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='programm')

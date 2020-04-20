# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Quetzal_1_HEX.py'],
             pathex=['C:\\Users\\My User\\Documents\\Trabajos UVG\\CubeSat\\Quetzal-1 GUI\\Quetzal-1 (Hex GUI - PyQT5) V2'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
          name='Quetzal_1_HEX',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Quetzal_1_HEX')

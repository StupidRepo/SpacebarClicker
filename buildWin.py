import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--add-data=assets;.',
    '--add-data=version.txt;.',
    '--name=SpacebarClicker',
    '--noconfirm',
    '--windowed'
])
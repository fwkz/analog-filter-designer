from distutils.core import setup
import py2exe
import matplotlib
import matplotlib.backends.backend_tkagg

datafiles = matplotlib.get_py2exe_datafiles()
print datafiles
print type(datafiles)

files = [
            ('img', ['img\\cap.jpg', 'img\\coil.jpg', 'img\\init.jpg', 'img\\out.jpg'])
        ]

for element in datafiles:
    files.append(element)

setup(
    name="Analog Filter Designer",
    version='1.0',
    description="Analog Filter Designer",
    author="Mariusz Kupidura",
    console=['gui.py'],
    data_files=files,
    options={
        "py2exe":{
                "skip_archive": False,
                "unbuffered": True,
                "optimize": 2,
                "includes": ["matplotlib.backends.backend_tkagg"]
        }
}
)
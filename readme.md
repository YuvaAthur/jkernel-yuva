![](http://i.imgur.com/wL5ZTfu.png)

To install: place the files in ~/.ipython/kernels/jkernel* directory. Make sure that the paths to J at the top of wrapper.py and jkernel.py are correct. For those unfamiliar with Python, the file path on Windows needs backslashes escaped; for example: `"C:\\Program Files\\j64-804\\bin"`. Open `jupyter notebook` (or `ipython notebook`, but it's deprecated) from this directory.

(* or the newer location: `~/.local/share/jupyter/kernels/jkernel` on Linux, `%APPDATA%\jupyter\kernels\jkernel` on Windows, `~/Library/Jupyter/kernels/jkernel` on OSX.)

Requires IPython 3.0+, possibly 4.0+.

(in theory jkernel.py should be placed in Python's `dist-packages` directory to be accessible from everywhere, but that's not important at this stage)

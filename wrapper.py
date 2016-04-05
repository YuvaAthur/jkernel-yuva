from __future__ import print_function

from ctypes import *

import sys
import os

# CUSTOMIZE HERE
# J binary directory (the one with all the binaries)
j_bin_path = os.path.expanduser("~/j64-804/bin")

def get_libj(binpath):
    if os.name == "nt":
        lib_path = binpath + "/j.dll" # Windows
    elif sys.platform == "darwin":
        lib_path = binpath + "/libj.dylib" # OSX
    else:
        lib_path = binpath + "/libj.so" # Linux
    libj = cdll.LoadLibrary(lib_path)

    libj.JInit.restype = c_void_p
    libj.JSM.argtypes = [c_void_p, c_void_p]
    libj.JDo.argtypes = [c_void_p, c_char_p]
    libj.JDo.restype = c_int
    libj.JFree.restype = c_int
    libj.JFree.argtypes = [c_void_p]

    return libj

class JWrapper:
    def __init__(self):

        binpath = j_bin_path

        self.libj = get_libj(binpath)
        self.j = self.libj.JInit()

        # buffer for multiline input,
        # for normal line input and J explicit definitions.
        self.input_buffer = []

        OUTPUT_CALLBACK = CFUNCTYPE(None, c_void_p, c_int, c_char_p)
        INPUT_CALLBACK = CFUNCTYPE(c_char_p, c_void_p, c_char_p)

        def output_callback(j, output_type, result):
            output_types = [None, "output", "error", "output log", "assert", "EXIT", "1!:2[2 (wat)"]
            self.output_type = output_types[output_type]
            self.output = result.decode('utf-8', 'replace')

        def input_callback(j, prompt):
            if not self.input_buffer:
                return b")"
            line = self.input_buffer.pop(0)
            return line.encode()

        callbacks_t = c_void_p*5
        callbacks = callbacks_t(
            cast(OUTPUT_CALLBACK(output_callback), c_void_p),
            0,
            cast(INPUT_CALLBACK(input_callback), c_void_p),
            0,
            c_void_p(3) # defines "console" frontend (for some reason, see jconsole.c, line 128)
        )
        self.libj.JSM(self.j, callbacks)

        self.sendline("ARGV_z_=:''")
        self.sendline("BINPATH_z_=:'{}'".format(binpath))
        self.sendline("1!:44'{}'".format(binpath))
        self.sendline("0!:0 <'profile.ijs'")
        self.sendline("(9!:7) 16 17 18 19 20 21 22 23 24 25 26 { a.") # pretty boxes

    def close(self):
        self.libj.JFree(self.j)

    def sendline(self, line):
        self.output = None
        self.libj.JDo(self.j, c_char_p(line.encode()))
        if not self.output:
            return ""
        return self.output

    def sendlines(self, lines):
        self.input_buffer = lines
        output = ""
        while self.input_buffer:
            line = self.input_buffer.pop(0)
            output += self.sendline(line)
        return output

if __name__ == "__main__":
    j = JWrapper()
    j.sendline("load 'viewmat'")
    j.sendline("load 'bmp'")
    j.sendline("VISIBLE_jviewmat_ =: 0")
    #j.sendline("viewmat i. 5 5")
    j.close()

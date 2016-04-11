# -*- coding: utf-8 -*-
"""
    jkernel
    ~~~~~~~

    Author:      Martin Saurer, 19.02.2016
    Description: Jupyter / J - integration.

    License:     GPL Version 3 (see gpl3.txt)
    Extended by: Yuvaraj 11.04.2016
"""
# Imports
import os
import sys
import time
import base64

# Import Jupyter Kernel
from ipykernel.kernelbase import Kernel

# Append this files path to sys.path
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.getcwd())

# Import qjide as a module
import qjide


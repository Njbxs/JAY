#
# Copyright (C) 2023 by stereoproject
# All rights reserved.

from glob import glob
from os.path import basename, dirname, isfile

from sub import *
from sub.config import *
from sub.modules import *


def all_modules():
    mod_paths = glob(f"{dirname(__file__)}/*.py")
    return sorted(
        [
            basename(f)[:-3]
            for f in mod_paths
            if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
        ]
    )


ALL_MODULES = sorted(all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]

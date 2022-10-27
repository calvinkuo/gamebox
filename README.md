# gamebox
 Rewrite of the gamebox library used at UVA

This repository contains:
* [gamebox.py](gamebox.py)
* Backwards-compatible versions of gamebox, rewritten to use type annotations and managed attributes.
  These are drop-in replacements for the version of `gamebox.py` used through the Summer 2022 semester.
  * [gamebox_compat.py](gamebox_compat.py) (compatible with Python 3.10)
  * [gamebox_compat_37.py](gamebox_compat_37.py) (compatible with Python 3.7 - 3.10)
* [gamebox_legacy.py](gamebox_legacy.py), the legacy version of gamebox used through the Summer 2022 semester
  (compatible with both Python 2 and Python 3)
* [sample.py](sample.py), an example project using gamebox
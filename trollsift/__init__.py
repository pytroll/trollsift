
from .parser import *

try:
    from trollsift.version import version as __version__  # noqa
except ModuleNotFoundError:  # pragma: no cover
    raise ModuleNotFoundError(
        "No module named trollsift.version. This could mean "
        "you didn't install 'trollsift' properly. Try reinstalling ('pip "
        "install').")

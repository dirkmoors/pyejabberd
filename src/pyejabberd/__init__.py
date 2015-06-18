__version__ = "0.2.3"

try:  # pragma: no cover
    # https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    pass

from .client import EjabberdAPIClient

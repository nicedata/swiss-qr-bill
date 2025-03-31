from swiss_qr_bill import __version__
from importlib.metadata import version


def test_version():
    assert __version__ == version("swiss-qr-bill")

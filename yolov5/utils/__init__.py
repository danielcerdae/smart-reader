# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
utils/initialization
"""

import contextlib
import platform
import threading


<<<<<<< HEAD
def emojis(str=""):
    # Return platform-dependent emoji-safe version of string
    return (
        str.encode().decode("ascii", "ignore")
        if platform.system() == "Windows"
        else str
    )
=======
def emojis(str=''):
    # Return platform-dependent emoji-safe version of string
    return str.encode().decode('ascii', 'ignore') if platform.system() == 'Windows' else str
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1


class TryExcept(contextlib.ContextDecorator):
    # YOLOv5 TryExcept class. Usage: @TryExcept() decorator or 'with TryExcept():' context manager
<<<<<<< HEAD
    def __init__(self, msg=""):
=======
    def __init__(self, msg=''):
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1
        self.msg = msg

    def __enter__(self):
        pass

    def __exit__(self, exc_type, value, traceback):
        if value:
<<<<<<< HEAD
            print(emojis(f"{self.msg}{value}"))
=======
            print(emojis(f'{self.msg}{value}'))
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1
        return True


def threaded(func):
    # Multi-threads a target function and returns thread. Usage: @threaded decorator
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper


def notebook_init(verbose=True):
    # Check system software and hardware
<<<<<<< HEAD
    print("Checking setup...")
=======
    print('Checking setup...')
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1

    import os
    import shutil

    from utils.general import check_font, check_requirements, is_colab
    from utils.torch_utils import select_device  # imports

<<<<<<< HEAD
    check_requirements(("psutil", "IPython"))
=======
    check_requirements(('psutil', 'IPython'))
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1
    check_font()

    import psutil
    from IPython import display  # to display images and clear console output

    if is_colab():
<<<<<<< HEAD
        shutil.rmtree(
            "/content/sample_data", ignore_errors=True
        )  # remove colab /sample_data directory
=======
        shutil.rmtree('/content/sample_data', ignore_errors=True)  # remove colab /sample_data directory
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1

    # System info
    if verbose:
        gb = 1 << 30  # bytes to GiB (1024 ** 3)
        ram = psutil.virtual_memory().total
        total, used, free = shutil.disk_usage("/")
        display.clear_output()
<<<<<<< HEAD
        s = f"({os.cpu_count()} CPUs, {ram / gb:.1f} GB RAM, {(total - free) / gb:.1f}/{total / gb:.1f} GB disk)"
    else:
        s = ""

    select_device(newline=False)
    print(emojis(f"Setup complete ✅ {s}"))
=======
        s = f'({os.cpu_count()} CPUs, {ram / gb:.1f} GB RAM, {(total - free) / gb:.1f}/{total / gb:.1f} GB disk)'
    else:
        s = ''

    select_device(newline=False)
    print(emojis(f'Setup complete ✅ {s}'))
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1
    return display

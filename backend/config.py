from __future__ import annotations

import os
import sys
from pathlib import Path


APP_NAME = "NCRE C语言计算机等级考试模拟系统"
APP_VERSION = "0.3.0"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resource_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return PROJECT_ROOT


def frontend_dir() -> Path:
    return resource_root() / "frontend"


def bundled_data_dir() -> Path:
    return resource_root() / "data"


def runtime_root() -> Path:
    custom_home = os.getenv("NCRE_APP_HOME")
    if custom_home:
        root = Path(custom_home)
    elif os.name == "nt":
        appdata = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
        root = appdata / "NCREPractice"
    else:
        root = Path.home() / ".ncre-practice"
    root.mkdir(parents=True, exist_ok=True)
    return root


def database_path() -> Path:
    return runtime_root() / "ncre_practice.db"

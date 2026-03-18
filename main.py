from __future__ import annotations

import argparse
import signal
import sys
import time

from backend.app import ApplicationContext, open_desktop, start_server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NCRE C语言计算机等级考试模拟系统")
    parser.add_argument("--browser", action="store_true", help="始终使用默认浏览器打开界面。")
    parser.add_argument("--serve", action="store_true", help="仅启动本地服务，不主动打开界面。")
    parser.add_argument("--host", default="127.0.0.1", help="服务监听地址，默认 127.0.0.1。")
    parser.add_argument("--port", type=int, default=0, help="服务监听端口，默认 0 表示自动分配。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    context = ApplicationContext()
    server, thread, address = start_server(context, host=args.host, port=args.port)
    print(f"NCRE practice app running at {address}")

    def shutdown(*_: object) -> None:
        server.shutdown()
        server.server_close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, shutdown)

    if not args.serve:
        open_desktop(address, use_webview=not args.browser)

    try:
        while thread.is_alive():
            time.sleep(0.5)
    finally:
        server.shutdown()
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

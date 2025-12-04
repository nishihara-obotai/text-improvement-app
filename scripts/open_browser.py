#!/usr/bin/env python3
"""
ブラウザを開くスクリプト

Usage:
    python scripts/open_browser.py [URL]

デフォルトURL: http://127.0.0.1:8000/

Examples:
    # デフォルトURL（http://127.0.0.1:8000/）で開く（既存ウィンドウを再利用）
    python scripts/open_browser.py

    # カスタムURLで開く
    python scripts/open_browser.py http://localhost:8080/

    # 管理画面を開く
    python scripts/open_browser.py http://127.0.0.1:8000/admin/
"""

import sys
import webbrowser
import time

# デフォルトURL
DEFAULT_URL = "http://127.0.0.1:8000/"

# 開発サーバー起動待機時間（秒）
WAIT_TIME = 2


def open_browser(url: str, wait: bool = True, reuse_window: bool = True) -> None:
    """
    指定されたURLをデフォルトブラウザで開く

    Args:
        url: 開くURL
        wait: Trueの場合、サーバー起動を待ってから開く
        reuse_window: Trueの場合、既存のウィンドウを再利用（デフォルト）
    """
    if wait:
        print(f"開発サーバーの起動を待っています... ({WAIT_TIME}秒)")
        time.sleep(WAIT_TIME)

    print(f"ブラウザでURLを開いています: {url}")

    try:
        # new=0: 可能であれば同じウィンドウで開く
        # new=1: 新しいウィンドウで開く
        # new=2: 新しいタブで開く
        new_window = 1 if not reuse_window else 0

        # デフォルトブラウザでURLを開く
        webbrowser.open(url, new=new_window)

        if reuse_window:
            print("✓ ブラウザで開きました（既存ウィンドウを再利用）")
        else:
            print("✓ ブラウザで新しいウィンドウを開きました")
    except Exception as e:
        print(f"✗ エラー: ブラウザを開けませんでした: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """メイン処理"""
    # コマンドライン引数からURLを取得
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

    # URLの検証（簡易的）
    if not url.startswith(("http://", "https://")):
        print(f"✗ エラー: 無効なURL: {url}", file=sys.stderr)
        print("URLは http:// または https:// で始まる必要があります", file=sys.stderr)
        sys.exit(1)

    # ブラウザを開く
    open_browser(url)


if __name__ == "__main__":
    main()

"""Upload finished Xbox Game Bar clips to PikPak through rclone."""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
LOG_PATH = ROOT / "uploader.log"


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        example = ROOT / "config.example.json"
        raise FileNotFoundError(
            f"{CONFIG_PATH.name}이 없습니다. {example.name}을 복사해 config.json을 만든 뒤 설정하세요."
        )

    with CONFIG_PATH.open(encoding="utf-8") as file:
        config = json.load(file)

    required = ("capture_folder", "rclone_remote", "remote_folder")
    missing = [key for key in required if not config.get(key)]
    if missing:
        raise ValueError(f"config.json의 설정이 비어 있습니다: {', '.join(missing)}")
    return config


def find_rclone(config: dict[str, Any]) -> str:
    configured_path = config.get("rclone_path")
    if configured_path:
        path = Path(configured_path)
        if path.is_file():
            return str(path)
        raise FileNotFoundError(f"rclone_path를 찾지 못했습니다: {path}")

    path_on_path = shutil.which("rclone") or shutil.which("rclone.exe")
    if path_on_path:
        return path_on_path

    downloads = Path.home() / "Downloads"
    candidates = list(downloads.rglob("rclone.exe")) if downloads.exists() else []
    if candidates:
        return str(candidates[0])

    raise FileNotFoundError("rclone.exe를 찾지 못했습니다. config.json의 rclone_path를 직접 지정하세요.")


def upload_once(config: dict[str, Any]) -> None:
    source = Path(config["capture_folder"])
    if not source.is_dir():
        raise FileNotFoundError(f"캡처 폴더를 찾지 못했습니다: {source}")

    rclone = find_rclone(config)
    remote = f"{config['rclone_remote']}:{config['remote_folder'].strip('/')}"
    min_age = int(config.get("min_file_age_seconds", 60))
    extensions = config.get("extensions", [".mp4"])

    command = [
        rclone,
        "move",
        str(source),
        remote,
        "--min-age",
        f"{min_age}s",
        "--transfers",
        "1",
        "--checkers",
        "2",
        "--retries",
        "3",
        "--low-level-retries",
        "10",
    ]
    for extension in extensions:
        command.extend(["--include", f"*{extension.lower()}"])

    logging.info("업로드 검사 시작: %s -> %s", source, remote)
    result = subprocess.run(
    command,
    text=True,
    capture_output=True,
    check=False,
    creationflags=subprocess.CREATE_NO_WINDOW,
)
    if result.stdout.strip():
        logging.info("rclone: %s", result.stdout.strip())
    if result.stderr.strip():
        logging.info("rclone: %s", result.stderr.strip())
    if result.returncode != 0:
        raise RuntimeError(f"rclone 실행 실패 (종료 코드 {result.returncode})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Game Bar 클립을 PikPak으로 자동 이동합니다.")
    parser.add_argument("--once", action="store_true", help="한 번만 검사하고 종료합니다.")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler(LOG_PATH, encoding="utf-8"), logging.StreamHandler()],
    )

    try:
        config = load_config()
        interval = max(15, int(config.get("scan_interval_seconds", 60)))
        while True:
            try:
                upload_once(config)
            except Exception:
                logging.exception("업로드 검사 실패")
            if args.once:
                break
            time.sleep(interval)
    except Exception as error:
        logging.error("시작 실패: %s", error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

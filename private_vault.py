#!/usr/bin/env python3
"""Encrypt and decrypt lab-private skill resources.

This script creates an encrypted tar.gz archive with a SHA-256 manifest. It is
intended for lab databases, case indexes, revision packages, and test outputs
that should stay private at rest.
"""

from __future__ import annotations

import argparse
import datetime as dt
import getpass
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path


MANIFEST_NAME = ".revision_private_manifest.json"
EXCLUDED_DIRS = {"__pycache__", ".git", ".svn", ".hg"}
EXCLUDED_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
OPENSSL_ARGS = [
    "openssl",
    "enc",
    "-aes-256-cbc",
    "-pbkdf2",
    "-iter",
    "200000",
    "-md",
    "sha256",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_passphrase(confirm: bool) -> str:
    existing = os.environ.get("REVISION_VAULT_PASS")
    if existing:
        return existing
    first = getpass.getpass("Vault passphrase: ")
    if confirm:
        second = getpass.getpass("Confirm passphrase: ")
        if first != second:
            raise SystemExit("Passphrases do not match.")
    if not first:
        raise SystemExit("Empty passphrase is not allowed.")
    return first


def should_include(path: Path, source: Path, include_hidden: bool) -> bool:
    try:
        relative = path.relative_to(source if source.is_dir() else source.parent)
    except ValueError:
        relative = Path(path.name)
    parts = relative.parts
    if any(part in EXCLUDED_DIRS for part in parts):
        return False
    if path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES:
        return False
    if path.is_symlink():
        return False
    if not include_hidden and any(part.startswith(".") for part in parts):
        return False
    return path.is_file()


def collect_files(source: Path, include_hidden: bool) -> list[Path]:
    if source.is_file():
        return [source] if should_include(source, source, include_hidden) else []
    files = [
        path
        for path in source.rglob("*")
        if should_include(path, source, include_hidden)
    ]
    return sorted(files)


def build_tarball(source: Path, tar_path: Path, include_hidden: bool) -> dict:
    source = source.expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Source does not exist: {source}")

    files = collect_files(source, include_hidden)
    root_name = source.name if source.is_dir() else f"{source.stem}_vault"
    manifest = {
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_name": source.name,
        "source_type": "directory" if source.is_dir() else "file",
        "file_count": len(files),
        "files": [],
    }

    with tempfile.TemporaryDirectory(prefix="revision-vault-manifest-") as tmp:
        manifest_path = Path(tmp) / MANIFEST_NAME
        for path in files:
            rel = path.relative_to(source) if source.is_dir() else Path(path.name)
            manifest["files"].append(
                {
                    "path": str(rel),
                    "size": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )

        with tarfile.open(tar_path, "w:gz") as tar:
            for path in files:
                rel = path.relative_to(source) if source.is_dir() else Path(path.name)
                tar.add(path, arcname=str(Path(root_name) / rel), recursive=False)
            tar.add(manifest_path, arcname=str(Path(root_name) / MANIFEST_NAME))

    return manifest


def run_openssl(encrypt: bool, input_path: Path, output_path: Path, passphrase: str) -> None:
    if shutil.which("openssl") is None:
        raise SystemExit("OpenSSL is required but was not found on PATH.")
    command = [*OPENSSL_ARGS, "-salt" if encrypt else "-d"]
    command.extend(["-in", str(input_path), "-out", str(output_path), "-pass", "env:REVISION_VAULT_PASS"])
    env = os.environ.copy()
    env["REVISION_VAULT_PASS"] = passphrase
    subprocess.run(command, check=True, env=env)


def ensure_writable_output(path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise SystemExit(f"Output already exists: {path}. Use --overwrite to replace it.")
    path.parent.mkdir(parents=True, exist_ok=True)


def encrypt_folder(args: argparse.Namespace) -> None:
    source = Path(args.source).expanduser()
    archive = Path(args.archive).expanduser()
    ensure_writable_output(archive, args.overwrite)
    passphrase = read_passphrase(confirm=True)

    with tempfile.TemporaryDirectory(prefix="revision-vault-encrypt-") as tmp:
        tar_path = Path(tmp) / "payload.tar.gz"
        manifest = build_tarball(source, tar_path, args.include_hidden)
        run_openssl(True, tar_path, archive, passphrase)

    print(json.dumps({
        "status": "encrypted",
        "archive": str(archive.resolve()),
        "file_count": manifest["file_count"],
    }, ensure_ascii=False, indent=2, sort_keys=True))


def safe_extract(tar_path: Path, out_dir: Path, overwrite: bool) -> None:
    out_dir = out_dir.expanduser().resolve()
    if out_dir.exists() and any(out_dir.iterdir()) and not overwrite:
        raise SystemExit(f"Output directory is not empty: {out_dir}. Use --overwrite to extract anyway.")
    out_dir.mkdir(parents=True, exist_ok=True)
    base = str(out_dir)
    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getmembers()
        for member in members:
            if member.issym() or member.islnk():
                raise SystemExit(f"Archive contains a link, refusing to extract: {member.name}")
            target = (out_dir / member.name).resolve()
            if not (str(target) == base or str(target).startswith(base + os.sep)):
                raise SystemExit(f"Unsafe archive path: {member.name}")
        try:
            tar.extractall(out_dir, members=members, filter="data")
        except TypeError:
            tar.extractall(out_dir, members=members)


def decrypt_archive(args: argparse.Namespace) -> None:
    archive = Path(args.archive).expanduser().resolve()
    if not archive.exists():
        raise SystemExit(f"Archive does not exist: {archive}")
    out_dir = Path(args.out).expanduser()
    passphrase = read_passphrase(confirm=False)

    with tempfile.TemporaryDirectory(prefix="revision-vault-decrypt-") as tmp:
        tar_path = Path(tmp) / "payload.tar.gz"
        run_openssl(False, archive, tar_path, passphrase)
        safe_extract(tar_path, out_dir, args.overwrite)

    print(json.dumps({
        "status": "decrypted",
        "archive": str(archive),
        "out": str(out_dir.resolve()),
    }, ensure_ascii=False, indent=2, sort_keys=True))


def find_manifest(root: Path) -> Path:
    matches = list(root.rglob(MANIFEST_NAME))
    if not matches:
        raise SystemExit("No manifest found inside decrypted archive.")
    return matches[0]


def inspect_archive(args: argparse.Namespace) -> None:
    archive = Path(args.archive).expanduser().resolve()
    if not archive.exists():
        raise SystemExit(f"Archive does not exist: {archive}")
    passphrase = read_passphrase(confirm=False)

    with tempfile.TemporaryDirectory(prefix="revision-vault-inspect-") as tmp:
        tmp_dir = Path(tmp)
        tar_path = tmp_dir / "payload.tar.gz"
        run_openssl(False, archive, tar_path, passphrase)
        safe_extract(tar_path, tmp_dir / "extract", overwrite=True)
        manifest = json.loads(find_manifest(tmp_dir / "extract").read_text(encoding="utf-8"))

    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Encrypt/decrypt lab-private revision skill resources.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    enc = subparsers.add_parser("encrypt", help="Encrypt a private file or directory into a .tar.gz.enc archive.")
    enc.add_argument("--source", required=True, help="Private file or directory to archive.")
    enc.add_argument("--archive", required=True, help="Encrypted archive path to create.")
    enc.add_argument("--include-hidden", action="store_true", help="Include hidden files. Defaults to false.")
    enc.add_argument("--overwrite", action="store_true", help="Replace an existing archive.")
    enc.set_defaults(func=encrypt_folder)

    dec = subparsers.add_parser("decrypt", help="Decrypt an archive into a local runtime directory.")
    dec.add_argument("--archive", required=True, help="Encrypted archive path.")
    dec.add_argument("--out", required=True, help="Directory where decrypted files should be extracted.")
    dec.add_argument("--overwrite", action="store_true", help="Extract into a non-empty output directory.")
    dec.set_defaults(func=decrypt_archive)

    ins = subparsers.add_parser("inspect", help="Decrypt temporarily and print the archive manifest.")
    ins.add_argument("--archive", required=True, help="Encrypted archive path.")
    ins.set_defaults(func=inspect_archive)
    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except subprocess.CalledProcessError as exc:
        print(f"OpenSSL failed with exit code {exc.returncode}. Check the passphrase and archive.", file=sys.stderr)
        return exc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

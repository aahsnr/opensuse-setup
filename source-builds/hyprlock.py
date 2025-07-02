#!/usr/bin/env python3

"""
Hyprlock Build Script for openSUSE Tumbleweed

A Python-based build utility to compile and install Hyprlock, featuring
enhanced dependency detection for a smoother experience on openSUSE.
"""

import argparse
import datetime
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# --- Configuration ---
PKGNAME = "hyprlock"
PKGVER = "0.8.2"
URL = "https://github.com/hyprwm/hyprlock"
LICENSE = "BSD-3-Clause"


# --- Colors for output ---
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"


# --- Logging Functions ---
def log_info(message):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")


def log_success(message):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")


def log_warning(message):
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")


def log_error(message):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")


# --- Command Execution Helper ---
def run_command(command, check=True, capture_output=False, text=True, env=None):
    """Runs a shell command with robust error handling and logging."""
    log_info(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(
            command, check=check, capture_output=capture_output, text=text, env=env
        )
        return result
    except FileNotFoundError:
        log_error(f"Command not found: {command[0]}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        log_error(f"Command failed with exit code {e.returncode}: {' '.join(command)}")
        if e.stdout:
            print("--- STDOUT ---\n" + e.stdout)
        if e.stderr:
            print("--- STDERR ---\n" + e.stderr)
        if check:
            sys.exit(1)
        return e


# --- Pre-flight Checks ---
def check_requirements():
    """Checks for essential commands and sudo privileges."""
    log_info("Verifying system requirements...")
    required_commands = ["zypper", "git", "cmake", "sudo", "pkg-config"]
    for cmd in required_commands:
        if not shutil.which(cmd):
            log_error(f"Required command '{cmd}' not found.")
            if cmd == "pkg-config":
                log_info("Install with: sudo zypper install pkg-config")
            sys.exit(1)

    log_info("Checking sudo permissions...")
    if run_command(["sudo", "-v"], check=False).returncode != 0:
        log_error("This script requires sudo privileges for package installation.")
        sys.exit(1)
    log_success("System requirements and sudo access verified.")


# --- Dependency Management ---
def find_package_for_pkgconfig(pkgconfig_name):
    """
    Finds the corresponding openSUSE package name for a pkg-config module.
    Handles direct mappings and falls back to querying zypper.
    """
    pkg_map = {
        "wayland-client": "wayland-devel",
        "wayland-server": "wayland-devel",
        "wayland-cursor": "wayland-devel",
        "wayland-egl": "wayland-devel",
        "wayland-protocols": "wayland-protocols-devel",
        "xkbcommon": "libxkbcommon-devel",
        "xkbcommon-x11": "libxkbcommon-x11-devel",
        "cairo": "cairo-devel",
        "cairo-ft": "cairo-devel",
        "pango": "pango-devel",
        "pangocairo": "pango-devel",
        "glib-2.0": "glib2-devel",
        "gio-2.0": "glib2-devel",
        "gobject-2.0": "glib2-devel",
        "libdrm": "libdrm-devel",
        "gbm": "libgbm-devel",
        "egl": "Mesa-libEGL-devel",
        "gl": "Mesa-libGL-devel",
        "opengl": "Mesa-libGL-devel",
        "glesv2": "Mesa-libGLESv2-devel",
        "libjpeg": "libjpeg8-devel",
        "libwebp": "libwebp-devel",
        "libmagic": "file-devel",
        "hyprlang": "hyprlang-devel",
        "hyprutils": "hyprutils-devel",
        "fontconfig": "fontconfig-devel",
        "freetype2": "freetype2-devel",
        "libpng16": "libpng16-devel",
        "pixman-1": "libpixman-1-0-devel",
        "harfbuzz": "harfbuzz-devel",
        "fribidi": "fribidi-devel",
    }
    if pkgconfig_name in pkg_map:
        return pkg_map.get(pkgconfig_name)

    # Fallback to querying zypper, with improved parsing
    pc_file = f"{pkgconfig_name}.pc"
    result = run_command(
        ["zypper", "what-provides", f"*/{pc_file}"], check=False, capture_output=True
    )
    if result.returncode == 0 and result.stdout:
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line or line.startswith(
                ("---", "Load", "Read", "S | Name", "Repository")
            ):
                continue
            # Handle table format: "i | Mesa-libEGL-devel | ..."
            if "|" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) > 1 and parts[1]:
                    return parts[1]
            # Handle colon format: "Mesa-libEGL-devel : EGL files"
            elif ":" in line:
                parts = [p.strip() for p in line.split(":")]
                if parts[0]:
                    return parts[0]
    return f"lib{pkgconfig_name}-devel"  # Generic fallback


def check_pkgconfig_available(pkgconfig_name):
    """Checks if a pkg-config module is available on the system."""
    return (
        run_command(["pkg-config", "--exists", pkgconfig_name], check=False).returncode
        == 0
    )


def get_pkgconfig_dependencies(srcdir):
    """Gets dependencies from a predefined list and by parsing CMakeLists.txt."""
    deps = {
        "wayland-client",
        "wayland-protocols",
        "wayland-cursor",
        "wayland-egl",
        "xkbcommon",
        "cairo",
        "pango",
        "glib-2.0",
        "libdrm",
        "gbm",
        "egl",
        "gl",
        "glesv2",
        "libjpeg",
        "libwebp",
        "libmagic",
        "fontconfig",
        "freetype2",
        "libpng16",
        "pixman-1",
        "harfbuzz",
        "hyprlang",
        "hyprutils",
    }
    cmake_file = srcdir / PKGNAME / "CMakeLists.txt"
    if cmake_file.is_file():
        log_info("Parsing CMakeLists.txt for additional dependencies...")
        content = cmake_file.read_text()
        # Find packages from pkg_check_modules(PACKAGE_PREFIX REQUIRED package1 package2)
        found = re.findall(
            r"pkg_check_modules\(.*?REQUIRED\s+(.*?)\)", content, re.IGNORECASE
        )
        for item in found:
            for pkg in item.split():
                # **FIX**: Safer cleanup that doesn't corrupt names like 'glib-2.0'
                cleaned_pkg = pkg.strip().rstrip(")")
                if cleaned_pkg:
                    deps.add(cleaned_pkg)
    return sorted(list(deps))


def install_dependencies(srcdir):
    """Refreshes repositories and installs all required build dependencies."""
    log_info("Installing build dependencies...")
    run_command(["sudo", "zypper", "refresh"])

    core_deps = [
        "cmake",
        "ninja",
        "gcc-c++",
        "git",
        "pkg-config",
        "meson",
        "pam-devel",
        "Mesa-devel",
        "Mesa-libGL-devel",
        "Mesa-libEGL-devel",
        "Mesa-libGLESv2-devel",
        "Mesa-libgbm-devel",
        "libdrm-devel",
        "wayland-devel",
        "wayland-protocols-devel",
        "cairo-devel",
        "pango-devel",
        "glib2-devel",
        "libxkbcommon-devel",
        "fontconfig-devel",
        "libjpeg8-devel",
    ]
    log_info("Installing core build tools...")
    run_command(["sudo", "zypper", "install", "-y", *core_deps])

    pkgconfig_deps = get_pkgconfig_dependencies(srcdir)
    log_info(f"Checking {len(pkgconfig_deps)} pkg-config dependencies...")
    packages_to_install = set()
    for dep in pkgconfig_deps:
        if not check_pkgconfig_available(dep):
            package_name = find_package_for_pkgconfig(dep)
            log_info(f"  → Dependency '{dep}' requires package '{package_name}'")
            packages_to_install.add(package_name)

    if packages_to_install:
        log_info(
            f"Installing {len(packages_to_install)} additional development packages..."
        )
        run_command(
            ["sudo", "zypper", "install", "-y", *sorted(list(packages_to_install))],
            check=False,
        )

    log_info("Final dependency verification...")
    if not all(
        check_pkgconfig_available(d) for d in ["wayland-client", "cairo", "egl"]
    ):
        log_warning(
            "Some critical dependencies might still be missing. Build may fail."
        )
    else:
        log_success("Critical dependencies appear to be satisfied.")


# --- Build Steps ---
def download_source(srcdir):
    """Downloads the Hyprlock source code from GitHub."""
    log_info(f"Downloading source for {PKGNAME} v{PKGVER}...")
    os.chdir(srcdir)
    clone_cmd = ["git", "clone", "--depth", "1", "--branch", f"v{PKGVER}", URL, PKGNAME]

    if run_command(clone_cmd, check=False).returncode != 0:
        log_warning(f"Failed to clone tag v{PKGVER}, falling back to main branch...")
        run_command(["git", "clone", "--depth", "1", URL, PKGNAME])

    pkg_src_dir = srcdir / PKGNAME
    os.chdir(pkg_src_dir)

    if (pkg_src_dir / ".gitmodules").is_file():
        log_info("Initializing and updating git submodules...")
        run_command(["git", "submodule", "update", "--init", "--recursive"])

    log_success("Source code downloaded successfully.")


def build_package(builddir, srcdir):
    """Configures and builds the package using CMake and Ninja."""
    log_info(f"Building {PKGNAME}...")
    os.chdir(builddir)

    cmake_args = [
        "cmake",
        "-GNinja",
        f"-DCMAKE_INSTALL_PREFIX=/usr",
        f"-DCMAKE_BUILD_TYPE=Release",
        str(srcdir / PKGNAME),
    ]

    log_info("Configuring build with CMake...")
    if run_command(cmake_args, check=False).returncode != 0:
        log_error("CMake configuration failed. Check logs above for errors.")
        sys.exit(1)

    cpu_count = os.cpu_count() or 1
    log_info(f"Starting compilation with {cpu_count} parallel jobs...")
    run_command(["ninja", "-j", str(cpu_count)])
    log_success("Build completed successfully.")


def stage_install(pkgdir, builddir, srcdir):
    """Installs the built files into a temporary staging directory."""
    log_info("Staging installation to package directory...")
    os.chdir(builddir)

    env = os.environ.copy()
    env["DESTDIR"] = str(pkgdir)
    run_command(["ninja", "install"], env=env)

    license_file = srcdir / PKGNAME / "LICENSE"
    if license_file.is_file():
        license_dest = pkgdir / "usr/share/licenses" / PKGNAME
        license_dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(license_file, license_dest)

    log_success("Package installation staged successfully.")


def install_to_system(pkgdir):
    """Copies files from the staging directory to the live system."""
    log_info("Installing to system...")
    if not any(pkgdir.iterdir()):
        log_error("Staging directory is empty. Cannot install.")
        sys.exit(1)

    log_info("Copying files to system directories using sudo...")
    # Use -rT to copy contents of pkgdir into '/'
    run_command(["sudo", "cp", "-rT", str(pkgdir), "/"])

    log_info("Updating shared library cache...")
    run_command(["sudo", "ldconfig"], check=False)

    if shutil.which("hyprlock"):
        log_success("System installation completed successfully!")
        version_info = run_command(
            ["hyprlock", "--version"], check=False, capture_output=True
        ).stdout.strip()
        log_info(f"Installed Version: {version_info or 'N/A'}")
    else:
        log_warning("Installation finished, but 'hyprlock' not found in PATH.")


# --- Main Logic ---
def main():
    """Parses arguments and orchestrates the build process."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--no-install",
        action="store_true",
        help="Build package but do not install to the system.",
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Do not clean up temporary directories after a successful build.",
    )
    args = parser.parse_args()

    # Set up temporary build environment
    base_dir = Path(tempfile.mkdtemp(prefix=f"{PKGNAME}_build_"))
    srcdir = base_dir / "src"
    builddir = base_dir / "build"
    pkgdir = base_dir / "pkg"

    success = False
    try:
        log_info(f"Temporary build directory: {base_dir}")
        for d in [srcdir, builddir, pkgdir]:
            d.mkdir()

        # --- Execute Build Steps ---
        check_requirements()

        log_info("--- Step 1/4: Downloading Source ---")
        download_source(srcdir)

        log_info("--- Step 2/4: Installing Dependencies ---")
        install_dependencies(srcdir)

        log_info("--- Step 3/4: Compiling Package ---")
        build_package(builddir, srcdir)

        log_info("--- Step 4/4: Staging and Installing ---")
        stage_install(pkgdir, builddir, srcdir)

        if not args.no_install:
            install_to_system(pkgdir)
        else:
            log_info("Skipping system installation as requested.")
            log_success(f"Build complete. Staged files are in: {pkgdir}")

        success = True

    except (Exception, SystemExit) as e:
        # A clean sys.exit(0) should not be treated as a failure
        if isinstance(e, SystemExit) and e.code == 0:
            success = True
        else:
            log_error(f"Build process failed.")
    finally:
        if success and not args.no_cleanup:
            log_info("Cleaning up temporary build directory...")
            shutil.rmtree(base_dir)
            log_success("Cleanup complete.")
        elif not success:
            log_warning(
                f"Build failed. Temporary files preserved for debugging at: {base_dir}"
            )
        elif args.no_cleanup:
            log_info(f"Skipping cleanup as requested. Files are at: {base_dir}")


if __name__ == "__main__":
    main()

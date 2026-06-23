#!/usr/bin/env python3
"""Owl Vision -- Local offline screen understanding via Moondream 2B.

Usage:
  python run.py "Describe this screenshot"
  python run.py --image path.png "Any errors on screen?"
  python run.py --json --dry-run "Check for crash dialogs"
"""

import argparse
import json
import os
import pathlib
import subprocess
import sys

SKILL_DIR = pathlib.Path(__file__).resolve().parent
MODEL_DIR = pathlib.Path("D:/bobo/models")
MODEL_FILE = MODEL_DIR / "moondream-2b-int8.q4_k_m.gguf"
DEFAULT_IMAGE = SKILL_DIR / "latest_screenshot.png"

# -- Standard CLI flags (v0.2.0) -------------------------------------------------


def _handle_std_flags():
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--version":
            print("owl-vision v0.1.0")
            sys.exit(0)
        if arg == "--json":
            return True
        if arg == "--dry-run":
            print(json.dumps({"status": "dry_run", "skill": "owl-vision",
                              "model": str(MODEL_FILE), "model_exists": MODEL_FILE.exists()}))
            sys.exit(0)
    return False


# -- Model loader ----------------------------------------------------------------


def ensure_model():
    """Auto-download Moondream if missing."""
    if MODEL_FILE.exists():
        return True

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    print("[owl-vision] Model not found. Downloading moondream-2b-int8... (this happens once)", file=sys.stderr)

    try:
        from huggingface_hub import hf_hub_download
        hf_hub_download(
            repo_id="vikhyatk/moondream2",
            filename="moondream-2b-int8.mf.gz",
            local_dir=str(MODEL_DIR),
        )
    except ImportError:
        print("[owl-vision] huggingface_hub not available. Please download manually:", file=sys.stderr)
        print("  https://huggingface.co/vikhyatk/moondream2", file=sys.stderr)
        print(f"  Place model at: {MODEL_FILE}", file=sys.stderr)
        return False

    return MODEL_FILE.exists()


def load_model():
    """Lazy-load Moondream model."""
    try:
        import moondream as md
        return md.vl(model=str(MODEL_FILE))
    except ImportError:
        print("[owl-vision] moondream not installed. Installing...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moondream"], stdout=subprocess.DEVNULL)
        import moondream as md
        return md.vl(model=str(MODEL_FILE))


# -- Screenshot capture ----------------------------------------------------------


def capture_screen(output_path):
    """Capture screenshot via Pillow."""
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab()
        img.save(str(output_path))
        return str(output_path)
    except ImportError:
        print("[owl-vision] Pillow not installed. Installing...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"], stdout=subprocess.DEVNULL)
        from PIL import ImageGrab
        img = ImageGrab.grab()
        img.save(str(output_path))
        return str(output_path)


# -- Main ------------------------------------------------------------------------


def main():
    json_mode = _handle_std_flags()

    parser = argparse.ArgumentParser(description="Owl Vision -- local offline screen understanding")
    parser.add_argument("prompt", nargs="?", default="Describe this screenshot in detail.",
                        help="Question to ask about the image")
    parser.add_argument("--image", "-i", default=None,
                        help="Path to image file. If omitted, captures current screen.")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    output_json = json_mode or args.json

    # Determine image
    if args.image:
        img_path = args.image
        if not pathlib.Path(img_path).exists():
            result = {"status": "error", "error": f"Image not found: {img_path}"}
            print(json.dumps(result))
            sys.exit(1)
    else:
        img_path = capture_screen(DEFAULT_IMAGE)

    # Ensure model
    if not ensure_model():
        result = {"status": "error", "error": "Model download failed. See stderr for manual instructions."}
        print(json.dumps(result))
        sys.exit(1)

    # Run inference
    try:
        model = load_model()
        res = model.query(image=str(img_path), question=args.prompt)

        if output_json:
            output = {
                "status": "ok",
                "image": str(img_path),
                "prompt": args.prompt,
                "answer": res.get("answer", str(res)),
            }
            print(json.dumps(output, ensure_ascii=False))
        else:
            print(f"[owl-vision] Image: {img_path}")
            print(f"[owl-vision] Prompt: {args.prompt}")
            print(f"[owl-vision] Answer: {res.get('answer', str(res))}")

    except Exception as e:
        result = {"status": "error", "error": str(e)}
        print(json.dumps(result))
        sys.exit(1)


if __name__ == "__main__":
    main()

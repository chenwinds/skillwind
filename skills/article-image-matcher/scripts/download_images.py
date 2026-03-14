#!/usr/bin/env python3
"""
Download images from URLs to a local directory.
Saves images with descriptive filenames and returns a manifest.
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library not installed. Run: pip install requests")
    sys.exit(1)


def download_image(url, output_dir, filename=None, timeout=30):
    """
    Download an image from URL to local directory.

    Args:
        url: Image URL
        output_dir: Directory to save the image
        filename: Optional filename (auto-generated if not provided)
        timeout: Request timeout in seconds

    Returns:
        dict with 'success', 'local_path', 'url', 'filename' keys
    """
    # Add user-agent header to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()

        # Verify it's an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            return {
                'success': False,
                'error': f'Not an image: {content_type}',
                'url': url
            }

        # Determine file extension
        ext_map = {
            'image/jpeg': '.jpg',
            'image/jpg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/svg+xml': '.svg',
        }
        ext = ext_map.get(content_type, '.jpg')

        # Generate filename if not provided
        if filename:
            # Sanitize filename - remove special characters
            safe_name = "".join(c for c in str(filename) if c.isalnum() or c in ' -_')[:50]
            if not safe_name:
                safe_name = f"img_{hashlib.md5(url.encode()).hexdigest()[:8]}"
        else:
            # Use URL hash for unique filename
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            safe_name = f"img_{url_hash}"

        # Create output directory if needed
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Ensure unique filename
        output_path = output_dir / f"{safe_name}{ext}"
        counter = 1
        while output_path.exists():
            output_path = output_dir / f"{safe_name}_{counter}{ext}"
            counter += 1

        # Save file
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        file_size = output_path.stat().st_size

        return {
            'success': True,
            'local_path': str(output_path),
            'relative_path': str(output_path.relative_to(Path.cwd())) if output_path.is_absolute() else str(output_path),
            'filename': f"{safe_name}{ext}",
            'url': url,
            'file_size': file_size
        }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': str(e),
            'url': url
        }


def download_images(image_list, output_dir="images"):
    """
    Download multiple images.

    Args:
        image_list: List of dicts with 'url' and optional 'alt'/'filename' keys
        output_dir: Directory to save images

    Returns:
        List of download results
    """
    results = []

    for i, img in enumerate(image_list, 1):
        url = img.get('url')
        if not url:
            print(f"Warning: Image {i} has no URL, skipping")
            continue

        # Generate filename from alt text if available
        filename = None
        if img.get('alt'):
            # Sanitize filename
            safe_name = "".join(c for c in img['alt'] if c.isalnum() or c in ' -_')[:50]
            filename = safe_name.replace(' ', '_').lower()

        print(f"Downloading image {i}/{len(image_list)}: {url}")
        result = download_image(url, output_dir, filename)

        if result['success']:
            print(f"  ✓ Saved to: {result['local_path']} ({result['file_size']} bytes)")
        else:
            print(f"  ✗ Failed: {result['error']}")

        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Download images from URLs to local directory"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="images",
        help="Output directory for images (default: images)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Read image list as JSON from stdin"
    )
    parser.add_argument(
        "--urls",
        nargs="+",
        help="Image URLs to download"
    )

    args = parser.parse_args()

    image_list = []

    if args.json:
        import json
        try:
            data = json.load(sys.stdin)
            if isinstance(data, list):
                image_list = data
            elif isinstance(data, dict) and 'images' in data:
                image_list = data['images']
            else:
                print("Error: JSON must be a list or dict with 'images' key")
                sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            sys.exit(1)
    elif args.urls:
        image_list = [{'url': url} for url in args.urls]
    else:
        print("Error: Provide --urls or pipe JSON with --json")
        sys.exit(1)

    if not image_list:
        print("No images to download")
        sys.exit(0)

    print(f"\nWill download {len(image_list)} images to '{args.output_dir}/'\n")

    results = download_images(image_list, args.output_dir)

    # Summary
    success_count = sum(1 for r in results if r.get('success'))
    print(f"\n{'='*50}")
    print(f"Downloaded {success_count}/{len(image_list)} images successfully")

    # Output manifest
    manifest = {
        'output_dir': args.output_dir,
        'total': len(image_list),
        'success': success_count,
        'images': results
    }

    if args.json:
        import json
        print("\nManifest:")
        print(json.dumps(manifest, indent=2))

    return 0 if success_count == len(image_list) else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Search for free stock images from China-accessible sources.
Filters by landscape orientation and returns direct image URLs.
"""

import argparse
import json
import sys
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("Error: requests library not installed. Run: pip install requests")
    sys.exit(1)


# API endpoints (free, no auth required for basic search)
# Note: Pexels works without API key for limited usage, but getting your own key is recommended
# Get Pexels API key: https://www.pexels.com/api/
# Get Pixabay API key: https://pixabay.com/api/docs/
SOURCES = {
    "pexels": {
        "search_url": "https://api.pexels.com/v1/search",
        "api_key_env": "PEXELS_API_KEY",  # Optional, works without for limited usage
        "orientation_param": "orientation",
        "no_key_fallback": True,  # Pexels allows limited requests without key
    },
    "pixabay": {
        "search_url": "https://pixabay.com/api/",
        "api_key_env": "PIXABAY_API_KEY",
        "orientation_param": "image_type",
        "no_key_fallback": False,  # Pixabay requires API key
    },
    "pexels_web": {
        "search_url": "https://www.pexels.com/search/",
        "note": "Web fallback when API not available - requires browser interaction",
        "no_key_fallback": True,
    }
}


def search_pexels(query, orientation="landscape", limit=10, api_key=None):
    """Search Pexels for images."""
    import os
    if not api_key:
        api_key = os.environ.get("PEXELS_API_KEY")

    # Pexels API limit: per_page must be between 1 and 80
    per_page = min(max(int(limit), 1), 80)

    url = f"https://api.pexels.com/v1/search?query={quote(query)}&orientation={orientation}&per_page={per_page}"
    headers = {}
    if api_key:
        headers["Authorization"] = api_key

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "photos" not in data:
            print(f"Warning: Pexels API returned error: {data.get('message', 'Unknown error')}", file=sys.stderr)
            return []

        results = []
        for photo in data.get("photos", []):
            if photo["width"] > photo["height"]:
                results.append({
                    "source": "pexels",
                    "id": photo["id"],
                    "url": photo["src"]["large2x"] or photo["src"]["large"],
                    "thumbnail": photo["src"]["medium"],
                    "width": photo["width"],
                    "height": photo["height"],
                    "photographer": photo.get("photographer", "Unknown"),
                    "alt": photo.get("alt", query)
                })
        return results
    except requests.exceptions.RequestException as e:
        print(f"Warning: Pexels search failed: {e}", file=sys.stderr)
        return []


def search_pixabay(query, orientation="landscape", limit=10, api_key=None):
    """Search Pixabay for images."""
    import os
    if not api_key:
        api_key = os.environ.get("PIXABAY_API_KEY")

    if not api_key:
        print(f"Warning: Pixabay requires API key. Get your free key at https://pixabay.com/api/docs/", file=sys.stderr)
        return []

    # Pixabay API limit: per_page must be between 1 and 100
    per_page = min(max(int(limit), 1), 100)

    # Build URL with proper parameter handling
    base_url = "https://pixabay.com/api/"
    params = {
        "key": api_key,
        "q": query,
        "image_type": "photo",
        "orientation": orientation,
        "per_page": per_page
    }

    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "hits" not in data:
            print(f"Warning: Pixabay API returned error: {data.get('message', 'Unknown error')}", file=sys.stderr)
            return []

        results = []
        for hit in data.get("hits", []):
            if hit["imageWidth"] > hit["imageHeight"]:
                results.append({
                    "source": "pixabay",
                    "id": hit["id"],
                    "url": hit["largeImageURL"] or hit["webformatURL"],
                    "thumbnail": hit["previewURL"],
                    "width": hit["imageWidth"],
                    "height": hit["imageHeight"],
                    "photographer": hit.get("user", "Unknown"),
                    "alt": query
                })
        return results
    except requests.exceptions.RequestException as e:
        print(f"Warning: Pixabay search failed: {e}", file=sys.stderr)
        return []


def search_unsplash_source(query, limit=10):
    """
    Search Unsplash using source URL pattern.
    Note: Unsplash official API requires authentication.
    This uses Unsplash's source URL pattern to generate image URLs.
    """
    results = []
    keywords = [query, f"{query} background", f"{query} landscape"]

    for i, keyword in enumerate(keywords[:min(limit, 3)]):
        # Use Unsplash source URL with landscape dimensions (1200x675 = 16:9)
        source_url = f"https://source.unsplash.com/1200x675/?{quote(keyword)}"
        results.append({
            "source": "unsplash",
            "id": f"unsplash-{i}",
            "url": source_url,
            "thumbnail": f"https://source.unsplash.com/400x225/?{quote(keyword)}",
            "width": 1200,
            "height": 675,
            "photographer": "Various",
            "alt": query,
            "note": "Unsplash source URL - redirects to random matching image"
        })
    return results


def search_images(query, orientation="landscape", limit=10, sources=None):
    """
    Search multiple image sources and return consolidated results.

    Args:
        query: Search keyword (Chinese or English)
        orientation: 'landscape', 'portrait', or 'all'
        limit: Max results per source
        sources: List of sources to search (default: ['pexels', 'pixabay'])

    Returns:
        List of image result dictionaries
    """
    if sources is None:
        sources = ['pexels', 'pixabay']

    all_results = []

    if 'pexels' in sources:
        print(f"Searching Pexels for '{query}'...", file=sys.stderr)
        results = search_pexels(query, orientation, limit)
        all_results.extend(results)
        print(f"  Found {len(results)} landscape images from Pexels", file=sys.stderr)

    if 'pixabay' in sources:
        print(f"Searching Pixabay for '{query}'...", file=sys.stderr)
        results = search_pixabay(query, orientation, limit)
        all_results.extend(results)
        print(f"  Found {len(results)} landscape images from Pixabay", file=sys.stderr)

    if 'unsplash' in sources:
        print(f"Searching Unsplash for '{query}'...", file=sys.stderr)
        results = search_unsplash_source(query, limit)
        all_results.extend(results)
        print(f"  Found {len(results)} images from Unsplash (source URL pattern)", file=sys.stderr)

    # Sort by relevance (could be improved with scoring)
    return all_results


def main():
    parser = argparse.ArgumentParser(
        description="Search free stock images from China-accessible sources",
        epilog="""
API Keys (optional but recommended):
  Pexels:  https://www.pexels.com/api/  (set PEXELS_API_KEY env var)
  Pixabay: https://pixabay.com/api/docs/ (set PIXABAY_API_KEY env var)

Examples:
  python search_images.py -q "人工智能" -o landscape -l 10
  python search_images.py -q "travel" --sources pexels unsplash
        """
    )
    parser.add_argument(
        "--query", "-q",
        required=True,
        help="Search keyword (Chinese or English)"
    )
    parser.add_argument(
        "--orientation", "-o",
        default="landscape",
        choices=["landscape", "portrait", "all"],
        help="Image orientation (default: landscape)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=10,
        help="Max results per source (default: 10)"
    )
    parser.add_argument(
        "--sources", "-s",
        nargs="+",
        default=["pexels", "pixabay"],
        help="Sources to search: pexels, pixabay, unsplash"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    results = search_images(
        query=args.query,
        orientation=args.orientation,
        limit=args.limit,
        sources=args.sources
    )

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        # Human-readable output
        if not results:
            print("No landscape images found.")
        else:
            print(f"\nFound {len(results)} landscape images:\n")
            for i, img in enumerate(results, 1):
                print(f"{i}. [{img['source']}] {img['alt']}")
                print(f"   Size: {img['width']}x{img['height']}")
                print(f"   URL: {img['url']}")
                print(f"   Thumbnail: {img['thumbnail']}")
                print()


if __name__ == "__main__":
    main()

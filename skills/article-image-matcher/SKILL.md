---
name: article-image-matcher
description: How to add matched images to Chinese Markdown articles. Use this skill whenever the user asks to add images to an article, add a cover image, insert illustrations, or match images to content. This includes phrases like "为文章配图", "添加封面", "插入图片", "找配图", "给文章加图", "配几张图", "找个封面", "配图推荐" etc. The skill analyzes article content, searches Chinese-friendly free stock photo sources (Pexels, Pixabay, Unsplash), selects 3-5 landscape-oriented images that match the article theme, and embeds them directly into the Markdown document. IMPORTANT: Always use this skill when processing articles that need visual enhancement - don't just embed random images, ensure they match the content theme and are properly formatted as landscape orientation. Before searching, ensure API keys are configured for best results.
---

# Article Image Matcher

This skill helps you add relevant, high-quality images to Chinese Markdown articles. Follow this workflow carefully.

## Overview

Your task is to:
1. Analyze the article content to understand its theme and key topics
2. Extract search keywords that will help find matching images
3. Search for free, open-source images from China-accessible sources
4. Select 3-5 landscape-oriented images (NOT square or portrait)
5. Embed the images into the Markdown document at appropriate locations

## Step 1: Analyze the Article Content

Before searching for images, you MUST thoroughly analyze the article:

1. **Read the entire article** to understand:
   - Main topic and theme
   - Key sections and their content
   - Emotional tone (technical, inspirational, casual, formal)
   - Target audience

2. **Extract keywords** for image search:
   - Identify 5-10 key terms that represent the article's content
   - Include both concrete objects (e.g., "computer", "office") and abstract concepts (e.g., "teamwork", "innovation")
   - Consider synonyms in both Chinese and English

3. **Determine image placement strategy**:
   - **Cover image**: Should represent the overall theme, placed at the very beginning (after title)
   - **Section images**: Should match specific section content, placed at the start of relevant sections
   - Aim for 3-5 total images including the cover

## Step 2: Search for Images

### API Configuration (IMPORTANT)

Before searching for images, ensure the API keys are properly configured for best results:

**Pexels API** (optional but recommended):
- Get your free API key: https://www.pexels.com/api/
- Set environment variable: `PEXELS_API_KEY=your_key_here`
- Without key: Limited to ~20 requests/hour

**Pixabay API** (required):
- Get your free API key: https://pixabay.com/api/docs/
- Set environment variable: `PIXABAY_API_KEY=your_key_here`
- Without key: API will not work

**Setting API keys on Windows**:
1. Open System Properties → Environment Variables
2. Add new user variable: `PEXELS_API_KEY` and `PIXABAY_API_KEY`
3. Restart your terminal/Claude Code to pick up the changes

Alternatively, create a `.env` file in the project root:
```
PEXELS_API_KEY=your_pexels_key
PIXABAY_API_KEY=your_pixabay_key
```

### Approved Image Sources

Use ONLY these China-accessible, free, open-source image platforms:

1. **Pexels** (https://www.pexels.com) - Best quality, requires API key for high volume
2. **Pixabay** (https://pixabay.com) - Wide selection, requires API key (free)
3. **Unsplash** (https://unsplash.com) - High quality, use source URL pattern

**Important**: Before using any source, verify it's accessible from China. Do NOT use sources that require special network tools to access.

### Search Strategy

1. **Use extracted keywords** - Search with both Chinese and English keywords for better results
2. **Filter by orientation** - ALWAYS filter for "landscape" or "horizontal" orientation
3. **Check image dimensions** - Ensure width > height (ideally 16:9 or similar ratio)
4. **Download multiple candidates** - Get 2-3 options per placement location

### Search Commands

Use the `search_images` script to search across multiple sources:

```bash
python scripts/search_images.py --query "<your-keyword>" --orientation landscape --limit 10
```

Options:
- `--query` / `-q`: Search keyword (Chinese or English)
- `--orientation` / `-o`: landscape, portrait, or all (default: landscape)
- `--limit` / `-l`: Max results per source (default: 10, max: 80 for Pexels, 100 for Pixabay)
- `--sources` / `-s`: Sources to search: pexels, pixabay, unsplash (default: pexels pixabay)
- `--json`: Output results as JSON

Examples:
```bash
# Search with Chinese keyword
python scripts/search_images.py -q "人工智能" -o landscape -l 10

# Search only Pexels
python scripts/search_images.py -q "technology" -s pexels

# Output as JSON for piping to download script
python scripts/search_images.py -q "nature" --json
```

If the script is unavailable, search manually via browser or use `curl` to query APIs directly.

## Step 3: Select and Validate Images

For each candidate image, verify:

1. **Orientation check**: Width must be greater than height (landscape only)
   - Reject square images (width == height)
   - Reject portrait images (height > width)

2. **Relevance check**: Image must clearly relate to the adjacent content
   - Ask: "Does this image help illustrate or enhance this section?"
   - If the connection is weak, keep searching

3. **Quality check**:
   - Resolution should be at least 800px wide
   - Image should be clear, not blurry or heavily compressed
   - Avoid images with visible watermarks

4. **License check**: Confirm the image is truly free/open source (CC0 or similar)

## Step 4: Embed Images in Markdown

### Image Placement

Insert images at these locations:

1. **Cover image**: Immediately after the title/frontmatter
   ```markdown
   # Article Title

   ![Cover: brief description](image-url)

   Article content begins...
   ```

2. **Section images**: At the start of relevant sections (before the first paragraph)
   ```markdown
   ## Section Title

   ![Description of what this image shows](image-url)

   Section content...
   ```

### Image Syntax

Use this format for all image embeddings:

```markdown
![<type>: <brief Chinese description>](<image-url>)
```

Examples:
```markdown
![封面：科技感办公室场景](https://images.pexels.com/photos/xxx.jpeg)
![配图：团队协作讨论场景](https://images.unsplash.com/photo-xxx?w=1200)
```

### Handling Image URLs

**Option A: Hotlinking (default)**
- Use direct image URLs from the source
- Add URL parameters for sizing if supported (e.g., `?w=1200` for Unsplash)

**Option B: Download and embed locally**
- If the user prefers local files, download images to an `images/` folder
- Use relative paths: `![描述](images/photo-001.jpeg)`

Ask the user which approach they prefer if not specified.

## Step 5: Final Review

Before completing:

1. **Count images**: Ensure 3-5 total images (including cover)
2. **Verify all are landscape**: Double-check dimensions
3. **Check relevance**: Each image should clearly match adjacent content
4. **Test URLs**: Verify all image links work
5. **Confirm markdown syntax**: Proper `![alt](url)` format throughout

## Scripts

This skill bundles the following scripts:

### search_images.py
Searches multiple image sources with orientation filtering.

Usage:
```bash
python scripts/search_images.py --query "关键词" --orientation landscape --limit 10
```

Output: Returns JSON or human-readable list of landscape images with URLs, dimensions, and metadata.

### download_images.py
Downloads images from URLs to a local directory.

Usage:
```bash
# Download from URLs
python scripts/download_images.py --urls URL1 URL2 -o images/

# Download from JSON (piped from search_images)
python scripts/search_images.py -q "keyword" --json | python scripts/download_images.py --json -o images/
```

Output: Saves images to specified directory, returns manifest with download results.

## Edge Cases and Notes

- **Technical articles**: Use abstract/conceptual images (diagrams, code on screen, workspace setups)
- **Very short articles**: May need fewer images (adjust 3-5 range accordingly)
- **Sensitive topics**: Avoid images with people's faces for controversial subjects
- **Brand-specific content**: Don't use images with competing brand logos
- **If exact matches aren't available**: Choose conceptually similar images rather than forcing poor matches

## Communication

Always tell the user:
1. What keywords you extracted from their article
2. Which sources you searched
3. How many images you found and where you placed them
4. Whether images are hotlinked or downloaded locally

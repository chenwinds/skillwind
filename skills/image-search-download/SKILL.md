---
name: image-search-download
description: 图片搜索和下载技能。根据用户输入的关键词自动从 Pexels、Pixabay、Unsplash 搜索图片并下载到本地目录。当用户需要找图、下载图片、搜索素材，或说"帮我找几张 XX 的图片"、"下载一些 XX 照片"等类似请求时，都要使用这个技能。技能会自动调用 bundled scripts 完成搜索和下载。
---

# Image Search & Download - 图片搜索和下载技能

这是一个专门用于搜索和下载免费版权图片的技能。

## 什么时候使用这个技能

当用户需要以下操作时，这个技能会被触发：

- 根据关键词搜索图片
- 下载网络图片到本地
- 为项目、演示、文档寻找配图素材
- 批量下载特定主题的图片
- 用户提到"找图"、"下载图片"、"搜索素材"等请求

## 支持的图片源

本技能使用以下中国可访问的免费图片平台：

| 来源 | 是否需要 API 密钥 | 说明 |
|------|------------------|------|
| **Pexels** | 可选（推荐） | 有限使用无需密钥，建议配置 |
| **Pixabay** | 必需 | 必须配置 API 密钥 |
| **Unsplash** | 否 | 使用 source URL 模式 |

### API 密钥配置

**Pexels API**（可选但推荐）：
- 获取密钥：https://www.pexels.com/api/
- 设置环境变量：`PEXELS_API_KEY=your_key_here`
- 无密钥：约 20 次请求/小时

**Pixabay API**（必需）：
- 获取密钥：https://pixabay.com/api/docs/
- 设置环境变量：`PIXABAY_API_KEY=your_key_here`
- 无密钥：无法使用

**Windows 设置方法**：
1. 打开"系统属性" → "环境变量"
2. 添加用户变量：`PEXELS_API_KEY` 和 `PIXABAY_API_KEY`
3. 重启终端或 Claude Code 以生效

或创建 `.env` 文件在项目根目录：
```
PEXELS_API_KEY=your_pexels_key
PIXABAY_API_KEY=your_pixabay_key
```

## 工作流程

### 步骤 1：确认用户需求

在开始搜索前，了解以下信息：

1. **搜索关键词** - 用户想要什么主题的图片（中英文均可）
2. **图片方向** - 横版（landscape）、竖版（portrait）或不限制
3. **数量** - 需要多少张图片（默认 10 张）
4. **保存目录** - 图片保存到哪里（默认 `images/`）

### 步骤 2：调用搜索脚本

使用 bundled 的 `search_images.py` 脚本搜索图片：

```bash
python scripts/search_images.py --query "<关键词>" --orientation <方向> --limit <数量> --json
```

参数说明：
- `--query` / `-q`: 搜索关键词（必填）
- `--orientation` / `-o`: `landscape`（横版）、`portrait`（竖版）、`all`（不限），默认 landscape
- `--limit` / `-l`: 每个来源的最大结果数，默认 10
- `--sources` / `-s`: 指定来源，默认 `pexels pixabay`
- `--json`: 以 JSON 格式输出，便于管道传递给下载脚本

### 步骤 3：调用下载脚本

将搜索结果管道传递给 `download_images.py`：

```bash
python scripts/search_images.py -q "<关键词>" --json | python scripts/download_images.py --json -o <输出目录>
```

或分步执行：
```bash
# 先搜索
python scripts/search_images.py -q "<关键词>" -o landscape -l 10

# 再下载（手动指定 URL）
python scripts/download_images.py --urls URL1 URL2 URL3 -o images/
```

### 步骤 4：报告结果

下载完成后，向用户报告：

1. 搜索的关键词和来源
2. 找到多少张图片
3. 成功下载多少张
4. 保存路径
5. 如果有失败的，说明原因

## Bundled Scripts

本技能包含以下脚本：

### search_images.py

搜索多个图片源并返回结果。

**用法**：
```bash
python scripts/search_images.py --query "关键词" --orientation landscape --limit 10 --json
```

**输出**：JSON 格式的图片列表，包含 URL、尺寸、摄影师等信息。

### download_images.py

从 URL 下载图片到本地目录。

**用法**：
```bash
# 从 JSON 输入（管道）
python scripts/search_images.py -q "keyword" --json | python scripts/download_images.py --json -o images/

# 从 URL 列表
python scripts/download_images.py --urls URL1 URL2 -o images/
```

**输出**：下载的图片保存到指定目录，返回下载清单。

## 使用示例

### 示例 1：搜索并下载科技感图片
```bash
python scripts/search_images.py -q "人工智能" -o landscape -l 10 --json | python scripts/download_images.py --json -o images/ai-tech/
```

### 示例 2：搜索竖版图片用于手机壁纸
```bash
python scripts/search_images.py -q "nature" -o portrait -l 5 --json | python scripts/download_images.py --json -o wallpapers/
```

### 示例 3：从多个来源搜索
```bash
python scripts/search_images.py -q "办公场景" -s pexels pixabay unsplash -l 15 --json | python scripts/download_images.py --json -o office-photos/
```

## 注意事项

1. **API 限制**：
   - Pexels 无密钥约 20 次/小时
   - Pixabay 必须配置密钥
   - 建议错开搜索时间，避免触发速率限制

2. **图片版权**：
   - 所有来源均为免费可商用
   - 建议保留摄影师署名（可选）

3. **网络问题**：
   - 确保网络可以访问这些图片源
   - 如遇连接问题可尝试切换来源

4. **文件名**：
   - 自动使用 alt 文本生成描述性文件名
   - 避免特殊字符和过长文件名

## 输出报告模板

向用户报告时使用以下格式：

```
## 图片搜索结果

**关键词**：<中文/英文关键词>
**搜索来源**：Pexels, Pixabay, Unsplash
**找到图片**：X 张

## 下载结果

**保存目录**：`<path/to/images/>`
**成功下载**：X/Y 张
**失败**：Z 张（说明原因）

## 下载的图片清单

1. `<filename1.jpg>` - <尺寸> - <来源>
2. `<filename2.jpg>` - <尺寸> - <来源>
...
```

# Demo video

## What to put

| Item | Path |
|------|------|
| File name | `assets/demo/policypal-demo.mp4` |
| Format | H.264 + AAC in MP4 (browser-friendly) |
| Length | Prefer **0:00–2:42** (pitch cut) |
| Size | Aim **&lt; 30 MB** (GitHub soft limit ~50 MB; hard 100 MB) |

Source noted in FortuneDiary: `Demo录像-配音字幕-定稿.md`  
(Original Downloads path may no longer exist on this PC.)

## Steps (local → GitHub Pages)

1. Export / trim the demo to MP4.
2. Optional compress (if you have ffmpeg):

   ```bash
   ffmpeg -i "source.mp4" -t 162 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k -movflags +faststart assets/demo/policypal-demo.mp4
   ```

3. Place the file at **`d:\Projects\PandaStudio\assets\demo\policypal-demo.mp4`**.
4. Commit and push `main` — GitHub Pages serves it at:

   - `https://pandastudio.hk/assets/demo/policypal-demo.mp4`
   - Embedded on Home and Products (native `<video controls>`).

5. Hard-refresh the site; click play. No extra hosting required.

If the file is missing, the page keeps the text placeholder (player hides on load error).

## Alternatives (if the file is too large)

- Upload to YouTube / Bilibili and embed an iframe instead of committing the MP4.
- Or host the MP4 on object storage (R2/S3) and point `src` to that URL.

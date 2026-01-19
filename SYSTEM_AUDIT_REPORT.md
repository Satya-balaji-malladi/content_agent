# 📊 SYSTEM AUDIT: SATYA BALAJI
*Hyper-Automated Cinematic Agency | Status: ACTIVE*

---

## 🎨 1. THE 'VIBE' & GENRE
**"Cinematic Noir: The Infinite Loop"**

The system is engineered to produce high-retention, dark, and atmospheric storytelling videos.

*   **Primary Genre**: **Cinematic Noir / Dark Tech**
*   **Visual Style**: 
    *   🎥 **16:9 Cinematic Experience** (Optimized for desktop/TV consumption but short-form paced)
    *   🌑 **Color Grade**: High Contrast (1.1x), Desaturated (0.9x), Vignette (15%) for a moody, "premium" look.
    *   ✨ **Typography**: "Cairo-Hybrid Glow v2" - Bold, Gold/White text with soft outer glow and drop shadows.
*   **Narrative Structure**:
    *   **The Hook (0-8s)**: Fast-paced, match-cut noir imagery (0.6s cuts) to grab attention immediately.
    *   **The Story (8s-45s)**: Slower, steady speed-ramped dolly zooms.
    *   **The "Infinite Loop"**: The final sentence creates a perfect semantic and visual bridge back to the opening hook, encouraging repeated viewing.
*   **Audio Signature**: Deep "ChristopherNeural" voiceover + layered SFX (Click, Riser, Ambient) + Hard Limiting (-1dB).

---

## 📅 2. POSTING SCHEDULE
**Frequency**: 1 Video Per Day
**Time**: **08:00 AM** (Local Server Time)

*   **Trigger**: Automated Cron Job (`APScheduler`)
*   **Mode**: "Generate-on-Demand" (Content is created fresh each morning, not pre-buffered).

---

## ⚙️ 3. AUTOMATED UPLOAD MECHANISM

### 🔴 YouTube (Public / Shorts)
1.  **Auth**: Authenticates via `token.json` (OAuth 2.0).
2.  **Metadata**: 
    *   Truncates Title to 100 chars.
    *   Applies SEO Tags: `["cinematic", "noir", "infiniteloop"]`.
    *   Privacy: **Public**.
3.  **Upload**: Uses **Resumable Chunked Upload** to handle large 4K files reliably.

### 🟣 Instagram (Feed / Reels)
1.  **Bridge**: Since Instagram API requires a *public URL* for media, the system first uploads the generated thumbnail/image to **ImgBB**.
2.  **Container Creation**: 
    *   POSTs the public ImgBB URL + Caption to Instagram's `media` endpoint.
    *   Receives a `creation_id`.
3.  **Publishing**: POSTs the `creation_id` to the `media_publish` endpoint to make it live.

---

## ⏳ 4. CURRENT QUEUE STATUS
**Status**: 🟢 **IDLE / WAITING**

*   **Pending Videos**: **0**
*   **Next Scheduled Job**: Tomorrow @ 08:00 AM
*   **Approval State**: No files awaiting manual approval (No `is_final_approved.txt` found).

> *System is currently standing by for the next scheduled trigger.*

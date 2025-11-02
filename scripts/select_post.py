import yaml, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "posts"

def pick_for_today_x():
    today = dt.date.today().isoformat()
    if not POSTS.exists():
        return None
    for d in sorted(POSTS.iterdir()):
        if not d.is_dir():
            continue
        meta_p = d / "meta.yaml"
        text_p = d / "post.txt"
        if not (meta_p.exists() and text_p.exists()):
            continue
        meta = yaml.safe_load(meta_p.read_text(encoding="utf-8"))
        if meta.get("date") == today and "x" in (meta.get("targets") or []):
            return {
                "dir": d,
                "text": text_p.read_text(encoding="utf-8").strip(),
                "meta": meta
            }
    return None

if __name__ == "__main__":
    sel = pick_for_today_x()
    if not sel:
        print("::notice ::No X post scheduled for today")
    else:
        print("::group::DRY-RUN Selection (X)")
        print("Post:", sel["dir"].name)
        print("Date:", sel["meta"].get("date"), sel["meta"].get("time"), sel["meta"].get("timezone"))
        print("Hashtags:", sel["meta"].get("hashtags"))
        print("Text:\n", sel["text"])
        medias = sorted([p.name for p in sel["dir"].iterdir() if p.name.startswith("media")])
        print("Media files:", medias)
        print("::endgroup::")

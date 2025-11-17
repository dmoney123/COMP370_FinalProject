import json
import csv
import re
import html
from pathlib import Path


def flatten_dict(d, parent_key="", sep="."):
    """Recursively flatten nested dictionaries."""
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items


# Fix common mojibake / encoding problems
REPLACEMENTS = {
    "‚Äô": "’",
    "â€™": "’",
    "â€œ": "“",
    "â€�": "”",
    "â€“": "–",
    "â€”": "—",
    "â€˜": "‘",
    "â€¦": "…",
    "‚Ä¶": "…",
}


def clean_text_value(v: str) -> str:
    """Clean strings: fix encoding, remove HTML, remove [+xxxx chars], normalize spacing."""
    # Decode HTML entities like &amp;, &quot;
    v = html.unescape(v)

    # Remove the "[+1234 chars]" text
    v = re.sub(r"\[\+\d+\schars]", "", v)

    # Remove HTML tags
    v = re.sub(r"<[^>]+>", " ", v)

    # Fix encoding issues
    for bad, good in REPLACEMENTS.items():
        v = v.replace(bad, good)

    # Collapse whitespace
    v = " ".join(v.split())

    return v


def clean_value(v):
    if isinstance(v, str):
        return clean_text_value(v)
    return v


def concat_news_json_to_csv(json_files, output_csv):
    all_rows = []
    all_keys = set()

    for file_path in json_files:
        file_path = Path(file_path)
        print(f"Processing {file_path} ...")

        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Remove unwanted top-level keys
        data.pop("status", None)
        data.pop("totalResults", None)

        top_level = {k: v for k, v in data.items() if k != "articles"}
        top_level_flat = flatten_dict(top_level)

        articles = data.get("articles", [])
        if not isinstance(articles, list):
            continue

        for article in articles:
            if not isinstance(article, dict):
                continue

            article_flat = flatten_dict(article)

            # Remove urlToImage
            article_flat.pop("urlToImage", None)

            # Merge everything
            row = {
                **top_level_flat,
                **article_flat,
                "from_json": file_path.name,  # 👈 ADD THIS
            }

            # Clean all string values
            row = {k: clean_value(v) for k, v in row.items()}

            all_rows.append(row)
            all_keys.update(row.keys())

    # Make sure removed fields don't appear
    for unwanted in ["status", "totalResults", "urlToImage"]:
        all_keys.discard(unwanted)

    # Ensure from_json is included
    all_keys.add("from_json")

    fieldnames = sorted(all_keys)

    # Write CSV in utf-8-sig so Excel shows correct characters
    with open(output_csv, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Done! Wrote {len(all_rows)} rows to {output_csv}")


if __name__ == "__main__":

    json_files = [
        "Left_pre.json",
        "Center_pre.json",
        "Right_pre.json",
        "Left_post.json",
        "Center_post.json",
        "Right_post.json",
        # add more here...
    ]

    output_csv = "all_articles.csv"

    concat_news_json_to_csv(json_files, output_csv)

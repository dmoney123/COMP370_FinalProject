import json
import csv
import re
import html
from pathlib import Path


def flatten_dict(d, parent_key="", sep="."):

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

    v = html.unescape(v)


    v = re.sub(r"\[\+\d+\schars]", "", v)


    v = re.sub(r"<[^>]+>", " ", v)


    for bad, good in REPLACEMENTS.items():
        v = v.replace(bad, good)

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


            article_flat.pop("urlToImage", None)


            row = {
                **top_level_flat,
                **article_flat,
                "from_json": file_path.name,  # 👈 ADD THIS
            }


            row = {k: clean_value(v) for k, v in row.items()}

            all_rows.append(row)
            all_keys.update(row.keys())

    # UNWANTED FIELDS
    for unwanted in ["status", "totalResults", "urlToImage"]:
        all_keys.discard(unwanted)


    all_keys.add("from_json")

    fieldnames = sorted(all_keys)


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

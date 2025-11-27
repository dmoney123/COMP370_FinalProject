import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    
    filename = "annotated_500.csv"  
    df = pd.read_csv(filename)

    print("Columns:", df.columns.tolist())

    
    df = df.rename(columns={"Topic Label": "topic"})

    
    if "N/A" in df["topic"].astype(str).unique():
        df = df[df["topic"] != "N/A"]

    
    df["title"] = df["title"].fillna("")
    df["description"] = df["description"].fillna("")
    df["text"] = df["title"] + " " + df["description"]

    print("Number of documents:", df.shape[0])
    print("\nTopic counts:\n", df["topic"].value_counts())

   
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_df=0.8,
        min_df=5,
    )
    X = vectorizer.fit_transform(df["text"])
    vocab = vectorizer.get_feature_names_out()

    print("\nTF-IDF matrix shape:", X.shape)

   
    topics = df["topic"].unique()
    rows = []

    for topic in topics:
        mask = (df["topic"] == topic).to_numpy()
        n_docs = mask.sum()
        print(f"\nTopic '{topic}': {n_docs} docs")

        if n_docs == 0:
            continue

        X_topic = X[mask, :]

        # average: tf-idf per word across docs of this topic
        mean_scores = X_topic.mean(axis=0).A1

        # indices of top 10 words
        top_idx = mean_scores.argsort()[::-1][:10]

        words = [vocab[i] for i in top_idx]
        scores = [float(mean_scores[i]) for i in top_idx]

        print("  Top words:")
        for w, s in zip(words, scores):
            print(f"    {w}: {s:.4f}")

        rows.append({
            "topic": topic,
            "top_words": ", ".join(words),
            "top_scores": ", ".join(f"{s:.4f}" for s in scores),
        })

    # results to CSV 
    tfidf_table = pd.DataFrame(rows)
    tfidf_table.to_csv("topic_tfidf_top10_500.csv", index=False)
    print("\nSaved results to topic_tfidf_top10_500.csv")


if __name__ == "__main__":
    main()

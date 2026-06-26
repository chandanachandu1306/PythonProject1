print("THIS IS THE NEW FEW_SHOT FILE")
import pandas as pd
import json


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        # Load JSON file
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            posts = json.load(f)

        # Clean invalid Unicode characters
        def clean_text(value):
            if isinstance(value, str):
                try:
                    return value.encode(
                        "utf-8",
                        errors="surrogatepass"
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )
                except Exception:
                    return ""
            return value

        # Clean all posts
        cleaned_posts = []
        for post in posts:
            cleaned_post = {}
            for key, value in post.items():
                cleaned_post[key] = clean_text(value)
            cleaned_posts.append(cleaned_post)

        # Create DataFrame
        self.df = pd.DataFrame(cleaned_posts)

        # Add length category
        self.df["length"] = self.df["line_count"].apply(
            self.categorize_length
        )

        # Collect unique tags
        all_tags = []
        for tags in self.df["tags"]:
            if isinstance(tags, list):
                all_tags.extend(tags)

        self.unique_tags = list(set(all_tags))

    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df["tags"].apply(lambda tags: tag in tags))
            & (self.df["language"] == language)
            & (self.df["length"] == length)
            ]

        return df_filtered.to_dict(orient="records")

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags


if __name__ == "__main__":
    fs = FewShotPosts()

    print("Available Tags:")
    print(fs.get_tags())

    posts = fs.get_filtered_posts(
        "Medium",
        "Hinglish",
        "Job Search"
    )

    print("\nFiltered Posts:")
    print(posts)

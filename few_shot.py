import pandas as pd
import json

class FewShotPosts:
    def __init__(self, file_path="processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            # Sanitize surrogate characters that break PyArrow on Python 3.14
            for post in posts:
                for key, val in post.items():
                    if isinstance(val, str):
                        post[key] = val.encode('utf-8', 'surrogatepass').decode('utf-8', 'replace')
            self.df = pd.json_normalize(posts)
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = list(set(all_tags))

    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df['tags'].apply(lambda tags: tag in tags)) &
            (self.df['language'] == language) &
            (self.df['length'] == length)
        ]
        # Sort by engagement descending so best-performing posts are used as examples
        if 'engagement' in df_filtered.columns:
            df_filtered = df_filtered.sort_values('engagement', ascending=False)
        return df_filtered.to_dict(orient='records')

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
    # print(fs.get_tags())
    posts = fs.get_filtered_posts("Medium","English","Job Search")
    print(posts)

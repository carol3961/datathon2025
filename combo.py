import joblib
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer


# Load the model
import cloudpickle
with open('/Users/nikolaj/Desktop/datathon/datathon2025/classifier_yumminess.pkl', 'rb') as f:
    classifier_yumminess = cloudpickle.load(f)
with open('/Users/nikolaj/Desktop/datathon/datathon2025/classifier_service.pkl', 'rb') as f:
    classifier_service = cloudpickle.load(f)


REVIEWS_PATH = '/Users/nikolaj/Desktop/datathon/review_chunks/reviews.csv'
df = pd.read_csv(REVIEWS_PATH, skiprows=1)



MAX_LEN = 512
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
# Filter out reviews that are too long
def is_within_limit(text):
    return len(tokenizer.encode(text, truncation=False)) <= MAX_LEN

# Drop rows where 'text' is missing
df = df.dropna(subset=['text'])

# Ensure all texts are strings
df['text'] = df['text'].astype(str)

# Filter based on token length
df = df[df['text'].apply(is_within_limit)].reset_index(drop=True)
print(f"🧹 Filtered down to {len(df)} reviews within token limit.")





yum_scores = []
serv_scores = []
print("Scoring reviews...")
for review in tqdm(df['text'], desc="Scoring"):
    yum_score = classifier_yumminess(review)[0]['score']
    serv_score = classifier_service(review)[0]['score']
    yum_scores.append(yum_score)
    serv_scores.append(serv_score)

# Create new dataframe
results_df = pd.DataFrame({
    'business_id': df['business_id'],
    'yumminess_score': yum_scores,
    'service_score': serv_scores
})

# Save to CSV
results_df.to_csv("business_scores.csv", index=False)
print("✅ Scores saved to business_scores.csv")


import joblib
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer


import cloudpickle
with open('/Users/nikolaj/Desktop/datathon/datathon2025/classifier_yumminess.pkl', 'rb') as f:
    classifier_yumminess = cloudpickle.load(f)
with open('/Users/nikolaj/Desktop/datathon/datathon2025/classifier_service.pkl', 'rb') as f:
    classifier_service = cloudpickle.load(f)


REVIEWS_PATH = '/Users/nikolaj/Desktop/datathon/review_chunks/reviews.csv'
df = pd.read_csv(REVIEWS_PATH, skiprows=1)



MAX_LEN = 512
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
def is_within_limit(text):
    return len(tokenizer.encode(text, truncation=False)) <= MAX_LEN

df = df.dropna(subset=['text'])

df['text'] = df['text'].astype(str)

df = df[df['text'].apply(is_within_limit)].reset_index(drop=True)





yum_scores = []
serv_scores = []
print("Scoring reviews...")
for review in tqdm(df['text'], desc="Scoring"):
    yum_score = classifier_yumminess(review)[0]['score']
    serv_score = classifier_service(review)[0]['score']
    yum_scores.append(yum_score)
    serv_scores.append(serv_score)

results_df = pd.DataFrame({
    'business_id': df['business_id'],
    'yumminess_score': yum_scores,
    'service_score': serv_scores
})

results_df.to_csv("business_scores.csv", index=False)


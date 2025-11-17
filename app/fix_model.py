import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# 1. Define where to save the file
# It must match the folder structure we set up
MODEL_DIR = os.path.join("app", "ml_logic", "models")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "resume_scorer.joblib")

print("Creating a compatible model...")

# 2. Create Dummy Data 
# (We fake the data just to get the file structure correct)
data = {
    "years_exp": [0, 2, 5, 10, 1],
    "skill_count": [2, 10, 20, 50, 5],
    "format_score": [5, 10, 15, 20, 8],
    "num_experience_items": [0, 2, 4, 8, 1],
    "label": [0, 0, 1, 1, 0] # 0=Low Score, 1=High Score
}
df = pd.DataFrame(data)

# 3. Train the Model
# This creates a "Brain" that understands your version of Python
X = df.drop("label", axis=1)
y = df["label"]

clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X, y)

# 4. Save the file
features = list(X.columns)
joblib.dump((clf, features), MODEL_PATH)

print(f"✅ SUCCESS! New compatible model saved to: {MODEL_PATH}")
print("You can now restart your server and test again.")
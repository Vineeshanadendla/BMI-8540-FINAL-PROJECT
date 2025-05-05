import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('bacteria.db')
df = pd.read_sql_query("SELECT * FROM bacteria", conn)

print("Top 5 Records:")
print(df.head())

type_counts = df['type'].value_counts()
type_counts.plot(kind='bar', title='Bacterial Type Distribution', color='skyblue')
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("type_distribution.png")
print("Saved plot as type_distribution.png")

conn.close()

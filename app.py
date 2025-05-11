from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
DB_PATH = 'bacteria.db'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        # Create the upload folder if it does not exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save the uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Load the data from the CSV file
        data = pd.read_csv(filepath)

        # Clean the 'Bacteria name' column
        data['Bacteria Name'] = data['Bacteria Name'].str.replace(':', '').str.strip()

        # Updated categorization based on your new data
        def categorize_bacteria(significance):
            significance = str(significance).lower()
            if 'probiotic' in significance:
                return 'Probiotic'
            elif 'pathogen' in significance:
                return 'Pathogen'
            elif 'scfa producer' in significance or 'scfa' in significance:
                return 'SCFA Producer'
            elif 'metabolic health marker' in significance or 'metabolic' in significance:
                return 'Metabolic Health Marker'
            elif 'inflammation marker' in significance or 'inflammation' in significance:
                return 'Inflammation Marker'
            elif 'dysbiosis' in significance:
                return 'Dysbiosis Indicator'
            elif 'aging' in significance:
                return 'Aging Associated'
            elif 'diversity loss' in significance or 'linked to diversity' in significance:
                return 'Diversity Loss'
            elif 'gut microbiota' in significance or 'microbiota' in significance:
                return 'Gut Microbiota'
            elif 'homeostasis' in significance:
                return 'Homeostasis Associated'
            else:
                return 'Other'

        # Apply the updated categorization function
        data['Category'] = data['Significance'].apply(categorize_bacteria)

        # Connect to SQLite database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Create table if not exists
        c.execute('''
            CREATE TABLE IF NOT EXISTS bacteria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                significance TEXT,
                category TEXT
            )
        ''')

        # Clear the existing data
        c.execute("DELETE FROM bacteria")

        # Insert the updated data into the database
        for _, row in data.iterrows():
            c.execute("INSERT INTO bacteria (name, type, significance, category) VALUES (?, ?, ?, ?)",
                      (row['Bacteria Name'], row['Type'], row['Significance'], row['Category']))

        conn.commit()
        conn.close()

        # Calculate counts for types and categories
        type_counts = data['Type'].value_counts().to_dict()
        category_counts = data['Category'].value_counts().to_dict()

        # Return the counts as JSON
        return jsonify({
            'type_counts': type_counts,
            'category_counts': category_counts
        })

    return jsonify({"error": "No file provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)

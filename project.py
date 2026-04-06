# ================================
# IMPORT LIBRARIES
# ================================
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# ================================
# CREATE SAMPLE DATA
# ================================
teams = ['Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab',
         'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
         'Royal Challengers Bangalore', 'Sunrisers Hyderabad']

data = []

for _ in range(1000):
    bt = np.random.choice(teams)
    bl = np.random.choice(teams)
    
    if bt == bl:
        continue

    overs = np.random.uniform(5, 20)
    runs = np.random.randint(30, 180)
    wickets = np.random.randint(0, 10)
    runs_last_5 = np.random.randint(20, 70)
    wickets_last_5 = np.random.randint(0, 5)

    total = runs + np.random.randint(20, 80)

    data.append([bt, bl, runs, wickets, overs, runs_last_5, wickets_last_5, total])

data = pd.DataFrame(data, columns=[
    'batting_team', 'bowling_team', 'runs', 'wickets',
    'overs', 'runs_last_5', 'wickets_last_5', 'total'
])

# ================================
# ENCODING
# ================================
data = pd.get_dummies(data, columns=['batting_team', 'bowling_team'])

X = data.drop('total', axis=1)
y = data['total']

# ================================
# TRAIN MODEL
# ================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor()
model.fit(X_train, y_train)

print("Model Trained")

# ================================
# PREDICTION FUNCTION
# ================================
def predict_score(batting_team, bowling_team, runs, wickets, overs, runs_last_5, wickets_last_5):
    
    input_data = [0] * len(X.columns)

    for col in X.columns:
        if f"batting_team_{batting_team}" == col:
            input_data[X.columns.get_loc(col)] = 1
        if f"bowling_team_{bowling_team}" == col:
            input_data[X.columns.get_loc(col)] = 1

    input_data[-5:] = [runs, wickets, overs, runs_last_5, wickets_last_5]

    prediction = model.predict([input_data])
    return int(prediction[0])

# ================================
# GUI
# ================================
root = tk.Tk()
root.title("IPL Score Predictor")
root.geometry("500x600")
root.configure(bg="#1e1e2f")

tk.Label(root, text="IPL Score Predictor",
         font=("Arial", 20, "bold"),
         bg="#1e1e2f", fg="white").pack(pady=20)

# Input function
def create_input(label):
    tk.Label(root, text=label, bg="#1e1e2f",
             fg="white", font=("Arial", 12)).pack()
    entry = tk.Entry(root, font=("Arial", 14), width=25)
    entry.pack(pady=5)
    return entry

# Inputs
batting_team = create_input("Batting Team")
bowling_team = create_input("Bowling Team")
runs = create_input("Runs")
wickets = create_input("Wickets")
overs = create_input("Overs")
runs_last_5 = create_input("Runs Last 5 Overs")
wickets_last_5 = create_input("Wickets Last 5 Overs")

# Button Function
def predict_gui():
    try:
        result = predict_score(
            batting_team.get(),
            bowling_team.get(),
            int(runs.get()),
            int(wickets.get()),
            float(overs.get()),
            int(runs_last_5.get()),
            int(wickets_last_5.get())
        )

        result_label.config(text=f"Predicted Score: {result}", fg="yellow")

    except:
        messagebox.showerror("Error", "Invalid Input or Team Name")

# Button
tk.Button(root, text="Predict Score",
          command=predict_gui,
          font=("Arial", 14),
          bg="#4CAF50", fg="white",
          width=20).pack(pady=20)

# Result
result_label = tk.Label(root, text="",
                        font=("Arial", 16, "bold"),
                        bg="#1e1e2f")
result_label.pack()

# Run App
root.mainloop()
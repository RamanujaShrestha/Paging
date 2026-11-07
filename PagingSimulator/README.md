
# 🧠 Paging Simulator

An interactive Operating Systems project that demonstrates virtual memory management and page replacement algorithms using Python and Streamlit.

## 📌 Project Overview

The Paging Simulator visually demonstrates how an operating system manages memory using paging. It allows users to enter a page reference string, select the number of memory frames, and observe how different page replacement algorithms work.

## 🚀 Features

- FIFO (First In First Out) page replacement.
- LRU (Least Recently Used) page replacement.
- Optimal page replacement.
- Interactive memory frame visualization.
- Page table representation.
- Page Hit and Page Fault detection.
- Automatic simulation playback.
- Play, Pause, Next, Previous and Reset controls.
- Live memory utilization monitoring.
- Live page hit and fault rate.
- Analytics dashboard.
- Algorithm performance comparison and ranking.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Plotly

## 📂 Project Structure

```text
PagingSimulator/
│
├── .streamlit/
│   └── config.toml
│
├── components/
│   ├── __init__.py
│   ├── memory.py
│   └── charts.py
│
├── algorithms.py
├── simulator.py
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Execution

### 1. Install Python

Install Python 3.10 or later.

### 2. Open the project folder

Open PowerShell and navigate to the project directory:

```powershell
cd "$HOME\PagingSimulator"
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the application

```powershell
python -m streamlit run app.py
```

The application will open in your web browser.

## 🧮 Algorithms Implemented

### 1. FIFO

First In First Out replaces the page that entered memory first.

### 2. LRU

Least Recently Used replaces the page that has not been accessed for the longest time.

### 3. Optimal

Optimal replaces the page whose next use is farthest in the future. It produces the minimum possible page faults when future page references are known.

## 📊 Performance Metrics

The simulator calculates:

- Total Page References
- Page Hits
- Page Faults
- Hit Ratio
- Fault Ratio
- Memory Utilization

### Formulas

Hit Ratio:

Hit Ratio = (Total Hits / Total References) × 100

Page Fault Rate:

Page Fault Rate = (Total Page Faults / Total References) × 100

Memory Utilization:

Memory Utilization = (Occupied Frames / Total Frames) × 100

## 🎯 Objective

The objective of this project is to provide an interactive learning platform for understanding paging, virtual memory management, and page replacement algorithms.

## 👨‍💻 Project Type

Academic Mini Project – Operating Systems

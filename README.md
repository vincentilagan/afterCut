# AfterCut 🎬

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![GitHub Repo](https://img.shields.io/badge/GitHub-AfterCut-green)](https://github.com/vincentilagan/afterCut)

Created by **Vincent Ilagan**

---

## ⚡ Overview

**AfterCut** is a Python tool that automatically detects scene cuts in your videos and generates a JSX script for Adobe After Effects. It speeds up editing by cutting your video into pre-compositions for easy background replacement and scene management. Perfect for revisions or quick edits!  

---

## 🛠 Features

- Automatically detect scene cuts in MP4 videos
- Generate After Effects JSX script with markers
- Auto-split your video layer at each scene cut
- Create pre-compositions for each cut for easy editing
- Allows bulk background replacement in pre-compositions
- Progress indicator during processing to prevent hanging

---

## 🚀 How to Use

1. Open `AfterCut.py`.
2. Click **Upload Your Video** and select an MP4 file.
3. Wait for the **progress indicator** while cuts are detected.
> ⚠️ **Note:** The app shows a "Processing..." message to indicate progress—do not close it until complete.
4. After completion, a JSX script is created in the same folder as your video.
5. Open Adobe After Effects, select your composition with the video layer, and run the JSX script.
6. Your video layer will be cut at each detected scene, and pre-compositions are created for easy editing.
> 💡 **Tip:** Pre-compositions allow you to replace the background for multiple clips at once.

---

## 💻 Installation

**Clone this repository:**
```bash
git clone https://github.com/vincentilagan/afterCut.git

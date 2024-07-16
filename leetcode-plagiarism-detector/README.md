


# 🕵️‍♂️ LeetCode Plagiarism Detector

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Work%20in%20Progress-yellow)

## 📜 Table of Contents
- [Motivation](#-motivation)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)

## 💡 Motivation

As an avid LeetCoder, I've grown increasingly frustrated with the prevalence of cheating in contests. The integrity of these competitions is compromised when participants submit plagiarized solutions, and unfortunately, LeetCode's current measures seem inadequate to address this issue effectively.

This project was born out of that frustration and a desire to level the playing field. By creating a robust plagiarism detection system, I aim to:

1. Identify potential cases of code plagiarism in LeetCode contests
2. Provide a tool for the community to maintain the integrity of competitions
3. Encourage fair play and original problem-solving

While this project is still a work in progress, I'm committed to refining and expanding its capabilities to make it a valuable asset in the fight against coding plagiarism.

## ✨ Features

- 🔍 Scrapes contest submissions from LeetCode
- 🧹 Preprocesses code to standardize format
- 📊 Detects similarities between submissions using advanced algorithms
- 🚩 Flags potentially plagiarized code
- 📝 Generates detailed plagiarism reports
- 🌐 User-friendly web interface for easy interaction

## 🚀 Installation

1. Clone the repository:
   ```
   git clone https://github.com/kartikdevsharma/leetcode-plagiarism-detector.git
   cd leetcode-plagiarism-detector
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## 🖥 Usage

1. Navigate to the `src/ui` directory:
   ```
   cd src/ui
   ```

2. Run the Flask application:
   ```
   python app.py
   ```

3. Open your web browser and go to `http://localhost:5000`

4. Select a contest, set the similarity and flag thresholds, and generate a plagiarism report.

## 📁 Project Structure

```
leetcode-plagiarism-detector/
├── src/
│   ├── data_collection/
│   ├── preprocessing/
│   ├── similarity_detection/
│   ├── flagging/
│   └── ui/
├── tests
│   ├── test_data_collection/
│   ├── test_preprocessing/
│   ├── test_imilarity_detection/
│   ├── test_flagging/
│   └── readme.md/
├── requirements.txt
└── README.md
```

## 🔮 Future Improvements

- Implement user authentication for secure access
- Enhance the similarity detection algorithm
- Add support for more programming languages
- Integrate with LeetCode's API (if available)
- Implement real-time monitoring of contest submissions
- Develop a more detailed and interactive report interface

## 🤝 Contributing

Contributions are welcome! If you'd like to help improve the LeetCode Plagiarism Detector, please:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Disclaimer:** This project is not officially affiliated with LeetCode. It is an independent tool created to promote fair competition and integrity in coding contests.



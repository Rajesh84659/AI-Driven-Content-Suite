# AI-Driven Content Suite

## Project Overview

AI-Driven Content Suite is a Generative AI project built using Python, Streamlit, and Large Language Models (LLMs).

This application helps users generate different types of content such as:

* Blogs
* Emails
* LinkedIn Posts

The system uses AI to generate:

1. Content Outline
2. Full Draft
3. Refined Version

The project also evaluates generated content using AI-powered analysis.

This project demonstrates:

* Prompt Engineering
* LLM Integration
* AI Workflow Design
* Streamlit Dashboard Development
* Content Evaluation
* Data Storage and Versioning

---

# Features

## 1. Multiple Content Types

Users can generate:

* Blog articles
* Professional emails
* LinkedIn posts

---

## 2. Dynamic Prompt Engineering

The application creates prompts dynamically based on:

* Topic
* Tone
* Target Audience
* Content Type

This improves output quality and makes the system flexible.

---

## 3. Outline Generation

The AI first creates a structured outline before generating the complete content.

This follows a multi-step AI workflow.

Example:

Topic → Outline → Draft → Refinement

---

## 4. Draft Generation

Using the generated outline, the AI creates a complete content draft.

The draft generation process supports:

* Professional tone
* Casual tone
* Friendly tone

---

## 5. Content Refinement

Users can refine the generated content.

Refinement options include:

* Professional
* Casual
* Friendly

The system improves:

* Grammar
* Readability
* Tone consistency
* Clarity

---

## 6. Evaluation Report

The application evaluates generated content using AI.

Evaluation includes:

* Word Count
* Readability Score
* Sentiment Analysis
* Timestamp Tracking

Example:

```json
{
  "word_count": 550,
  "readability": 82,
  "sentiment": "Positive"
}
```

---

## 7. Versioned Storage System

The project stores:

* Prompts
* Generated Outputs
* Evaluation Reports

All data is stored in JSON format for future:

* comparison
* tracking
* versioning
* analytics

---

# Technologies Used

| Technology    | Purpose                 |
| ------------- | ----------------------- |
| Python        | Core programming        |
| Streamlit     | Web application UI      |
| Gemini API    | AI content generation   |
| JSON          | Data storage            |
| Pandas        | Table display           |
| python-dotenv | Secure API key handling |

---

# Project Architecture

```text
User Input
    ↓
Prompt Manager
    ↓
Generator Module
    ↓
LLM API
    ↓
Generated Content
    ↓
Evaluator Module
    ↓
Storage Module
    ↓
Streamlit Dashboard
```

---

# Folder Structure

```text
AI_Content_Suite/
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
│
├── modules/
│   ├── generator.py
│   ├── prompt_manager.py
│   ├── evaluator.py
│   ├── storage.py
│
├── templates/
│   ├── prompt_templates.json
│
├── data/
│   ├── prompts/
│   ├── outputs/
│   ├── evaluations/
│
└── screenshots/
```

---

# How the Project Works

## Step 1 — User Input

The user selects:

* Content Type
* Topic
* Tone
* Target Audience

---

## Step 2 — Prompt Generation

The Prompt Manager creates the final AI prompt dynamically using templates.

Example:

```text
Write a professional blog about AI in Healthcare for beginners.
```

---

## Step 3 — Outline Generation

The AI generates a structured outline.

Example:

```text
1. Introduction
2. Benefits
3. Applications
4. Challenges
5. Conclusion
```

---

## Step 4 — Draft Generation

Using the outline, the AI creates the complete content.

---

## Step 5 — Refinement

Users can refine the generated draft.

The AI improves:

* readability
* tone
* engagement
* professionalism

---

## Step 6 — Evaluation

The Evaluator module analyzes generated content.

Metrics:

* Word Count
* Readability
* Sentiment

---

## Step 7 — Storage

The system stores:

* prompts
* outputs
* evaluations

inside the `data/` folder.

---

# Prompt Engineering

This project uses Prompt Engineering techniques to improve AI output quality.

The application supports:

* dynamic prompts
* prompt templates
* refinement prompts
* multi-step prompting

Prompt templates are stored separately in:

```text
templates/prompt_templates.json
```

This keeps the system scalable and organized.

---

# Future Improvements

Possible future enhancements:

* Multiple LLM support
* User authentication
* Export to PDF/DOCX
* Prompt comparison dashboard
* Content history viewer
* AI analytics dashboard
* SEO scoring
* Grammar scoring
* Database integration

---

# Author

**Rajesh Jella**

Developed as part of an AI internship project focused on:

* Generative AI
* Prompt Engineering
* AI Application Development

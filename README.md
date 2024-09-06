# How to Run on Local Environment

Follow these steps to set up and run the project on your local environment:

## 1. Clone this repository

First, clone the repository to your local machine using `git`:

```bash
git clone https://github.com/StevenSiahaann/rag-chatbot.git

```
## 2. Make a secret.toml file on .streamlit directory and .env on root folder. Look at the example
## 3. Create a Virtual Environment
```bash
python -m venv {your_env_name}
```
## 4. Activate your Virtual Environment
```bash
.\{your_env_name}\Scripts\activate
```
## 5. Install dependencies
```bash
pip install -r requirements.txt
```
## 6. Run the streamlit
```bash 
streamlit run app.py
```


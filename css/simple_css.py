import streamlit as st
def add_custom_css():
    st.markdown("""
        <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
        }
        
        .stApp {
            background-color: #121212;
            color: #e0e0e0;
        }

        .main-title {
            font-size: 48px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 20px;
        }
        .description {
            color: #b0b0b0;
            font-style: italic;
            font-size: 18px;
        }        
        .stTextInput > div, .stTextArea > div {
            background-color: #1c1c1c !important;
            color: #e0e0e0 !important;
            border: 1px solid #333333;
            border-radius: 10px;
        }
        
        .stSelectbox > div {
            background-color: #1c1c1c !important;
            color: #e0e0e0 !important;
            border-radius: 10px;
        }

        .sidebar .sidebar-content {
            background-color: #1e1e1e;
        }
        .sidebar .sidebar-title {
            font-size: 24px;
            color: #80cbc4;
            font-weight: bold;
        }
        .sidebar .contributor-name {
            font-size: 16px;
            color: #b39ddb;
            margin-top: 10px;
        }

        .stFileUploader > div {
            background-color: #1c1c1c !important;
            color: #e0e0e0 !important;
            border-radius: 10px;
        }

        .stButton > button {
            background-color: #29b6f6;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #0288d1;
        }

        .st-chat-message-user {
            background-color: #2c2c2c;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }
        .st-chat-message-assistant {
            background-color: #424242;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }
        .st-chat-input > div {
            background-color: #1c1c1c !important;
            color: #e0e0e0 !important;
            border-radius: 10px;
        }

        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #424242;
        }
        ::-webkit-scrollbar-thumb {
            background: #1e88e5;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #1565c0;
        }

        /* Sidebar Links */
        .sidebar .element-container a {
            color: #ffffff !important;
            text-decoration: underline;
        }
        </style>
    """, unsafe_allow_html=True)

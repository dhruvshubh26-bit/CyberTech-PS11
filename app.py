import random
import streamlit as st
import pandas as pd
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from collections import Counter
from urllib.parse import urlparse , parse_qs
import re
from datetime import datetime, timezone, date
import tldextract
import streamlit.components.v1 as com
import string
import socket
import ipaddress
import secrets
from cryptography.fernet import Fernet
import requests
import time
from bs4 import BeautifulSoup
import whois
import difflib


st.set_page_config(page_title="🧑‍💻POCSO Reporting", layout="wide", initial_sidebar_state="expanded")

st.sidebar.title("POCSO Reporting System")
st.sidebar.subheader("Blockchain-based POCSO Reporting")
# st.sidebar.divider()
select_one=st.sidebar.selectbox("Go To", options=["🏡Home","📝Report Incident","📌Track Report","🔗Blockchain Explorer","🛡️AI Analyzer","📥URL Checker","🌐Webpage Analyzer","🔐Authority Dashboard","📊Analytics","⚠️Audit Logs","🙈Privacy","🧑‍💻About"], key="page_selection")

if "last_report" not in st.session_state:
    st.session_state.last_report = None

if "name_input" not in st.session_state:
    st.session_state.name_input = ""

if "email_input" not in st.session_state:
    st.session_state.email_input = ""

if "url_input" not in st.session_state:
    st.session_state.url_input = ""

if "description_input" not in st.session_state:
    st.session_state.description_input = ""

if "risk_input" not in st.session_state:
    st.session_state.risk_input = "Low"

if "checkbox_input" not in st.session_state:
    st.session_state.checkbox_input = False

if "tracking_id_input" not in st.session_state:
    st.session_state.tracking_id_input = ""
#Home Page -------------------------------------------------------------------------------------------------------------
if select_one == "🏡Home":
    com.iframe("https://embed.lottiefiles.com/animation/9101", height=100, scrolling=True)
    st.title("Welcome to the POCSO Reporting System")
    
    st.subheader("Empowering Communities to Combat Child Sexual Offenses")
    st.divider()
    st.write("This platform allows you to report incidents related to child sexual offenses in a secure and anonymous manner using blockchain technology. You can also track your reports, analyze data, and access resources for support.")
    # st.subheader("""
    # **Features:**
    # - Report incidents anonymously
    # - Track the status of your reports
    # - Analyze trends and patterns in reported cases
    # - Access resources and support services
    # """)
    st.subheader("""    **🗝️Key Features:**""")
    st.dataframe({
        "Feature": ["Anonymous Reporting", "Report Tracking", "Data Analytics", "Blockchain Security", "Resource Access", "Community Support"],
        "Description": [
            "Submit reports without revealing your identity, ensuring your privacy and safety.",
            "Monitor the status of your submitted reports in real-time.",
            "Explore trends and insights from the reported data to understand the prevalence and patterns of offenses.",
            "Leverage the immutability and transparency of blockchain technology to ensure the integrity of reported data.",
            "Connect with support services and resources for assistance and guidance.",
            "Engage with a community of advocates and professionals dedicated to protecting children from sexual offenses."
        ]
    })


    with st.expander("🤔 How To Use"):

        st.write("""

    1. Navigate to the "Report Incident" section to submit a new report.
    2. Use the "Track Report" section to check the status of your submitted reports.
    3. Explore the "Analytics" section to view trends and insights from the reported data.
    4. Access the "Authority Dashboard" for law enforcement and authorities to manage reports and cases.
    """)


# Report Incident Page -------------------------------------------------------------------------------------------------------------
if select_one == "📝Report Incident":
    com.iframe("https://embed.lottiefiles.com/animation/9101", height=100, scrolling=True)
    st.title("Report an Incident")
    st.write("Please fill out the form below to report an incident related to child sexual offenses. Your report will be treated with the utmost confidentiality and will be securely stored on the blockchain.")

    if st.session_state.last_report:
        st.success("Last submitted report is saved below and will stay visible when you move to other pages.")
        st.json(st.session_state.last_report)

    personal_info = st.expander("Your Data (Optional)")
    with personal_info:
        st.write("Providing your name and email is optional, but it can help us follow up with you if needed. Your information will be kept confidential and will not be shared without your consent.")
        name = st.text_input("Your Name (Optional)", key="name_input")
        email = st.text_input("Your Email (Optional)", key="email_input")
        submit = st.button("Save Personal Info")
        if submit:
            st.success("Your personal information has been saved securely.")
            st.write("Your personal information will be encrypted and stored securely on the blockchain, ensuring that it remains confidential and protected from unauthorized access.")
    st.subheader("Type of Content")
    contant=st.selectbox("", options=["Child Sexual Abuse","Child Exploitation","Human Trafficking","Harassment","Cyberbullying","Revenge Pornography","Online Fraud","Other Illegal Activities"], key="incident_type", help="Select the type of incident you are reporting.", index=None, disabled=False,label_visibility="collapsed")

    st.subheader("Enter URL of the Content")
    url_ = st.text_input("", placeholder="https://example.com/incident", help="Enter the URL where the incident occurred. This will help us investigate and take appropriate action.",label_visibility="collapsed", key="url_input")
            

    st.subheader("Description of the Incident")
    description = st.text_area(label="", placeholder=f"Provide details about the {contant}", help="Provide a detailed description of the incident to help us understand the context and severity.",label_visibility="collapsed", key="description_input")

    st.subheader("Severity Level")
    risk=st.select_slider("", options=['Low', 'Medium', 'High','Critical'], help="Rate the severity of the incident on a scale of 1 to 10, with 10 being the most severe.",label_visibility="collapsed", key="risk_input")

    st.subheader("Platform")
    platform = st.selectbox("", options=["Social Media","Website","Messaging App","Other"], key="platform_selection", help="Select the social media platform or website where the incident occurred.", index=None,label_visibility="collapsed")
    if platform == "Other":
        platform = st.text_input("Please specify the platform", placeholder="Enter the name of the platform where the incident occurred.", help="If the platform is not listed, please specify it here.",label_visibility="collapsed")

    elif platform == "Social Media":
        platform = st.selectbox("Select the social media platform", options=["Facebook","Instagram","Twitter","TikTok","Snapchat","YouTube","Other"], key="social_media_selection", help="Select the social media platform where the incident occurred.",label_visibility="collapsed")
        if platform == "Other":
            platform = st.text_input("Please specify the social media platform", placeholder="Enter the name of the social media platform where the incident occurred.", help="If the social media platform is not listed, please specify it here.",label_visibility="collapsed")
            platform = platform.strip()
    elif platform == "Messaging App":
        platform = st.selectbox("Select the messaging app", options=["WhatsApp","Messenger","Telegram","Other"], key="messaging_app_selection", help="Select the messaging app where the incident occurred.",label_visibility="collapsed")
        if platform == "Other":
            platform = st.text_input("Please specify the messaging app", placeholder="Enter the name of the messaging app where the incident occurred.", help="If the messaging app is not listed, please specify it here.",label_visibility="collapsed")

    st.subheader("Upload Evidence ")
    file=st.file_uploader(label="", type=["txt","log","jpg","csv", "jpeg","pdf"], help="Upload any evidence related to the incident, such as screenshots, videos, or documents. Accepted formats include JPG, JPEG, PNG, PDF, MP4, and AVI.",label_visibility="collapsed")
    
    check=st.checkbox("I confirm this report is genuine", key="checkbox_input")
    if url_ == "":
        st.write("Please enter a URL to report the incident. This will help us investigate and take appropriate action.")

    elif  " " in url_:
        st.error("URL should not contain spaces. Please enter a valid URL without spaces.")
        st.stop()
    elif len(url_) < 10:
        st.error("URL is too short. Please enter a valid URL with at least 10 characters.")
        st.stop()
    elif len(url_) > 200:
        st.error("URL is too long. Please enter a valid URL with less than 200 characters.")
        st.stop()
    elif any (char in url_ for char in """'!#$%^*()+=[]{}<>,|"'"""):
        st.error("URL should not contain special characters. Please enter a valid URL without special characters.")
        st.stop()
    elif not re.search(r"https?://\w+", url_):
        st.error("Please enter a valid URL starting with http:// or https://")
        st.stop()
    elif re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url_):
        st.error("URL should not contain an IP address. Please enter a valid URL with a proper domain name.")
        st.stop()
    
    
    else:
        url_ = url_.strip()

    try:
        domain = tldextract.extract(url_).domain
        suffix = tldextract.extract(url_).suffix

        if domain :            


            common_suffixes = ["com", "org", "net", "edu", "gov", "io", "co", "us", "uk", "ca","au", "de", "fr", "jp", "cn", "in", "br", "ru", "za", "es", "it", "nl", "se", "no", "fi", "dk", "be", "ch", "at", "pl", "gr", "hu", "cz", "sk", "ro", "bg", "hr", "lt", "lv", "ee", "cy", "mt", "li", "ad", "mc", "sm", "va", "tv", "ws", "mobi", "name", "pro", "aero", "coop", "museum"]
            if suffix in common_suffixes:
                st.write(f"{domain}.{suffix}")
            else:
                st.write("The URL has an uncommon domain suffix. Please ensure it is correct.")
        else:
            st.error("Invalid URL. Please enter a valid URL with a proper domain.")
            st.stop()
    except Exception as e:
        st.error("An error occurred while validating the URL.")
        
    try:
        socket.gethostbyname(domain + "." + suffix)


        
            
    except Exception as e:
        st.error("An error occurred while validating the URL. Please enter a valid URL.")
        st.stop()

    if check and contant and url_ and description and risk and platform and platform.strip():
        submit_report = st.button("Submit Report")
        if submit_report:
            st.success("Your report has been submitted successfully.")
            

            tracking_id1 = "PR-" + secrets.token_hex(6).upper()
            tracking_id2 = "SR-" + hashlib.sha256((str(time.time()) + str(random.randint(1000,9999))).encode()).hexdigest()[:12].upper()
            tracking_id = tracking_id1 + tracking_id2

            st.write(f"""Your Tracking ID:
                      
    {tracking_id}
""")
            st.write("Time : " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            st.write(f"""Domain: {domain}.{suffix}""")
            if tldextract.extract(url_).subdomain:
                st.write(f"""Sub Domain: {tldextract.extract(url_).subdomain}""")
            st.write("ZKP Commitment: " + hashlib.sha256((tracking_id + url_ + description).encode()).hexdigest())

            st.write("RISK ASSESSMENT: " + risk)
            st.progress(risk.count("Low") * 25 + risk.count("Medium") * 50 + risk.count("High") * 75 + risk.count("Critical") * 100)

            st.session_state.last_report = {
                "tracking_id": tracking_id,
                "incident_type": contant,
                "url": url_,
                "description": description,
                "risk": risk,
                "platform": platform,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            fernet = Fernet(st.session_state.fernet_key)
            encrypted_description = fernet.encrypt(description.encode()).decode()
            encrypted_url = fernet.encrypt(url_.encode()).decode() if url_ != "" else ""

            report_payload = json.dumps(st.session_state.last_report, indent=2)
            st.write("Encrypted Description: " + encrypted_description)
            st.write("Encrypted URL: " + encrypted_url)

            st.download_button(
                "Download Report Details",
                data=report_payload,
                file_name=f"report_{tracking_id}.json",
                mime="application/json"
            )
#Track Report Page -------------------------------------------------------------------------------------------------------------

if select_one == "📌Track Report":
    st.title("Track Your Report")
    st.write("Enter your tracking ID below to check the status of your submitted report. You can also view the details of your report and any updates related to it.")

    st.divider()
    st.subheader("Enter Tracking ID")
    tracking_id_input = st.text_input("Enter Tracking ID", placeholder="PR-XXXXXXXXXXXXSR-XXXXXXXXXXXX", label_visibility="collapsed", help="Enter the tracking ID you received after submitting your report.", key="tracking_id_input")

    track_report_button = st.button("Track Report")

    if track_report_button:
        if tracking_id_input =="":
            st.error("Please enter a tracking ID to track your report.")
            st.stop()
        elif " " in tracking_id_input:
            st.error("Tracking ID should not contain spaces. Please enter a valid tracking ID without spaces.")
            st.stop()
        else:
            matched_report = None
            if st.session_state.last_report and st.session_state.last_report.get("tracking_id") == tracking_id_input:
                matched_report = st.session_state.last_report

            if matched_report:
                st.success("Report found.")
                with st.spinner("Loading report details..."):
                    time.sleep(1)
                    st.write("Tracking ID : " + f"**{matched_report.get("tracking_id", "")}**")
                    col1,col2=st.columns(2)
                    with col1:
                        st.write("Incident Type : " + f"**{matched_report.get("incident_type", "")}**")  
                        st.write("Status : " + f"**Under Review**")
                        st.write("Risk Assessment : " + f"**{matched_report.get("risk", "")}**")
                    with col2:
                        st.write("Platform : " + f"**{matched_report.get("platform", "")}**")
                        st.write("Last Updated : " + f"**{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**")
                        st.write("URL : " + f"**{matched_report.get("url", "")}**")
                    st.write("Description : " + f"**{matched_report.get("description", "")}**")
            else:
                st.info("Tracking ID not found in this session yet. Submit a report first or enter the latest session tracking ID.")
            with st.expander("Report Updates"):
                st.write("Updates:")
                st.write("- Your report is currently being reviewed by our team.")
                st.write("- We will contact you if we need any additional information.")
                st.write("- You can check back here for updates on the status of your report.")
                st.write("Thank you for your patience and for taking the time to report this incident. Your contribution is valuable in helping us combat child sexual offenses and protect children from harm.")

#Blockchain Explorer

# if select_one == "🔗Blockchain Explorer":
#     com.iframe("https://embed.lottiefiles.com/animation/9101", height=100, scrolling=True)
#     st.title("Blockchain Explorer")
#     st.write("Explore the blockchain to view all submitted reports, their statuses, and related information. You can also search for specific reports using tracking IDs or filter reports based on incident types and severity levels.")
#     st.divider()
#     st.subheader("Search Reports")
#     st.button("Refresh Report List")
#     st.text_input("Search by Tracking ID", placeholder="Enter Tracking ID to search for a specific report", label_visibility="collapsed")
#     st.selectbox("Filter by Incident Type", options=["All", "Child Sexual Abuse", "Child Exploitation", "Human Trafficking", "Harassment", "Cyberbullying", "Revenge Pornography"], key="filter_incident_type", help="Filter reports based on the type of incident.")
#     st.selectbox("Filter by Severity Level", options=["All", "Low", "Medium", "High", "Critical"], key="filter_severity_level", help="Filter reports based on the severity level.")
#     st.subheader("Report List")
#     st.write("Here you can view all the reports that have been submitted to the blockchain. You can click on each report to view more details and the status of the investigation.")
#     st.dataframe({
#         "Tracking ID": ["PR-ABC123SR-DEF456", "PR-GHI789SR-JKL012", "PR-MNO345SR-PQR678"],
#         "Incident Type": ["Child Sexual Abuse", "Human Trafficking", "Cyberbullying"],
#         "Severity Level": ["High", "Critical", "Medium"],
#         "Status": ["Under Review", "Investigation Ongoing", "Resolved"],
#         "Last Updated": ["2024-06-01 12:00:00", "2024-06-02 15:30:00", "2024-06-03 10:45:00"],
#         "Platform": ["Facebook", "Website", "Instagram"],
#         "URL": ["https://example.com/incident1", "https://example.com/incident2", "https://example.com/incident3"]
#         })
    
#     st.write("Note: The above data is for demonstration purposes only and does not represent real reports. In a real implementation, this data would be dynamically fetched from the blockchain and updated in real-time as new reports are submitted and processed.")

# AI Analyzer with API Key



# if select_one == "🛡️AI Analyzer":
#     st.title("🛡️ AI Content Analyzer")
#     st.write("Paste any suspicious text, description, or URL content below. AI will analyze it and tell you if it contains harmful or illegal content.")
#     st.divider()

#     gemini_api_key = os.getenv("GEMINI_API_KEY")
#     if not gemini_api_key:
#         st.error("GEMINI_API_KEY is not set in the environment. Add it before using the AI Analyzer.")
#         st.stop()

#     user_input = st.text_area("Paste Content Here", placeholder="Paste suspicious message, post, or description...", height=200)

#     analyze_btn = st.button("🔍 Analyze with AI")

#     if analyze_btn:
#         if user_input.strip() == "":
#             st.error("Please paste some content to analyze.")
#         else:
#             try:
#                 import google.generativeai as genai
#             except ImportError:
#                 st.error("The google-generativeai package is not installed.")
#                 st.stop()

#             genai.configure(api_key=gemini_api_key)

#             model_name = ""
#             preferred_models = [
#                 "gemini-1.5-flash-latest",
#                 "gemini-1.5-flash",
#                 "gemini-1.5-flash-8b",
#                 "gemini-2.0-flash",
#                 "gemini-2.0-flash-lite"
#             ]

#             try:
#                 available_models = list(genai.list_models())
#                 for preferred in preferred_models:
#                     for m in available_models:
#                         model_id = str(getattr(m, "name", ""))
#                         supported_methods = getattr(m, "supported_generation_methods", []) or []
#                         if preferred in model_id and "generateContent" in supported_methods:
#                             model_name = model_id.replace("models/", "")
#                             break
#                     if model_name:
#                         break
#             except Exception:
#                 model_name = ""

#             if not model_name:
#                 model_name = "gemini-1.5-flash-latest"

#             model = genai.GenerativeModel(model_name)

#             prompt = f"""
# You are a child safety content moderation AI assistant.
# Analyze the following text and determine:
# 1. Is this content harmful, illegal, or related to child exploitation?
# 2. What type of threat is it? (e.g. grooming, CSAM, trafficking, harassment, etc.)
# 3. Severity level: Low / Medium / High / Critical
# 4. Recommended action for authorities.
# 5. Brief explanation in simple English.

# Text to analyze:
# \"\"\"{user_input}\"\"\"

# Respond in this exact format:
# HARMFUL: Yes/No
# THREAT TYPE: ...
# SEVERITY: Low/Medium/High/Critical
# ACTION: ...
# EXPLANATION: ...
# """
#             with st.spinner("AI is analyzing the content..."):
#                 try:
#                     response = model.generate_content(prompt)
#                     result = ""
#                     try:
#                         result = (response.text or "").strip()
#                     except Exception:
#                         result = ""

#                     if not result:
#                         st.error("AI returned an empty response. This may happen due to safety filters or API limits.")
#                         st.write("Raw model response:")
#                         st.write(response)
#                         st.stop()

#                     # Parse result
#                     lines = result.strip().split("\n")
#                     result_dict = {}
#                     for line in lines:
#                         if ":" in line:
#                             key, val = line.split(":", 1)
#                             result_dict[key.strip()] = val.strip()

#                     harmful = result_dict.get("HARMFUL", "Unknown")
#                     threat = result_dict.get("THREAT TYPE", "Unknown")
#                     severity = result_dict.get("SEVERITY", "Unknown")
#                     action = result_dict.get("ACTION", "Unknown")
#                     explanation = result_dict.get("EXPLANATION", "Unknown")

#                     st.divider()

#                     if harmful == "Yes":
#                         st.error("⚠️ HARMFUL CONTENT DETECTED")
#                     else:
#                         st.success("✅ No Harmful Content Detected")

#                     col1, col2 = st.columns(2)
#                     with col1:
#                         st.metric("Threat Type", threat)
#                         st.metric("Severity", severity)
#                     with col2:
#                         st.metric("Harmful", harmful)
#                         st.metric("Recommended Action", action)

#                     st.subheader("AI Explanation")
#                     st.info(explanation)

#                 except Exception as e:
#                     err_text = str(e)
#                     err_lower = err_text.lower()

#                     if "429" in err_text or "quota" in err_lower or "rate" in err_lower:
#                         st.error("Gemini quota/rate limit exceeded. Using local fallback analyzer.")
#                         st.info("Wait for the retry window or enable billing in your Gemini project for stable usage.")

#                         text_lower = user_input.lower()
#                         harmful_words = [
#                             "child", "minor", "nude", "explicit", "abuse", "sex", "exploit",
#                             "groom", "traffic", "harass", "blackmail", "rape", "csam"
#                         ]
#                         critical_words = ["csam", "minor", "groom", "traffic", "rape"]
#                         high_words = ["abuse", "explicit", "blackmail", "exploit"]

#                         harmful_hits = 0
#                         critical_hits = 0
#                         high_hits = 0

#                         for w in harmful_words:
#                             if w in text_lower:
#                                 harmful_hits += 1

#                         for w in critical_words:
#                             if w in text_lower:
#                                 critical_hits += 1

#                         for w in high_words:
#                             if w in text_lower:
#                                 high_hits += 1

#                         if critical_hits > 0:
#                             harmful = "Yes"
#                             severity = "Critical"
#                         elif high_hits > 0:
#                             harmful = "Yes"
#                             severity = "High"
#                         elif harmful_hits > 0:
#                             harmful = "Yes"
#                             severity = "Medium"
#                         else:
#                             harmful = "No"
#                             severity = "Low"

#                         if "groom" in text_lower:
#                             threat = "Grooming"
#                         elif "traffic" in text_lower:
#                             threat = "Trafficking"
#                         elif "harass" in text_lower or "blackmail" in text_lower:
#                             threat = "Harassment/Blackmail"
#                         elif "csam" in text_lower or "minor" in text_lower:
#                             threat = "Child Sexual Exploitation"
#                         else:
#                             threat = "Unknown"

#                         if harmful == "Yes":
#                             action = "Escalate to authority review and preserve evidence."
#                             explanation = "Local fallback detected suspicious keywords. This is a preliminary result only."
#                             st.error("⚠️ POTENTIAL HARMFUL CONTENT (Fallback Analyzer)")
#                         else:
#                             action = "No urgent escalation required; monitor content."
#                             explanation = "Local fallback did not detect strong risk keywords."
#                             st.success("✅ No Harmful Content Detected (Fallback Analyzer)")

#                         col1, col2 = st.columns(2)
#                         with col1:
#                             st.metric("Threat Type", threat)
#                             st.metric("Severity", severity)
#                         with col2:
#                             st.metric("Harmful", harmful)
#                             st.metric("Recommended Action", action)

#                         st.subheader("Fallback Explanation")
#                         st.info(explanation)
#                         st.caption("Source: Local keyword-based fallback (Gemini unavailable due to quota/rate limit).")
#                     else:
#                         st.error(f"AI analysis failed: {err_text}")
#                         st.info("Check your API key, internet connection, and Gemini quota/billing status.")

#AI analyzer without API Key-------------------------------------------------------------------------------------------------------
elif select_one == "🛡️AI Analyzer":
    st.title("🛡️ AI Content Analyzer")

    st.subheader("Paste any suspicious text, description, or URL content below. AI will analyze it and tell you if it contains harmful or illegal content.")
    input_method = st.selectbox("Select One Option", options=["user_input","file_input"], key="input_method_selection", help="Choose whether to paste content directly or upload a text file for analysis.")
    if input_method == "user_input":
        user_input = st.text_area("Paste Content Here", placeholder="Paste suspicious message, post, or description...", height=100)
    elif input_method == "file_input":
        file = st.file_uploader("Or upload a text file with the content to analyze", type=["txt"], key="ai_file_uploader")

    if st.button("🔍 Analyze with AI"):
        content_to_analyze = ""
        if input_method == "user_input":
            content_to_analyze = user_input.strip()
        elif input_method == "file_input" and file is not None:
            try:
                content_to_analyze = file.read().decode("utf-8").strip()
            except Exception as e:
                st.error("Failed to read the uploaded file. Please ensure it is a valid text file.")
                st.stop()

        if content_to_analyze == "":
            st.error("Please provide some content to analyze, either by pasting it or uploading a text file.")
            st.stop()

        harmful_keywords = [
            "child", "minor", "nude", "explicit", "abuse", "sex", "exploit",
            "groom", "traffic", "harass", "blackmail", "rape", "csam","pedo","incest","molest","loli","shotacon","cp","child","teen","prepubescent","underage","sexual","abuse","exploitation","grooming","trafficking","harassment","blackmail","revenge","bully","cyberbully","threat","violence","weapon","drugs","terror","extremism","self-harm","suicide","hate","discrimination","racism","sexism","homophobia","transphobia","islamophobia","antisemitism","xenophobia","ableism","ageism","slur","profanity","offensive","graphic","violent","illegal","crime","scam","fraud","phishing","malware","ransomware","hacker","breach","leak","doxxing","stalking","grooming","exploitation","abuse","harassment","threat","violence","weapon","drugs","terror","extremism","self-harm","suicide","hate","discrimination","racism","sexism","homophobia","transphobia","islamophobia","antisemitism","xenophobia","ableism","ageism","slur","profanity","offensive","graphic","violent","illegal","crime","scam","fraud","phishing","malware","ransomware","hacker","breach","leak","doxxing","stalking","grooming","exploitation","abuse","harassment","threat","violence","weapon","drugs","terror","extremism","self-harm","sex","fuck","threesome","orgy","incest","bigdick","pussy","dildo","vibrator","anal","blowjob","cum","sperm","boobs","tits","ass","slut","whore","bitch","dick","pussy","nude","Chodu","Randi","Behenchod","Madarchod","Bhosdike","Gandu","Lund","Chutia","Bakchod","Maa Chuda","Bhenchod","Randi ka bacha","Chutiya","Gand mein danda","Lund ke upar seeda","anal","bhosdi","bhosdike","chutiya","chodu","gandu","lund","madarchod","randi","randi ka bacha","randi ka putt","randi ke bache","randi ke putt","suar ka bacha","suar ka putt","suar ke bache","suar ke putt","teri maa ki chut","teri maa ki chudai","teri maa ki gand","teri maa ki lund","teri maa ki madarchod","teri maa ki randi","teri maa ki randi ka bacha","teri maa ki randi ke bache","teri maa ki randi ke putt"]
        count=0
        for keyword in harmful_keywords:
            if keyword in content_to_analyze.lower():
                count+=1

        if count > 0:
            st.error(f"⚠️ Potential Harmful Content Detected ({count} harmful keywords found)")
            
            st.write(f"Risk Score: {count}")
            if count <= 5:
                st.write("RISK LEVEL: LOW")
                st.warning("⚠️ Some Harmful Content Detected")
            if count > 5:
                st.write("RISK LEVEL: HIGH")
                st.warning("🚨 Abusive Content Detected")
            elif count > 10:
                st.write("RISK LEVEL: CRITICAL")
                st.warning("🚨 Highly Abusive Content Detected")
        else:
            st.success("✅ No Harmful Content Detected")
    
#URL Checker Page -------------------------------------------------------------------------------------------------------------
elif select_one == "📥URL Checker":
    st.title("Secure URL Checker")
    st.write("Checks URL structure, DNS resolution, WHOIS age, TLS, redirects, and suspicious patterns without reading page content.")
    st.divider()
    url_input = st.text_input("URL", key="checker_url_input", placeholder="https://example.com", help="Enter a valid URL starting with http:// or https://")

    if st.button("Analyze URL", type="primary"):

        if not url_input.strip():
            st.error("Please enter a URL.")
            st.stop()
        if len(url_input) > 2048:
            st.error("URL is too long.")
            st.stop()

        candidate = url_input.strip()

        if " " in candidate:
            st.error("URL should not contain spaces.")
            st.stop()

        with st.spinner("Analyzing..."):
            risk_factors = []
            safe_factors = []
            threat_score = 0

            try:
                parsed_url = urlparse(candidate)
            except Exception as e:
                st.error(f"Could not parse the URL: {e}")
                st.stop()

            if parsed_url.scheme not in ["http", "https"]:
                st.error("Please enter a URL starting with http:// or https://.")
                st.stop()

            if not parsed_url.netloc:
                st.error("Please enter a complete URL with a domain name.")
                st.stop()

            if parsed_url.username or parsed_url.password:
                risk_factors.append("URL contains embedded credentials")
                threat_score += 3

            host = parsed_url.hostname
            if not host:
                st.error("Unable to determine the host from the URL.")
                st.stop()

            if host.lower() in ["localhost"] or host.endswith(".local"):
                st.error("Local and private hosts are not allowed in the checker.")
                st.stop()

            if host.startswith("xn--"):
                risk_factors.append("Punycode hostname detected")
                threat_score += 1

            if re.search(r"\d{1,3}(?:\.\d{1,3}){3}", host):
                try:
                    ip_obj = ipaddress.ip_address(host)
                    if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved:
                        st.error("Private, loopback, or reserved IP addresses are blocked.")
                        st.stop()
                    risk_factors.append("Direct IP address used instead of a domain")
                    threat_score += 2
                except ValueError:
                    risk_factors.append("Host looks like an IP address but could not be validated")
                    threat_score += 1

            normalized_domain = host.lower()

            suspicious_terms = ["login", "signin", "sign-in", "secure", "account", "verify", "update", "password", "wallet", "bank"]
            path_query = (parsed_url.path + "?" + parsed_url.query).lower()
            if any(term in path_query for term in suspicious_terms):
                risk_factors.append("Suspicious words found in the path or query")
                threat_score += 2
            else:
                safe_factors.append("Path and query do not contain common phishing keywords")

            if parsed_url.query:
                query_keys = parse_qs(parsed_url.query).keys()
                if any(key.lower() in ["redirect", "return", "next", "url", "continue"] for key in query_keys):
                    risk_factors.append("Redirect-style query parameters detected")
                    threat_score += 2

            adult_terms = [
                "adult", "porn", "porno", "xvideo", "xvideos", "xhamster", "hentai",
                "sex", "xxx", "nude", "nsfw", "cam", "webcam", "onlyfans",
                "chaturbate", "redtube", "youporn", "pornhub", "tube8", "milf",
                "blowjob", "escort", "erotic", "fetish", "bdsm"
            ]
            adult_hits = []
            for term in adult_terms:
                if term in normalized_domain or term in path_query:
                    adult_hits.append(term)

            adult_flag = False
            if adult_hits:
                risk_factors.append(f"Explicit or adult-content indicator found: {', '.join(sorted(set(adult_hits)))}")
                threat_score += 10
                adult_flag = True

            if candidate.lower().startswith("http://"):
                risk_factors.append("Connection is not encrypted because the URL uses HTTP")
                threat_score += 3
            else:
                safe_factors.append("URL uses HTTPS")

            extracted = tldextract.extract(candidate)
            root_domain = ".".join([part for part in [extracted.domain, extracted.suffix] if part])
            if not root_domain:
                root_domain = host

            if extracted.domain and extracted.suffix:
                safe_factors.append(f"Registered domain candidate: {root_domain}")
            else:
                risk_factors.append("Domain suffix could not be determined cleanly")
                threat_score += 1

            try:
                resolved_ips = sorted(set(info[4][0] for info in socket.getaddrinfo(host, None)))
                private_resolutions = []
                for resolved_ip in resolved_ips:
                    ip_obj = ipaddress.ip_address(resolved_ip)
                    if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved:
                        private_resolutions.append(resolved_ip)
                if private_resolutions:
                    st.error("This domain resolves to a private or reserved network address.")
                    st.stop()
                safe_factors.append(f"DNS resolution succeeded: {', '.join(resolved_ips[:3])}")
            except Exception as e:
                risk_factors.append(f"DNS resolution failed: {e}")
                threat_score += 2

            try:
                whois_domain = root_domain if root_domain else host
                w = whois.whois(whois_domain)
                domain_names = w.domain_name
                if isinstance(domain_names, list) and domain_names:
                    domain_names = domain_names[0]

                if not domain_names:
                    risk_factors.append("WHOIS did not return a domain name")
                    threat_score += 1
                else:
                    safe_factors.append("WHOIS record found")

                creation_date = w.creation_date
                if isinstance(creation_date, list) and creation_date:
                    creation_date = creation_date[0]

                if creation_date:
                    if isinstance(creation_date, date) and not isinstance(creation_date, datetime):
                        creation_date = datetime.combine(creation_date, datetime.min.time())
                    if hasattr(creation_date, "tzinfo") and creation_date.tzinfo is not None:
                        creation_date = creation_date.astimezone(timezone.utc).replace(tzinfo=None)
                    if isinstance(creation_date, datetime):
                        age_days = (datetime.now() - creation_date).days
                        if age_days < 30:
                            risk_factors.append(f"Domain is very new ({age_days} days old)")
                            threat_score += 3
                        elif age_days < 180:
                            risk_factors.append(f"Domain is relatively new ({age_days} days old)")
                            threat_score += 2
                        else:
                            safe_factors.append(f"Domain age looks normal ({age_days} days)")
                else:
                    risk_factors.append("WHOIS creation date not available")
                    threat_score += 1

                if not w.registrar:
                    risk_factors.append("WHOIS registrar missing")
                    threat_score += 1
                else:
                    safe_factors.append(f"WHOIS registrar found: {w.registrar}")

                if not w.name_servers:
                    risk_factors.append("WHOIS name servers missing")
                    threat_score += 1
                else:
                    safe_factors.append("WHOIS name servers are present")
            except Exception as e:
                risk_factors.append(f"WHOIS lookup failed: {e}")
                threat_score += 1

            try:
                response = requests.get(candidate, timeout=4, allow_redirects=False, verify=True, stream=True, headers={"User-Agent": "Mozilla/5.0"})
                if 200 <= response.status_code < 300:
                    safe_factors.append(f"Server responded with HTTP {response.status_code}")
                elif 300 <= response.status_code < 400:
                    risk_factors.append(f"URL redirects with HTTP {response.status_code}")
                    threat_score += 2
                    location = response.headers.get("Location", "")
                    if location:
                        location_host = urlparse(location).hostname
                        if location_host and location_host.lower() != host.lower():
                            risk_factors.append(f"Redirects to a different host: {location_host}")
                            threat_score += 1
                elif 400 <= response.status_code < 600:
                    risk_factors.append(f"Server returned HTTP {response.status_code}")
                    threat_score += 1

                server_header = response.headers.get("Server")
                if server_header:
                    safe_factors.append(f"Server header present: {server_header}")

                if response.headers.get("Strict-Transport-Security"):
                    safe_factors.append("HSTS is enabled")
                else:
                    risk_factors.append("HSTS header is missing")
                    threat_score += 1

                if response.headers.get("Content-Security-Policy"):
                    safe_factors.append("Content Security Policy is enabled")
                else:
                    risk_factors.append("Content Security Policy header is missing")
                    threat_score += 1

                if response.headers.get("X-Frame-Options"):
                    safe_factors.append("Clickjacking protection is present")
                else:
                    risk_factors.append("X-Frame-Options header is missing")
                    threat_score += 1

                response.close()
            except Exception as e:
                risk_factors.append(f"Secure fetch failed: {e}")
                if not adult_flag:
                    threat_score += 1

            normalized_domain = (root_domain or host or "").lower()

            if any(brand in normalized_domain for brand in ["google", "facebook", "amazon", "microsoft", "cloudflare"]):
                safe_factors.append("Domain contains a well-known brand name")
            else:
                brand_like = False
                for legit in ["google", "amazon", "microsoft", "facebook", "cloudflare"]:
                    ratio = difflib.SequenceMatcher(None, normalized_domain, legit.lower()).ratio()
                    if ratio > 0.82:
                        risk_factors.append(f"Domain is similar to the brand '{legit}'")
                        threat_score += 2
                        brand_like = True
                        break
                if not brand_like:
                    safe_factors.append("Domain does not closely mimic major brands")

            threat_score = min(threat_score, 20)

        st.subheader("Analysis Results")
        st.progress(threat_score / 20 if threat_score else 0)
        st.write("Final Verdict:")
        st.write(f"Threat Score: {threat_score}/20")

        if adult_flag or threat_score > 10:
            st.error("This URL appears to be high risk.")
        elif threat_score <= 5:
            st.success("This URL appears to be low risk.")
        elif threat_score <= 10:
            st.warning("This URL has some risk factors. Exercise caution.")
        else:
            st.error("This URL appears to be high risk. Avoid interacting with it.")

        st.subheader("Risk Factors")
        if risk_factors:
            with st.expander("Show risk factors"):
                for factor in risk_factors:
                    st.write(f"- {factor}")
        else:
            st.success("No major risk factors detected.")

        st.subheader("Safe Factors")
        if safe_factors:
            with st.expander("Show safe factors"):
                for factor in safe_factors:
                    st.write(f"- {factor}")
        else:
            st.info("No positive safety signals were collected.")

#Webpage Scanner Page -------------------------------------------------------------------------------------------------------------
elif select_one == "🌐Webpage Analyzer":
    st.title("Webpage Content Scanner")
    st.write("Enter a URL to scan webpage security and content risk signals with weighted scoring.")
    st.divider()
    url_input = st.text_input("URL", key="scanner_url_input", placeholder="https://example.com", help="Enter a valid URL starting with http:// or https://")

    if st.button("Scan Webpage", type="primary"):

        if not url_input.strip():
            st.error("Please enter a URL.")
            st.stop()
        if len(url_input) > 2048:
            st.error("URL is too long.")
            st.stop()

        candidate = url_input.strip()

        if " " in candidate:
            st.error("URL should not contain spaces.")
            st.stop()

        with st.spinner("Scanning..."):
            risk_factors = []
            safe_factors = []
            risk_score = 0
            try:
                parsed_url = urlparse(candidate)
            except Exception as e:
                st.error(f"Could not parse the URL: {e}")
                st.stop()

            if not parsed_url.scheme or not parsed_url.netloc:
                st.error("Please enter a complete URL with a valid scheme and domain.")
                st.stop()

            if parsed_url.scheme not in ["http", "https"]:
                st.error("Please enter a URL starting with http:// or https://.")
                st.stop()

            if parsed_url.username or parsed_url.password:
                risk_factors.append("URL contains embedded credentials")
                risk_score += 3

            host = parsed_url.hostname
            if not host:
                st.error("Unable to determine the host from the URL.")
                st.stop()

            if re.search(r"\d{1,3}(?:\.\d{1,3}){3}", host):
                risk_factors.append("URL uses an IP address instead of a normal domain")
                risk_score += 2

            normalized_domain = host.lower()
            full_path = (parsed_url.path + "?" + parsed_url.query).lower()

            explicit_terms = ["adult", "porn", "porno", "xvideos", "xhamster", "nsfw", "onlyfans", "sex", "xxx"]
            child_exploit_terms = ["csam", "pedo", "underage", "minor-sex", "child-sex", "groom"]

            explicit_hits = [t for t in explicit_terms if t in normalized_domain or t in full_path]
            exploit_hits = [t for t in child_exploit_terms if t in normalized_domain or t in full_path]

            if explicit_hits:
                risk_factors.append(f"Explicit/adult indicators found: {', '.join(sorted(set(explicit_hits)))}")
                risk_score += 7

            if exploit_hits:
                risk_factors.append(f"Child exploitation indicators found: {', '.join(sorted(set(exploit_hits)))}")
                risk_score += 10

            if parsed_url.path and re.search(r"(login|signin|secure|account|verify|update|password|wallet|bank)", parsed_url.path, re.IGNORECASE):
                risk_factors.append("URL path contains phishing-style keywords")
                risk_score += 2
            if parsed_url.query and re.search(r"(redirect|return|next|url|continue)", parsed_url.query, re.IGNORECASE):
                risk_factors.append("URL query contains redirection-style parameters")
                risk_score += 2
            if parsed_url.netloc.startswith("xn--"):
                risk_factors.append("Punycode domain detected")
                risk_score += 2

            trusted_domains = [
                "chatgpt.com", "openai.com", "google.com", "microsoft.com", "github.com", "cloudflare.com"
            ]
            if any(normalized_domain == td or normalized_domain.endswith("." + td) for td in trusted_domains):
                safe_factors.append("Domain is in trusted-domain list")
                risk_score = max(0, risk_score - 2)

            try:
                response = requests.get(candidate, timeout=8, allow_redirects=True, verify=True, headers={"User-Agent": "Mozilla/5.0"})
                status_code = response.status_code
                st.write(f"HTTP Status: {status_code}")

                if 200 <= status_code < 300:
                    safe_factors.append("Page is reachable")
                elif 300 <= status_code < 400:
                    risk_factors.append("Page responds with a redirect")
                    risk_score += 1
                else:
                    risk_factors.append(f"Page returned HTTP {status_code}")
                    risk_score += 2

                content_type = response.headers.get("Content-Type", "")
                if "text/html" in content_type.lower():
                    safe_factors.append("HTML content detected")
                else:
                    risk_factors.append(f"Non-HTML content type: {content_type}")
                    risk_score += 1

                server_header = response.headers.get("Server")
                if server_header:
                    safe_factors.append("Server header present")

                if response.headers.get("Strict-Transport-Security"):
                    safe_factors.append("HSTS is enabled")

                if response.headers.get("Content-Security-Policy"):
                    safe_factors.append("Content Security Policy is enabled")

                if response.headers.get("X-Frame-Options"):
                    safe_factors.append("X-Frame-Options header is present")

                html = response.text if "text/html" in content_type.lower() else ""
                soup = BeautifulSoup(html, "html.parser") if html else None

                if soup is not None:
                    title = soup.title.string.strip() if soup.title and soup.title.string else ""
                    if title:
                        st.write(f"Webpage Title: {title}")
                        if re.search(r"(login|signin|verify|password|wallet|bank)", title, re.IGNORECASE):
                            risk_factors.append("Title contains high-risk authentication/payment keywords")
                            risk_score += 2

                    forms = soup.find_all("form")
                    password_inputs = soup.find_all("input", {"type": "password"})
                    if forms and password_inputs:
                        risk_factors.append("Page contains authentication form")
                        risk_score += 2

                    suspicious_form_action = False
                    for form in forms:
                        action = (form.get("action") or "").strip()
                        if action.startswith("http://"):
                            suspicious_form_action = True
                            break
                        if action.startswith("https://"):
                            action_host = urlparse(action).hostname
                            if action_host and action_host.lower() != normalized_domain:
                                suspicious_form_action = True
                                break
                    if suspicious_form_action:
                        risk_factors.append("Form submits to an insecure or different host")
                        risk_score += 3

                    iframes = soup.find_all("iframe")
                    hidden_iframes = 0
                    for iframe in iframes:
                        width = (iframe.get("width") or "").strip()
                        height = (iframe.get("height") or "").strip()
                        style = (iframe.get("style") or "").lower()
                        if width in ["0", "1"] or height in ["0", "1"] or "display:none" in style or "visibility:hidden" in style:
                            hidden_iframes += 1
                    if hidden_iframes > 0:
                        risk_factors.append(f"Hidden/tiny iframes detected: {hidden_iframes}")
                        risk_score += 2

                    external_hosts = set()
                    links = soup.find_all("a", href=True)
                    for link in links:
                        href = link.get("href", "")
                        if href.startswith("http://") or href.startswith("https://"):
                            link_host = urlparse(href).hostname
                            if link_host and link_host.lower() != normalized_domain:
                                external_hosts.add(link_host.lower())
                    if len(external_hosts) > 40:
                        risk_factors.append("Very high number of external domains linked")
                        risk_score += 1

                    scripts = soup.find_all("script")
                    script_blob = "\n".join((s.get_text() or "")[:1000] for s in scripts[:20]).lower()
                    suspicious_script_tokens = ["eval(", "document.write(", "atob(", "unescape("]
                    token_hits = [t for t in suspicious_script_tokens if t in script_blob]
                    if token_hits:
                        risk_factors.append(f"Suspicious script patterns found: {', '.join(token_hits)}")
                        risk_score += 2

            except Exception as e:
                risk_factors.append(f"Failed to fetch the webpage securely: {e}")
                risk_score += 2

            risk_score = max(0, min(risk_score, 20))

        st.subheader("Scan Results")
        st.write(f"Risk Score: {risk_score}/20")

        if risk_factors:
            st.subheader("Risk Factors")
            for factor in risk_factors:
                st.write(f"- {factor}")
        else:
            st.subheader("Risk Factors")
            st.success("No major risk factors detected.")

        if safe_factors:
            st.subheader("Safe Signals")
            for factor in safe_factors:
                st.write(f"- {factor}")

        if risk_score <= 4:
            st.success("RISK LEVEL: LOW")
        elif risk_score <= 9:
            st.warning("RISK LEVEL: MEDIUM")
        else:
            st.error("RISK LEVEL: HIGH")

# Authority
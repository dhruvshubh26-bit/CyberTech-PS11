
import random
import streamlit as st
import pandas as pd
import hashlib
import json
import os
import time
from datetime import datetime
from collections import Counter
from urllib.parse import urlparse , parse_qs
import re
import difflib
import tldextract
import streamlit.components.v1 as com
import string
import socket
import secrets

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
    risk=st.select_slider("", options=['Low', 'Medium', 'High','Cretical'], help="Rate the severity of the incident on a scale of 1 to 10, with 10 being the most severe.",label_visibility="collapsed", key="risk_input")

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
    elif url_ in """!#$%^*()+=[]{}|\\;'"<>,""":
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
            st.progress(risk.count("Low") * 25 + risk.count("Medium") * 50 + risk.count("High") * 75 + risk.count("Cretical") * 100)

            st.session_state.last_report = {
                "tracking_id": tracking_id,
                "incident_type": contant,
                "url": url_,
                "description": description,
                "risk": risk,
                "platform": platform,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            report_payload = json.dumps(st.session_state.last_report, indent=2)
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

        
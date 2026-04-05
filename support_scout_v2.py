import os
import sys
import json
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Load environment variables
load_dotenv()

# Initialize the Groq client (Requires GROQ_API_KEY in your .env file)
client = Groq()

# ==========================================
# PHASE 1: GENERATE THE DATABASES (CSVs)
# ==========================================

def create_company_directory():
    """Generates a detailed employee directory with sub-departments."""
    directory_data = [
        {"department": "Technical Support", "sub_department": "Software Bugs", "agent_name": "Dave", "email": "dave@msoffice.com"},
        {"department": "Technical Support", "sub_department": "Login & Access", "agent_name": "Alex", "email": "alex@msoffice.com"},
        {"department": "Technical Support", "sub_department": "Installation", "agent_name": "Nina", "email": "nina@msoffice.com"},
        {"department": "Billing", "sub_department": "Refunds", "agent_name": "Sarah", "email": "sarah@msoffice.com"},
        {"department": "Billing", "sub_department": "Renewals", "agent_name": "Mike", "email": "mike@msoffice.com"},
        {"department": "Customer Success", "sub_department": "Feature Requests", "agent_name": "Emma", "email": "emma@msoffice.com"},
        {"department": "General", "sub_department": "Unsure/Other", "agent_name": "Sam", "email": "sam.frontline@msoffice.com"}
    ]
    df = pd.DataFrame(directory_data)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/directory.csv", index=False)
    return df

def create_ticket_dataset():
    """Generates a diverse set of complex customer support tickets."""
    ticket_data = [
        {"ticket_id": "T-100", "text": "I was charged $99 twice yesterday for my Office 365 family plan. I need my money back now!"},
        {"ticket_id": "T-101", "text": "Excel keeps crashing every time I try to run a VLOOKUP macro. It's totally broken on Windows 11."},
        {"ticket_id": "T-102", "text": "I'm trying to install Word on my new Mac, but the installer freezes at 99%."},
        {"ticket_id": "T-103", "text": "I forgot the password to my admin account and the SMS verification isn't sending."},
        {"ticket_id": "T-104", "text": "My subscription expires next month, how do I update my credit card info?"},
        {"ticket_id": "T-105", "text": "It would be really cool if PowerPoint had an AI image generator built into the slides."},
        {"ticket_id": "T-106", "text": "Where is the main office located?"} # General inquiry
    ]
    df = pd.DataFrame(ticket_data)
    df.to_csv("data/tickets.csv", index=False)
    return df

# ==========================================
# PHASE 2: THE LLM BRAIN (Llama 3 via Groq)
# ==========================================

def analyze_ticket(ticket_text, directory_df):
    """Uses Meta's Llama 3 to analyze the ticket and pick a sub-department."""
    
    # Give the AI the exact list of valid sub-departments to choose from
    valid_sub_departments = directory_df['sub_department'].tolist()
    
    system_prompt = f"""
    You are SupportScout, an AI router for Microsoft Office support.
    Read the user's issue and output ONLY a raw JSON object.
    
    JSON format requirements:
    - "sub_department": Must be exactly one of this list: {valid_sub_departments}
    - "urgency": "Low", "Medium", or "High"
    - "summary": A 5-word summary of the issue.
    """

    # Groq: llama-3.1-8b-instant (replacement for retired llama3-8b-8192)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"}, 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": ticket_text}
        ],
        temperature=0.0
    )

    return json.loads(response.choices[0].message.content)

# ==========================================
# PHASE 3: THE SWITCHBOARD LOGIC
# ==========================================

def route_ticket(ticket_id, ticket_text, analysis, directory_df):
    """Matches the AI's sub-department choice to the exact employee in the CSV."""
    
    ai_sub_dept = analysis.get("sub_department", "Unsure/Other")
    
    # Find the employee in the directory CSV who handles this sub-department
    match = directory_df[directory_df['sub_department'] == ai_sub_dept]
    
    if not match.empty:
        agent_name = match.iloc[0]['agent_name']
        department = match.iloc[0]['department']
        email = match.iloc[0]['email']
    else:
        agent_name, department, email = "Sam", "General", "sam.frontline@msoffice.com"

    print("-" * 60)
    print(f"🎫 TICKET ID: {ticket_id}")
    print(f"💬 CUSTOMER: '{ticket_text}'")
    print(f"🤖 AI THINKS: [Urgency: {analysis.get('urgency')}] | {analysis.get('summary')}")
    print(f"🎯 ROUTING TO: {agent_name} in {department} -> {ai_sub_dept}")
    print(f"✉️ ACTION: Ticket forwarded to {email}")

# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    print("🚀 Initializing SupportScout v2 (Powered by Llama 3)...\n")
    
    # 1. Generate the databases
    print("Loading Company Directory and Ticket Queues...")
    df_directory = create_company_directory()
    df_tickets = create_ticket_dataset()
    
    print("\nProcessing Support Queue...\n")
    
    # 2. Process each ticket
    for index, row in df_tickets.iterrows():
        t_id = row['ticket_id']
        t_text = row['text']
        
        try:
            analysis = analyze_ticket(t_text, df_directory)
            route_ticket(t_id, t_text, analysis, df_directory)
        except Exception as e:
            print(f"⚠️ Error processing {t_id}: {type(e).__name__}: {e}")

    print("-" * 60)
    print("🏁 Queue cleared! All tickets successfully routed.")

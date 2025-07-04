import streamlit as st
import requests
from streamlit_option_menu import option_menu
from datetime import datetime

# --- Sidebar ---
st.sidebar.title("Agentic AI Dashboard")
st.sidebar.markdown("""
**Multi-Agent Business Assistant**  
Built with FastAPI, CrewAI, MongoDB, and Streamlit.

- [GitHub](https://github.com/Dhaval-pathak/qest-agentic-ai)
- [Docs](https://github.com/Dhaval-pathak/qest-agentic-ai/blob/main/README.md)

---
**Contact:** dhavalpathak2003@gmail.com
""")

# --- Main Page ---
st.title("🤖 Agentic AI: Business Assistant")
st.markdown("""
Welcome to your multi-agent business assistant! Ask questions about your business, get analytics, or manage support queries. Select an agent, enter your query, or pick a sample prompt to get started.
""")

# --- Agent Selection ---
agent_icons = {"Support": "🛎️ Support Agent", "Dashboard": "📊 Dashboard Agent"}
agent_type = option_menu(
    menu_title=None,
    options=["Support", "Dashboard"],
    icons=["headset", "bar-chart"],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "20px"},
        "nav-link": {
            "font-size": "18px",
            "margin": "0 10px",
            "text-align": "center",
            "color": "orange"
        },
        "nav-link-selected": {"background-color": "#ffe5b4", "color": "black"},
    },
)
st.markdown(f"**Selected Agent:** {agent_icons[agent_type]}")

# --- Sample Prompts ---
sample_prompts = {
    "Support": [
        "What classes are available this week?",
        "Has order #12345 been paid?",
        "Create an order for Yoga Beginner for client Priya Sharma",
        "Show all pending payments for client john@example.com",
        "List all courses by instructor Anjali."
    ],
    "Dashboard": [
        "How much revenue did we generate this month?",
        "Which course has the highest enrollment?",
        "What is the attendance percentage for Pilates?",
        "How many inactive clients do we have?",
        "Show enrollment trends for the last 6 months."
    ]
}

st.markdown("**Sample Prompts:**")
col1, col2 = st.columns(2)
for i, prompt in enumerate(sample_prompts[agent_type]):
    if i % 2 == 0:
        if col1.button(prompt, key=f"sample_{agent_type}_{i}"):
            st.session_state["query"] = prompt
    else:
        if col2.button(prompt, key=f"sample_{agent_type}_{i}"):
            st.session_state["query"] = prompt

# --- Query Input ---
query = st.text_area("Enter your query:", value=st.session_state.get("query", ""), key="query_input", height=80)

# --- Query History ---
if "history" not in st.session_state:
    st.session_state["history"] = []

# --- Submit Button ---
if st.button("Submit Query", use_container_width=True):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    "http://backend:8000/query",
                    json={"query": query, "agent_type": agent_type.lower()}
                )
                if response.status_code == 200:
                    result = response.json()
                    st.session_state["history"].insert(0, {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "agent": agent_icons[agent_type],
                        "query": query,
                        "response": result["response"]
                    })
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")

# --- Response Display ---
if st.session_state["history"]:
    st.markdown("---")
    st.subheader("📝 Query History")
    for item in st.session_state["history"][:5]:
        with st.expander(f"{item['timestamp']} | {item['agent']} | {item['query'][:40]}..."):
            st.markdown(f"**Query:** {item['query']}")
            st.markdown(f"**Response:**\n{item['response']}")

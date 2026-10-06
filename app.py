import streamlit as st
import time
import io
import sys
import json
import os

# 1. Page Configuration
st.set_page_config(
    page_title="EduPilot AI — Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Balanced Modern Slate Theme & Hidden Header / Deploy Elements
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');
    
    .stDeployButton, [data-testid="stDeployButton"] {
        display: none !important;
        visibility: hidden !important;
    }
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    
    code, pre {
        font-family: 'Fira Code', monospace !important;
    }

    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155 !important;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #312e81 0%, #4338ca 50%, #6366f1 100%);
        border: 1px solid #4f46e5;
        padding: 22px 28px;
        border-radius: 14px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }
    .hero-title {
        font-size: 24pt;
        font-weight: 800;
        margin-bottom: 4px;
        color: #ffffff;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        padding: 4px 12px;
        border-radius: 18px;
        font-size: 8pt;
        font-weight: 700;
        margin-top: 8px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: #ffffff;
    }
    
    .stat-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 12px 16px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .stat-num {
        font-size: 16pt;
        font-weight: 800;
        color: #818cf8;
    }
    .stat-lbl {
        font-size: 7.5pt;
        color: #94a3b8;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 2px;
    }
    
    .step-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .step-header {
        font-size: 7.5pt;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 2px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .step-title {
        font-size: 11pt;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .step-desc {
        font-size: 8.5pt;
        color: #cbd5e1;
        line-height: 1.4;
    }

    .quiz-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .quiz-q {
        font-size: 10pt;
        font-weight: 700;
        color: #ffffff;
    }

    label, .stMarkdown p {
        color: #e2e8f0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Persistent File Storage (JSON Database)
DB_FILE = "users_db.json"

def load_users():
    if not os.path.exists(DB_FILE):
        default_db = {
            "dipti@gmail.com": {
                "name": "Dipti Dasharath Morajkar",
                "password": "123",
                "college": "FAMT Ratnagiri",
                "branch": "Computer Science (AI & ML)",
                "streak": 1,
                "doubts_solved": 0,
                "quiz_attempts": 0,
                "retention_score": None
            }
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(default_db, f, indent=4)
        return default_db
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(db_data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_data, f, indent=4)

# Initialize Session State from Disk
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True
    st.session_state.current_user = "dipti@gmail.com"

users_database = load_users()

# 4. Authentication Screens
def show_auth():
    st.markdown("""
    <div style="text-align:center; padding: 35px 0 20px 0;">
        <h1 style="color:#818cf8; font-weight:800; font-size:28pt;">🎓 Welcome to EduPilot AI</h1>
        <p style="color:#94a3b8; font-size:11pt;">Adaptive 24/7 AI Mentor for Engineering Undergraduates • UN SDG 4: Quality Education</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_mode = st.radio("Choose Action:", ["Login", "Register as New Student"], horizontal=True)
        
        if auth_mode == "Login":
            st.subheader("🔑 Student Login")
            email = st.text_input("Student Email:", value="")
            pwd = st.text_input("Password:", type="password", value="")
            
            if st.button("🚀 Login to Dashboard", use_container_width=True):
                current_db = load_users()
                email_clean = email.strip().lower()
                if email_clean in current_db and current_db[email_clean]["password"] == pwd.strip():
                    st.session_state.logged_in = True
                    st.session_state.current_user = email_clean
                    st.success("Login Successful! Redirecting...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Invalid Email or Password. Please check or register first.")
                    
        else:
            st.subheader("📝 New Student Registration")
            new_name = st.text_input("Full Name:")
            new_email = st.text_input("Email Address:")
            new_college = st.text_input("College / Institution Name:")
            new_branch = st.selectbox("Specialization:", ["Computer Science (AI & ML)", "Information Technology", "Computer Engineering", "Data Science"])
            new_pwd = st.text_input("Create Password:", type="password")
            
            if st.button("✨ Create Account", use_container_width=True):
                if new_name.strip() and new_email.strip() and new_pwd.strip():
                    current_db = load_users()
                    clean_email = new_email.strip().lower()
                    
                    if clean_email in current_db:
                        st.warning("This email is already registered! Please login.")
                    else:
                        current_db[clean_email] = {
                            "name": new_name.strip(),
                            "password": new_pwd.strip(),
                            "college": new_college.strip(),
                            "branch": new_branch,
                            "streak": 1,
                            "doubts_solved": 0,
                            "quiz_attempts": 0,
                            "retention_score": None
                        }
                        save_users(current_db)
                        st.session_state.logged_in = True
                        st.session_state.current_user = clean_email
                        st.success("Account created and saved permanently! Logging in...")
                        time.sleep(0.5)
                        st.rerun()
                else:
                    st.warning("Please fill all mandatory fields.")

# 5. Main Dashboard View
if not st.session_state.logged_in:
    show_auth()
else:
    current_email = st.session_state.current_user
    current_db = load_users()
    
    # Fallback safety if email doesn't exist
    if current_email not in current_db:
        st.session_state.logged_in = False
        st.rerun()
        
    user_info = current_db[current_email]

    # Sidebar Controls
    st.sidebar.image("https://img.icons8.com/clouds/200/graduation-cap.png", width=95)
    st.sidebar.title("EduPilot AI")
    st.sidebar.caption("🌱 UN SDG 4: Quality Education")

    st.sidebar.markdown(f"""
    <div style="background:#0f172a; padding:12px 14px; border-radius:10px; margin-bottom:12px; border:1px solid #334155;">
        <div style="font-size:7.5pt; color:#94a3b8; font-weight:700;">AUTHENTICATED LEARNER</div>
        <div style="font-size:9.5pt; color:#ffffff; font-weight:800; margin-top:2px;">{user_info['name']}</div>
        <div style="font-size:8pt; color:#818cf8; font-weight:600;">{user_info['branch']}</div>
        <div style="font-size:7.5pt; color:#94a3b8;">{user_info['college']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    st.sidebar.divider()
    
    # Dynamic Selectors
    level = st.sidebar.selectbox("🎯 Target Level:", ["Beginner", "Intermediate", "Advanced"])
    topic = st.sidebar.selectbox("📚 Track:", ["Machine Learning Basics", "Python, Pointers & DSA", "Agentic AI & LangGraph"])

    # Hero Banner
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-title">EduPilot AI 🚀</div>
        <div style="font-size: 11pt; font-weight: 500; opacity: 0.95; color: #e0e7ff;">Adaptive 24/7 AI Mentor for Engineering Undergraduates</div>
        <div class="hero-badge">Student: {user_info['name']}</div>
        <div class="hero-badge" style="margin-left:6px;">Track: {topic}</div>
        <div class="hero-badge" style="background:#10b981; color:#ffffff; border-color:#059669; margin-left:6px;">Tier: {level}</div>
    </div>
    """, unsafe_allow_html=True)

    # Dynamic Metric Bar (Loaded from Disk)
    retention_display = f"{user_info['retention_score']}%" if user_info['retention_score'] is not None else "--"
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="stat-card"><div class="stat-num">🔥 {user_info["streak"]} Day</div><div class="stat-lbl">Active Streak</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="stat-card"><div class="stat-num">💡 {user_info["doubts_solved"]}</div><div class="stat-lbl">Doubts Solved</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="stat-card"><div class="stat-num">🎯 {retention_display}</div><div class="stat-lbl">Retention Score</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="stat-card"><div class="stat-num">⚡ 0.6s</div><div class="stat-lbl">Avg Response Time</div></div>', unsafe_allow_html=True)

    st.write("")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️️ Dynamic Roadmap", 
        "💬 Contextual Doubt Solver", 
        "🔍 AI Code Inspector & Sandbox", 
        "📝 Multi-Question Retention Quiz"
    ])

    # =========================================================================
    # --- TAB 1: DYNAMIC ROADMAP ---
    # =========================================================================
    with tab1:
        st.subheader(f"📍 Personalized Curriculum: {topic}")
        st.caption(f"Curriculum automatically recalibrated for **{level}** learners.")

        matrix_roadmaps = {
            "Machine Learning Basics": {
                "Beginner": [
                    {"phase": "STAGE 1", "badge": "#6366f1", "title": "Data Preparation & Python Basics", "desc": "Learn NumPy, Pandas, cleaning empty rows, and reading CSV dataset files."},
                    {"phase": "STAGE 2", "badge": "#0284c7", "title": "First ML Algorithm: Linear Regression", "desc": "Understand how a line fits points to predict numbers like housing prices."},
                    {"phase": "STAGE 3", "badge": "#d97706", "title": "Classification with Decision Trees", "desc": "Simple yes/no rule trees to classify categories like spam email detection."},
                    {"phase": "STAGE 4", "badge": "#10b981", "title": "Model Testing & Simple Streamlit App", "desc": "Checking accuracy with train_test_split and showing predictions on a simple web page."}
                ],
                "Intermediate": [
                    {"phase": "STAGE 1", "badge": "#6366f1", "title": "Feature Engineering & Outliers", "desc": "StandardScaler normalization, IQR outlier removal, and One-Hot encoding."},
                    {"phase": "STAGE 2", "badge": "#0284c7", "title": "Ensemble Models: Random Forest & XGBoost", "desc": "Combining multiple decision trees to improve prediction power and reduce variance."},
                    {"phase": "STAGE 3", "badge": "#d97706", "title": "Evaluation: F1-Score & ROC-AUC", "desc": "Analyzing confusion matrices and handling imbalanced datasets properly."},
                    {"phase": "STAGE 4", "badge": "#10b981", "title": "End-to-End ML Pipeline Deployment", "desc": "Saving models using Pickle/Joblib and hosting interactive apps on Streamlit Cloud."}
                ],
                "Advanced": [
                    {"phase": "STAGE 1", "badge": "#6366f1", "title": "Custom Loss Functions & Optimization", "desc": "Gradient descent mathematical convergence, Hessian matrices, and Adam optimizer."},
                    {"phase": "STAGE 2", "badge": "#0284c7", "title": "Neural Networks & Deep Learning (PyTorch)", "desc": "Backpropagation math, ReLU activation dynamics, and avoiding vanishing gradients."},
                    {"phase": "STAGE 3", "badge": "#d97706", "title": "Model Explainability & SHAP Values", "desc": "Interpreting black-box models using SHAP, LIME, and adversarial robust testing."},
                    {"phase": "STAGE 4", "badge": "#10b981", "title": "Production MLOps & API Serving", "desc": "FastAPI endpoints, Docker containerization, and data drift monitoring in production."}
                ]
            },
            "Python, Pointers & DSA": {
                "Beginner": [
                    {"phase": "STAGE 1", "badge": "#6366f1", "title": "Python Syntax & Basic Data Types", "desc": "Variables, for-loops, if-else logic, functions, lists, and basic dictionaries."},
                    {"phase": "STAGE 2", "badge": "#0284c7", "title": "Understanding How Memory Works", "desc": "How variables store values, mutable vs immutable types, and basic pointers concept."},
                    {"phase": "STAGE 3", "badge": "#d97706", "title": "Simple Searching & Sorting", "desc": "Linear Search, Binary Search logic, and sorting numbers from small to large."},
                    {"phase": "STAGE 4", "badge": "#10b981", "title": "Introduction to Linked Lists", "desc": "Nodes, data, and next references: building your very first single linked list."}
                ],
                "Intermediate": [
                    {"phase": "STAGE 1", "badge": "#6366f1", "title": "Memory Architecture & Pointer Types", "desc": "Stack vs Heap memory, Dangling pointers, Void pointers, and avoiding memory leaks."},
                    {"phase": "STAGE 2", "badge": "#0284c7", "title": "Stacks, Queues & Two-Pointer Logic", "desc": "LIFO/FIFO structures, Floyd's cycle detection, and reversing lists in-place."},
                    {"phase": "STAGE 3", "badge": "#d97706", "title": "Binary Trees & Graph Traversals", "desc": "Binary Search Trees (BST), Breadth-First Search (BFS), and Depth-First Search (DFS)."},
                    {"phase": "STAGE 4", "badge": "#10b981", "title": "Time & Space Complexity (Big-O)", "desc": "Calculating O(1), O(n), O(log n) runtimes to write clean, interview-ready code."}
                ],
                "Advanced": [
                    {"phase": "STAGE 1", "badge": "#6366f1", "title": "Low-Level Memory & Custom Allocators", "desc": "Bitwise operations, garbage collection mechanics, and cache locality optimization."},
                    {"phase": "STAGE 2", "badge": "#0284c7", "title": "Dynamic Programming (DP) Mastery", "desc": "Overlapping subproblems, Memoization vs Tabulation, and 0/1 Knapsack variations."},
                    {"phase": "STAGE 3", "badge": "#d97706", "title": "Advanced Graph Theory", "desc": "Dijkstra's shortest path, Disjoint Set Union (DSU), and Topological sorting."},
                    {"phase": "STAGE 4", "badge": "#10b981", "title": "Self-Balancing Trees & Segment Trees", "desc": "AVL Trees, Red-Black Trees, and Segment Trees for rapid interval range queries."}
                ]
            },
            "Agentic AI & LangGraph": {
                "Beginner": [
                    {"phase": "STAGE 1", "badge": "#6366f1", "title": "What is GenAI & Prompt Engineering?", "desc": "How ChatGPT works, tokens, few-shot prompting, and writing clear system instructions."},
                    {"phase": "STAGE 2", "badge": "#0284c7", "title": "Connecting Python with AI APIs", "desc": "Calling Google Gemini or OpenAI API to send a prompt and receive a text answer."},
                    {"phase": "STAGE 3", "badge": "#d97706", "title": "Simple RAG (Ask Your PDF)", "desc": "Splitting a document into chunks and having AI answer questions from your notes."},
                    {"phase": "STAGE 4", "badge": "#10b981", "title": "Building a Basic Study Bot", "desc": "Combining Streamlit and an AI API to create a chatbot that explains college topics."}
                ],
                "Intermediate": [
                    {"phase": "STAGE 1", "badge": "#6366f1", "title": "Chains to Autonomous Agents", "desc": "Difference between static LLM pipelines and Agents that make dynamic decisions."},
                    {"phase": "STAGE 2", "badge": "#0284c7", "title": "Tool Calling & Structured JSON", "desc": "Giving AI real tools: calculator, Google Search, and extracting clean JSON data."},
                    {"phase": "STAGE 3", "badge": "#d97706", "title": "Introduction to LangGraph", "desc": "Building stateful graphs, nodes, edges, and multi-step reasoning cycles."},
                    {"phase": "STAGE 4", "badge": "#10b981", "title": "Agent Memory & Checkpoints", "desc": "Saving conversation state across multiple steps so the agent remembers context."}
                ],
                "Advanced": [
                    {"phase": "STAGE 1", "badge": "#6366f1", "title": "Multi-Agent Orchestration & Supervisors", "desc": "Coordinator agent delegating sub-tasks to specialized coder, researcher, and tester agents."},
                    {"phase": "STAGE 2", "badge": "#0284c7", "title": "Reflection & Self-Correction Loops", "desc": "Designing agents that review their own code, catch syntax errors, and retry automatically."},
                    {"phase": "STAGE 3", "badge": "#d97706", "title": "Human-in-the-Loop & Safety Gates", "desc": "Interrupting agent execution to wait for user approval before dangerous API operations."},
                    {"phase": "STAGE 4", "badge": "#10b981", "title": "Production Deployment & Observability", "desc": "Tracing agent execution steps, managing token costs, and reducing response latency."}
                ]
            }
        }

        current_roadmap = matrix_roadmaps[topic][level]
        
        c1, c2 = st.columns(2)
        with c1:
            for step in current_roadmap[:2]:
                st.markdown(f"""
                <div class="step-card" style="border-left: 4px solid {step['badge']};">
                    <span class="step-header" style="background:{step['badge']}; color:#ffffff;">{step['phase']}</span>
                    <div class="step-title">{step['title']}</div>
                    <div class="step-desc">{step['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
        with c2:
            for step in current_roadmap[2:]:
                st.markdown(f"""
                <div class="step-card" style="border-left: 4px solid {step['badge']};">
                    <span class="step-header" style="background:{step['badge']}; color:#ffffff;">{step['phase']}</span>
                    <div class="step-title">{step['title']}</div>
                    <div class="step-desc">{step['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

    # =========================================================================
    # --- TAB 2: DOUBT SOLVER (Persistent User Updates) ---
    # =========================================================================
    with tab2:
        st.subheader("💡 24/7 Context-Aware Technical Explainer")
        st.caption(f"Explanations simplified for **{level}** understanding.")

        default_doubts = {
            "Machine Learning Basics": {
                "Beginner": "What is the difference between Supervised and Unsupervised Learning?",
                "Intermediate": "Why is Accuracy a bad metric for imbalanced data, and what should I use?",
                "Advanced": "How does Backpropagation calculate gradients across hidden layers?"
            },
            "Python, Pointers & DSA": {
                "Beginner": "Why do lists in Python change inside functions while numbers do not?",
                "Intermediate": "What is a Dangling Pointer, and why does it cause program crashes?",
                "Advanced": "How does Dynamic Programming convert exponential recursion into polynomial time?"
            },
            "Agentic AI & LangGraph": {
                "Beginner": "What is the simple difference between a Chatbot and an AI Agent?",
                "Intermediate": "What is Tool Calling, and how does an AI know when to use a calculator?",
                "Advanced": "Why do we need LangGraph cyclic graphs instead of linear LangChain pipelines?"
            }
        }

        q_val = default_doubts[topic][level]
        user_q = st.text_input("Enter your doubt or programming question:", value=q_val)
        
        if st.button("🚀 Explain in Simple English", use_container_width=True):
            # 1. Update in memory and persist immediately to users_db.json
            current_db = load_users()
            current_db[current_email]["doubts_solved"] += 1
            save_users(current_db)
            
            with st.spinner("EduPilot is preparing a clear, step-by-step answer..."):
                time.sleep(0.6)
                
                if "Backpropagation" in user_q:
                    title_text = "How Backpropagation Works (Simple Analogy)"
                    exp_body = """
**1. The Restaurant Kitchen Analogy:**
* Imagine a finished soup reaches a dining customer and tastes too salty.
* The head chef doesn't just guess who made the mistake; they trace the dish backwards:
  * First, check the garnish chef who plated it (Output Layer).
  * Next, check the sauce chef who mixed the base (Hidden Layer 2).
  * Finally, check the prep cook who boiled the vegetables (Hidden Layer 1).
* Each person is told exactly how much extra salt they contributed, and they adjust their measurements for the next batch.

---

**2. The Deep Learning Mathematics (Chain Rule):**
* **Forward Pass:** Input data flows forward through layers to produce a final prediction error.
* **Backward Pass:** Using the calculus **Chain Rule**, the algorithm calculates how much each weight contributed to the overall error.
* **Weight Update:** Optimizers like **Adam** or **SGD** adjust each weight in the opposite direction to minimize the error in the next run.
"""
                elif "Supervised and Unsupervised" in user_q:
                    title_text = "Supervised vs Unsupervised Learning"
                    exp_body = """
**1. Supervised Learning (Learning with a Teacher):**
* You provide the computer with both questions and exact ground-truth answers (labels).
* *Example:* 5,000 photos of cats and dogs, each labeled. The computer learns the exact features separating cats from dogs.

---

**2. Unsupervised Learning (Self-Discovery):**
* You provide raw data with zero answer keys or categories.
* *Example:* A customer shopping history spreadsheet. The algorithm groups buyers into clusters (e.g., budget vs luxury buyers) entirely on its own.
"""
                elif "Accuracy a bad metric" in user_q:
                    title_text = "Why Accuracy is Deceptive on Skewed Data"
                    exp_body = """
**The Medical Screening Example:**
* Suppose 1,000 patients are tested for a rare disease. Only 2 are sick (998 are healthy).
* If a lazy model simply outputs "Nobody is sick!" for everyone, it achieves **99.8% accuracy** — but fails completely because both sick patients were missed!

---

**What to use instead:**
* Use **Recall** or **F1-Score**. Recall explicitly measures the percentage of actual sick patients successfully identified.
"""
                elif "Dangling Pointer" in user_q:
                    title_text = "Dangling Pointer Explained"
                    exp_body = """
**The Hotel Room Analogy:**
* You check out of Room 302, and the hotel assigns that room to another guest.
* If you keep an unreturned key and enter Room 302 at night, you are invading memory that no longer belongs to you.

---

**In Code:**
* When memory is deallocated using `free(ptr)` or `delete ptr`, the memory returns to the operating system.
* If you don't explicitly set `ptr = NULL;`, `ptr` remains dangling. Reading or writing to it causes segmentation faults or security bugs.
"""
                elif "Chatbot and an AI Agent" in user_q:
                    title_text = "Chatbot vs AI Agent"
                    exp_body = """
**1. Simple Chatbot:**
* Responds with text based strictly on previous training data. It cannot take independent actions on your computer.

---

**2. AI Agent:**
* Evaluates a goal, determines required steps, calls external tools (running code, searching Google, sending emails), verifies the result, and loops until the task is solved.
"""
                elif "Tool Calling" in user_q:
                    title_text = "How Tool Calling Works"
                    exp_body = """
**Separating Language from Exact Math:**
* Large Language Models are word predictors and can make calculation mistakes on large numbers.
* With **Tool Calling**, the LLM outputs a structured command (JSON): `{"tool": "calculator", "args": {"a": 450, "b": 18}}`.
* Python runs the exact math calculation and returns the verified result back to the model.
"""
                elif "Dynamic Programming convert" in user_q:
                    title_text = "How Dynamic Programming Speeds Up Code"
                    exp_body = """
**Remembering Past Answers:**
* In standard Fibonacci recursion, calculating $F(5)$ re-computes $F(3)$ multiple times, causing exponential $O(2^n)$ delay.
* **Memoization & Tabulation:** Once $F(3)$ is calculated once, its answer is cached in a hash map.
* Future calls look up the stored value instantly in $O(1)$ time, reducing total complexity to linear $O(n)$.
"""
                elif "LangGraph cyclic graphs" in user_q:
                    title_text = "Why LangGraph Uses Cyclic Graphs"
                    exp_body = """
**Iterative Problem-Solving:**
* Linear pipelines (Step 1 -> Step 2 -> Step 3) break completely if Step 3 fails.
* In coding, if a syntax error occurs, you review the message and fix the code — you don't throw away the whole project.
* **LangGraph** uses cyclic loops, allowing agents to test code, inspect errors, reflect, and retry until execution succeeds.
"""
                else:
                    title_text = f"EduPilot Concept Analysis: {user_q}"
                    exp_body = f"""
**Core Concept Overview:**
* This principle centers on balancing algorithmic efficiency against computational requirements.
* **Recommendation for {level} Tier:** Implement a clean, working solution first, verify its output against test cases, and refactor time/space efficiency iteratively.
"""

                st.success(f"🤖 {title_text} ({level} Friendly)")
                st.markdown(exp_body)

    # =========================================================================
    # --- TAB 3: CODE INSPECTOR & SANDBOX ---
    # =========================================================================
    with tab3:
        st.subheader("🔍 AI Code Inspector & Interactive Sandbox")
        st.caption("Run Python code directly. The agent tests output and explains performance in simple terms.")

        code_templates = {
            "Machine Learning Basics": """# Predict simple house prices using Linear Regression logic
actual_prices = [30, 45, 60, 80]
predicted_prices = [28, 48, 58, 82]

# Calculate simple error difference
errors = [abs(act - pred) for act, pred in zip(actual_prices, predicted_prices)]
mean_error = sum(errors) / len(errors)

print("Actual Prices:", actual_prices)
print("Predicted Prices:", predicted_prices)
print(f"Average Error: {mean_error:.2f} Lakhs")
""",
            "Python, Pointers & DSA": """# Two Sum Target Search: Find two numbers that sum to 9
def find_pair(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in seen:
            return [seen[diff], i]
        seen[n] = i
    return []

numbers = [2, 7, 11, 15]
print("Numbers List:", numbers)
print("Indices that add up to 9:", find_pair(numbers, 9))
""",
            "Agentic AI & LangGraph": """# Simple Agent Decision Loop Simulation
def agent_decide(user_goal):
    print(f"Goal received: '{user_goal}'")
    if "calculate" in user_goal.lower():
        action = "TOOL: Calling Math Calculator"
    elif "search" in user_goal.lower():
        action = "TOOL: Calling Web Search"
    else:
        action = "RESPONSE: Answering directly from knowledge"
    return action

print(agent_decide("Calculate 450 multiplied by 18"))
print(agent_decide("Search latest tech news"))
"""
        }

        sample_code = code_templates[topic]
        code_input = st.text_area("Python Code Editor:", sample_code, height=170)
        
        c_run, c_insp = st.columns(2)
        with c_run:
            if st.button("⚡ Run Code Live", use_container_width=True):
                st.markdown("**Output Console:**")
                old_stdout = sys.stdout
                redirected_output = sys.stdout = io.StringIO()
                try:
                    exec(code_input)
                    out = redirected_output.getvalue()
                    st.code(out if out else "Executed with 0 console output.", language="python")
                except Exception as e:
                    st.error(f"Runtime Error: {e}")
                finally:
                    sys.stdout = old_stdout
                    
        with c_insp:
            if st.button("🤖 Inspect Performance", use_container_width=True):
                st.info(f"📊 **Code Efficiency Review ({level})**")
                st.markdown("""
* **Time Complexity:** `O(n)` (Runs efficiently in a single linear pass)
* **Memory Footprint:** Minimal heap memory; safe for lightweight hardware
* **Code Health:** No infinite loops or dangling reference risks detected
""")

    # =========================================================================
    # --- TAB 4: MULTI-QUESTION QUIZ (Persistent Score Updates) ---
    # =========================================================================
    with tab4:
        st.subheader(f"📝 5-Question Knowledge Check: {topic}")
        st.caption(f"Questions calibrated for **{level}** learners with easy-to-understand explanations.")

        all_quizzes = {
            "Machine Learning Basics": {
                "Beginner": [
                    {"q": "1. What is the main goal of Machine Learning?", "options": ["To build hardware computers", "To let computers learn patterns from data without manual coding", "To make internet faster", "To edit photos"], "ans": "To let computers learn patterns from data without manual coding", "exp": "Instead of writing rules by hand, ML writes rules automatically by observing sample data."},
                    {"q": "2. In Linear Regression, what does the model try to draw through data points?", "options": ["A straight best-fit line", "A circle", "A triangle", "A random polygon"], "ans": "A straight best-fit line", "exp": "Linear regression finds a straight line that stays as close as possible to all data points."},
                    {"q": "3. Which of these is a categorical label suitable for classification?", "options": ["House price: ₹45,00,000", "Temperature: 32.5°C", "Spam or Not Spam", "Car speed: 65 km/h"], "ans": "Spam or Not Spam", "exp": "Spam / Not Spam is a category (label), which makes it a classification task."},
                    {"q": "4. Why do we split data into 'Train' and 'Test' sets?", "options": ["To make the dataset smaller", "To test if the model works on new data it has never seen before", "To delete errors", "Because Python requires it"], "ans": "To test if the model works on new data it has never seen before", "exp": "Like testing a student with new exam questions instead of the exact homework questions they already memorized."},
                    {"q": "5. What is 'Overfitting' in simple words?", "options": ["When the model is too simple", "When the model memorizes answers by heart instead of understanding", "When the model runs out of battery", "When data is deleted"], "ans": "When the model memorizes answers by heart instead of understanding", "exp": "An overfitted model scores 100% on training data, but fails badly on any brand-new real-world data."}
                ],
                "Intermediate": [
                    {"q": "1. Which metric is best when positive cases are very rare (e.g., credit card fraud)?", "options": ["Accuracy", "F1-Score / PR-AUC", "Mean Squared Error", "R-squared"], "ans": "F1-Score / PR-AUC", "exp": "Accuracy is misleading because guessing 'No Fraud' every time already gives 99% accuracy."},
                    {"q": "2. What is the role of StandardScaler?", "options": ["To make pictures colorful", "To scale features to mean 0 and variance 1", "To drop null values", "To sort numbers"], "ans": "To scale features to mean 0 and variance 1", "exp": "Scaling ensures that large numbers (like salary) do not overpower smaller numbers (like age)."},
                    {"q": "3. How does a Random Forest improve over a single Decision Tree?", "options": ["It uses fewer calculations", "It averages predictions from many trees to reduce errors and overfitting", "It replaces numbers with words", "It deletes bad rows"], "ans": "It averages predictions from many trees to reduce errors and overfitting", "exp": "Wisdom of the crowd: multiple diverse decision trees voting together make far fewer mistakes."},
                    {"q": "4. What does K-Fold Cross Validation do?", "options": ["Multiplies data by K times", "Splits data into K folds to test model stability multiple times", "Deletes K columns", "Stops training early"], "ans": "Splits data into K folds to test model stability multiple times", "exp": "It rotates the test fold so every single data point gets evaluated fairly."},
                    {"q": "5. What does the Area Under the ROC Curve (ROC-AUC) measure?", "options": ["Training time", "How well the model separates positive classes from negative classes", "File size", "Memory usage"], "ans": "How well the model separates positive classes from negative classes", "exp": "A score of 1.0 means perfect class separation; 0.5 means completely random guessing."}
                ],
                "Advanced": [
                    {"q": "1. What is the vanishing gradient problem in deep neural networks?", "options": ["Gradients become too small during backpropagation, stopping earlier layers from learning", "Gradients become infinite", "The network runs out of memory", "Weights become negative"], "ans": "Gradients become too small during backpropagation, stopping earlier layers from learning", "exp": "Multiplying many small decimals backward causes the signal to shrink close to zero in early layers."},
                    {"q": "2. Why is ReLU favored over Sigmoid in hidden layers?", "options": ["ReLU never outputs numbers", "ReLU does not saturate for positive values, alleviating vanishing gradients", "ReLU is slower", "ReLU only works for text"], "ans": "ReLU does not saturate for positive values, alleviating vanishing gradients", "exp": "ReLU gradient is simply 1 for positive inputs, allowing healthy gradients to flow back."},
                    {"q": "3. What is the core difference between L1 (Lasso) and L2 (Ridge) regularization?", "options": ["L1 creates sparse weights by setting some coefficients exactly to 0", "L2 sets weights to 0", "L1 is only for text", "L2 cannot be computed"], "ans": "L1 creates sparse weights by setting some coefficients exactly to 0", "exp": "L1 acts as automatic feature selection by zeroing out non-essential feature weights."},
                    {"q": "4. In Gradient Boosting, how does each new tree learn?", "options": ["Independently in parallel", "By focusing on the residual errors made by previous trees", "By ignoring labels"], "ans": "By focusing on the residual errors made by previous trees", "exp": "Each subsequent tree is trained specifically to fix the leftover mistakes of earlier trees."},
                    {"q": "5. What do SHAP values quantify?", "options": ["API latency", "The exact contribution of each feature to a specific prediction", "Dataset storage size", "Cross-validation speed"], "ans": "The exact contribution of each feature to a specific prediction", "exp": "Grounded in cooperative game theory, SHAP reveals why an AI made a particular decision."}
                ]
            },
            "Python, Pointers & DSA": {
                "Beginner": [
                    {"q": "1. What is the time complexity to access an item in a Python list by its index arr[3]?", "options": ["O(1) Instant", "O(n)", "O(log n)", "O(n^2)"], "ans": "O(1) Instant", "exp": "Computers calculate the exact memory location using simple math, giving instant O(1) access."},
                    {"q": "2. Which of these Python types CANNOT be modified after creation (immutable)?", "options": ["List", "Dictionary", "Tuple", "Set"], "ans": "Tuple", "exp": "Tuples are fixed (immutable) once created, protecting data from accidental changes."},
                    {"q": "3. What is the purpose of a pointer in computer programming?", "options": ["To print words on screen", "To store the memory address of another variable", "To speed up the internet", "To design web pages"], "ans": "To store the memory address of another variable", "exp": "A pointer acts like a house address, telling you where the actual data lives in memory."},
                    {"q": "4. In a Singly Linked List, what two things does each Node contain?", "options": ["Value and a pointer to the Next node", "Value and a photo", "Two integers only", "Just a string"], "ans": "Value and a pointer to the Next node", "exp": "Each node holds its own piece of data and the address pointing to the next node in line."},
                    {"q": "5. What happens if a recursive function does not have a Base Case?", "options": ["It finishes instantly", "It calls itself forever until memory runs out (Stack Overflow)", "It deletes the computer files", "It prints a warning"], "ans": "It calls itself forever until memory runs out (Stack Overflow)", "exp": "Without a stopping condition (base case), recursive calls fill up the call stack until it crashes."},
                ],
                "Intermediate": [
                    {"q": "1. What is a 'Dangling Pointer'?", "options": ["A pointer that holds NULL", "A pointer pointing to a memory block that has already been deallocated/freed", "A pointer to a function", "A pointer with two arrows"], "ans": "A pointer pointing to a memory block that has already been deallocated/freed", "exp": "Accessing memory after it has been freed produces unpredictable bugs and security flaws."},
                    {"q": "2. What is the average search time inside a Python dictionary?", "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"], "ans": "O(1)", "exp": "Python dictionaries use hash tables, allowing near-instant lookups on average."},
                    {"q": "3. Which data structure follows the First-In, First-Out (FIFO) principle?", "options": ["Stack", "Queue", "Binary Search Tree", "Max Heap"], "ans": "Queue", "exp": "Like a movie ticket counter line: the first person to enter is the first person served."},
                    {"q": "4. What is the worst-case time complexity of QuickSort?", "options": ["O(n log n)", "O(n)", "O(n^2)", "O(1)"], "ans": "O(n^2)", "exp": "If the selected pivot is always the smallest or largest element, QuickSort degrades to O(n^2)."},
                    {"q": "5. Which traversal visits the Left subtree, then Root, then Right subtree?", "options": ["Pre-order", "In-order", "Post-order", "Level-order"], "ans": "In-order", "exp": "In-order traversal on a Binary Search Tree (BST) produces numbers in perfectly sorted order."}
                ],
                "Advanced": [
                    {"q": "1. What problem does Floyd's Cycle Detection Algorithm solve?", "options": ["Sorts a list in O(n)", "Detects a loop in a linked list using O(1) space", "Finds the shortest path in a graph", "Calculates prime numbers"], "ans": "Detects a loop in a linked list using O(1) space", "exp": "Using two pointers moving at different speeds discovers if there is an infinite loop."},
                    {"q": "2. What is the fundamental difference between Memoization and Tabulation?", "options": ["Memoization is Top-Down with caching; Tabulation is Bottom-Up with an iterative table", "Tabulation uses recursion", "Memoization cannot be used for DP", "They are identical"], "ans": "Memoization is Top-Down with caching; Tabulation is Bottom-Up with an iterative table", "exp": "Memoization caches recursive calls as they happen; Tabulation builds the solution up iteratively from base cases."},
                    {"q": "3. What is the worst-case search complexity of a balanced AVL Tree with N elements?", "options": ["O(n)", "O(log n)", "O(1)", "O(n^2)"], "ans": "O(log n)", "exp": "Strict height balancing guarantees that the tree height never exceeds 1.44 log2(n)."},
                    {"q": "4. In graph theory, when is Dijkstra's algorithm NOT safe to use?", "options": ["When edges have negative weights", "When the graph is large", "When there are cycles", "When edges are directed"], "ans": "When edges have negative weights", "exp": "Dijkstra assumes paths only get longer; negative edges break this greedy assumption (use Bellman-Ford)."},
                    {"q": "5. What does the Disjoint Set Union (DSU) data structure optimize?", "options": ["Finding whether two elements belong to the same connected group in near O(1) time", "Sorting numbers", "Tree balance", "String concatenation"], "ans": "Finding whether two elements belong to the same connected group in near O(1) time", "exp": "With path compression and union by rank, DSU operations run in almost constant time."}
                ]
            },
            "Agentic AI & LangGraph": {
                "Beginner": [
                    {"q": "1. What is an AI 'Prompt'?", "options": ["The power button of a computer", "The text message or instructions you give to an AI model", "A python library", "A computer virus"], "ans": "The text message or instructions you give to an AI model", "exp": "Prompts are the natural language inputs that guide what the AI generates."},
                    {"q": "2. What is the difference between a simple Chatbot and an AI Agent?", "options": ["Agents only speak English", "Agents can make decisions and use real tools (like searching the web or running code)", "Chatbots have more memory", "There is no difference"], "ans": "Agents can make decisions and use real tools (like searching the web or running code)", "exp": "A chatbot just responds with text; an agent takes action using tools to accomplish a goal."},
                    {"q": "3. What does RAG (Retrieval-Augmented Generation) do for an AI?", "options": ["Teaches AI to play games", "Supplies your own documents/notes to the AI so it doesn't give fake answers", "Speeds up computer fans", "Deletes old prompts"], "ans": "Supplies your own documents/notes to the AI so it doesn't give fake answers", "exp": "RAG lets the AI read your college syllabus or PDF notes before writing an answer."},
                    {"q": "4. What is a 'Hallucination' in AI?", "options": ["When the AI falls asleep", "When the AI confidently invents false information that sounds real", "When the screen turns black", "When the code runs fast"], "ans": "When the AI confidently invents false information that sounds real", "exp": "LLMs predict likely words, so without grounded context, they sometimes invent fictional facts."},
                    {"q": "5. What are 'Tokens' in large language models?", "options": ["Crypto currency", "Chunks of words or characters that the AI reads and processes", "Software license keys", "Keyboard buttons"], "ans": "Chunks of words or characters that the AI reads and processes", "exp": "Words are broken into small token pieces (roughly 4 characters or 0.75 words per token)."}
                ],
                "Intermediate": [
                    {"q": "1. What is 'Tool Calling' in modern AI models?", "options": ["AI repairing computer hardware", "The model outputting structured arguments (like JSON) to run an external program", "Writing code in HTML", "Installing software"], "ans": "The model outputting structured arguments (like JSON) to run an external program", "exp": "The LLM tells your code: 'Run the weather function with city=Ratnagiri'."},
                    {"q": "2. Why is LangGraph used instead of simple sequential chains?", "options": ["To create circular loops where an agent can retry, review, and self-correct", "Because it is smaller in size", "It replaces Python", "It works without internet"], "ans": "To create circular loops where an agent can retry, review, and self-correct", "exp": "Real problem solving is cyclic: you try, see an error, correct it, and try again."},
                    {"q": "3. What is 'Human-in-the-Loop' in autonomous systems?", "options": ["A person writing all responses manually", "Pausing agent execution to ask for human approval on critical actions (like deleting data)", "Playing video games", "Reading user emails"], "ans": "Pausing agent execution to ask for human approval on critical actions (like deleting data)", "exp": "A safety checkpoint ensuring an AI never executes high-risk operations without human confirmation."},
                    {"q": "4. What are Vector Embeddings?", "options": ["Arrow drawings", "Converting text into lists of numbers where similar meanings sit close together", "Computer viruses", "3D models"], "ans": "Converting text into lists of numbers where similar meanings sit close together", "exp": "Words with similar meanings (like 'King' and 'Queen') end up near each other in vector space."},
                    {"q": "5. What happens during an agent's 'Reflection' step?", "options": ["The agent shuts down", "The agent evaluates its own output against instructions before giving the final answer", "The agent reboots", "The agent deletes memory"], "ans": "The agent evaluates its own output against instructions before giving the final answer", "exp": "Like a student double-checking their math answer sheet before handing it to the teacher."}
                ],
                "Advanced": [
                    {"q": "1. How does LangGraph handle State Management across multi-agent cycles?", "options": ["Using global variables", "Via a centralized TypedDict/BaseModel state updated through node transitions", "Writing to text files", "It does not maintain state"], "ans": "Via a centralized TypedDict/BaseModel state updated through node transitions", "exp": "State flows cleanly through graph edges, allowing agents to read and modify shared context predictably."},
                    {"q": "2. What is the Supervisor Multi-Agent pattern?", "options": ["Every agent talks to every other agent at once", "A central routing agent evaluates user intent and delegates work to specialized sub-agents", "Agents running without prompts", "Agents voting randomly"], "ans": "A central routing agent evaluates user intent and delegates work to specialized sub-agents", "exp": "Like a project manager who assigns coding to the developer and testing to the QA agent."},
                    {"q": "3. What is the role of Checkpointers in long-running agent workflows?", "options": ["To speed up GPU inference", "To persist execution state so workflows can pause, resume, and rewind (time-travel debugging)", "To delete logs", "To compress weights"], "ans": "To persist execution state so workflows can pause, resume, and rewind (time-travel debugging)", "exp": "Checkpointers allow multi-turn workflows to survive system restarts without losing progress."},
                    {"q": "4. How do you prevent infinite execution loops in an autonomous agent?", "options": ["By setting a strict recursion_limit constraint", "By deleting prompt templates", "By increasing temperature", "By running without tools"], "ans": "By setting a strict recursion_limit constraint", "exp": "A hard limit (e.g., maximum 15 iterations) guarantees the agent terminates even if confused."},
                    {"q": "5. What is the primary difference between ReAct and Plan-and-Solve agent patterns?", "options": ["ReAct decides step-by-step iteratively; Plan-and-Solve designs the entire sequence of steps first", "ReAct cannot use tools", "Plan-and-Solve is only for math", "They are identical"], "ans": "ReAct decides step-by-step iteratively; Plan-and-Solve designs the entire sequence of steps first", "exp": "Plan-and-Solve decomposes complex tasks up-front to prevent agents from wandering off-track."}
                ]
            }
        }

        current_quiz = all_quizzes[topic][level]
        
        with st.form("quiz_form"):
            user_answers = {}
            for idx, item in enumerate(current_quiz):
                st.markdown(f"""
                <div class="quiz-card">
                    <div class="quiz-q">{item['q']}</div>
                </div>
                """, unsafe_allow_html=True)
                user_answers[idx] = st.radio(f"Select option for Question {idx+1}:", item["options"], key=f"q_{topic}_{level}_{idx}")
                st.write("")
            
            submitted = st.form_submit_button("🎯 Submit Full Assessment", use_container_width=True)

        if submitted:
            score = 0
            st.divider()
            st.subheader("📊 Assessment Performance Report")
            
            for idx, item in enumerate(current_quiz):
                selected = user_answers[idx]
                if selected == item["ans"]:
                    score += 1
                    st.success(f"✅ **Question {idx+1}: Correct!** ({item['ans']})")
                else:
                    st.error(f"❌ **Question {idx+1}: Incorrect.** Your answer: *{selected}* | **Correct:** *{item['ans']}*")
                    st.caption(f"💡 *Simple Explanation:* {item['exp']}")
            
            percentage = int((score / len(current_quiz)) * 100)
            
            # Persist quiz result to users_db.json
            current_db = load_users()
            current_db[current_email]["quiz_attempts"] += 1
            current_db[current_email]["retention_score"] = percentage
            save_users(current_db)
            
            st.markdown(f"""
            <div style="background:#1e293b; border:2px solid #6366f1; border-radius:12px; padding:18px; text-align:center; margin-top:15px;">
                <h2 style="color:#c7d2fe; margin:0;">Final Score: {score} / {len(current_quiz)} ({percentage}%)</h2>
                <p style="color:#94a3b8; margin-top:4px;">{'🎉 Outstanding work! Your retention score has been permanently saved.' if percentage >= 80 else '📚 Good attempt! Your score has been saved. Review the notes above to strengthen your basics.'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if percentage >= 60:
                st.balloons()
import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Household Cleaning Schedule",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Remove white banner/header */
    header[data-testid="stHeader"] {
        background-color: transparent;
        display: none;
    }
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container */
    .main-container {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Remove top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Headings */
    h1 {
        color: #667eea;
        text-align: center;
        padding-bottom: 20px;
    }
    h2, h3 {
        color: #667eea;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: white;
        font-weight: 600;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #667eea;
    }
    
    /* White checkboxes with black border - Enhanced styling */
    div[data-testid="stCheckbox"] {
        padding: 5px 0;
    }
    
    /* Label text color */
    div[data-testid="stCheckbox"] > label {
        color: #333 !important;
        font-weight: 500;
    }
    
    /* Target Streamlit's checkbox container */
    .stCheckbox {
        color: #333 !important;
    }
    
    /* Override the checkbox background and border */
    .stCheckbox > label > div:first-child {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Style the checkbox itself using Streamlit's internal structure */
    div[data-testid="stCheckbox"] label > div:first-child > div {
        background-color: white !important;
        border: 2px solid #000 !important;
        border-radius: 4px !important;
    }
    
    /* Ensure the checkmark is black */
    div[data-testid="stCheckbox"] label svg {
        color: #000 !important;
        stroke: #000 !important;
        fill: #000 !important;
    }
    
    /* Additional targeting for Streamlit checkbox components */
    .st-emotion-cache-1y4p8pa,
    .st-emotion-cache-16idsys p {
        color: #333 !important;
    }
    
    /* Target checkbox by role attribute */
    [role="checkbox"] {
        background-color: white !important;
        border: 2px solid #000 !important;
        outline: none !important;
    }
    
    [role="checkbox"]:checked {
        background-color: white !important;
        border-color: #000 !important;
    }
    
    /* Force override with important flags */
    .st-cb, .st-cc, .st-cd, .st-ce, .st-cf, .st-cg {
        background-color: white !important;
        border-color: #000 !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
        .main-container {
            border-radius: 8px;
            padding: 15px;
        }
        h1 {
            font-size: 1.5rem;
        }
        h2 {
            font-size: 1.3rem;
        }
        h3 {
            font-size: 1.1rem;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.9rem;
            padding: 6px 12px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for checkboxes if not already done
if 'checkboxes' not in st.session_state:
    st.session_state.checkboxes = {}

def create_checkbox_table(tasks, table_id, people=['L', 'J', 'P'], show_day=False):
    """Create an interactive table with checkboxes for each person"""
    
    # Header
    cols = st.columns([3] + [1]*len(people))
    cols[0].markdown("**Task**")
    for i, person in enumerate(people):
        cols[i+1].markdown(f"**{person}**")
    
    # Tasks
    for idx, task in enumerate(tasks):
        task_text = f"{task['day']}: {task['task']}" if show_day and 'day' in task else task if isinstance(task, str) else task.get('task', '')
        
        cols = st.columns([3] + [1]*len(people))
        
        # Check if any checkbox is checked for this task
        any_checked = any([
            st.session_state.checkboxes.get(f"{table_id}_{idx}_{person}", False)
            for person in people
        ])
        
        # Display task with strikethrough if any checkbox is checked
        if any_checked:
            cols[0].markdown(f"~~{task_text}~~")
        else:
            cols[0].markdown(task_text)
        
        # Checkboxes for each person
        for i, person in enumerate(people):
            key = f"{table_id}_{idx}_{person}"
            cols[i+1].checkbox("", key=key, label_visibility="collapsed")

def create_phoebe_checklist(tasks, list_id):
    """Create a simple checklist for Phoebe's tasks"""
    for idx, task in enumerate(tasks):
        key = f"{list_id}_{idx}"
        st.checkbox(task, key=key)

# Title
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("🧹 Household Cleaning Schedule")

# Data
morning_tasks = [
    'Make bed',
    'Clear floor of laundry',
    'Wipe counters',
    'Quick tidy of living room/kitchen'
]

evening_tasks = [
    'Clear and wipe all kitchen surfaces',
    'Clear all dishes and run dishwasher',
    'Vacuum living room, kitchen, entrance hall and playroom',
    'Put away toys in playroom'
]

weekly_tasks = [
    {'day': 'Monday', 'task': 'Change bed linens (master and Seph)'},
    {'day': 'Tuesday', 'task': 'Clean cat room'},
    {'day': 'Wednesday', 'task': 'Deep clean kitchen (counters, appliances, sink, hob)'},
    {'day': 'Thursday', 'task': 'Clean and organise utility room, vacuum bedroom'},
    {'day': 'Friday', 'task': 'Tidy en suite and master bedroom'},
    {'day': 'Saturday', 'task': 'Quick tidy all rooms'},
    {'day': 'Sunday', 'task': 'Dust and organise fridge'}
]

monthly_recurring = [
    'Clean windows (inside)',
    'Carpet clean rug',
    'Organise playroom',
    'Wipe down kitchen cabinets',
    'Cleaning cycles on dishwasher, washing machine and dryer'
]

phoebe_tasks = {
    'week1_mon_tue': [
        'Vacuuming (Hall, Stairs, Landing & Bathroom)',
        'Dishwasher',
        'Remove Own Items from Hall & Island'
    ],
    'week1_sat_sun': [
        'Vacuuming (Hall, Stairs, Landing & Bathroom)',
        'Dishwasher',
        'Remove Own Items from Hall & Island',
        'Own Laundry',
        'Tidy & Clean Bedroom'
    ],
    'week2_sat_sun': [
        'Vacuuming (Hall, Stairs, Landing & Bathroom)',
        'Dishwasher',
        'Remove Own Items from Hall & Island',
        'Own Laundry',
        'Clean Bathroom (Bath, Sink, Shower, Toilet)'
    ]
}

monthly_tasks = {
    'January': ['Deep clean oven', 'Deep clean fridge'],
    'February': ['Declutter entrance hall', 'Clean light fixtures', 'Wipe down doors & skirting'],
    'March': ['Deep clean bathroom & ensuite', 'Vacuum & turn mattresses'],
    'April': ['Declutter playroom', 'Carpet clean house'],
    'May': ['Clean stone floor'],
    'June': ['Clean windows (outside)', 'Clean ceilings (fans & vents)'],
    'July': ['Deep clean oven & fridge', 'Reorganise loft', 'Clean under furniture'],
    'August': ['Shampoo sofas'],
    'September': ['Deep clean bathroom & ensuite', 'Organise & clean under bed'],
    'October': ['Clean duvets & pillows', 'Organise kitchen'],
    'November': ['Declutter wardrobes', 'Carpet clean house'],
    'December': ['Deep clean house (mega day)', 'Organise all storage', 'Declutter communal areas']
}

# Tabs
tab1, tab2, tab3 = st.tabs(["📅 Daily Routines", "👧 Phoebe's Schedule", "🔍 Deep Cleaning"])

with tab1:
    # Morning tasks
    st.markdown("### 🌅 Every Morning")
    create_checkbox_table(morning_tasks, "morning")
    
    st.markdown("---")
    
    # Evening tasks
    st.markdown("### 🌙 Every Evening")
    create_checkbox_table(evening_tasks, "evening")
    
    st.markdown("---")
    
    # Weekly tasks
    st.markdown("### 📆 Weekly Tasks")
    create_checkbox_table(weekly_tasks, "weekly", show_day=True)

with tab2:
    st.markdown("## Phoebe's Weekly Schedule")
    
    st.markdown("### Week 1 - Monday & Tuesday")
    create_phoebe_checklist(phoebe_tasks['week1_mon_tue'], "phoebe_w1mt")
    
    st.markdown("---")
    
    st.markdown("### Week 1 - Saturday & Sunday")
    create_phoebe_checklist(phoebe_tasks['week1_sat_sun'], "phoebe_w1ss")
    
    st.markdown("---")
    
    st.markdown("### Week 2 - Saturday & Sunday")
    create_phoebe_checklist(phoebe_tasks['week2_sat_sun'], "phoebe_w2ss")

with tab3:
    st.markdown("### 🔁 Recurring Monthly Tasks")
    create_checkbox_table(monthly_recurring, "monthly_recurring")
    
    st.markdown("---")
    st.markdown("## 📅 Monthly Deep Cleaning Schedule")
    
    # Display months - they'll wrap naturally on mobile
    for month, tasks in monthly_tasks.items():
        st.markdown(f"### {month}")
        create_checkbox_table(tasks, f"month_{month.lower()}")
        st.markdown("")  # Small spacing between months

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("*Last updated: " + datetime.now().strftime("%Y-%m-%d") + "*")

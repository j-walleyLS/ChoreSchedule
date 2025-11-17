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
    
    /* Remove top padding */
    .block-container {
        padding-top: 1rem;
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
    
    /* Task styling */
    .task-title {
        font-weight: 600;
        color: #333;
        margin-bottom: 8px;
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
    
    /* ===== CHECKBOX STYLING ===== */
    
    /* Force checkbox container to be white */
    [data-baseweb="checkbox"] {
        background-color: white !important;
        background: white !important;
        border: 2px solid #000 !important;
        border-radius: 4px !important;
        outline: none !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Override any default dark theme */
    div[data-baseweb="checkbox"] {
        background-color: white !important;
        background: white !important;
    }
    
    /* Checkbox when checked - keep white */
    [data-baseweb="checkbox"][data-checked="true"] {
        background-color: white !important;
        background: white !important;
        border: 2px solid #000 !important;
    }
    
    /* Make the checkmark black */
    [data-baseweb="checkbox"] svg {
        color: #000 !important;
        stroke: #000 !important;
        fill: none !important;
        stroke-width: 3px !important;
    }
    
    /* Label text should be white on gradient background */
    .stCheckbox label {
        color: white !important;
        background-color: transparent !important;
        border: none !important;
        font-weight: 500;
    }
    
    /* Remove ALL hover effects */
    [data-baseweb="checkbox"]:hover {
        background-color: white !important;
        background: white !important;
        border-color: #000 !important;
    }
    
    /* Remove focus highlight */
    [data-baseweb="checkbox"]:focus {
        background-color: white !important;
        background: white !important;
        border-color: #000 !important;
        box-shadow: none !important;
    }
    
    /* Force white background for all states */
    [data-baseweb="checkbox"],
    [data-baseweb="checkbox"]:hover,
    [data-baseweb="checkbox"]:focus,
    [data-baseweb="checkbox"]:active,
    [data-baseweb="checkbox"][data-checked="true"],
    [data-baseweb="checkbox"][data-checked="false"] {
        background-color: white !important;
        background: white !important;
    }
    
    /* Prevent text selection */
    .stCheckbox label {
        user-select: none !important;
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
    }
    
    /* Keep checkboxes compact on mobile */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        gap: 0 !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }
    
    /* Make columns very narrow for checkboxes */
    [data-testid="column"] {
        min-width: 0 !important;
        flex-shrink: 1 !important;
        padding: 0 2px !important;
    }
    
    /* Ultra compact checkbox styling */
    .stCheckbox {
        display: inline-flex !important;
        align-items: center !important;
        white-space: nowrap !important;
        font-size: 0.85rem !important;
        min-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        width: auto !important;
    }
    
    /* Minimize the checkbox label spacing */
    .stCheckbox > label {
        padding: 0 !important;
        margin: 0 !important;
        gap: 2px !important;
        display: inline-flex !important;
        align-items: center !important;
    }
    
    /* Make the actual checkbox square smaller */
    [data-baseweb="checkbox"] {
        width: 16px !important;
        height: 16px !important;
        min-width: 16px !important;
        margin: 0 !important;
        flex-shrink: 0 !important;
    }
    
    /* Remove all column padding and gaps */
    div[data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
        gap: 0 !important;
    }
    
    div[data-testid="stHorizontalBlock"] {
        gap: 2px !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Mobile specific ultra-compact */
    @media (max-width: 768px) {
        [data-baseweb="checkbox"] {
            width: 16px !important;
            height: 16px !important;
            min-width: 16px !important;
        }
        .stCheckbox label {
            font-size: 0.8rem !important;
            letter-spacing: -0.5px !important;
        }
        div[data-testid="column"] {
            max-width: 40px !important;
        }
        /* First 3 columns should be tiny */
        div[data-testid="stHorizontalBlock"] > div:nth-child(1),
        div[data-testid="stHorizontalBlock"] > div:nth-child(2),
        div[data-testid="stHorizontalBlock"] > div:nth-child(3) {
            flex: 0 0 auto !important;
            width: 35px !important;
            max-width: 35px !important;
        }
    }
    
    /* Section styling - text in white color instead of white background */
    .stMarkdown h2, .stMarkdown h3 {
        color: white !important;
        padding: 10px 0;
        margin-bottom: 10px;
    }
    
    /* Make all text white for visibility on gradient */
    .stMarkdown p {
        color: white !important;
    }
    
    /* Divider/separator styling */
    hr {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.5rem;
            padding-top: 0.5rem;
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
            font-size: 0.85rem;
            padding: 6px 10px;
        }
        /* Compact checkboxes on mobile */
        .stCheckbox label {
            padding: 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for checkboxes if not already done
if 'checkboxes' not in st.session_state:
    st.session_state.checkboxes = {}

def create_task_with_checkboxes(task_text, task_id, people=['L', 'J', 'P']):
    """Create a task with checkboxes for each person below it"""
    
    # Check if any checkbox is checked for this task
    any_checked = any([
        st.session_state.checkboxes.get(f"{task_id}_{person}", False)
        for person in people
    ])
    
    # Display task title with white text
    if any_checked:
        st.markdown(f'<div style="color: white; padding: 8px 0; margin-bottom: 4px;">~~**{task_text}**~~</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color: white; padding: 8px 0; margin-bottom: 4px;">**{task_text}**</div>', unsafe_allow_html=True)
    
    # Create extremely compact checkboxes - all three in a tiny space
    col1, col2, col3, spacer = st.columns([0.15, 0.15, 0.15, 3.55])
    
    with col1:
        st.checkbox("L", key=f"{task_id}_L")
    with col2:
        st.checkbox("J", key=f"{task_id}_J")
    with col3:
        st.checkbox("P", key=f"{task_id}_P")
    # spacer takes up the rest
    
    st.markdown("")  # Add some spacing

def create_task_list(tasks, list_id, people=['L', 'J', 'P'], show_day=False):
    """Create a list of tasks with checkboxes"""
    for idx, task in enumerate(tasks):
        if isinstance(task, dict):
            task_text = f"{task['day']}: {task['task']}" if show_day else task['task']
        else:
            task_text = task
        
        create_task_with_checkboxes(task_text, f"{list_id}_{idx}", people)

def create_phoebe_checklist(tasks, list_id):
    """Create a simple checklist for Phoebe's tasks"""
    for idx, task in enumerate(tasks):
        key = f"{list_id}_{idx}"
        st.checkbox(task, key=key)

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
    create_task_list(morning_tasks, "morning")
    
    st.markdown("---")
    
    # Evening tasks
    st.markdown("### 🌙 Every Evening")
    create_task_list(evening_tasks, "evening")
    
    st.markdown("---")
    
    # Weekly tasks
    st.markdown("### 📆 Weekly Tasks")
    create_task_list(weekly_tasks, "weekly", show_day=True)

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
    create_task_list(monthly_recurring, "monthly_recurring")
    
    st.markdown("---")
    st.markdown("## 📅 Monthly Deep Cleaning Schedule")
    
    # Display months
    for month, tasks in monthly_tasks.items():
        st.markdown(f"### {month}")
        create_task_list(tasks, f"month_{month.lower()}")

# Footer
st.markdown("---")
st.markdown('<p style="color: white; opacity: 0.8;">*Last updated: ' + datetime.now().strftime("%Y-%m-%d") + '*</p>', unsafe_allow_html=True)

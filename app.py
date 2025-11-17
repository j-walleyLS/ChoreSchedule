import streamlit as st
from datetime import datetime
import json

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
    
    /* Disable horizontal scrolling completely */
    html, body {
        overflow-x: hidden !important;
        max-width: 100vw !important;
        position: relative !important;
    }
    
    * {
        max-width: 100vw !important;
    }
    
    .stApp {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    
    section.main > div {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    
    /* Force all content to stay within viewport */
    [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    
    .main .block-container {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
</style>

<script>
    // JavaScript to prevent horizontal scrolling
    document.addEventListener('DOMContentLoaded', function() {
        // Prevent horizontal scroll
        document.body.style.overflowX = 'hidden';
        document.documentElement.style.overflowX = 'hidden';
        
        // Prevent touchmove horizontally on mobile
        let startX = 0;
        document.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
        });
        
        document.addEventListener('touchmove', function(e) {
            let deltaX = e.touches[0].clientX - startX;
            if (Math.abs(deltaX) > 5) {
                e.preventDefault();
            }
        }, { passive: false });
        
        // Also prevent scroll event
        window.addEventListener('scroll', function() {
            if (window.scrollX !== 0) {
                window.scrollTo(0, window.scrollY);
            }
        });
    });
</script>

<style>
    
    /* Remove ALL shadows */
    * {
        box-shadow: none !important;
    }
    
    /* Remove top padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 100% !important;
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
    
    /* Task styling - text in white color */
    .task-text {
        color: white !important;
        font-weight: bold;
        padding: 8px 0;
        margin-bottom: 4px;
    }
    
    /* Section styling - text in white color */
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
    
    /* Tabs styling - full width and no shadows */
    .stTabs {
        width: 100% !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: transparent;
        flex-wrap: nowrap !important;
        width: 100% !important;
        justify-content: stretch !important;
        box-shadow: none !important;
    }
    .stTabs [data-baseweb="tab-list"] button {
        flex: 1 1 0 !important;
        min-width: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
        font-weight: 600;
        padding: 6px 12px;
        font-size: 0.9rem;
        white-space: nowrap;
        box-shadow: none !important;
        border: none !important;
        flex: 1 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #667eea;
        box-shadow: none !important;
    }
    
    /* Remove any tab panel shadows */
    .stTabs [data-baseweb="tab-panel"] {
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Even smaller tabs on mobile but full width */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 0.8rem !important;
            padding: 8px 4px !important;
            flex: 1 !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px !important;
            padding: 0 !important;
            margin: 0 !important;
            width: 100% !important;
        }
        .stTabs {
            margin: 0 !important;
            padding: 0 !important;
            width: 100vw !important;
            margin-left: -0.5rem !important;
            margin-right: -0.5rem !important;
            padding: 0 0.5rem !important;
        }
    }
    
    /* Style normal checkboxes for Phoebe's section */
    [data-baseweb="checkbox"] {
        background-color: white !important;
        background: white !important;
        border: 2px solid #000 !important;
        border-radius: 4px !important;
    }
    
    [data-baseweb="checkbox"][data-checked="true"] {
        background-color: white !important;
        background: white !important;
        border: 2px solid #000 !important;
    }
    
    [data-baseweb="checkbox"] svg {
        color: #000 !important;
        stroke: #000 !important;
        fill: none !important;
    }
    
    .stCheckbox label {
        color: white !important;
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Force compact Streamlit checkboxes */
    /* Target columns that contain checkboxes */
    div[data-testid="column"]:has(.stCheckbox) {
        max-width: 60px !important;
        flex: 0 1 60px !important;
        display: inline-block !important;
    }
    
    /* Force horizontal layout */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
        align-items: center !important;
        max-width: 200px !important;
    }
    
    /* Make Streamlit checkboxes compact */
    .stCheckbox {
        margin: 0 !important;
        padding: 0 !important;
        display: inline-flex !important;
        width: auto !important;
    }
    
    .stCheckbox label {
        padding: 0 2px !important;
        font-size: 0.9rem !important;
        white-space: nowrap !important;
    }
    
    /* Prevent vertical stacking */
    .element-container {
        width: auto !important;
        display: inline-block !important;
    }
    
    .row-widget {
        display: flex !important;
        flex-direction: row !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.5rem;
            padding-top: 0.5rem;
        }
        h2 {
            font-size: 1.3rem;
        }
        h3 {
            font-size: 1.1rem;
        }
        
        /* Keep checkboxes horizontal on mobile */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            max-width: 180px !important;
        }
        
        div[data-testid="column"]:has(.stCheckbox) {
            max-width: 50px !important;
            flex: 0 1 50px !important;
        }
        
        .stCheckbox {
            width: auto !important;
            display: inline-flex !important;
        }
        
        .stCheckbox label {
            font-size: 0.85rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for checkboxes if not already done
if 'checkboxes' not in st.session_state:
    st.session_state.checkboxes = {}

def create_task_with_checkboxes(task_text, task_id, people=['L', 'J', 'P']):
    """Create a task with compact checkboxes"""
    
    # Check if any checkbox is checked for this task
    any_checked = any([
        st.session_state.checkboxes.get(f"{task_id}_{person}", False)
        for person in people
    ])
    
    # Display task title
    if any_checked:
        st.markdown(f'<div class="task-text">~~{task_text}~~</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="task-text">{task_text}</div>', unsafe_allow_html=True)
    
    # Create checkboxes in equal columns - 3 small ones
    cols = st.columns([1, 1, 1])
    
    with cols[0]:
        st.checkbox("L", key=f"{task_id}_L")
    with cols[1]:
        st.checkbox("J", key=f"{task_id}_J")
    with cols[2]:
        st.checkbox("P", key=f"{task_id}_P")
    
    st.markdown("")  # Add spacing between tasks

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
    'week2_wed_thu_fri': [
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
tab1, tab2, tab3 = st.tabs(["Daily Routines", "Phoebe's Schedule", "Deep Cleaning"])

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
    
    st.markdown("### Week 2 - Wednesday, Thursday & Friday")
    create_phoebe_checklist(phoebe_tasks['week2_wed_thu_fri'], "phoebe_w2wtf")

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

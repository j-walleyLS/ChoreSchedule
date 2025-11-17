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
    
    /* Custom checkbox styling */
    .custom-checkbox-group {
        display: flex !important;
        gap: 10px !important;
        margin-bottom: 15px !important;
        padding-left: 10px;
    }
    
    .custom-checkbox {
        display: flex !important;
        align-items: center !important;
        gap: 4px !important;
        cursor: pointer;
        user-select: none;
    }
    
    .custom-checkbox input[type="checkbox"] {
        width: 18px !important;
        height: 18px !important;
        background-color: white !important;
        border: 2px solid #000 !important;
        border-radius: 3px !important;
        margin: 0 !important;
        cursor: pointer;
        -webkit-appearance: none;
        appearance: none;
    }
    
    .custom-checkbox input[type="checkbox"]:checked {
        background-color: white !important;
        position: relative;
    }
    
    .custom-checkbox input[type="checkbox"]:checked::after {
        content: "✓";
        position: absolute;
        left: 2px;
        top: -2px;
        color: black;
        font-weight: bold;
        font-size: 14px;
    }
    
    .custom-checkbox label {
        color: white !important;
        font-size: 0.9rem !important;
        margin: 0 !important;
        cursor: pointer;
    }
    
    /* Divider/separator styling */
    hr {
        border-color: rgba(255, 255, 255, 0.3) !important;
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
        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem;
            padding: 6px 10px;
        }
        .custom-checkbox-group {
            gap: 8px !important;
        }
        .custom-checkbox input[type="checkbox"] {
            width: 16px !important;
            height: 16px !important;
        }
        .custom-checkbox label {
            font-size: 0.85rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for checkboxes if not already done
if 'checkboxes' not in st.session_state:
    st.session_state.checkboxes = {}

# JavaScript for handling custom checkboxes
def create_checkbox_js():
    return """
    <script>
    function toggleCheckbox(taskId, person) {
        const checkbox = document.getElementById(taskId + '_' + person);
        const isChecked = checkbox.checked;
        
        // Send state back to Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            data: {
                key: taskId + '_' + person,
                value: isChecked
            }
        }, '*');
    }
    </script>
    """

def create_task_with_custom_checkboxes(task_text, task_id, people=['L', 'J', 'P']):
    """Create a task with custom HTML checkboxes"""
    
    # Display task title
    task_html = f'<div class="task-text">{task_text}</div>'
    
    # Create custom checkbox HTML
    checkbox_html = '<div class="custom-checkbox-group">'
    for person in people:
        checkbox_id = f"{task_id}_{person}"
        checked = st.session_state.checkboxes.get(checkbox_id, False)
        checked_attr = "checked" if checked else ""
        checkbox_html += f'''
        <div class="custom-checkbox">
            <input type="checkbox" id="{checkbox_id}" {checked_attr} 
                   onchange="toggleCheckbox('{task_id}', '{person}')">
            <label for="{checkbox_id}">{person}</label>
        </div>
        '''
    checkbox_html += '</div>'
    
    # Display the HTML
    st.markdown(task_html + checkbox_html, unsafe_allow_html=True)

def create_task_with_streamlit_checkboxes(task_text, task_id, people=['L', 'J', 'P']):
    """Fallback to regular Streamlit checkboxes but ultra-compact"""
    
    # Check if any checkbox is checked for this task
    any_checked = any([
        st.session_state.checkboxes.get(f"{task_id}_{person}", False)
        for person in people
    ])
    
    # Display task title with white text
    if any_checked:
        st.markdown(f'<div style="color: white; font-weight: bold; padding: 8px 0;">~~{task_text}~~</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color: white; font-weight: bold; padding: 8px 0;">{task_text}</div>', unsafe_allow_html=True)
    
    # Create a single row with HTML for the checkboxes
    checkbox_container = st.container()
    with checkbox_container:
        # Use markdown with custom HTML instead of columns
        st.markdown("""
        <div style="display: flex; gap: 15px; padding-left: 10px; margin-bottom: 10px;">
        """, unsafe_allow_html=True)
        
        # Create three small columns
        c1, c2, c3, empty = st.columns([0.8, 0.8, 0.8, 10])
        with c1:
            st.checkbox("L", key=f"{task_id}_L")
        with c2:
            st.checkbox("J", key=f"{task_id}_J")
        with c3:
            st.checkbox("P", key=f"{task_id}_P")

def create_task_list(tasks, list_id, people=['L', 'J', 'P'], show_day=False):
    """Create a list of tasks with checkboxes"""
    for idx, task in enumerate(tasks):
        if isinstance(task, dict):
            task_text = f"{task['day']}: {task['task']}" if show_day else task['task']
        else:
            task_text = task
        
        # Use custom HTML checkboxes for better mobile control
        create_task_with_custom_checkboxes(task_text, f"{list_id}_{idx}", people)

def create_phoebe_checklist(tasks, list_id):
    """Create a simple checklist for Phoebe's tasks"""
    for idx, task in enumerate(tasks):
        key = f"{list_id}_{idx}"
        st.checkbox(task, key=key)

# Add JavaScript
st.markdown(create_checkbox_js(), unsafe_allow_html=True)

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

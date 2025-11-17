# 🧹 Household Cleaning Schedule

An interactive cleaning schedule tracker built with Streamlit for managing daily, weekly, and monthly household tasks.

## Features

- **Daily Routines**: Morning and evening tasks with individual tracking for L, J, and P
- **Phoebe's Schedule**: Separate weekly schedule tracking across two-week cycles
- **Deep Cleaning**: Monthly recurring tasks and month-specific deep cleaning schedules
- **Interactive Checkboxes**: Check off completed tasks with automatic strikethrough
- **Responsive Design**: Works on desktop and mobile devices

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/cleaning-schedule.git
cd cleaning-schedule
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the app locally:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Deployment

### Deploy to Streamlit Cloud (Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository, branch, and `app.py`
6. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app`

## Structure

```
cleaning-schedule/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Customization

Edit the task lists in `app.py` to customize:
- Morning and evening routines
- Weekly tasks and assigned days
- Monthly recurring tasks
- Deep cleaning schedules by month

## License

MIT License - feel free to use and modify for your household!

# Financial Wizard

Financial Wizard is a full-stack web application designed to help users analyze their financial data, visualize expenses over time and by type, and predict savings goals with automated expense-cutting suggestions. Built with a Python Flask backend and a React frontend, it supports uploading financial files (CSV, XLSX, PDF), filtering data by date range, and calculating savings plans in Indian Rupees (₹).

## Features
- **File Upload**: Upload financial data in CSV, XLSX, or PDF formats.
- **Expense Visualization**:
  - Line chart for expenses over time.
  - Doughnut chart for expenses by type.
- **Date Range Filter**: Filter data from a start year/month to an end year/month (e.g., 2024-01 to 2025-02).
- **Savings Prediction**:
  - Calculates monthly savings needed to achieve a goal (e.g., car, house).
  - Automatically applies 10% cuts to non-essential expenses (excludes Rent, Education).
  - Displays base and adjusted scenarios with detailed cut breakdowns.
- **Currency**: All monetary values are in Indian Rupees (₹).
- **Responsive UI**: Built with Tailwind CSS for a modern, gradient-themed interface.

## Directory Structure
Financial_wizard/
├── financial_tool_backend/         # Backend directory (Python Flask)
│   ├── uploads/                    # Temporary storage for uploaded files (auto-created)
│   ├── templates/                  # HTML templates (minimal, for Flask root)
│   │   └── index.html              # Basic landing page
│   ├── .venv/                      # Virtual environment (not tracked in Git)
│   ├── app.py                      # Flask application entry point
│   ├── process_file.py             # File processing and savings calculation logic
│   ├── requirements.txt            # Backend dependencies
│   └── README.md                   # This file (root copy)
├── financial_tool_frontend/        # Frontend directory (React)
│   ├── node_modules/               # Node.js dependencies (not tracked in Git)
│   ├── public/                     # Public assets
│   │   ├── index.html              # React entry HTML
│   │   ├── favicon.ico             # App favicon
│   │   └── manifest.json           # Web app manifest
│   ├── src/                        # React source code
│   │   ├── App.js                  # Main React component
│   │   ├── index.js                # React entry point
│   │   ├── index.css               # Global CSS (with Tailwind)
│   │   └── reportWebVitals.js      # Performance monitoring (optional)
│   ├── package.json                # Frontend dependencies and scripts
│   └── README.md                   # This file (root copy)
├── sample_data/                    # Optional: Sample financial data for testing
│   └── sample.csv                  # Example CSV file
└── README.md                       # This file (root)


## Prerequisites
- **Python 3.8+**: For the backend.
- **Node.js 16+ and npm**: For the frontend.
- **Git**: To clone and manage the repository.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/Financial_wizard.git
cd Financial_wizard
### 2. Backend Setup
cd financial_tool_backend
Install Dependencies
Create and activate a virtual environment, then install requirements
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
pip install -r requirements.txt
### 3. Frontend Setup
Navigate to the frontend directory and install Node.js dependencies.
cd ../financial_tool_frontend
npm install
##Running the Application
###1. Start the Backend
From the financial_tool_backend directory, with the virtual environment activated
```bash
python app.py

###2. Start the Frontend
In a separate terminal, from the financial_tool_frontend directory
```bash
npm start
###3. Test the App
1.Visit http://localhost:3000.
2.Upload a financial file.
Eg:
Date,Expense,Type of Expense
2024-01-01,10000,Food
2024-01-02,20000,Rent
2024-02-01,15000,Utilities
3.Filter by date range.
4.Enter monthly income, goal and goal cost.
5.Click ' Predict to see savings plans.
6.Sample Output
Monthly expenses (average over 2 months): ₹22500
Without cuts: Save ₹37500 monthly to get your house in 13.3 months (1.1 years).
With automated cuts: Save ₹41250 monthly to achieve it in 12.1 months (1 years).
Total monthly cut: ₹3750. Cuts applied (10% on non-essential expenses):
- Food: 10% (₹500)
- Utilities: 10% (₹750)
Note: Essential expenses like Rent and Education are not cut.

##Notes

1.File Format: Ensure uploaded files have Date (YYYY-MM-DD), Expense (numeric), and Type of Expense columns.
2.Protected Expenses: "Rent" and "Education" are not cut; modify protected_types in process_file.py to change this.
3.Logging: Backend logs are set to INFO level; adjust in app.py if needed.
4.Proxy: The frontend uses a proxy ("proxy": "http://localhost:5000") in package.json to communicate with the backend.

##Contributing
Feel free to fork this repository, submit issues, or send pull requests to enhance functionality!
##License
MIT License - feel free to use and modify as you see fit.
##Author
K. Taraka Ramu
Date : March 27, 2025
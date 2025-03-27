import pandas as pd
import PyPDF2
import logging

logger = logging.getLogger(__name__)

def process_financial_file(file_path):
    file_extension = file_path.split('.')[-1].lower()
    logger.info(f"Processing file type: {file_extension}")
    
    try:
        if file_extension == 'csv':
            data = pd.read_csv(file_path, usecols=['Date', 'Expense', 'Type of Expense'])
        elif file_extension == 'xlsx':
            data = pd.read_excel(file_path, usecols=['Date', 'Expense', 'Type of Expense'])
        elif file_extension == 'pdf':
            return extract_from_pdf(file_path)
        else:
            logger.error(f"Unsupported file type: {file_extension}")
            return None
        
        required = ['Date', 'Expense', 'Type of Expense']
        if not all(col in data.columns for col in required):
            logger.warning("Missing required columns")
            return None
        
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce', format='%Y-%m-%d')
        data['Expense'] = pd.to_numeric(data['Expense'], errors='coerce', downcast='float')
        data['Type of Expense'] = data['Type of Expense'].astype('category')
        data = data.dropna(subset=['Date', 'Expense'])
        
        data['Month'] = data['Date'].dt.to_period('M').astype(str)
        time_series = data.groupby('Month', observed=True)['Expense'].sum().to_dict()
        type_summary = data.groupby('Type of Expense', observed=True)['Expense'].sum().to_dict()
        total = float(data['Expense'].sum())
        
        min_date = data['Date'].min()
        max_date = data['Date'].max()
        years = list(range(min_date.year, max_date.year + 1))
        months = data['Month'].unique().tolist()
        
        return {
            'time_series': time_series,
            'type_summary': type_summary,
            'total': total,
            'years': years,
            'months': months,
            'expense_types': data['Type of Expense'].cat.categories.tolist()
        }
    except Exception as e:
        logger.error(f"File processing error: {str(e)}")
        raise Exception(f"Error processing file: {str(e)}")

def extract_from_pdf(file_path):
    logger.info("Extracting data from PDF")
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''.join(page.extract_text() or '' for page in reader.pages)
        
        data = {'Date': [], 'Expense': [], 'Type of Expense': []}
        for line in text.split('\n'):
            parts = line.split()
            if len(parts) >= 3 and parts[0].count('-') == 2:
                try:
                    date = parts[0]
                    expense = float(parts[-1])
                    type_expense = ' '.join(parts[1:-1])
                    data['Date'].append(date)
                    data['Expense'].append(expense)
                    data['Type of Expense'].append(type_expense)
                except (ValueError, IndexError):
                    continue
        
        if not data['Date']:
            logger.warning("No valid data extracted from PDF")
            return None
        
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='%Y-%m-%d')
        df['Expense'] = pd.to_numeric(df['Expense'], downcast='float')
        df['Type of Expense'] = df['Type of Expense'].astype('category')
        df = df.dropna(subset=['Date', 'Expense'])
        
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        return {
            'time_series': df.groupby('Month', observed=True)['Expense'].sum().to_dict(),
            'type_summary': df.groupby('Type of Expense', observed=True)['Expense'].sum().to_dict(),
            'total': float(df['Expense'].sum()),
            'years': list(range(df['Date'].min().year, df['Date'].max().year + 1)),
            'months': df['Month'].unique().tolist(),
            'expense_types': df['Type of Expense'].cat.categories.tolist()
        }
    except Exception as e:
        logger.error(f"PDF extraction error: {str(e)}")
        return None

def calculate_savings_goal(total_expenses, monthly_income, goal_type, goal_cost, type_summary, filtered_time_series):
    logger.info(f"Calculating savings: total_expenses={total_expenses}, monthly_income={monthly_income}, goal_cost={goal_cost}")
    
    # Calculate monthly average expenses
    num_months = len(filtered_time_series) if filtered_time_series else 1  # Default to 1 if no filter
    monthly_expenses = total_expenses / num_months if num_months > 0 else total_expenses
    logger.info(f"Monthly expenses (average over {num_months} months): {monthly_expenses}")
    
    monthly_savings = monthly_income - monthly_expenses
    logger.info(f"Initial monthly savings: {monthly_savings}")
    
    # Base case without cuts
    if monthly_savings <= 0:
        base_result = {'error': 'No savings possible without cuts—see adjusted scenario.'}
    else:
        base_months = goal_cost / monthly_savings
        base_result = {
            'months': round(base_months, 1),
            'years': round(base_months / 12, 1),
            'monthly_savings': round(monthly_savings, 2),
            'cuts': {}
        }
        logger.info(f"Base case: months={base_months}, savings={monthly_savings}")

    # Automated cuts (10% on non-essential expenses)
    protected_types = ['Rent', 'Education']
    cut_percentage = 10
    total_cut_amount = 0
    cuts_details = {}

    filtered_total = sum(filtered_time_series.values()) if filtered_time_series else total_expenses
    monthly_filtered = filtered_total / num_months if num_months > 0 else filtered_total
    logger.info(f"Filtered total expenses: {filtered_total}, monthly: {monthly_filtered}")

    for expense_type, amount in type_summary.items():
        if expense_type not in protected_types:
            type_proportion = amount / total_expenses
            type_in_filtered = monthly_filtered * type_proportion
            cut_amount = type_in_filtered * (cut_percentage / 100)
            total_cut_amount += cut_amount
            cuts_details[expense_type] = {
                'percentage': cut_percentage,
                'amount': round(cut_amount, 2)
            }
            logger.info(f"Cut applied: {expense_type} - {cut_percentage}% (₹{cut_amount})")

    adjusted_expenses = monthly_filtered - total_cut_amount
    adjusted_savings = monthly_income - adjusted_expenses
    
    if adjusted_savings > 0:
        adjusted_months = goal_cost / adjusted_savings
        base_result.update({
            'adjusted_months': round(adjusted_months, 1),
            'adjusted_years': round(adjusted_months / 12, 1),
            'adjusted_monthly_savings': round(adjusted_savings, 2),
            'cuts': cuts_details,
            'total_cut_amount': round(total_cut_amount, 2),
            'monthly_expenses': round(monthly_expenses, 2)
        })
        logger.info(f"Adjusted case: months={adjusted_months}, savings={adjusted_savings}, total_cut={total_cut_amount}")
    else:
        base_result.update({'error': 'No savings possible even with cuts—reduce expenses further or increase income!'})
        logger.warning("Adjusted savings still negative after cuts")

    return base_result
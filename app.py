from flask import Flask, render_template, request, redirect, url_for
import json
import os
import threading
import webbrowser

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key for production

# JSON files for storing each form's data.
# Each file stores a dictionary mapping a save name to the record.
DATA_FILES = {
    'w2': 'w2_data.json',
    '1099-int': '1099int_data.json',
    '1099-div': '1099div_data.json',
    '1099-ssa': '1099ssa_data.json',
    '1099-r': '1099r_data.json'
}

# --------------------------
# Helper Functions
# --------------------------
def save_data(form_type, data):
    file_name = DATA_FILES.get(form_type)
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            try:
                records = json.load(f)
                if not isinstance(records, dict):
                    records = {}
            except json.JSONDecodeError:
                records = {}
    else:
        records = {}
    records[data['save_name']] = data
    with open(file_name, 'w') as f:
        json.dump(records, f, indent=4)

def load_record(form_type, save_name):
    file_name = DATA_FILES.get(form_type)
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            try:
                records = json.load(f)
                return records.get(save_name)
            except json.JSONDecodeError:
                return None
    return None

def get_options(form_type):
    file_name = DATA_FILES.get(form_type)
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            try:
                records = json.load(f)
                # return the list of save names
                return list(records.keys())
            except json.JSONDecodeError:
                return []
    return []

# --------------------------
# Existing Form Routes
# (These remain essentially the same as before, with a "save_name" field.)
# --------------------------
@app.route('/w2')
def w2():
    save_name = request.args.get('save_name')
    record = load_record('w2', save_name) if save_name else None
    return render_template('w2.html', title="W-2 Input", active_tab='w2', record=record)

@app.route('/submit/w2', methods=['POST'])
def submit_w2():
    data = {
        "save_name": request.form.get('save_name'),
        "employee_ssn": request.form.get('employee_ssn'),
        "employer_ein": request.form.get('employer_ein'),
        "employer_name": request.form.get('employer_name'),
        "employer_address": request.form.get('employer_address'),
        "employee_name": request.form.get('employee_name'),
        "employee_address": request.form.get('employee_address'),
        "wages": request.form.get('wages'),
        "federal_tax": request.form.get('federal_tax'),
        "social_security_wages": request.form.get('social_security_wages'),
        "social_security_tax": request.form.get('social_security_tax'),
        "medicare_wages": request.form.get('medicare_wages'),
        "medicare_tax": request.form.get('medicare_tax'),
        "additional_information": request.form.get('additional_information')
    }
    save_data('w2', data)
    return redirect(url_for('w2', save_name=data["save_name"]))

@app.route('/1099-int')
def int_form_view():
    save_name = request.args.get('save_name')
    record = load_record('1099-int', save_name) if save_name else None
    return render_template('1099-int.html', title="1099-INT Input", active_tab='1099-int', record=record)

@app.route('/submit/1099-int', methods=['POST'])
def submit_int():
    data = {
        "save_name": request.form.get('save_name'),
        "payer_name": request.form.get('payer_name'),
        "payer_address": request.form.get('payer_address'),
        "recipient_tin": request.form.get('recipient_tin'),
        "recipient_name": request.form.get('recipient_name'),
        "interest_income": request.form.get('interest_income'),
        "federal_tax_withheld": request.form.get('federal_tax_withheld'),
        "additional_information": request.form.get('additional_information')
    }
    save_data('1099-int', data)
    return redirect(url_for('int_form_view', save_name=data["save_name"]))

@app.route('/1099-div')
def div_form_view():
    save_name = request.args.get('save_name')
    record = load_record('1099-div', save_name) if save_name else None
    return render_template('1099-div.html', title="1099-DIV Input", active_tab='1099-div', record=record)

@app.route('/submit/1099-div', methods=['POST'])
def submit_div():
    data = {
        "save_name": request.form.get('save_name'),
        "payer_name": request.form.get('payer_name'),
        "payer_address": request.form.get('payer_address'),
        "recipient_tin": request.form.get('recipient_tin'),
        "recipient_name": request.form.get('recipient_name'),
        "total_ordinary_dividends": request.form.get('total_ordinary_dividends'),
        "qualified_dividends": request.form.get('qualified_dividends'),
        "total_capital_gain_distributions": request.form.get('total_capital_gain_distributions'),
        "federal_tax_withheld": request.form.get('federal_tax_withheld'),
        "additional_information": request.form.get('additional_information')
    }
    save_data('1099-div', data)
    return redirect(url_for('div_form_view', save_name=data["save_name"]))

@app.route('/1099-ssa')
def ssa_form_view():
    save_name = request.args.get('save_name')
    record = load_record('1099-ssa', save_name) if save_name else None
    return render_template('1099-ssa.html', title="1099-SSA Input", active_tab='1099-ssa', record=record)

@app.route('/submit/1099-ssa', methods=['POST'])
def submit_ssa():
    data = {
        "save_name": request.form.get('save_name'),
        "payer_name": request.form.get('payer_name'),
        "payer_address": request.form.get('payer_address'),
        "recipient_ssn": request.form.get('recipient_ssn'),
        "recipient_name": request.form.get('recipient_name'),
        "social_security_benefit": request.form.get('social_security_benefit'),
        "federal_tax_withheld": request.form.get('federal_tax_withheld'),
        "additional_information": request.form.get('additional_information')
    }
    save_data('1099-ssa', data)
    return redirect(url_for('ssa_form_view', save_name=data["save_name"]))

@app.route('/1099-r')
def r_form_view():
    save_name = request.args.get('save_name')
    record = load_record('1099-r', save_name) if save_name else None
    return render_template('1099-r.html', title="1099-R Input", active_tab='1099-r', record=record)

@app.route('/submit/1099-r', methods=['POST'])
def submit_r():
    data = {
        "save_name": request.form.get('save_name'),
        "payer_name": request.form.get('payer_name'),
        "payer_address": request.form.get('payer_address'),
        "recipient_tin": request.form.get('recipient_tin'),
        "recipient_name": request.form.get('recipient_name'),
        "gross_distribution": request.form.get('gross_distribution'),
        "taxable_amount": request.form.get('taxable_amount'),
        "federal_tax_withheld": request.form.get('federal_tax_withheld'),
        "distribution_code": request.form.get('distribution_code'),
        "additional_information": request.form.get('additional_information')
    }
    save_data('1099-r', data)
    return redirect(url_for('r_form_view', save_name=data["save_name"]))

# --------------------------
# New 1040 Routes
# --------------------------
# Display the 1040 page – it gathers available records from all form types.
@app.route('/1040')
def form_1040():
    w2_options = get_options('w2')
    int_options = get_options('1099-int')
    div_options = get_options('1099-div')
    ssa_options = get_options('1099-ssa')
    r_options = get_options('1099-r')
    # Optionally, if query parameters are provided, load a record to pre-populate the 1040.
    w2_record = load_record('w2', request.args.get('w2_save')) if request.args.get('w2_save') else None
    int_record = load_record('1099-int', request.args.get('int_save')) if request.args.get('int_save') else None
    div_record = load_record('1099-div', request.args.get('div_save')) if request.args.get('div_save') else None
    ssa_record = load_record('1099-ssa', request.args.get('ssa_save')) if request.args.get('ssa_save') else None
    r_record = load_record('1099-r', request.args.get('r_save')) if request.args.get('r_save') else None
    
    return render_template('1040.html',
                           title="1040 Form",
                           active_tab='1040',
                           w2_options=w2_options,
                           int_options=int_options,
                           div_options=div_options,
                           ssa_options=ssa_options,
                           r_options=r_options,
                           w2_record=w2_record,
                           int_record=int_record,
                           div_record=div_record,
                           ssa_record=ssa_record,
                           r_record=r_record)

# When the user clicks Save on the 1040 page, aggregate the data,
# perform calculations, and save the consolidated record.
@app.route('/submit/1040', methods=['POST'])
def submit_1040():
    # Retrieve chosen saved record names from each form.
    chosen_w2 = request.form.get('w2_save')
    chosen_int = request.form.get('int_save')
    chosen_div = request.form.get('div_save')
    chosen_ssa = request.form.get('ssa_save')
    chosen_r = request.form.get('r_save')
    # Load records if selected.
    w2_record = load_record('w2', chosen_w2) if chosen_w2 else {}
    int_record = load_record('1099-int', chosen_int) if chosen_int else {}
    div_record = load_record('1099-div', chosen_div) if chosen_div else {}
    ssa_record = load_record('1099-ssa', chosen_ssa) if chosen_ssa else {}
    r_record = load_record('1099-r', chosen_r) if chosen_r else {}
    
    # Perform basic calculations.
    try:
        wages = float(w2_record.get('wages', 0))
    except:
        wages = 0
    try:
        interest = float(int_record.get('interest_income', 0))
    except:
        interest = 0
    try:
        dividends = float(div_record.get('total_ordinary_dividends', 0))
    except:
        dividends = 0
    try:
        ssa_benefit = float(ssa_record.get('social_security_benefit', 0))
    except:
        ssa_benefit = 0
    try:
        gross_dist = float(r_record.get('gross_distribution', 0))
    except:
        gross_dist = 0
    total_income = wages + interest + dividends + ssa_benefit + gross_dist
    
    try:
        federal_tax_w2 = float(w2_record.get('federal_tax', 0))
    except:
        federal_tax_w2 = 0
    try:
        federal_tax_int = float(int_record.get('federal_tax_withheld', 0))
    except:
        federal_tax_int = 0
    try:
        federal_tax_div = float(div_record.get('federal_tax_withheld', 0))
    except:
        federal_tax_div = 0
    try:
        federal_tax_ssa = float(ssa_record.get('federal_tax_withheld', 0))
    except:
        federal_tax_ssa = 0
    try:
        federal_tax_r = float(r_record.get('federal_tax_withheld', 0))
    except:
        federal_tax_r = 0
    total_federal_tax_withheld = federal_tax_w2 + federal_tax_int + federal_tax_div + federal_tax_ssa + federal_tax_r
    
    # Aggregate the 1040 record.
    data = {
        "1040_save_name": request.form.get('1040_save_name'),
        "w2": w2_record,
        "1099_int": int_record,
        "1099_div": div_record,
        "1099_ssa": ssa_record,
        "1099_r": r_record,
        "total_income": total_income,
        "total_federal_tax_withheld": total_federal_tax_withheld
    }
    
    # Save the aggregated record in 1040_data.json.
    file_name = '1040_data.json'
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            try:
                records = json.load(f)
                if not isinstance(records, dict):
                    records = {}
            except json.JSONDecodeError:
                records = {}
    else:
        records = {}
    records[data["1040_save_name"]] = data
    with open(file_name, 'w') as f:
        json.dump(records, f, indent=4)
    
    return redirect(url_for('form_1040'))

# --------------------------
# Auto-Open Browser and Run
# --------------------------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/w2")

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from App.controllers.entry import add_entry, get_all_entries, submit_entries_for_review

entry_views = Blueprint('entry_views', __name__, template_folder='../templates')

@entry_views.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        # --- DEBUG LOG ---
        print("👉 Received POST to /entry with form data:", dict(request.form))

        # --- COMMON FIELDS ---
        year     = request.form.get('year') or ''
        campus   = request.form.get('campus') or ''
        category = request.form.get('question_type') or 'General Entry'

        label = None
        value = None

        # --- CATEGORY-SPECIFIC PARSING ---
        if category == 'degree_percent':
            age     = request.form.get('age')
            degree  = request.form.get('degree')
            percent = request.form.get('percent')
            if not (age and degree and percent):
                flash("Please fill out age, degree and percentage.", "danger")
                return redirect(url_for('entry_views.entry'))
            label = f"{percent}% of age {age} in {degree}"
            try:
                value = int(percent)
            except ValueError:
                flash("Percentage must be a number.", "danger")
                return redirect(url_for('entry_views.entry'))

        elif category == 'avg_gpa_age':
            age = request.form.get('age')
            gpa = request.form.get('gpa')
            if not (age and gpa):
                flash("Please fill out age and GPA.", "danger")
                return redirect(url_for('entry_views.entry'))
            label = f"Avg GPA for age {age}"
            try:
                value = float(gpa)
            except ValueError:
                flash("GPA must be a number.", "danger")
                return redirect(url_for('entry_views.entry'))

        elif category == 'housing_feedback':
            rating  = request.form.get('housing_rating')
            comment = request.form.get('housing_comment', '')
            if not rating:
                flash("Please provide a housing rating (1–5).", "danger")
                return redirect(url_for('entry_views.entry'))
            label = f"Housing Rating {rating}: {comment or 'No comment'}"
            try:
                value = int(rating)
            except ValueError:
                flash("Rating must be an integer between 1 and 5.", "danger")
                return redirect(url_for('entry_views.entry'))

        else:
            # Fallback generic entry
            label = request.form.get('label') or ''
            raw_val = request.form.get('value')
            if raw_val is None:
                flash("Please provide a label and value.", "danger")
                return redirect(url_for('entry_views.entry'))
            label = label or 'N/A'
            try:
                value = float(raw_val)
            except ValueError:
                flash("Value must be a number.", "danger")
                return redirect(url_for('entry_views.entry'))

        # --- SAVE TO DB ---
        user_id = session.get('user_id')
        add_entry(category, label, value, year=year, campus=campus, user_id=user_id)
        flash("✅ Entry submitted successfully!", "success")
        return redirect(url_for('entry_views.entry'))

    # GET: show form & current entries
    data = get_all_entries()
    print("📦 Entries shown on page:", data)  # debug
    return render_template('entry.html', data=data)


@entry_views.route('/entry/submit', methods=['POST'])
def submit_for_review():
    submit_entries_for_review()
    flash("Your entries have been submitted for admin review.", "info")
    return redirect(url_for('entry_views.entry'))


@entry_views.route('/api/entries', methods=['GET'])
def api_entries():
    data = get_all_entries()
    return jsonify([{'label': e.label, 'value': e.value} for e in data])

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from App.controllers.entry import add_entry, get_all_entries, submit_entries_for_review

entry_views = Blueprint('entry_views', __name__, template_folder='../templates')

@entry_views.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST' and request.form.get('submit_data'):
        year = request.form.get('year')
        campus = request.form.get('campus')
        category = request.form.get('question_type') or 'General Entry'
        label = ''
        value = 0

        if category == 'degree_percent':
            age = request.form.get('age')
            degree = request.form.get('degree')
            percent = request.form.get('percent')
            label = f"{percent}% of age {age} in {degree}"
            value = int(percent)

        elif category == 'avg_gpa_age':
            age = request.form.get('age')
            gpa = request.form.get('gpa')
            label = f"Avg GPA for age {age}"
            value = float(gpa)

        elif category == 'housing_feedback':
            rating = request.form.get('housing_rating')
            comment = request.form.get('housing_comment') or 'No comment'
            label = f"Housing Rating {rating}: {comment}"
            value = int(rating)

        # FINAL STEP: SAVE TO DB
        from App.controllers.entry import add_entry
        add_entry(category, label, value, year=year, campus=campus)
        flash("✅ Entry submitted successfully!", "success")
        return redirect(url_for('entry_views.entry'))

    # Load and show entries
    from App.controllers.entry import get_all_entries
    data = get_all_entries()
    print("📦 Entries shown on page:", data)
    return render_template('entry.html', data=data)

    # Load all current entries
    data = get_all_entries()
    print("📦 Entries shown on page:", data)  # Debugging line, remove later
    return render_template('entry.html', data=data)

@entry_views.route('/entry/submit', methods=['POST'])
def submit_for_review():
    submit_entries_for_review()
    flash("Your entries have been submitted for admin review.", "info")
    return redirect(url_for('entry_views.entry'))

@entry_views.route('/api/entries', methods=['GET'])
def api_entries():
    data = get_all_entries()
    return jsonify([
        {'label': e.label, 'value': e.value}
        for e in data
    ])

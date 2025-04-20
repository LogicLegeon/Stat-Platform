from flask import Blueprint, render_template, request, redirect, url_for
from App.controllers.entry import add_entry, get_all_entries

entry_views = Blueprint('entry_views', __name__, template_folder='../templates')

@entry_views.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        category = request.form['category']
        label = request.form['label']
        value = int(request.form['value'])
        add_entry(category, label, value)
        return redirect(url_for('entry_views.entry'))

    data = get_all_entries()
    return render_template('entry.html', data=data)

import os
from datetime import datetime
from flask import request, render_template, redirect, url_for, session, current_app, flash, abort
from project import app
from project.functions.functions import food, convert_iso_datetime, terms_conditions, process_file


@app.route('/', methods=['GET'])
def landing():
    try:
        """
        - Method: GET
        - Displays landing page
        - Show welcome message if first session.
        - Passes food options to `landing.html` template.
        """
        return render_template('landing.html', food=food(), show_hero=True)
    except Exception as e:
        abort(500, description=str(e))


@app.route('/pre-submit', methods=['GET', 'POST'])
def pre_submit():
    try:
        """
        Collects form from landing,redirects to /review
        - Methods: GET, POST
        - GET: Redirect to Landing
        - POST:
            - Clears old form data
            - Validates file uploaded
            - Get new form data (name, datetime, selected papers, uploaded file).
            - Process/extract content from uploaded file.
            - Stores form data in session
            - Redirects to review template
        """
        if request.method == 'GET':
            session['show_welcome_msg'] = True
            return redirect(url_for('landing'))
        # new request so remove clients previous session data
        session.pop('form_data', None)
        file = request.files.get("uploadedFile")
        if not file:
            flash("Please upload a file to continue.", "info")
            return redirect(url_for('landing'))
        try:
            session['form_data'] = {
                'fullName': request.form.get('fullName'),
                'foodChoiceDateTime': convert_iso_datetime(request.form.get('foodChoiceDateTime')),
                'food': request.form.getlist('food'),
                'file': process_file(file)
            }
        except ValueError as e:
            abort(400, description=str(e))
        return redirect(url_for('review'))
    except Exception as e:
        abort(500, description=str(e))


@app.route('/review', methods=['GET'])
def review():
    try:
        """
        Review route. User reviews their choices before submitting.
        - Method: GET
        - Requires `form_data` in session, else redirects to `landing.html`.
        - Injects terms and conditions to template
        - Renders `presubmit.html` template with session form data
            and user confirmation before final submission.
        """
        if not session.get('form_data'):
            session['show_welcome_msg'] = True
            return redirect(url_for('landing'))

        tc = terms_conditions()
        return render_template('presubmit.html',
                                form_data=session['form_data'],
                                terms_conditions = tc)
    except Exception as e:
        abort(500, description=str(e))


@app.route('/submit', methods=['POST'])
def submit():
    try:
        """
        Submit route.
        - Methods: GET, POST
        - GET: Ensures session form data exists; else redirect to landing.
        - POST:
            - Retrieves user-submitted data from session.
            - Generates timestamped filename.
            - Saves submission details (name, datetime, food choices, and file data)
                into a text file inside `saved_files/`.
            - Removes `form_data` from session to prevent duplicate submissions.
            - Renders `submitted.html` to confirm submission to user.
        """

        # in case user navigates back and clicks submit
        if not session.get('form_data'):
            return redirect(url_for('landing'))

        name = session['form_data']['fullName']
        processed_name = name.lower().replace(" ", "-")
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        folder = os.path.join(current_app.root_path, 'saved_files')
        file_id = f"{processed_name}-{now}"
        file_path = os.path.join(folder, f"{file_id}.txt")

        with open(file_path, 'w') as f:
            f.write(f"Name: {name}\n")
            f.write(f"Date and Time: {session['form_data']['foodChoiceDateTime']}\n")
            for index, p in enumerate(session['form_data']['food'], start=1):
                f.write(f"Food choice {index}: {p}\n")
            f.write(f"File: {session['form_data']['file']}\n")
        # avoiding duplicate submissions
        session.pop('form_data', None)
        return render_template('submitted.html', name=name, file_id=file_id)
    except Exception as e:
        abort(500, description=str(e))


@app.route('/submission-review/<submission_id>', methods=['GET'])
def submission_review(submission_id):
    try:
        """
        Review route. User reviews their choices after submission.
        - Method: GET
        - Accepts `submission_id` path parameter, which corresponds to a saved filename (without .txt) in `saved_files/`.
        - If file not found, flashes message and redirects to landing.
        - If found, file content is parsed into a dict and passed to `submission_review.html`.
        """
        folder = os.path.join(current_app.root_path, 'saved_files')
        file_path = os.path.join(folder, f"{submission_id}.txt")  # add .txt automatically
        if not os.path.exists(file_path):
            flash("No submission found for provided ID.", "danger")
            return redirect(url_for('landing'))
        # Read and parse the saved file into a dict
        saved_data = {}
        with open(file_path, 'r') as f:
            for line in f:
                if ":" in line:
                    key, value = line.split(":", 1)
                    saved_data[key.strip()] = value.strip()
        return render_template('submission-review.html', saved_file=saved_data)
    except Exception as e:
        abort(500, description=str(e))








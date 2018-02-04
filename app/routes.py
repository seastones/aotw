from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SubmissionForm
import app.database as database

@app.route('/')
@app.route('/index')
def index():
    current_album = database.get_current_album()
    if current_album == False:
        error_report = "There is currently no album selected."
        return render_template('index.html', error_report=error_report)
    else:
        return render_template('index.html', title=current_album['album_title'], info=current_album)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmissionForm()
    if form.validate_on_submit():
        db_submission = {'album_title': form.album_title.data, 'album_artist': form.album_artist.data, 'user': form.user.data, 'details': form.details.data}
        if database.submit_album(db_submission) == True:
            flash("Album submitted!")
        else:
            flash("Something may have gone wrong...")
        return redirect(url_for('index'))
    return render_template('submission.html', title='Submission Form', form=form)

@app.route('/pending')
@app.route('/pending/page<int:page>')
def current_submission_list(page=1):
    length = database.db_list_length('submission_list')
    total_pages = int(length / 25) + 1
    named_submissions = database.submission_names('submission_list',((page - 1)*25),((page*25) - 1))
    return render_template('list.html', list_type='Pending Submissions', to_list=named_submissions, page=page,last_page=total_pages,page_type='current')

@app.route('/previous')
@app.route('/previous/page<int:page>')
def past_submissions_list(page=1):
    length = database.db_list_length('previous_submissions')
    total_pages = int(length / 25) + 1
    named_submissions = database.submission_names('previous_submissions',((page - 1)*25),((page*25) - 1))
    return render_template('list.html', list_type='Previous Submissions', to_list=named_submissions, page=page,last_page=total_pages,page_type='previous')

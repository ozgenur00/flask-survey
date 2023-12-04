from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "Iknownothinghehe"
# debug = DebugToolbarExtension(app)

@app.route('/')
def home_page_survey():
    """Select a survey."""

    return render_template("survey_start.html", survey=survey)

@app.route('/begin', methods=["POST"])
def start_survey():
    """Clear the session of responses"""

    session[RESPONSES_KEY] = []

    return redirect('/questions/0')


@app.route('/answer', methods=["POST"])
def handling_question():
    """Save the response and redirect to the next question."""

    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route('/questions/<int:qid>')
def show_question(qid):
    """display the question you in"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')
    
    if (len(responses) != qid):

        flash(f"Invalid question id: {qid}.")
        return redirect(f'/questions/{len(responses)}')
    
    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route('/complete')
def complete():
    """Show completion page"""
    return render_template('completion.html')

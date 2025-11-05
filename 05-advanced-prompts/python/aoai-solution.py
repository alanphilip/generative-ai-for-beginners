
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from dotenv import load_dotenv
import os, logging

load_dotenv()  # Load variables from .env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

class HelloForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def hello():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        # Optionally flash a message
        flash(f'Hello, {name} ({email})!')
        # Redirect to a success page or render it directly
        return render_template('success.html', name=name, email=email)
        #return redirect(url_for('hello'))  # Clears form on reload
    return render_template('hello.html', form=form)


@app.errorhandler(400)
def bad_request(error):
    return jsonify(error='Bad request', message=str(error)), 400

@app.errorhandler(404)
def page_not_found(error):
    return '404 - Page Not Found', 404

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {e}")
    return 'Something went wrong', 500

if __name__ == '__main__':
    app.run(debug=True)

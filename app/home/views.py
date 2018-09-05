from flask import abort, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import home
from app.home.forms import IdeaForm

from .. import db
from ..models import User, Idea


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/terms')
def terms():
    """
    Render the homepage template on the / route
    """
    return render_template('home/terms.html', title="Terms Of Service")


@home.route('/privacy')
def privacy():
    """
    Render the homepage template on the / route
    """
    return render_template('home/privacy.html', title="Privacy Policy")


# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")


# Ideas

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard", current_user=current_user)


@home.route('/profile')
@login_required
def profile():
     return render_template('home/profile.html', title="Profile", current_user=current_user)



@home.route('/ideas', methods=['GET', 'POST'])
@login_required
def list_ideas():
    """
    List all ideas for a user
    """

    ideas = Idea.query.all()

    return render_template('home/ideas.html',
                           ideas=ideas, title="Ideas")


@home.route('/ideas/add', methods=['GET', 'POST'])
@login_required
def add_idea():
    """
    Add a idea to the database
    """

    add_idea = True

    form = IdeaForm()
    if form.validate_on_submit():
        idea = Idea(name=form.name.data,
                    category=form.category.data,
                    description=form.description.data,
                    retailer=form.retailer.data,
                    user_id=current_user.id)
        try:
            # add idea to the database
            db.session.add(idea)
            db.session.commit()
            flash('You have successfully added a new idea.')
        except:
            # in case idea name already exists
            flash('Error: idea name already exists.')

            # redirect to ideas page
        return redirect(url_for('home.list_ideas'))

    # load idea template
    return render_template('home/idea.html', action="Add",
                           add_idea=add_idea, form=form,
                           title="Add Idea")


@home.route('/ideas/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_idea(id):
    """
    Edit an idea
    """

    add_idea = False

    idea = Idea.query.get_or_404(id)
    form = IdeaForm(obj=idea)
    if form.validate_on_submit():
        idea.name = form.name.data
        idea.category = form.category.data
        idea.description = form.description.data
        idea.retailer = form.retailer.data
        idea.id = current_user.id
        db.session.commit()
        flash('You have successfully edited the idea.')

        # redirect to the ideas page
        return redirect(url_for('idea.list_ideas'))

    form.description.data = idea.description
    form.name.data = idea.name
    return render_template('home/idea.html', action="Edit",
                           add_idea=add_idea, form=form,
                           idea=idea, title="Edit Idea")


@home.route('/ideas/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_idea(id):
    """
    Delete a idea from the database
    """

    idea = Idea.query.get_or_404(id)
    db.session.delete(idea)
    db.session.commit()
    flash('You have successfully deleted the idea.')

    # redirect to the ideas page
    return redirect(url_for('home.list_ideas'))

    # return render_template(title="Delete Idea")

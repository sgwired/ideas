from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from app.admin.forms import GroupForm
from .. import db
from ..models import Group


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Group Views


@admin.route('/groups', methods=['GET', 'POST'])
@login_required
def list_groups():
    """
    List all groups
    """
    check_admin()

    groups = Group.query.all()

    return render_template('admin/groups/groups.html',
                           groups=groups, title="Groups")


@admin.route('/groups/add', methods=['GET', 'POST'])
@login_required
def add_group():
    """
    Add a group to the database
    """
    check_admin()

    add_group = True

    form = GroupForm()
    if form.validate_on_submit():
        group = Group(name=form.name.data,
                                description=form.description.data)
        try:
            # add group to the database
            db.session.add(group)
            db.session.commit()
            flash('You have successfully added a new group.')
        except:
            # in case group name already exists
            flash('Error: group name already exists.')

        # redirect to groups page
        return redirect(url_for('admin.list_groups'))

    # load group template
    return render_template('admin/groups/group.html', action="Add",
                           add_group=add_group, form=form,
                           title="Add Group")


@admin.route('/groups/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_group(id):
    """
    Edit a group
    """
    check_admin()

    add_group = False

    group = Group.query.get_or_404(id)
    form = GroupForm(obj=group)
    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the group.')

        # redirect to the groups page
        return redirect(url_for('admin.list_groups'))

    form.description.data = group.description
    form.name.data = group.name
    return render_template('admin/groups/group.html', action="Edit",
                           add_group=add_group, form=form,
                           group=group, title="Edit Group")


@admin.route('/groups/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_group(id):
    """
    Delete a group from the database
    """
    check_admin()

    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    flash('You have successfully deleted the group.')

    # redirect to the groups page
    return redirect(url_for('admin.list_groups'))

    return render_template(title="Delete Group")
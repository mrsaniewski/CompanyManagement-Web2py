# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
# ---- example index page ----
def index():
    response.flash = T("Witaj na stronie głównej")
    return dict(user=auth.user, message=T('Welcome to web2py!'))


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status': 'success', 'email': auth.user.email})


# ---- Smart Grid (example) -----
@auth.requires_membership('admin')  # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html'  # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)


# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu()  # add the wiki to the menu
    return auth.wiki()


# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def tasks():
    form = SQLFORM(db.task)
    if form.process().accepted:
        db.task.created_time.default = request.now
        session.flash = 'Task added successfully!'
        redirect(URL('default', 'tasks'))
    return dict(form=form, user=auth.user)


def delete_task():
    task_id = request.args(0)
    db(db.task.id == task_id).delete()
    session.flash = 'Task deleted successfully!'
    redirect(URL('default', 'tasks'))


def toggle_task():
    task_id = request.post_vars.task_id
    task = db.task(task_id)
    user_id = auth.user_id
    if user_id:
        db.point.update_or_insert(db.point.id == user_id, points=db.point.points + 20)
    task.update_record(completed=True)
    redirect(URL('default', 'tasks'))


def loyality():
    response.flash = T("Loyality")
    return dict(user=auth.user, message=T('Welcome to about!'))

def toggle_prize():
    prize_id = request.post_vars.prize_id
    prize = db.prize(prize_id)
    user_id = auth.user_id
    val = prize.valu
    if user_id:
        db.point.update_or_insert(db.point.id == user_id, points=db.point.points - val)
    prize.update_record(claimed=True)
    redirect(URL('default', 'loyality'))

def about():
    response.flash = T("About")
    return dict(user=auth.user, message=T('Welcome to about!'))

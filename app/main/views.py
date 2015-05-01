
from flask import render_template, session, redirect, url_for, current_app, flash, request, make_response
from .. import db
from ..models import User, Permission, Role, Post, Follow, Comment
from ..email import send_email
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from datetime import datetime
from ..decorators import admin_required, permission_required
from flask.ext.login import login_required, abort, current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    show_followed = False
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLE) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('main.index'))
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    if current_user.is_authenticated():
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POST_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, form=form, pagination=pagination, show_followed=show_followed)


@main.route('/invite', methods=['GET', 'POST'])
def invite():
    form = NameForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email = form.name.data).first()
        if user is  None:
            #user= User(username = form.name.data)
            #db.session.add(user)
            #db.session.commit()
            session['known']= False
            send_email(form.name.data, 'This message is send on behalf of '+str(current_user.username), 'mail/new_user', user=current_user.username , message=form.message.data)
        else:

            session['known']= True
            pass
            flash('User is already on board.')
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            pass
            # flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data= ''
        return redirect(url_for('.index'))
    return render_template('invite.html', form=form, name=session.get('name'),  current_time=datetime.utcnow(), known=session.get('known', False))


@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return "For Administrators!"


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For Comment moderators!"


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    if user is None:
        abort(404)
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    user = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.username.data = user.about_me
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    if post.views is None:
        post.views = 1
    else:
        post.views = int(post.views) + 1
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data,
            post=post,
            author=current_user._get_current_object()
        )
        db.session.add(comment)
        flash('Your comment have been publish')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
            current_app.config['FLASK_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASK_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form, comments=comments, pagination=pagination, endpoint='.post')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user ==  post.author or  current_user.can(Permission.ADMINISTER):
        form = PostForm()
        if form.validate_on_submit():
            post.body = form.body.data
            db.session.add(post)
            flash('The  post has updated')
            return redirect(url_for('.post', id=post.id))
    else:
        abort(403)
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/user-list/')
@login_required
def user_list():
    users = User.query.order_by(User.last_seen.desc()).all()
    if (users is None):
        abort(500)
    return render_template('user_list.html', users=users)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid User')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page = current_app.config['FLASK_FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    follows = [{'user': item.follower, 'timestamp': item.timestamp } for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of ", endpoint='.followers', pagination=pagination, follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASK_FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    follows = [{'user': item.followed, 'timestamp': item.timestamp } for item in pagination.items]
    return render_template('followers.html', user=user, title="Following by ", endpoint='.followed_by', pagination=pagination, follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page = current_app.config['FLASK_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('moderate.html', comments=comments, pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))

@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Liii0531@localhost:3306/photopia?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_LLS'] = True
app.config['MAIL_USERNAME'] = 'photopiaofficial@126.com'
app.config['MAIL_PASSWORD'] = 'JUGARWBNRAHBDOAP'
app.config['MAIL_DEFAULT_SENDER'] = 'photopiaofficial@126.com'

from app.models.model import db
from app.models.users import User
from app.models.works import Artworks
from app.models.resetpasswd import PasswordResetCode
from app.models.likes import Like
from app.models.collects import Collect
from app.models.follows import Follow
from app.models.comments import Comment
from app.models.places import Places
from app.models.devices import Devices
from app.models.notice import Notice

import base64
import requests

from sqlalchemy import or_
from flask import flash

import hashlib
import re
from sqlalchemy import func

import random
import string
from flask_mail import Mail, Message

from werkzeug.utils import secure_filename
from qiniu import Auth, put_data

from werkzeug.utils import secure_filename

# 七牛云配置
ACCESS_KEY = 'lhI10PH16FA9XwN466ObuakhIvfj_7M2eptgYl2P'
SECRET_KEY = '_fXrxKdrs3n8cxI0e5snwSzpCiZ3gcCau7NB-T6-'
BUCKET_NAME = 'photopia'

# 初始化七牛云的认证
q = Auth(ACCESS_KEY, SECRET_KEY)


#密码加密
def encrypt_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode("utf-8"))
    return md5.hexdigest()

#检查密码是否符合要求
def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[a-zA-Z]', password):
        return False
    return True

# @：装饰器，将函数原本没有的功能加入
@app.route('/')
def index_page():
    if 'username' in session:
        return redirect(url_for('list_artwork'))
    else:
        return redirect(url_for('login'))
    

@app.route('/index')
def list_artwork():
    if 'username' in session:

        current_user = User.query.filter_by(user_name=session['username']).first()

        page = request.args.get('page', 1, type=int)  # 页码从请求的查询参数中获取
        artwork_type = request.args.get('type')  # 获取作品类型参数
        search_query = request.args.get('search')  # 获取搜索参数
        per_page = 12  # 每页显示数量设为15

        query = Artworks.query  # 基础查询

        if search_query:
            # 更新查询以包含搜索条件
            query = query.filter(
                or_(
                    Artworks.artwork_name.ilike(f'%{search_query}%'),
                    Artworks.keyword1.ilike(f'%{search_query}%'),
                    Artworks.keyword2.ilike(f'%{search_query}%'),
                    Artworks.keyword3.ilike(f'%{search_query}%'),
                    Artworks.keyword4.ilike(f'%{search_query}%'),
                    Artworks.keyword5.ilike(f'%{search_query}%')
                )
            )
        elif artwork_type and artwork_type.isdigit():
            # 根据作品类型过滤结果
            artwork_type = int(artwork_type)
            query = query.filter_by(artwork_type=artwork_type)

        pagination = query.order_by(Artworks.artwork_id).paginate(page=page, per_page=per_page, error_out=False)

        works = pagination.items  # 当前页的作品列表
        total_pages = pagination.pages  # 总页数

        # 存储点赞数量
        likes_counts = {}
    
        # 存储点赞状态
        likes_status = {}

        # 对于每个作品获取作者名
        author_info = {}
        for work in works:
            user = User.query.filter_by(user_id=work.user_id).first()
            if user:
                author_info[work.artwork_id] = {'name': user.name, 'photo': user.photo}
            num_of_likes = Like.query.filter_by(liked_id=work.artwork_id).count()
            likes_counts[work.artwork_id] = num_of_likes

            # 检查当前用户是否点赞过该作品
            is_liked = Like.query.filter_by(user_id=current_user.user_id, liked_id=work.artwork_id).first() is not None
            likes_status[work.artwork_id] = is_liked

        # 在session中存储用户名
        session.permanent = True

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # 返回作品列表部分的HTML，包括分页控件
            return render_template(
            'works_list.html',
            works=works,
            author_info=author_info,
            likes_counts=likes_counts,
            likes_status=likes_status,
            current_page=page,
            total_pages=total_pages,
            search_query=search_query,
            photo = current_user.photo,
            current_user=current_user
        )
        else:
        # 返回整个页面的HTML
            return render_template(
            'index.html',
            works=works,
            author_info=author_info,
            likes_status=likes_status,
            likes_counts=likes_counts,
            username=session['username'],
            current_page=page,
            total_pages=total_pages,
            search_query=search_query,
            photo = current_user.photo,
            current_user=current_user
        )
    else:
        return redirect(url_for('login'))


@app.route('/work_detail/<int:workid>') 
def work_detail(workid):
    current_user = User.query.filter_by(user_name=session['username']).first()
    work = Artworks.query.filter_by(artwork_id=workid).first_or_404()
    author = User.query.filter_by(user_id=work.user_id).first_or_404()
    likes_count = Like.query.filter_by(liked_id=workid).count()

    num_of_collects = Collect.query.filter_by(collected_id=workid).count()
    
    # 一次性获取所有评论及对应的用户信息
    comments_with_users = db.session.query(Comment, User).join(User, Comment.user_id == User.user_id).filter(Comment.commented_id == workid).all()
    
    # 将评论和用户信息转换成更方便的结构
    work_comments = [comment for comment, user in comments_with_users]
    comment_user_mapping = {comment.comment_id: user for comment, user in comments_with_users}

    comment_likes_counts = {}
    for comment, _ in comments_with_users:
        comment_likes_counts[comment.comment_id] = Like.query.filter_by(liked_id=comment.comment_id).count()

    like_status = Like.query.filter_by(user_id=current_user.user_id, liked_id=work.artwork_id).first() is not None
    collect_status = Collect.query.filter_by(user_id=current_user.user_id, collected_id=work.artwork_id).first() is not None

    is_author = current_user.user_id == author.user_id

    follow_status = False
    if not is_author:
        follow_status = Follow.query.filter_by(follower_id=current_user.user_id, followed_id=author.user_id).first() is not None

    num_of_comments = len(work_comments)

    return render_template(
        'work_detail.html',
        work=work,
        author=author,
        likes_count=likes_count,
        num_of_collects=num_of_collects,
        work_comments=work_comments,
        num_of_comments=num_of_comments,
        like_status=like_status,
        collect_status=collect_status,
        is_author=is_author,
        follow_status=follow_status,
        current_user=current_user,
        comment_likes_counts=comment_likes_counts,
        comment_user_mapping=comment_user_mapping  # 新增传递用户信息映射
    )

#点赞操作
@app.route('/like/<int:artwork_id>', methods=['POST'])
def like_artwork(artwork_id):
    if 'username' not in session:
        # 如果用户没有登录，返回错误
        return jsonify({'error': 'User not logged in'}), 401

    user = User.query.filter_by(user_name=session['username']).first()
    if user is None:
        # 如果没有找到用户，返回错误
        return jsonify({'error': 'User not found'}), 404

    like = Like.query.filter_by(user_id=user.user_id, liked_id=artwork_id).first()
    
    # 点赞或取消点赞后，查询最新的点赞计数
    likes_count = Like.query.filter_by(liked_id=artwork_id).count()

    if like:
        # 如果已经点赞过，则取消点赞
        db.session.delete(like)
        db.session.commit()
        return jsonify({'result': 'unliked', 'likes_count': likes_count-1}), 200
    else:
        # 如果还没有点赞，添加点赞
        new_like = Like(user_id=user.user_id, liked_id=artwork_id,like_time=datetime.now(),like_type=1)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({'result': 'liked', 'likes_count': likes_count+1}), 200

# 作品详情页收藏操作
@app.route('/collect_artwork/<int:artwork_id>', methods=['POST'])
def collect_artwork(artwork_id):
    # 确保用户已经登录
    if 'username' not in session:
        return jsonify({'error': '用户未登录'}), 403
    
    current_user = User.query.filter_by(user_name=session['username']).first_or_404()
    current_user_id = current_user.user_id

    collect = Collect.query.filter_by(user_id=current_user_id, collected_id=artwork_id).first()

    # 收藏或取消收藏后，查询最新的计数
    num_of_collects = Collect.query.filter_by(collected_id=artwork_id).count()

    if collect:
        # 如果已经收藏了，则取消收藏
        db.session.delete(collect)
        db.session.commit()
        return jsonify({'result': 'uncollected', 'num_of_collects': num_of_collects-1}), 200
    else:
        # 否则，添加收藏
        new_collect = Collect(user_id=current_user_id, collected_id=artwork_id, collect_time=datetime.now())
        db.session.add(new_collect)
        db.session.commit()
        return jsonify({'result': 'collected', 'num_of_collects': num_of_collects+1}), 200

#关注操作
@app.route('/follow/<int:user_id>', methods=['POST'])
def follow(user_id):
    # 确保用户已经登录
    if 'username' not in session:
        return jsonify({'error': '用户未登录'}), 403
    
    current_user = User.query.filter_by(user_name=session['username']).first_or_404()
    
    follow = Follow.query.filter_by(follower_id=current_user.user_id).first()

    if follow:
        #如果已经关注则取消关注
        db.session.delete(follow)
        db.session.commit()
        return jsonify({'result': 'unfollowed'}), 200
    else:
        #否则关注
        new_follow = Follow(follower_id=current_user.user_id, followed_id=user_id, follow_time=datetime.now())
        db.session.add(new_follow)
        db.session.commit()
        return jsonify({'result': 'followed'}), 200
    
#保存作品评论
@app.route('/save_comment/<int:artwork_id>', methods=['POST'])
def save_comment(artwork_id):
    if 'username' not in session:
        return jsonify({'error': '用户未登录'}), 403

    # 从session中获取当前登录的用户信息
    current_user = User.query.filter_by(user_name=session['username']).first()
    if not current_user:
        return jsonify({'error': '用户不存在'}), 404

    content = request.form.get('content')
    if not content:
        return jsonify({'error': '评论内容不得为空'}), 400
    
    else:
        # 创建一个新的评论对象
        new_comment = Comment(
            user_id=current_user.user_id,
            commented_id=artwork_id,
            comment_content=content,
            comment_time=datetime.now(),
        )
        db.session.add(new_comment)
        db.session.commit()  # 保存到数据库

    return jsonify({'success': True, 'message': '评论已保存', 'comment': content})



@app.route('/message/likes_and_collects')
def likes_and_collects():
    # 假设current_user_id是当前登录用户的ID
    current_user = User.query.filter_by(user_name=session['username']).first()
    current_user_id = current_user.user_id

    # 查询当前用户作品相关的点赞记录，并按照like_time逆序排列
    likes = (
        db.session.query(Like, User, Artworks)
        .join(User, User.user_id == Like.user_id)
        .join(Artworks, Artworks.artwork_id == Like.liked_id)
        .filter(Artworks.user_id == current_user_id)
        .order_by(Like.like_time.desc())  # 假设Like模型有一个like_time字段
        .all()
    )
    
    # 查询当前用户作品相关的收藏记录，并按照collect_time逆序排列
    collects = (
        db.session.query(Collect, User, Artworks)
        .join(User, User.user_id == Collect.user_id)
        .join(Artworks, Artworks.artwork_id == Collect.collected_id)
        .filter(Artworks.user_id == current_user_id)
        .order_by(Collect.collect_time.desc())  # 假设Collect模型有一个collect_time字段
        .all()
    )
    
    # 将查询结果传递给前端模板
    return render_template('likes_and_collects.html', 
                           likes=likes, 
                           collects=collects)



@app.route('/message/follows')
def follows():
    # 获取当前登录用户的ID
    current_user = User.query.filter_by(user_name=session['username']).first()
    current_user_id = current_user.user_id

    # 查询当前用户的关注者记录，并按照follow_time逆序排列
    follow_records = (
        db.session.query(Follow, User)
        .join(User, User.user_id == Follow.follower_id)
        .filter(Follow.followed_id == current_user_id)
        .order_by(Follow.follow_time.desc())  # 假设Follow模型有一个follow_time的字段
        .all()
    )
    
    # 将查询结果传递给前端模板
    return render_template('follows.html', follow_records=follow_records)


@app.route('/message/comments')
def comments():
    current_user = User.query.filter_by(user_name=session['username']).first()
    current_user_id = current_user.user_id

    # 构建查询，并按照comment_time逆序排列
    comment_records = db.session.query(Comment, User, Artworks) \
        .join(User, User.user_id == Comment.user_id) \
        .join(Artworks, Artworks.artwork_id == Comment.commented_id) \
        .filter(Artworks.user_id == current_user_id) \
        .order_by(Comment.comment_time.desc()) \
        .all()

    print(comment_records)

    return render_template('comments.html', comment_records=comment_records)


@app.route('/message/notices')
def notices():
    # 获取公告记录并按发布时间逆序排序
    notice_records = Notice.query.order_by(Notice.notice_time.desc()).all()

    # 将查询结果传递给前端模板
    return render_template('notices.html', notice_records=notice_records)


@app.route('/message')
def get_comments():
    user = User.query.filter_by(user_name=session['username']).first()
    page = request.args.get('page', 1, type=int)  # 页码从请求的查询参数中获取
    per_page = 10  # 每页显示数量设为10

    # 进行一个联合查询，同时获取评论和用户信息
    comments = db.session.query(Comment, User).join(User, User.user_id == Comment.user_id)\
        .order_by(Comment.comment_id).paginate(error_out=False,page=page, per_page=per_page)
     
    if comments.items:
        print(comments.items[0])
    else:
        print("没有获取到评论数据")

    return render_template(
        'message.html',
        comments=comments.items, # .items 包含了 Comment 和 User 的联合对象
        current_page=page,
        total_pages=comments.pages,
        username=session['username'],
        photo=user.photo,
        current_user=user
    )


@app.route('/resources')
def resources_page():
    user = User.query.filter_by(user_name=session['username']).first()
    return render_template(
            'resources.html',
            username=session['username'],
            photo = user.photo,
            current_user=user
        )


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        session['username'] = username
        session.permanent = True

        #数据库更新
        #将last_login更新
        user = User.query.filter_by(user_name=username).first()
        if user is None:
            return render_template('login.html', msg_type='error', msg='用户名不存在！')
        elif encrypt_password(password)!=user.password:
            return render_template('login.html', msg_type='error', msg='密码错误！')
        else:
            user.last_login = datetime.now()
            db.session.commit()
        
        if user.power==1 or user.power==2:
            return redirect(url_for('index_page'))
        else:
            return redirect(url_for('admin_index'))
    else:
        print(request.args.get('username'))
        return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        name = request.form.get('name')
        email = request.form.get('email')


        existing_username = User.query.filter_by(user_name=username).all()
        if len(existing_username)>0:
            return render_template('register.html', msg_type='error', msg='用户名已存在')
        if not validate_password(password):
            return render_template('register.html', msg_type='error', msg='密码必须大于8位,且同时包含字母和数字！')
        
        if password != repassword:
            return render_template('register.html', msg_type='error', msg='两次输入密码不一致！')


        new_user = User(
            user_name=username,
            name=name,
            password=encrypt_password(password),  
            birthday=None, 
            gender=None,  
            photo=None, 
            power=1,  
            self_description=None,
            email=email
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return render_template('login.html', msg_type='success', msg='注册成功，请登录!')
    else:
        return render_template('register.html')




@app.route('/personal')
def personal_page():
    if 'username' not in session:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))
    else:
        current_user = User.query.filter_by(user_name=session['username']).first()
        # 查询该用户的作品
        works = Artworks.query.filter_by(user_id=current_user.user_id).all()

        # 查询该用户赞过的作品
        likes = Like.query.filter_by(user_id=current_user.user_id).all()
        liked_ids = [like.liked_id for like in likes]
        like_works = Artworks.query.filter(Artworks.artwork_id.in_(liked_ids)).all()

        # 查询该用户收藏的作品
        collects = Collect.query.filter_by(user_id=current_user.user_id).all()
        collected_ids = [collect.collected_id for collect in collects]
        collect_works = Artworks.query.filter(Artworks.artwork_id.in_(collected_ids)).all()

        # 查询用户粉丝数
        followers_count = Follow.query.filter_by(followed_id=current_user.user_id).count()

        # 查询用户关注数
        follows_count = Follow.query.filter_by(follow_id=current_user.user_id).count()

        # 计算该用户所有作品的总点赞数
        total_likes = db.session.query(func.count(Like.liked_id))\
            .join(Artworks, Artworks.artwork_id == Like.liked_id)\
            .filter(Artworks.user_id == current_user.user_id).scalar()

        # 计算该用户所有作品的总收藏数
        total_collects = db.session.query(func.count(Collect.collected_id))\
            .join(Artworks, Artworks.artwork_id == Collect.collected_id)\
            .filter(Artworks.user_id == current_user.user_id).scalar()


        # 存储点赞数量
        likes_counts = {}
        # 存储点赞状态
        likes_status = {}

        # 对作品获取作者信息
        author_info = {}
        for work in works:
            user = User.query.filter_by(user_id=work.user_id).first()
            if user:
                author_info[work.artwork_id] = {'name': user.name, 'photo': user.photo, 'user_id':user.user_id}
            num_of_likes = Like.query.filter_by(liked_id=work.artwork_id).count()
            likes_counts[work.artwork_id] = num_of_likes

            # 检查当前用户是否点赞过该作品
            is_liked = Like.query.filter_by(user_id=current_user.user_id, liked_id=work.artwork_id).first() is not None
            likes_status[work.artwork_id] = is_liked

        # 在session中存储用户名
        session.permanent = True

        return render_template(
            'personal.html',
            works=works,
            current_user=current_user,
            author_info=author_info,
            likes_status=likes_status,
            likes_counts=likes_counts,
            username=session['username'],
            photo=current_user.photo if hasattr(current_user, 'photo') else None,
            like_works=like_works,
            collect_works=collect_works,
            followers_count=followers_count,
            follows_count=follows_count,
            total_likes_collects=total_likes+total_collects
        )


@app.route('/personal/<int:userid>')
def personal(userid):
    if 'username' not in session:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))
    else:
        current_user = User.query.filter_by(user_name=session['username']).first()
        home_user = User.query.filter_by(user_id = userid).first()
        # 查询该用户的作品
        works = Artworks.query.filter_by(user_id=home_user.user_id).all()

        # 查询该用户赞过的作品
        likes = Like.query.filter_by(user_id=home_user.user_id).all()
        liked_ids = [like.liked_id for like in likes]
        like_works = Artworks.query.filter(Artworks.artwork_id.in_(liked_ids)).all()

        # 查询该用户收藏的作品
        collects = Collect.query.filter_by(user_id=home_user.user_id).all()
        collected_ids = [collect.collected_id for collect in collects]
        collect_works = Artworks.query.filter(Artworks.artwork_id.in_(collected_ids)).all()

        # 查询用户粉丝数
        followers_count = Follow.query.filter_by(followed_id=home_user.user_id).count()

        # 查询用户关注数
        follows_count = Follow.query.filter_by(follow_id=home_user.user_id).count()

         # 计算该用户所有作品的总点赞数
        total_likes = sum([Like.query.filter_by(liked_id=work.artwork_id).count() for work in works])


        # 计算该用户所有作品的总收藏数
        total_collects = sum([Collect.query.filter_by(collected_id=work.artwork_id).count() for work in works])
        
        # 存储点赞数量
        likes_counts = {}
        # 存储点赞状态
        likes_status = {}

        # 对作品获取作者信息
        author_info = {}
        for work in works:
            user = User.query.filter_by(user_id=work.user_id).first()
            if user:
                author_info[work.artwork_id] = {'name': user.name, 'photo': user.photo, 'user_id': user.user_id}
            num_of_likes = Like.query.filter_by(liked_id=work.artwork_id).count()
            likes_counts[work.artwork_id] = num_of_likes

            # 检查当前用户是否点赞过该作品
            is_liked = Like.query.filter_by(user_id=current_user.user_id, liked_id=work.artwork_id).first() is not None
            likes_status[work.artwork_id] = is_liked

        # 在session中存储用户名
        session.permanent = True

        return render_template(
            'personal.html',
            works=works,
            
            home_user=home_user,
            current_user=current_user,
            author_info=author_info,
            likes_status=likes_status,
            likes_counts=likes_counts,
            username=session['username'],
            photo=current_user.photo if hasattr(current_user, 'photo') else None,
            like_works=like_works,
            collect_works=collect_works,
            followers_count=followers_count,
            follows_count=follows_count,
            total_likes_collects=total_likes+total_collects
        )




@app.route('/personal/works')
def personal_works():
    current_user=User.query.filter_by(user_name=session['username']).first()
    # 查询该用户的作品
    works = Artworks.query.filter_by(user_id=current_user.user_id).all()
    # 存储点赞数量
    likes_counts = {}
    # 存储点赞状态
    likes_status = {}

    # 对作品获取作者信息
    author_info = {}
    for work in works:
        user = User.query.filter_by(user_id=work.user_id).first()
        if user:
            author_info[work.artwork_id] = {'name': user.name, 'photo': user.photo}
        num_of_likes = Like.query.filter_by(liked_id=work.artwork_id).count()
        likes_counts[work.artwork_id] = num_of_likes

        # 检查当前用户是否点赞过该作品
        is_liked = Like.query.filter_by(user_id=current_user.user_id, liked_id=work.artwork_id).first() is not None
        likes_status[work.artwork_id] = is_liked

    # 在session中存储用户名
    session.permanent = True
    return render_template(
            'personal_works.html',
            works=works,
            current_user=current_user,
            author_info=author_info,
            likes_status=likes_status,
            likes_counts=likes_counts,
            username=session['username'],
            photo=current_user.photo if hasattr(current_user, 'photo') else None,
        )



@app.route('/personal/likes')
def personal_likes():
    current_user=User.query.filter_by(user_name=session['username']).first()
    #查询该用户点赞记录
    likes = Like.query.filter_by(user_id=current_user.user_id,like_type=1).all()
    #查询点赞
    liked_ids = [like.liked_id for like in likes]
    works = Artworks.query.filter(Artworks.artwork_id.in_(liked_ids)).all()

    # 存储点赞数量
    likes_counts = {}
    # 存储点赞状态
    likes_status = {}

    # 对作品获取作者信息
    author_info = {}
    for work in works:
        user = User.query.filter_by(user_id=work.user_id).first()
        if user:
            author_info[work.artwork_id] = {'name': user.name, 'photo': user.photo}
        num_of_likes = Like.query.filter_by(liked_id=work.artwork_id).count()
        likes_counts[work.artwork_id] = num_of_likes

        # 检查当前用户是否点赞过该作品
        is_liked = Like.query.filter_by(user_id=current_user.user_id, liked_id=work.artwork_id).first() is not None
        likes_status[work.artwork_id] = is_liked

    # 在session中存储用户名
    session.permanent = True


    return render_template(
            'personal_like.html',
            works=works,
            current_user=current_user,
            author_info=author_info,
            likes_status=likes_status,
            likes_counts=likes_counts,
            username=session['username'],
            photo=current_user.photo if hasattr(current_user, 'photo') else None,
        )


@app.route('/personal/collects')
def personal_collects():
    current_user=User.query.filter_by(user_name=session['username']).first()
    # 查询该用户收藏的作品
    collects = Collect.query.filter_by(user_id=current_user.user_id).all()
    collected_ids = [collect.collected_id for collect in collects]
    works = Artworks.query.filter(Artworks.artwork_id.in_(collected_ids)).all()

    # 存储点赞数量
    likes_counts = {}
    # 存储点赞状态
    likes_status = {}

    # 对作品获取作者信息
    author_info = {}
    for work in works:
        user = User.query.filter_by(user_id=work.user_id).first()
        if user:
            author_info[work.artwork_id] = {'name': user.name, 'photo': user.photo}
        num_of_likes = Like.query.filter_by(liked_id=work.artwork_id).count()
        likes_counts[work.artwork_id] = num_of_likes

        # 检查当前用户是否点赞过该作品
        is_liked = Like.query.filter_by(user_id=current_user.user_id, liked_id=work.artwork_id).first() is not None
        likes_status[work.artwork_id] = is_liked

    # 在session中存储用户名
    session.permanent = True


    return render_template(
            'personal_collect.html',
            works=works,
            current_user=current_user,
            author_info=author_info,
            likes_status=likes_status,
            likes_counts=likes_counts,
            username=session['username'],
            photo=current_user.photo if hasattr(current_user, 'photo') else None,
        )




ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#提取关键词的函数
def extract_and_store_keywords(data):
    # 提取关键词和分数
    result = data.get('result', [])
    # 按照分数排序
    sorted_result = sorted(result, key=lambda x: x['score'], reverse=True)
    # 提取前五个关键词
    keywords = [item['keyword'] for item in sorted_result[:5]]
    # 存储在五个独立的变量
    keyword1 = keywords[0] if len(keywords) > 0 else None
    keyword2 = keywords[1] if len(keywords) > 1 else None
    keyword3 = keywords[2] if len(keywords) > 2 else None
    keyword4 = keywords[3] if len(keywords) > 3 else None
    keyword5 = keywords[4] if len(keywords) > 4 else None
    keywords = [keyword1,keyword2,keyword3,keyword5,keyword4]
    return keywords

def process_image(img, process_type):
    BAIDU_ACCESS_TOKEN = '[24.f8570f35810c7f43741c406b1a0bc1f3.2592000.1720297207.282335-79414318]'
    BAIDU_ACCESS_TOKEN = '[24.be41a7bdb0867a9e763c1c04d6e1baf0.2592000.1720308169.282335-79414318]'
    if process_type not in ['colourize', 'selfie_anime']:
        return None

    if process_type == 'colourize':
        request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/colourize"
    elif process_type == 'selfie_anime':
        request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime"

    params = {"image": img}
    request_url = request_url + "?access_token=" + BAIDU_ACCESS_TOKEN
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response and response.status_code == 200:
        response_json = response.json()
        if "image" in response_json:
            return base64.b64decode(response_json["image"])
    return None

@app.route('/process_image', methods=['POST'])
def process_image_route():
    file = request.files.get('file')
    if not file or not file.filename:
        return jsonify({"error": "没有文件上传"}), 400

    filename = secure_filename(file.filename)
    img_data = base64.b64encode(file.read()).decode()

    processed_image = None
    if 'colourize' in request.form:
        processed_image = process_image(img_data, 'colourize')
    elif 'cartoonanime' in request.form:
        processed_image = process_image(img_data, 'selfie_anime')

    if processed_image:
        return jsonify({"image": base64.b64encode(processed_image).decode()})
    else:
        return jsonify({"error": "图片处理失败"}), 500

@app.route('/publish', methods=['POST', 'GET'])
def add_work():
    if 'username' not in session:
        return jsonify({"error": "用户未登录"}), 401

    user = User.query.filter_by(user_name=session['username']).first()
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    if request.method == 'POST':
        artwork_name = request.form.get('title')
        artwork_description = request.form.get('description')
        artwork_type = request.form.get('type')
        user_id = user.user_id

        file = request.files.get('file')
        if not file or not file.filename:
            return jsonify({"error": "没有文件上传"}), 400

        filename = secure_filename(file.filename)
        img_data = base64.b64encode(file.read()).decode()

        token = q.upload_token(BUCKET_NAME, filename)
        ret, info = put_data(token, filename, base64.b64decode(img_data))

        if info.status_code == 200 and 'key' in ret:
            file_url = f"http://sdxa2uyxf.bkt.gdipper.com/{ret['key']}"
        else:
            return jsonify({"error": "文件上传到云存储失败"}), 500

        # 处理打标签API调用
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
        img_data = base64.b64encode(requests.get(file_url).content).decode()
        ACCESS_TOKEN = '[24.5685c95d10965949ad882b5bd97d2c00.2592000.1720285940.282335-77446533]'
        params = {"image": img_data}
        request_url = request_url + "?access_token=" + ACCESS_TOKEN
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)

        if response.status_code == 200:
            tag = response.json()
            keywords = extract_and_store_keywords(tag)
            keyword1, keyword2, keyword3, keyword4, keyword5 = keywords[:5]

            artwork = Artworks(
                artwork_name=artwork_name,
                artwork_description=artwork_description,
                artwork_time=datetime.now(),
                artwork_type=artwork_type,
                user_id=user_id,
                artwork_picture=file_url,
                keyword1=keyword1,
                keyword2=keyword2,
                keyword3=keyword3,
                keyword4=keyword4,
                keyword5=keyword5
            )

            db.session.add(artwork)
            db.session.commit()

            return render_template(
                'publish.html',
                msg_type='success',
                msg='发布成功！',
                username=session['username'],
                photo=user.photo,
                current_user=user
            )
        else:
            return jsonify({"error": "打标签API调用失败"}), 500

    else:
        return render_template(
            'publish.html',
            username=session['username'],
            photo=user.photo,
            current_user=user
        )

#发布公告
@app.route('/publish_notice', methods=['GET', 'POST'])
def publish_notice():
    if 'username' not in session:
        # 用户未登录，可能需要返回错误或重定向
        return jsonify({"error": "用户未登录"}), 401
        
    user = User.query.filter_by(user_name=session['username']).first()
    
    if not user:
        # 用户不存在，可能需要返回错误或重定向
        return jsonify({"error": "用户不存在"}), 404

    if request.method == 'POST':
        # 处理文本字段
        notice_name = request.form.get('title')
        notice_content = request.form.get('content')
        # 从用户对象获取 user_id
        user_id = user.user_id
        print(request.files)
        if 'file' in request.files:
            print('File found:', request.files['file'])
        else:
            print('File not found')

        
        # 处理文件上传
        file = request.files.get('file')
        
        notice_picture = None  # 初始化变量以确保它总是有定义

        if file and file.filename:
            filename = secure_filename(file.filename)
            token = q.upload_token(BUCKET_NAME, filename)
            ret, info = put_data(token, filename, file.read())

            if info.status_code == 200 and 'key' in ret:
                file_url = f"http://sdxa2uyxf.bkt.gdipper.com/{ret['key']}"
                notice_picture = file_url
            else:
                # 出现错误，可以记录日志或者返回更详细的错误信息
                error_message = ret.get('error', '文件上传失败') if ret else '文件上传失败'
                return jsonify({"error": error_message, "info": info}), 500
        else:
            return jsonify({"error": "没有文件上传"}), 400


        # 创建作品实例并保存到数据库
        notice = Notice(
            notice_name = notice_name, 
            notice_content = notice_content,
            notice_time = datetime.now(),
            user_id = user_id, 
            notice_picture = notice_picture
           )
        
        db.session.add(notice)
        db.session.commit()

        return render_template(
            'publish_notice.html', 
            msg_type='success',
            msg='发布成功！',
            username=session['username'],
            photo=user.photo,
            current_user=user
            )

    else:
        return render_template(
            'publish_notice.html',
            username=session['username'],
            photo=user.photo,
            current_user=user
            )
    

@app.route('/delete_work')
def delete_book():
    id = request.args.get('id')
    book = db.session.query(Artworks).filter(Artworks.artwork_id == int(id)).first()
    db.session.delete(book)
    db.session.commit()
    
    return redirect(url_for('list_artworks'))

from flask import Flask, request, jsonify

#生成验证码
def generate_verification_code():
    """Generate a 6-digit numeric verification code."""
    code = ''.join(random.choices(string.digits, k=6))
    return code

#发送验证码
mail = Mail(app)

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

def send_verification_code(email, code):
    msg = Message("Your Verification Code", recipients=[email])
    msg.body = f"Your verification code is {code}. This code will expire in 10 minutes."
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


@app.route('/send_verification_code', methods=['POST'])
def send_verification_code_route():
    email = request.json.get('email')
    if not email:
        return jsonify(message='Email is required'), 400
    code = generate_verification_code()
    send_verification_code(email, code)
    reset_code = PasswordResetCode(user_id=1, old_passwd='', new_passwd='', reset_date=datetime.now())
    db.session.add(reset_code)
    db.session.commit()
    return jsonify(message='验证码已发送，请检查你的邮箱。')


@app.route('/verify_code', methods=['POST'])
def verify_code_route():
    email = request.form.get('email')
    user_code = request.form.get('code')
    reset_code = PasswordResetCode.query.filter_by(email=email).first()
    if reset_code and reset_code.code == user_code and reset_code.expiry > datetime.now():
        return redirect(url_for('reset_password', email=email))
    else:
        return render_template('verify_code.html', error='Invalid or expired verification code.')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_route():
    if request.method == 'POST':
        email = request.args.get('email')
        new_password = request.form.get('password')
        encrypted_password = encrypt_password(new_password, method='sha256')
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = encrypted_password
            db.session.commit()
            # 删除已用的验证码
            PasswordResetCode.query.filter_by(email=email).delete()
            db.session.commit()
            return 'Password updated successfully.'
    return render_template('reset_password.html')



@app.route('/edit_userinfo', methods=['GET', 'POST'])
def edit_userinfo():
    if 'username' in session:

        user = User.query.filter_by(user_name=session['username']).first()
        if not user:
            return jsonify({"error": "用户未找到"}), 404

        if request.method == 'POST':
            username = request.form.get('username')
            # 将性别的字符串值转换为布尔值
            sex = True if request.form.get('sex') == 'True' else False
            birthdate = request.form.get('birthdate')
            name = request.form.get('name')
            email = request.form.get('email')
            self_description = request.form.get('self_description')

            # 更新用户资料
            if username:
                user.user_name = username
            if sex is not None:  # 确保sex不是None
                user.gender = sex
            if birthdate:
                user.birthday = birthdate
            if name:
                user.name = name
            if email and email != user.email:
                user.email = email
            if self_description:
                user.self_description = self_description


            # 处理文件上传
            file = request.files.get('photo')
            if file and file.filename:
                filename = secure_filename(file.filename)
                token = q.upload_token(BUCKET_NAME, filename)
                ret, info = put_data(token, filename, file.read())

                if info.status_code == 200:
                    photo_url = f"http://sdxa2uyxf.bkt.gdipper.com/{ret['key']}"
                    user.photo = photo_url  # 直接更新 user.photo
                else:
                    pass

            # 提交数据库更改
            db.session.commit()

            # 使用Flask的redirect和url_for来重定向用户
            return redirect(url_for('edit_userinfo'))
        else:
            # 对于GET请求，我们不需要特别处理，只需渲染模板
            return render_template('edit_userinfo.html', user=user)
    else:
        redirect(url_for('login'))

# 显示首页的函数，可以显示首页里的信息
@app.route('/admin_index', methods=['GET'])
def admin_index():
    return render_template('admin_index.html')


@app.route('/users', methods=['GET'])
def all_users():
    if 'username' not in session:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))
    else:
        current_user = User.query.filter_by(user_name=session['username']).first()
        users = User.query.all()
        user_counts = len(users)
        return render_template('users.html',
                                users=users,
                                current_user=current_user,
                                user_counts=user_counts,
                                photo=current_user.photo if hasattr(current_user, 'photo') else None,
                                )


@app.route('/delete_user/<int:user_id>', methods=['POST'])  
def delete_user(user_id):  
    data = User.query.get(user_id)  
    if data:  
        db.session.delete(data)  
        db.session.commit()  
        return jsonify({'status': 'success', 'message': '用户已删除'})
    return jsonify({'status': 'error', 'message': '用户删除失败'}), 404

#编辑用户 
@app.route('/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 404

    try:
        # 从request.json中获取数据，如果request.json为None则使用默认值
        user.user_name = request.json.get('user_name', user.user_name)
        user.name = request.json.get('name', user.name)
        user.power = request.json.get('power', user.power)
        user.email = request.json.get('email', user.email)
        user.self_description = request.json.get('self_description', user.self_description)

        db.session.commit()
        return jsonify({'status': 'success', 'message': '用户信息已更新'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': '更新失败', 'error': str(e)})
#作品管理页
@app.route('/works', methods=['GET'])
def works():
    if 'username' not in session:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))
    else:
        current_user = User.query.filter_by(user_name=session['username']).first()
        works_with_users = []   
        works = Artworks.query.all()
        work_counts = len(works)
        for work in works:
            user = User.query.filter_by(user_id=work.user_id).first()  # 获取每个作品的作者信息
            if user:
                work_data = {
                'work': work,
                'user': user
            }
                works_with_users.append(work_data)  # 将作品信息和作者信息添加到列表中
    
        return render_template('works.html',
                            works_with_users=works_with_users,
                            current_user=current_user,
                            work_counts = work_counts,
                            photo=current_user.photo if hasattr(current_user, 'photo') else None,
                            )



#作品的删除
@app.route('/works/<int:artwork_id>/delete', methods=['POST'])
def delete_work(artwork_id):
    try:
        # 首先删除所有依赖于该艺术品的'likes'记录
        likes = Like.query.filter_by(liked_id=artwork_id).all()
        for like in likes:
            db.session.delete(like)
        
        # 然后删除艺术品本身
        artwork = Artworks.query.get(artwork_id)
        if artwork:
            db.session.delete(artwork)
            db.session.commit()
        return redirect(url_for('works'))
    except Exception as e:
        db.session.rollback()
        # 这里可以添加一些错误处理的逻辑
        return str(e), 500


#作品的编辑
@app.route('/works/<int:artwork_id>/edit', methods=['GET', 'POST'])
def edit_work(artwork_id):
    artwork = Artworks.query.get(artwork_id)
    if not artwork:
        # 如果没有找到艺术品，可能需要处理错误
        pass
    
    if request.method == 'POST':
        # 更新作品信息
        artwork.uniprice = request.form['uniprice']
        artwork.discount = request.form['discount']

        db.session.commit()
        return redirect(url_for('works'))
    
    return render_template('edit_work.html', artwork=artwork)


#评论管理页
@app.route('/admin_comments', methods=['GET'])
def admin_comments():
    if 'username' not in session:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))
    else:
        current_user = User.query.filter_by(user_name=session['username']).first()
        comments_with_users = []   
        comments = Comment.query.all()
        comment_counts = len(comments)
        for comment in comments:
            user = User.query.filter_by(user_id=comment.user_id).first()  # 获取每个评论的用户信息
            if user:
                comment_data = {
                'comment': comment,
                'user': user
            }
                comments_with_users.append(comment_data)  # 将评论信息和用户信息添加到列表中
    
        return render_template('admin_comments.html',
                            comments_with_users = comments_with_users,
                            current_user = current_user,
                            comment_counts = comment_counts,
                            photo=current_user.photo if hasattr(current_user, 'photo') else None,
                            )

#评论的删除
@app.route('/admin_comments/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    try:
        # 首先删除所有依赖于该评论的'likes'记录
        likes = Like.query.filter_by(liked_id=comment_id).all()
        for like in likes:
            db.session.delete(like)
        
        # 然后删除评论本身
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
        return redirect(url_for('admin_comments'))
    except Exception as e:
        db.session.rollback()
        # 这里可以添加一些错误处理的逻辑
        return str(e), 500


#公告管理页
@app.route('/admin_notice', methods=['GET'])
def admin_notice():
    if 'username' not in session:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))
    else:
        current_user = User.query.filter_by(user_name=session['username']).first()
        notices_with_users = []   
        notices = Notice.query.all()
        notice_counts = len(notices)
        for notice in notices:
            user = User.query.filter_by(user_id=notice.user_id).first()  # 获取每个公告的管理员信息
            if user:
                notice_data = {
                'notice': notice,
                'user': user
            }
                notices_with_users.append(notice_data)  # 将公告信息和发布者信息添加到列表中
    
        return render_template('admin_notice.html',
                            notices_with_users = notices_with_users,
                            current_user = current_user,
                            notice_counts = notice_counts,
                            photo=current_user.photo if hasattr(current_user, 'photo') else None,
                            )
    
#公告的删除
@app.route('/admin_notice/<int:notice_id>/delete', methods=['POST'])
def delete_notice(notice_id):

        notice = Notice.query.get(notice_id)
        if notice:
            db.session.delete(notice)
            db.session.commit()
        return redirect(url_for('admin_notice'))

#公告的编辑
@app.route('/admin_notice/<int:notice_id>/edit', methods=['GET', 'POST'])
def edit_notice(notice_id):
    notice = Notice.query.get(notice_id)
    if not notice:
        pass
    
    if request.method == 'POST':
        # 更新作品信息
        notice.uniprice = request.form['']
        notice.discount = request.form['']

        db.session.commit()
        return redirect(url_for('notice'))
    
    return render_template('admin_notice.html', notice=notice)
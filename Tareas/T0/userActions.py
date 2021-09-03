from datetime import datetime

import parametros as p
import csvUtils as csv

def register_user(user, users):
    is_valid = False
    if user not in users and "," not in user:
        is_valid = len(user) <= p.MAX_CARACTERES and len(user) >= p.MIN_CARACTERES
    
    if is_valid:
        users.add(user)
        csv.write_csv("usuarios.csv", users)

    return is_valid

def publish_comment(text, user, post, comments):
    post += 1
    comment = [str(post), user, datetime.now().strftime("%Y/%m/%d %H:%M:%S"), text]
    if str(post) in comments:
        comments[str(post)].append(comment)
    else:
        comments[str(post)] = [comment]
    csv.write_csv("comentarios.csv", comments)

def find_self_posts(user, posts):
    result = []
    for post in posts:
        if post[2] == user:
            result.append(post)

    return result

def publish_post(title, price, desc, user, posts):
    current_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    posts.append([str(len(posts) + 1), title, user, current_date, price, desc])
    csv.write_csv("publicaciones.csv", posts)
    return len(posts) - 1


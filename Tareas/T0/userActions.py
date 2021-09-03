import parametros
import csvUtils as csv
from datetime import datetime

def register_user(user, users):
    pass

def publish_comment(text, user, post, comments):
    post += 1
    comment = [str(post), user, datetime.now().strftime("%Y/%m/%d %H:%M:%S"), text]
    comments[str(post)].append(comment)
    csv.write_csv("comentarios.csv", comments)

def publish_post():
    pass

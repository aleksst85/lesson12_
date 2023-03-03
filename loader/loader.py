from flask import Blueprint, render_template, request
from functions import load_post, uploads_posts
import logging
logging.basicConfig(encoding='utf-8', level=logging.INFO)

loader_blueprint = Blueprint('loader_blueprint', __name__, url_prefix='/post', static_folder='static', template_folder="templates") 


@loader_blueprint.route('/form/')
def form():
    return render_template('post_form.html')


@loader_blueprint.route('/upload/', methods = ['POST'])
def upload():
    try:
        file = request.files['picture']
        filename = file.filename
        content= request.values['content']
        posts = load_post()
        posts.append({
            'pic':f'/uploads/images/{filename}',
            'content': content
        })
        uploads_posts(posts)
        file.save(f"uploads/images/{filename}")
        if filename.split('.')[-1] not in ['png', 'jpg']:
            logging.info("Файл не изображение")
    except FileNotFoundError:
        logging.error('Ошибка при загрузке файла')
        return '<h1>Файл не найден<br>'
    else:
        return render_template('post_uploaded.html', pic = f'/uploads/images/{filename}', content = content)


    return render_template('post_form.html')
from models import Document, db

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_to_db(filename, filepath):
    # Cria um novo documento
    document = Document(filename=filename, filepath=filepath)

    # Adiciona e commita o documento ao banco de dados
    db.session.add(document)
    db.session.commit()

    # Retorna o ID e o caminho do documento
    return str(document.id), document.filepath

from flask import redirect

from config import connexion_app

connexion_app.add_api('swagger.yml')


@connexion_app.route('/')
def index():
    return redirect('/api/v1/ui')


if __name__ == '__main__':
    connexion_app.run(host='127.0.0.1', port=8080, debug=True)

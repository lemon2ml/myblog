from fabric.api import run, env, local
from fabric.operations import sudo

git_repo = 'https://github.com/lemon2ml/myblog.git'

env.user = 'www'
env.password = '111111'
env.hosts = ['127.0.0.1']
env.port = '22'

def deploy():
	source_folder = '/home/www/sites/demo.leimeilian.com/myblog'

	# run('cd %s && git pull' % source_folder)

	run("""
		cd {} && 
		../env/bin/pip install -r requirements.txt &&
		../env/bin/python manage.py collectstatic --noinput &&
		../env/bin/python manage.py makemigrations
		../env/bin/python manage.py migrate
		""".format(source_folder))

	local('gunicorn --bind 127.0.0.1:8000 myblog.wsgi:application &')
	local('sudo nginx -s reload')

	
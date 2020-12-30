# django-file-upload-download
Demo code examples for uploading and downloading files using Django, including setting storage directory, file renaming, Ajax upload and streaming of large files.
Type 'manage.py help <subcommand>' for help on a specific subcommand.

Available subcommands:

[auth]
    changepassword
    createsuperuser

[contenttypes]
    remove_stale_contenttypes

[django]
    check
    compilemessages
    createcachetable
    dbshell
    diffsettings
    dumpdata
    flush
    inspectdb
    loaddata
    makemessages
    makemigrations
    migrate
    sendtestemail
    shell
    showmigrations
    sqlflush
    sqlmigrate
    sqlsequencereset
    squashmigrations
    startapp
    startproject
    test
    testserver

[sessions]
    clearsessions

[staticfiles]
    collectstatic
    findstatic
    runserver
python manage.py createsuperuser         # 创建超级管理员
python manage.py migrate                 # 合并数据库设定
python manage.py runserver 0.0.0.0:80    # 启动服务
python manage.py collectstatic           # 收集静态文件导入路径
python manage.py makemigrations          # 依据models生成数据库合并前文件
python manage.py startapp                # 创建一个APP

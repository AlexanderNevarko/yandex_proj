================================================
# Проект для прохождения вступительного 
# испытания в школу бэкенд-разработки от Яндекса
================================================

------------------------------------------------
 Разворачивание на сервере
------------------------------------------------

Для разворачивания на сервере с адресом 84.201.140.250
необходимо установить гит и иметь python3

Далее нужно склонировать репозиторий:

	$ git clone https://github.com/AlexanderNevarko/yandex_proj.git

Логин и пароль, к сожалению, выложить не могу :)

Далее необходимо перейти в директорию проекта,
удалить файлы с миграциями БД и создать вирутальное окружение,
и перейти в него:

    $ cd yandex_proj
    $ rm -rf migrations
    $ python3 -m venv venv
    $ source venv/bin/activate

После этого необходимо установить pip, а затем и все необходимы пакеты
(необходимы права администратора или знание пароля):

    $ sudo apt install python3-pip
    $ pip install --upgrade pip
    $ pip install -r requirements.txt

После успешного выполнения этих команд, инициализируем базу данных:
    
    $ flask db init
    $ flask db migrate -m "init"
    $ flask db upgrade

До запуска сервера осталась одна команда!

    $ flask run --host=0.0.0.0 --port=8080

Если вы хотите запустить сервер в фоне, чтобы после 
разлогинивания он продолжил работать, нужно выполнить другую команду:

    $ flask run --host=0.0.0.0 --port=8080 &> /dev/null &

Спасибо за внимание!
При возникновении вопросов, со мной можно связаться в телеграм: @alex_nevarko

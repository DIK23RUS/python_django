# Первым делом устанавливаем Питон нужной версии
FROM python:3.11

# Указываем название рабочей "папки/директории", нужно указывать название так, чтобы его уже не существовало на диске
WORKDIR /django-dik23rus-site

# Копируем файл с зависимостями в рабочую директорию
COPY requirements.txt requirements.txt

# Запускаем обновленние pip
RUN pip install --upgrade pip
# Запускаем установку зависимостей из ранее скопированного файла
RUN pip install -r requirements.txt

# Копируем содержимое папки нашего проекта в WORKDIR
COPY site_dik23rus .

# Теперь можно собирать Docker контейнер.
# В терминале, переходим в директорию где лежит файл Dockerfile.
# И пишем команду в одну строку, ниже пояснение - "docker build . -t django-dik23rus-site"
# docker - это обращение к самому Docker
# build - это команда для создания контейнера, которую должен выполнить Docker
# . - это где собирать контейнер, "точка" значит, что собираем в текущей директории
# -t - это флаг означает "тэг", который мы будем присваивать контейнеру
# django-dik23rus-site - это название "тэга"
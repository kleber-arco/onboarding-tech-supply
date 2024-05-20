# Usar uma imagem base do Python
FROM python:3.9

# Configurar a variável de ambiente
ENV PYTHONUNBUFFERED 1

# Definir o diretório de trabalho no contêiner
WORKDIR /code

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt /code/

# Instalar as dependências do projeto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar o restante do código do projeto para o diretório de trabalho
COPY . /code/

# Executar as migrações e iniciar o servidor Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]

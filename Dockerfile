# Use a imagem oficial do Python
FROM python:3.9

# Configurar variáveis de ambiente
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Criar e definir o diretório de trabalho
WORKDIR /app

# Copiar os requisitos do projeto para o contêiner
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código-fonte para o contêiner
COPY . /app/

# Adicionar o alembic.ini à imagem
COPY alembic.ini /app/alembic.ini

# Instalar o Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

# Expor a porta que a aplicação FastAPI estará escutando
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["sh", "-c", "/usr/local/bin/alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

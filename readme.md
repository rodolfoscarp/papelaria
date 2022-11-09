# Sistema de Papelaria (BackEnd)

## Como Executar

### Pré Requisitos

- Python 3.8 ou superior
- Banco de dados PostsgreSQL

### Executando

- Clonar este diretorio

  `git clone git@github.com:rodolfoscarp/papelaria.git`

- Criei um ambiente virtual e ative:

  `python -m venv venv`

  - Windows:

    `venv\Scripts\activate`

  - Linux e Mac

    `source venv/bin/activate`

- Instale as dependecias:

  `pip install -r requirements.txt`

- Configure as variaveis de ambiente:

  - Dentro do diretorio existe um arquivo `.env.example`
  - Preencha as variaveis de ambiente e renomeie para `.env`
  - Se não tem uma chave se segurança pode utilizar o comando abaixo dentro do shell do python.

    ```python
    from django.core.management.utils import get_random_secret_key
    get_random_secret_key()
    ```

- Execute as Migration do Models Django.

  `python manage.py migrate`

- Crie um Usuario Administrador:

  `python manage.py createsuperuser`

- Executando o projeto:

  `python manage.py runserver`

### Testando

- Para executar os testes utilize o comando pytest

`pytest -s`

### Documentação da API

- Para vizualizar a documentação da API com o servidor rodando acesse o endereço:

  [http://127.0.0.1:8000/doc/](http://127.0.0.1:8000/doc/)

[]()

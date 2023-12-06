# Sistema_Rega_Flask
Sistema de rega escrita em python com uma dashboard web usando frameworks como flask, socket-io e até scikit!

Este documento servirá como introdução e orientação para executar e testar o projeto por conta própria.

Neste readme o seguinte será explicado sobre o projeto:
- [Instalação](#Instalação)
- [Aplicação AccuWeather](#AplicaçãoAccuWeather)
- [Execução do código](#execucao)
- [Atenções](#avisos)


![imagem](https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/67eaa2f6-7ec6-43e2-aa8d-9ea692b59515)


## Instalação <a name="Instalação"></a>

Para o sistema funcionar *Corretamente* será necessário
* Um sistema base de dados postgresql
* Uma aplicação AccuWeather

## Instalação de um sistema PostGreSQL
Uma base de dados PostGresql será necessária para o correto funcionamento deste trabalho, embora o mesmo não seja obrigatório este será necessário para a gestão do histórico de valores do sistema.

### Sistema postgresql
Neste projeto a conexão com a base de dados é feita com a seguinte função em "Main\pred_test.py":
```
[...]
def db_connection():
    try:
        db = psycopg2.connect(host="yipiee.sytes.net" , dbname="LP_DB" ,user="postgres" ,password='EpicPassword123')
        return db
    except Exception as e:
        print("Cant connect to postgres server... not saving ")
        print(e)
[...]
```
Será necessário trocar as definições nesta conexão para refletir a base de dados que vai ser usada.

Será demonstrada uma recomendação de como a instalação desta base de dados deve ser feita:
### Docker
Docker é uma ferramenta popular de criação de containers para separar as dependencias de uma aplicação com todas as outras facilitando a manutenção e partilha das várias aplicações no mesmo sistema.
A instalação do mesmo começa no [website official do docker](https://www.docker.com/products/docker-desktop/)
<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/354e0648-9698-47be-981c-91df78fbfc8c" width="400" height="200">
</p>

Após concluir a sua instalação e configuração no sistema:
<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/f26fbab1-29c1-4a83-bea5-b8c2cb1893be" width="350" height="310">
</p>

Uma imagem postgres será necessária para executar um container, existem vários tipos destas imagens, mas é recomendada instalar a imagem official distribuida pelo docker:
<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/2772762f-9d62-4531-86c1-ef604f7db3c7" width="350" height="200">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/f397eedf-cacd-4a6e-bf72-2d545e509b53" width="350" height="200">
</p>
Após a sua instalação podemos começar um novo container ao fazer "run" desta imagem em "Images", com atenção aos parametros necessários para a sua inicialização como mostrado no exemplo abaixo:

Este parametro será usado como uma password para o "superuser" com o nome de utilizador "postgres" por isso é recomendado meter uma password forte nesta configuração. 
<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/535b2c89-af1d-4c6d-ba2e-db69020fae89" width="700" height="400">
</p>



Embora não seja necessário é recomendado tambem a instalação do pgAdmin para a administração desta base de dados postgres:
<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/24070063-6399-4640-8e9d-ad9910120863" width="450" height="200">
</p>
Ao proceder com a implementação do mesmo é favor ter atenção ás variáveis necessárias para a sua inicialização:

É necessário definir um email e password por defeito para fazer login nesta página de gestão como mostrado no exemplo abaixo.

<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/6090af8f-d831-4492-acd5-632d9984d774" width="500" height="400">
</p>

Se a configuração estiver feita de forma correta e com o porto 80, será possivel aceder ao PgAdmin a partir [deste Link](http://localhost:80)

A página terá um aspeto semalhante ao abaixo, para entrar na dashboard é preciso usar o email e password definidos no container do pgAdmin:
<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/087a6795-9cde-42cf-a989-0bc2ac9cb838" width="700" height="400">
</p>



## Carregar Base de Dados

Para adicionar uma conexão á base de dados é feita com o seguinte (A partir do pgAdmin):
<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/dddc219a-6a41-4b7a-87dc-87670903f80a" width="350" height="160">
</p>

Aqui será especificado os parametros de conexão configurados na base de dados postgres:
<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/78350f45-c554-49b1-b6bb-c0196cb1ff06" width="350" height="200">
</p>

Para criar uma base de dados nova neste servidor é feito o seguinte:
<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/82dc1339-7a26-473c-bc50-ba711e371d2e" width="500" height="100">
</p>
<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/b1891c2c-c45c-4cb4-8b53-2d7d676ee201" width="500" height="400">
</p>


Após esta ser criada podemos importar a estrutura de base de dados para a mesma.
A estrutura da base de dados desenhada para este projeto estará disponivel no ficheiro "Main/BackUp/code.sql"

Para executar este ficheiro é preciso abrir um script para a sua query:
<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/5fd3edd5-4c10-4b62-93c2-bbf192616c0a" width="420" height="450">
</p>

E carregar esse script nesta query, depois executando este script, clicando no butao "play" ou clicando F5:

<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/4d2a7d3b-80e7-414d-8771-d36f0b55724f" width="500" height="400">
</p>


Para confirmar que a importação foi feita com sucesso é necessário verificar se a tabela e as funções estão presentes no schema public, a sua estrutura deverá ser semalhante a esta:

<p align="center">
<img src="https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/94453623-8c59-46bf-b80d-3b4b1579dd34" width="300" height="360">
</p>


Por fim tenha atenção aos endereços, nomes e contas configuradas para concluir a sua implementação neste projeto, relembrando que a sua configuração está localizada em "Main\pred_test.py"

```
[...]
def db_connection():
    try:
        db = psycopg2.connect(host="yipiee.sytes.net" , dbname="LP_DB" ,user="postgres" ,password='EpicPassword123')
        return db
    except Exception as e:
        print("Cant connect to postgres server... not saving ")
        print(e)
[...]
```
* host -> IP do servidor postgresql
* dbname -> Nome da base de dados criada
* user -> nome do utilizador com acesso a esta base de dados
* password -> password definida para o utilizador

O sistema pode funcionar sem uma conexão com a base de dados, mas não é recomendável

### Aplicação AccuWeather <a name="AplicaçãoAccuWeather"></a>
Uma conta AccuWeather dev é necessária para criar uma [Aplicação AccuWeather](https://developer.accuweather.com/user/me/apps)

Esta aplicação deverá ter um produto CoreWeather

![imagem](https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/2aa6e0ba-5787-45c7-a6df-3371e937dd44)

O limited trial funciona perfeitamente.
Atenção com o **limite de pedidos diários** pois ao exceder o limite o sistema pode parar de funcionar

Ao criar uma aplicação com sucesso poderás ter acesso a uma chave API, que é necessária para o sistema.
![imagem](https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/1fb979dd-ccf8-4f9d-a1ab-667e5f05edce)


## Execução do código <a name="execucao"></a>
Para o correto funcionamento do código foi criada um ambiente virtual python com todas as bibliotecas e a versão python usada para o desenvolvimento da mesma.

Será necessário carregar este ambiente para garantir que nenhum problema fora do ordinário aconteça.
O seguinte ficheiro é para ser executado numa terminal, basta inserir o seguinte:
```
Main\LPVirtualEnv\Scripts\activate
```
Onde a seguir com o mesmo será executado o código.
Para executar o código é recomendado estar localizado no diretório "Main" (Os ficheiros do sistema ficarão guardados no diretório de onde carregar o script)
```
cd Main
```

E para o executar:
```
python main.py
```

Ao ser executado irá pedir o seguinte:
```
Insert your API key:
```
Aqui é onde precisará daquela chave API de uma aplicação AccuWeather:

![imagem](https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/1fb979dd-ccf8-4f9d-a1ab-667e5f05edce)


## Atenções <a name="avisos"></a>
* O sistema pode funcionar sem uma conexão á base de dados
* A configuração de IP e portos está localizado no "Main\main.py"
* Uma chave API de uma aplicação AccuWeather é ***obrigatória***

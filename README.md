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
Será necessário trocar estas definições para refletir a base de dados que vai ser usada.

A estrutura da base de dados desenhada para este projeto estará disponivel em "Main/BackUp/code.sql"


### Aplicação AccuWeather <a name="AplicaçãoAccuWeather"></a>
Uma conta AccuWeather dev é necessária para criar uma [Aplicação AccuWeather](https://developer.accuweather.com/user/me/apps)

Esta aplicação deverá ter um produto CoreWeather

![imagem](https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/2aa6e0ba-5787-45c7-a6df-3371e937dd44)

O limited trial funciona perfeitamente.
Atenção com o **limite de pedidos diários** pois ao exceder o limite o sistema pode parar de funcionar

Ao criar uma aplicação com sucesso poderás ter acesso a uma chave API, que é necessária para o sistema.
![imagem](https://github.com/Besteres/Sistema_Rega_Flask/assets/76634807/1fb979dd-ccf8-4f9d-a1ab-667e5f05edce)


## Execução do código <a name="execucao"></a>
Para o correto funcionamento do código foi criada um ambiente virtual python com todas as bibliotecas e a versão python usada para o desenvolvimento desta.

Será necessário carregar este ambiente para garantir nenhum problema fora do ordinário.
O seguinte comando é para ser executado numa terminal:
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

# CLoud test task

There is a test task for Selectel Cloud team

API создано, чтобы создавать в openstack виртуальные машины двух типов:
*  Standart (стандартные)
*  Preemptible (вытесняемые)

Суть вытесянемых в том, что они могут уничтожаться, если необходимо создать стандартную виртуальную машину.


## Make команды:
* Запустить докер контейнеры приложения и БД PostgreSQL
```shell script
make build
```

* Запуск тестов
```shell script
make run_test
```

* Запустить линтер
```shell script
make lint
```

## Описание url:
* /api/v1/ - стартовая страница с списком API endpoints ( swager)
* POST /api/v1/vm - api endpint для создания виртуальных машин в облаке devstack
* GET /api/v1/vm - api endpint для запроса существующих в облаке виртуальных машин
* DELETE /api/v1/vm/{cloud_id} - api endpint для удаления виртуальной машины

## DEVSTACK:
* http://89.248.207.43/dashboard/ - доступ к horizon развернутого devstack


## Работа с API:
### API endpoint: /api/v1/vm
* метод: POST
* Decription: Ендпоинт нужен, чтобы создавать вм в развернутом openstack.
В качестве параметра запроса выступает флаг is_preemptible,
который говорит, какую вм создавать:
** стандартную: is_preemptible=false
** вытесняемую: is_preemptible=true

* JSON request:
```shell script
{
    "is_preemptible": true or false - флаг, для создания стандратных или вытесняемых вм
}
``` 
* JSON response:
```shell script
{
  "code": "201",
  "message:": "Standart vm 03f0f27e-f325-4c3e-a70d-d64b65ce181c was created succesfully"
}
``` 
### API endpoint: /api/v1/vm
* метод: GET
* Decription: Ендпоинт нужен, запросить информацию о существующших вм в развернутом openstack.
* JSON request:
```shell script
{}
``` 
* JSON response:
```shell script
{
  "servers": [
    {
      "id": "03f0f27e-f325-4c3e-a70d-d64b65ce181c",
      "name": "standart",
      "links": [
        {
          "rel": "self",
          "href": "http://89.248.207.43/compute/v2.1/servers/03f0f27e-f325-4c3e-a70d-d64b65ce181c"
        },
        {
          "rel": "bookmark",
          "href": "http://89.248.207.43/compute/servers/03f0f27e-f325-4c3e-a70d-d64b65ce181c"
        }
      ]
    }
  ]
}
``` 
### API endpoint: /api/v1/vm/{cloud_vm_id}
* метод: GET
* Decription: Ендпоинт нужен, чтобы удобно удалять вм в облаке и локальной базе.
В качестве параметра url выступает cloud_vm_id, которое соотвуствует id вм из openstack.
* JSON request:
```shell script
{
    "cloud_vm_id": "03f0f27e-f325-4c3e-a70d-d64b65ce181c"
}
``` 
* JSON response:
```shell script
{
  "code": "204",
  "message:": "vm 03f0f27e-f325-4c3e-a70d-d64b65ce181c was deleted succesfully"
}
``` 


## Authors and acknowledgment
Victor Pyatakov

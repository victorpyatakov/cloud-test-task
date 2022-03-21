# CLoud test task

There is a test task for Selectel Cloud team

API создано, чтобы создавать в openstack виртуальные машины двух типов:
*  Standart (стандартные)
*  Preemptible (вытесняемые)

Суть вытесянемых в том, что они могут уничтожаться, если необходимо создать стандартную виртуальную машину.


## Запуск:
* Запуск докер контейнеров приложения и БД PostgreSQL
```shell script
make build
```

* Запуск тестов
```shell script
make run_test
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
* JSON request:
```shell script
{
    "is_preemptible": true or false - флаг, для создания стандратных или вытесняемых вм
}
``` 
* JSON response:
```shell script
{
    сообщение об созданной вм или о неудаче
}
``` 

## Authors and acknowledgment
Victor Pyatakov

# Busov
## Задание 2.3.2 (2 балла)
### Тестирование
![image](https://user-images.githubusercontent.com/88937120/205491804-43a447ad-a3a0-47ac-9168-35be2feb8bce.png)

____

## Задание 2.3.3 (2 балла)
### Профилирование
- Вариант с datetime.strptime...
```python
year = int(datetime.datetime.strptime(vac.published_at, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y"))
```
...составил 52.444 секунды
![datetime.strptime](https://user-images.githubusercontent.com/88937120/205498198-1375c568-2a4e-4359-8624-c7935f5820ca.png)
- Вариант с regexp...
```python
year = int(re.findall(r'20[0-9][0-9]',vac.published_at)[0])
```
... составил 4.099 секунды
![regexp](https://user-images.githubusercontent.com/88937120/205498337-52bcfa54-dbd0-4942-907e-db4fd3faf1da.png)
- Вариант с обрезкой строки...
```python
year = int(vac.published_at[:4])
```
... составил 0.675 секунды
![pycharm64_2RKlv8QNGH](https://user-images.githubusercontent.com/88937120/205498421-eb15aed9-87c0-4a4f-9c2a-61b6d27f0c28.png)

____

## Задание 3.2.1 (1 балл)
### Разделить данные
![opera_IwjpdY2zL9](https://user-images.githubusercontent.com/88937120/206467657-ef755690-780e-46e6-a5dc-a73305038f72.png)

____

## Задание 3.2.2 (2 балла)
### Многопроцессорная обработка
До использование многопроцессорности - 1 вызов занимал 2.209 секунды
![pycharm64_kFCrDAIVoA](https://user-images.githubusercontent.com/88937120/206787254-10dcda41-788d-4513-ad6c-d7152b96a312.png)
После использования многопроцессорности - 1 вызов занимал 0.685 секунды
![pycharm64_8u9qVchfUe](https://user-images.githubusercontent.com/88937120/206787858-91ad672e-1345-4e84-8c48-9da1493467e6.png)

____

## Задание 3.2.3 (3 балла)
### Concurrent futures
При использовании Concurrent futures - 1 вызов занимал 0.671 секунды
![pycharm64_qnB1H4hdjH](https://user-images.githubusercontent.com/88937120/206793796-7baa26d2-af8c-46b3-af23-e4170ba61851.png)

____

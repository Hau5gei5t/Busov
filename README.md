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

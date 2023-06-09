# Тестовое задание

### Дано:
- Имеется сервис дислокации вагонов, который возвращает список вагонов, их дату прибытия на станцию, а такж привязанную накладную. Вызов сервиса эмулируется функцией get_current_dislocation()
- Имеется сервис, который предсказывает дату прибытия по накладной. На вход передается список из уникальных накладных.
Вызов сервиса эмулируется функцией get_predicted_date_by_invoices()


### Необходимо сформировать сервис (функцию api_call), которая бы:
1. Получал бы список вагонов из сервиса дислокации.
2. Формировал список накладных тех вагонов, у котороых отсутствует дата прибытия.
3. Отправлял этот список в сервис предсказания даты прибытия.
4. У всех вагонов без даты прибытия выставлял предсказанную дату прибытия.
5. Возвращал список с обновленными данными. 


# Решение

Формирование списка уникальных накладных для вагонов без указанной даты прибытия:
```python
@timing
def get_invoices_without_arrival_date(locations: List) -> (List, List):
    """
    Формирование списка уникальных накладных для вагонов без указанной даты прибытия.
    """
    invoices = []
    indices = []
    for i, loc in enumerate(locations):
        if loc["arrivale_date"] is None:
            invoices.append(loc["arrivale_date"])
            indices.append(i)
    return invoices, indices
```

Выставление предсказанной даты прибытия:
```python
@timing
def refresh_locations(locations: List, indices: List, predicted_data: List) -> List:
    """
    Обновление даты прибытия вагонов в соответствии с сервисом 'get_predicted_date_by_invoices'.
    """
    for i, item in enumerate(indices):
        if locations[item]["arrivale_date"] == predicted_data[i]["invoice"]:
            locations[item]["arrivale_date"] = predicted_data[i]["predicted_date"]
    return locations
```

Сервис `api_call`:
```python
@timing
def api_call():
    """
    В качестве ответа должен выдаваться повагонный список из сервиса get_current_dislocation 
    с обновленной датой прибытия вагона из сервиса get_predicted_dates
    только по вагоном, у которых она отсутствует
    """
    locations = get_current_dislocation()
    invoices, indices = get_invoices_without_arrival_date(locations)
    predicted_data = get_predicted_date_by_invoices(invoices)
    locations = refresh_locations(locations, indices, predicted_data)
    return locations

```

### Важное замечание

Стоит отметить, что в изначальной задаче __у одной и той же накладной могло быть 3 разных времени прибытия!__ 

Это, по идее, может противоречить природе реальной задачи, где к одной накладной могут быть привязаны разные вагоны, но
у накладной должно быть одно время прибытия. 

При решении задачи было данное противоречие было опущено, так как:
- Не было указаний по выбору даты прибытия для таких накладных.
- Предполагается, что в реальной задаче данное противоречие невозможно или обрабатывается другим сервисом/сервисами.
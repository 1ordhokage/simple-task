import time
import random
from datetime import datetime, timedelta
from typing import List
from benchmark import timing


@timing
def get_current_dislocation() -> List:
    """
    Формирование текущей дислокации вагонов. 
    Получаем список вагонов и их дату прибытия.
    Каждый вагон может быть привязан к одной и той же накладной!
    Для того, чтобы получить предсказанную дату прибытия, необходимо вызывать сервис 'get_predicted_dates'
    """
    locations = []
    arrivale_dates = [None, None, None, datetime.now() - timedelta(days=3), datetime.now()]
    time.sleep(2)

    for i in range(0, 20000):
        arrivale_date = random.choice(arrivale_dates)
        location = {
            "wagon": random.randint(10000, 90000),
            "invoice": f"{random.randint(1, 30000)}__HASH__",
            "arrivale_date": arrivale_date.strftime("%d.%m.%Y") if arrivale_date else None,            
        }
        locations.append(location)    
    return locations


@timing
def get_predicted_date_by_invoices(invoices: List) -> List:
    """
    На вход необходимо передать список из уникальных накладных. 
    По каждой накладной будет сформировано время прибытия
    """
    time.sleep(1)
    predicted_results = []
    for invoice in invoices:        
        predicted_date = datetime.now() + timedelta(days=random.randint(1, 5))
        data = {
            "invoice": invoice,
            "predicted_date": predicted_date.strftime("%d.%m.%Y")
        }
        predicted_results.append(data)
    
    return predicted_results


def get_invoices_without_arrival_date(locations: List) -> List:
    """
    Формирование списка уникальных накладных для вагонов без указанной даты прибытия.
    """
    return list(
        set(
            item["invoice"] for item in filter(
                lambda x: x["arrivale_date"] is None,
                locations
            )
        )
    )


@timing
def refresh_locations(locations: List, predicted_data: List) -> List:
    """
    Обновление даты прибытия вагонов в соответствии с сервисом 'get_predicted_date_by_invoices'.
    """
    for loc in locations:
        if loc["arrivale_date"]:
            continue
        for data in predicted_data:
            if loc["invoice"] == data["invoice"]:
                loc["arrivale_date"] = data["predicted_date"]
    return locations


@timing
def api_call():
    """
    В качестве ответа должен выдаваться повагонный список из сервиса get_current_dislocation 
    с обновленной датой прибытия вагона из сервиса get_predicted_dates
    только по вагоном, у которых она отсутствует
    """
    locations = get_current_dislocation()
    invoices = get_invoices_without_arrival_date(locations)
    predicted_data = get_predicted_date_by_invoices(invoices)
    locations = refresh_locations(locations, predicted_data)
    return locations

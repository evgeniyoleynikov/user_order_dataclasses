from dataclasses import dataclass, asdict
import random
from typing import List
import json;


@dataclass
class Adress:
    city: str
    street: str
    house_number: str

@dataclass
class OrderItem:
    tov_name: str
    tov_price: float;
    tov_quantity: int;

@dataclass
class UserOrder:
    user_id: int;
    user_name: str
    adress: Adress
    order_items: List[OrderItem]

#-----------------------------------------------------------------------------------------
def get_city()->str:
    city = "Київ"
    return city
#------------------------------------------------------------------------------------------
def get_street()->str:
    try:
        file = open("list_street.json", "r");
    except FileNotFoundError:
        print("Файл не знайдено...")
        return "";
    list_street = json.load(file);
    file.close();
    #номер улицы - случайное число
    str_number=random.randint(0, len(list_street)-1);
    return list_street[str_number];
#------------------------------------------------------------------------------
def get_house_number()->str:
    house_number =str( random.randint(1, 100));
    return house_number;
#------------------------------------------------------------------------------
def get_user_name()->str:
    try:
        file = open("names.json", "r");
    except FileNotFoundError:
        print("Файл з іменами не знайдено...")
        return "";
    name_list=[];
    name_list = json.load(file);
    name_number=random.randint(0, len(name_list)-1);
    return name_list[name_number];
#-----------------------------------------------------------------------------
def get_tov_info()->dict:
    try:
        file = open("tov_base.json", "r");
    except FileNotFoundError:
        print("Файл з товарами не знайдено");
        return {};

    tov_base = json.load(file);
    tov_number=str(random.randint(1, len(tov_base)));
    return dict(tov_name = tov_base[tov_number]['tov_name'], tov_cena = tov_base[tov_number]['tov_cena']);
    #--------------------------------------------------------------------------------------------
def get_tov_quantity()->int:
    tov_quantity = random.randint(1, 100);
    return tov_quantity;
#--------------------------------------------------------------------------------------------

if __name__ == '__main__':
    REC_NUMBER=10; #количество записей в БД, большими буквати типа это константа
    order_list=[];
    for i in range(REC_NUMBER):
        tov_info = get_tov_info();
        if len(tov_info)==0:
            tov_name="";
            tov_cena=0;
        tov_name=tov_info['tov_name'];
        tov_cena=tov_info['tov_cena'];
        user_order = UserOrder(user_id=i+1, user_name=get_user_name(),
                               adress=Adress(city=get_city(), street=get_street(),
                                             house_number=get_house_number()),
                               order_items=[OrderItem(tov_name=tov_name, tov_price=tov_cena,
                                                      tov_quantity=get_tov_quantity(),)])

        order_list.append(asdict(user_order));

    #теперь попробуем это сериализовать
    json_str=json.dumps(order_list, indent=4);
    file = open('order.json', 'w');
    file.write(json_str);
    file.close();

    #Теперь выполним десериалзацию
    try:
      file = open('order.json', 'r');
    except FileNotFoundError:
        print("Помилка. Файл не знайдено.");
        exit();
    json_str = json.load(file);
    order_list=[];
    for nitem in json_str:
        order_list.append(UserOrder(**nitem));
    #теперь переберем в цикле элементы этого списка и выведем построчно все параметры
    if len(order_list)==0:
        print("Поки що замовлень не було, почекайте трохи...");
        exit();
    print("Список замовлень: ");
    print("{---------------------------------------------------------------------------}")
    for i in range(len(order_list)):
        print(f"Замовлення № {i+1}");
        print(f"Ідентифікатор: {order_list[i].user_id}");
        print(f"ПІБ замовника: {order_list[i].user_name}");
        print("Адресса: ")
        print(f"Місто: {order_list[i].adress['city']}");
        print(f"Вулиця: {order_list[i].adress['street']}");
        print(f"Номер будинку: {order_list[i].adress['house_number']}");
        print("Товари: ");
        for ntov in range(len(order_list[i].order_items)):
            print(f"Назва товару: {order_list[i].order_items[ntov]['tov_name']}");
            print(f"Ціна за одиницю: {order_list[i].order_items[ntov]['tov_price']} гривень");
            print(f"Кількість: {order_list[i].order_items[ntov]['tov_quantity']} штук");
        print("{---------------------------------------------------------------------------}")








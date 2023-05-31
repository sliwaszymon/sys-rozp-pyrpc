# Kalkulator umożliwiający wykonywanie operacji matematycznych na serwerze z użyciem biblioteki PyRPC

## Spis treści
- [1. Wstęp](#1-wstęp)
  - [1.1. Czym jest RPC](#11-czym-jest-rpc)
  - [1.2. Opis zadania](#12-opis-zadania)
- [2. Kalkulator w PyRPC](#2-kalkulator-w-pyrpc)
  - [2.1. Biblioteka PyRPC](#21-biblioteka-pyrpc)
  - [2.2. Podział aplikacji](#22-podział-aplikacji)
  - [2.3. Dostępne funkcje](#23-dostępne-funkcje)
  - [2.4. Sposób działania aplikacji](#24-sposób-działania-aplikacji)
- [3. Podsumowanie](#3-podsumowanie)
  - [3.1. Osiągnięte cele](#31-osiągnięte-cele)
  - [3.2. Napotkane problemy](#32-napotkane-problemy)
- [Bibliografia](#bibliografia)


# 1. Wstęp

## 1.1. Czym jest RPC

RPC (Remote Procedure Call) to protokół komunikacyjny, który umożliwia zdalne wywoływanie procedur lub funkcji w rozproszonym środowisku. Jak to działa? Otóż RPC umożliwia klientowi wywoływanie funkcji lub procedur na odległych maszynach w sieci. Klient wysyła żądanie, w którym określa nazwę funkcji, jej parametry i adres docelowy. To może być zdalnie uruchamiana metoda lub funkcja której parametry są serializowane, czyli przekształcane w ciąg znaków lub binarne dane, przed wysłaniem przez sieć. Po stronie serwera dane są deserializowane, czyli przywracane do pierwotnej formy.

RPC korzysta z istniejących protokołów transportowych, takich jak TCP/IP lub UDP, do przesyłania danych przez sieć. Zapewnia niezawodną i uporządkowaną dostawę żądań i odpowiedzi.

W RPC istnieją dwa rodzaje synchronizacji danych: połączenie synchroniczne, w przypadku którego klient oczekuje na odpowiedź od serwera przed kontynuacją działania oraz asynchroniczne, gdzie klient może kontynuować działanie bez konieczności oczekiwania na odpowiedź zwrotną.

Aby klient i serwer mogli komunikować się ze sobą, muszą znać definicję dostępnych funkcji i parametrów. W tym celu stosuje się protokoły opisu interfejsu, takie jak IDL (Interface Description Language).

RPC jest szeroko stosowany w systemach rozproszonych, takich jak aplikacje internetowe, usługi sieciowe, gry wieloosobowe i wiele innych, gdzie potrzebna jest komunikacja międzykomputerowa.

## 1.2. Opis zadania

Celem zadania jest zapoznanie się z protokołem komunikacyjnym RPC w trakcie tworzenia kalkulatora wykonującego proste operacje matematyczne przy użyciu języka Python oraz biblioteki PyRPC.

# 2. Kalkulator w PyRPC

## 2.1. Biblioteka PyRPC

Biblioteka PyRPC jest bardzo podstawowym modułem rozwijanym dość niesystematycznie do 2020 roku. Moduł ten pozwala na tworzenie aplikacji eksportujących różne funkcje jako usługi, a następnie wywoływanie ich poprzez aplikacje klienckie. Moduł ten wykorzystuje ZeroMQ w celu transferu informacji.

ZeroMQ (ZMQ) to biblioteka komunikacyjna umożliwiająca efektywną wymianę danych między aplikacjami w rozproszonym środowisku. Opiera się na wzorcach publish-subscribe, request-reply oraz push-pull. Działa w architekturze bezbrokera, eliminując potrzebę centralnego punktu komunikacji. ZeroMQ zapewnia wysoką wydajność poprzez minimalizację narzutu komunikacyjnego i zoptymalizowane operacje przesyłania danych. Obsługuje różne wzorce komunikacji, takie jak publikuj-subskrybuj, żądanie-odpowiedź, potokowy przepływ danych, dystrybucję równoległą itp.

## 2.2. Podział aplikacji

W poprzednim podroździale wspomnieliśmy, że biblioteka PyRPC pozwala na tworzenie aplikacji eksportujących moduły i wywołujących te moduły aplikacji klienckich. Jak łatwo więc wydedukować w celu prezentacji działania naszego kalkulatora byliśmy wręcz zmuszeni do stworzenia dwóch aplikacji: aplikacji będącej odwzorowaniem serwera, który eksportuje usługi oraz aplikacji klienckiej, która jest w stanie wywołać udostępnione usługi.

## 2.3. Dostępne funkcje

Do dostępnych funkcjonalności kalkulatora należą:
- dodawanie liczby a do liczby b
- odejmowanie liczby b od liczby a
- mnożenie liczby a przez liczbę b
- dzielenie liczby a przez liczbę b
- podnoszenie liczby a do potęgi b
- obliczanie pierwiastka stopnia b z liczby a
- obliczanie delty i miejsc zerowych funkcji kwadratowej
- upraszczanie funkcji
- obliczanie całki
- obliczanie pierwszej i drugiej pochodnej

Implementacja funkcji różni się w przypadku aplikacji klienckiej i serwerowej.

Przykład implementacji funkcji dodawania oraz całkowania po stronie serwera:

```python
# Import wymaganych paczek
from pyRpc import PyRpc
import sympy as sp
# Deklaracja nowego obiektu PyRPC
myRpc = PyRpc("pl.UWMWMII.pyRpcCalculator") 
# Deklaracja metod add() i calculate_integral()
def add(a, b):
	""" Returns result of sum a + b """
	return a + b

def calculate_integral(expresion):
    """ Calculates integral of given function
		example input: "x**2 + 2*x" """
    return sp.integrate(expresion)

# Publikacja / eksport metod add() i calculate_integral()
myRpc.publishService(add)
```

Domyślnie nowy obiekt PyRpc używa protokołu IPC, który jest przeznaczony dla procesów działających na tej samej maszynie hosta. W celu wyeksportowania usługi przez tcp można opcjonalnie określić adres tcp ip:port do użycia.

Implementacja tych samych funkcji po stronie aplikacji klienckiej wygląda zupełnie inaczej:

```python
from pyRpc import RpcConnection
# Deklaracja nowego obiektu RpcConnection
remote = RpcConnection("pl.UWMWMII.pyRpcCalculator")
# Deklaracja metod add() i calculate_integral()
def add(a, b):
    # Przypisanie do zmiennej wyniku zapytania do serwera
    resp = remote.call('add', args=(a, b))
    print(f'Result of {a} + {b} is {resp.result}')

def calculate_integral(expresion):
    resp = remote.call('calculate_integral', args=[expresion])
    print(f'Integral of expresion {expresion} is {resp.result}')
```

Poza deklaracjami obiektów PyRpc i RpcConnection, które są deklarowane jednorazowo, deklaracje pozostałych funkcjonalności wyglądają analogicznie.

## 2.4. Sposób działania aplikacji

Tworząc kalkulator w oparciu o protokół RPC musieliśmy posłużyć się językiem Python w wersji 3.8.10 oraz biblioteką PyRPC w wersji 0.4.0 (najnowsza wersja ze stycznia 2020 roku).

Po stworzeniu wirtualnego środowiska zaktualizowaliśmy system zarządzania pakietami pip, a następnie zainstalowaliśmy odpowiednie pakiety posługując się poleceniem konsolowym:

> pip install -r requirements.txt

Następnie przy użyciu bibliotek PyRPC oraz wbudowanej biblioteki time stworzyliśmy następującą aplikację serwerową:

```python
import time
from pyRpc import PyRpc
import sympy as sp

def add(a, b):
	""" Returns result of sum a + b """
	return a + b

[...]

myRpc = PyRpc("pl.UWMWMII.pyRpcCalculator") 
time.sleep(.1)

myRpc.publishService(add)

[...]

myRpc.start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    myRpc.stop()
```

Tak wygląda aplikacja kliencka:

```python
import time
from pyRpc import RpcConnection
	 
remote = RpcConnection("pl.UWMWMII.pyRpcCalculator")
time.sleep(.1)

def add(a, b):
    resp = remote.call('add', args=(a, b))
    print(f'Result of {a} + {b} is {resp.result}')

[...]

def help():
    resp = remote.availableServices()
    print('\n===== Available services =====\n')
    for service in resp.result:
        print('Service: %(service)s \nDescription: %(doc)s \nUsage: %(format)s\n' % service)
    print("==============================\n")

listen = True
print('Welcome in PyRpc calculator')
print('If you need help type "help"')
print('To exit program type "exit"\n')
while listen:
    command = str(input('$ '))
    if command == 'exit':
        listen = False
        break
    if command == 'help':
        help()
    elif command.split('(')[0] in [service['service'] for service in remote.availableServices().result]:
        exec(command)
    else:
        print('Service does not exist or you entered the command incorrectly.')
    time.sleep(1)

remote.close()

time.sleep(1)
```

Jak można zauważyć aplikacje te diametralnie się różnią (o czym wspomnieliśmy w poprzednim rozdziale). Aplikacja kliencka została stworzona na wzór konsoli przyjmującej od użytkownika polecenia. Została rozbudowana o funkcję, która nie występuje w ręcznie zadeklarowanych w aplikacji serwerowej funkcjach - help(). Funkcja ta pozwala użytkownikowi na wyświetlenie na ekranie listy wszystkich wyeksportowanych przez aplikacje serwerową funkcji.

Aby przetestować działanie kalkulatora należy ***uruchomić aplikację serwerową***, a następnie (najwygodniej w drugim oknie konsoli) ***uruchomić aplikację kliencką***, dzięki której można wysyłać żądania (używać funkcji wyeksportowanych przez serwer).

# 3. Podsumowanie

## 3.1. Osiągnięte cele

Podczas tworzenia aplikacji udało się nam wyprodukować aplikację serwerową RPC działającą w oparciu o protokołu IPC oraz aplikację kliencką, która potrafi łączyć się i wysyłać zapytania do aplikacji serwerowej oraz odbierać wiadomości zwrotne.

## 3.2. Napotkane problemy

- Ze względu na brak dalszego rozwoju biblioteki PyRPC zostaliśmy zmuszeni do użycia starszej wersji Pythona (3.8.10).
- Brak bezpośredniej kompatybilności protokołu ZMQ z systemem Windows. Do poprawnego działania wymagane jest jądro systemu Linux lub np. środowisko takie jak Conda / Anaconda.

# Bibliografia

- [Czym jest RPC - Wikipedia](https://pl.wikipedia.org/wiki/Zdalne_wywo%C5%82anie_procedury)
- [Czym jest ZeroMQ - Wikipedia](https://en.wikipedia.org/wiki/ZeroMQ)
- [Dokumentacja PyRPC](https://pythonhosted.org/pyRpc/pyRpc.html)
- [Dokumentacja pakietu sympy](https://docs.sympy.org/latest/index.html)

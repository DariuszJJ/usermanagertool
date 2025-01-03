import routeros_api
import csv


def connect_to_router(ip, username, password, port=8728):
    """
    Funkcja łączy się z routerem MikroTik za pomocą API.

    Args:
        ip (str): Adres IP routera.
        username (str): Nazwa użytkownika.
        password (str): Hasło użytkownika.
        port (int): Port API (domyślnie 8728).

    Returns:
        RouterOsApi: Połączenie z API routera.

    Raises:
        Exception: Jeśli połączenie się nie powiedzie.
    """
    try:
        api_pool = routeros_api.RouterOsApiPool(
            ip, username=username, password=password, port=port, plaintext_login=True
        )
        return api_pool.get_api()
    except routeros_api.exceptions.RouterOsApiConnectionError as e:
        print(f"Błąd połączenia z routerem {ip}: {e}")
        raise
    except routeros_api.exceptions.RouterOsApiCommunicationError as e:
        print(f"Błąd komunikacji z routerem {ip}: {e}")
        raise
    except Exception as e:
        print(f"Nieznany błąd podczas łączenia z routerem {ip}: {e}")
        raise


def import_users(source_api):
    """
    Importuje użytkowników z routera źródłowego (RouterOS 6).

    Args:
        source_api: Połączenie z API routera źródłowego.

    Returns:
        list: Lista użytkowników z routera źródłowego.
    """
    users_resource = source_api.get_resource('/tool/user-manager/user')
    users = users_resource.get()
    return users


def create_users(target_api, users):
    """
    Tworzy użytkowników na routerze docelowym (RouterOS 7) na podstawie danych.

    Args:
        target_api: Połączenie z API routera docelowego.
        users (list): Lista użytkowników do utworzenia.
    """
    users_resource = target_api.get_resource('/user-manager/user')
    for user in users:
        try:
            # Dodanie użytkownika z komentarzem, jeśli email istnieje
            users_resource.add(
                name=user['username'],
                password=user['password'],
                comment=f"Email: {user.get('email', 'brak')}"  # Komentarz z email (lub brak)
            )
            print(f"Użytkownik {user['username']} został pomyślnie dodany.")
        except Exception as e:
            print(f"Błąd podczas dodawania użytkownika {user['username']}: {e}")


def export_users_to_csv(users, file_path='exported_users.csv'):
    """
    Eksportuje użytkowników do pliku CSV.

    Args:
        users (list): Lista użytkowników do eksportu.
        file_path (str): Ścieżka do pliku CSV.
    """
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Password', 'Email'])
        for user in users:
            writer.writerow([
                user['username'],
                user['password'],
                user.get('email', 'brak')
            ])
    print(f"Użytkownicy zostali wyeksportowani do pliku {file_path}.")


def main():
    # Dane do połączenia z routerami
    source_router_ip = "192.168.0.1"
    source_username = "admin"
    source_password = "password"

    target_router_ip = "192.168.20.1"
    target_username = "admin"
    target_password = "password"

    # Połączenie z routerami
    source_api = connect_to_router(source_router_ip, source_username, source_password)
    target_api = connect_to_router(target_router_ip, target_username, target_password)

    # Import użytkowników z routera źródłowego
    print("Importowanie użytkowników z routera źródłowego...")
    users = import_users(source_api)

    # Eksport użytkowników do pliku CSV (opcjonalne)
    export_users_to_csv(users)

    # Tworzenie użytkowników na routerze docelowym
    print("Tworzenie użytkowników na routerze docelowym...")
    create_users(target_api, users)

    # Zamknięcie połączenia z API
    source_api.disconnect()
    target_api.disconnect()
    print("Proces zakończony pomyślnie.")


if __name__ == "__main__":
    main()

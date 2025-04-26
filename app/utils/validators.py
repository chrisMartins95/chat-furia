import re

def validate_age(age: str) -> bool:
    """
    Valida se a idade é um número inteiro entre 1 e 120.

    Args:
        age (str): Idade recebida como string.

    Returns:
        bool: True se a idade for válida, False caso contrário.
    """
    try:
        age = int(age)
        return 1 <= age <= 120
    except ValueError:
        return False

def validate_city(city: str) -> bool:
    """
    Valida se o nome da cidade contém apenas letras e espaços.

    Args:
        city (str): Nome da cidade.

    Returns:
        bool: True se o nome for válido, False caso contrário.
    """
    # Permite letras (maiúsculas, minúsculas, acentos) e espaços
    pattern = r"^[A-Za-zÀ-ÿ\s]+$"
    return bool(re.match(pattern, city.strip()))

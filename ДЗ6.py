import requests
from tkinter import Tk, Label, Button, ttk, messagebox as mb
from datetime import datetime

# Поддерживаемые криптовалюты (id в CoinGecko API -> отображаемое имя)
CRYPTO_MAP = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "solana": "Solana (SOL)",
    "binancecoin": "BNB",
    "ripple": "XRP",
}

API_URL = "https://api.coingecko.com/api/v3/simple/price"


def fetch_crypto_prices():
    """Запрашивает CoinGecko API и возвращает разобранные JSON-данные."""
    ids = ",".join(CRYPTO_MAP.keys())
    params = {
        "ids": ids,
        "vs_currencies": "usd",
    }
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def refresh_display():

    try:
        data = fetch_crypto_prices()

        # Очистить таблицу
        for row in tree.get_children():
            tree.delete(row)

        # Заполнить данными
        for coin_id, display_name in CRYPTO_MAP.items():
            if coin_id in data and "usd" in data[coin_id]:
                price = data[coin_id]["usd"]
                price_str = f"$ {price:,.2f}"
            else:
                price_str = "Н/Д"
            tree.insert("", "end", values=(display_name, price_str))

        # Обновить строку состояния
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        status_label.config(text=f"Статус: данные обновлены {now}")

    except requests.exceptions.RequestException as e:
        mb.showerror("Ошибка сети", f"Не удалось связаться с API: {e}")
    except (KeyError, ValueError) as e:
        mb.showerror("Ошибка", f"Получены некорректные данные: {e}")


# ---------- Построение интерфейса ----------
root = Tk()
root.title("Панель курсов криптовалют — CoinGecko")
root.geometry("420x320")
root.resizable(False, False)

# Заголовок
title_label = Label(
    root,
    text="Курсы популярных криптовалют к USD",
    font=("Arial", 13, "bold"),
)
title_label.pack(pady=10)

# Таблица
columns = ("name", "price")
tree = ttk.Treeview(root, columns=columns, show="headings", height=6)
tree.heading("name", text="Криптовалюта")
tree.heading("price", text="Цена в USD")
tree.column("name", width=180, anchor="w")
tree.column("price", width=160, anchor="e")
tree.pack(padx=20, pady=5, fill="x")

# Кнопка обновления
refresh_btn = Button(root, text="Обновить", command=refresh_display, width=18)
refresh_btn.pack(pady=10)

# Строка состояния
status_label = Label(root, text="Статус: ожидание обновления...", fg="red")
status_label.pack(pady=5)

# Автоматическая загрузка при запуске
root.after(100, refresh_display)

root.mainloop()
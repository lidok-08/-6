import requests
from tkinter import Tk, Label, Button, ttk
from tkinter import messagebox as mb
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


def refresh_display():
    try:

        # Заполнить данными
        for coin_id, display_name in CRYPTO_MAP.items():
            if coin_id in data and "usd" in data[coin_id]:
                price = data[coin_id]["usd"]
                price_str = f"$ {price:,.2f}"
            else:
                price_str = "Н/Д"
            tree.insert("", "end", values=(display_name, price_str))

    except (KeyError, ValueError) as e:
        mb.showerror("Ошибка данных", f"Получены некорректные данные: {e}")


# ---------- Построение интерфейса ----------
root = Tk()
root.title("Панель курсов криптовалют — CoinGecko")
root.geometry("420x320")
root.resizable(False, False)

# Заголовок
title_label = Label(
    root,
    text="Курсы популярных криптовалют к USD",
    font=("Arial", 12),
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

root.mainloop()
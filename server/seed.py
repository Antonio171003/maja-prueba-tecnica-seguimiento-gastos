from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import db
from app.models.category import Category
from app.models.expense import Expense

app = create_app()

CATEGORIES = [
    "Alimentación",
    "Transporte",
    "Entretenimiento",
    "Salud",
    "Servicios",
]

EXPENSES = [
    (850.00,  "Despensa semanal",      "2026-03-01", "Alimentación"),
    (320.00,  "Gasolina",              "2026-03-02", "Transporte"),
    (180.00,  "Netflix + Spotify",     "2026-03-03", "Entretenimiento"),
    (650.00,  "Consulta médica",       "2026-03-05", "Salud"),
    (1200.00, "Renta internet",        "2026-03-05", "Servicios"),
    (220.00,  "Uber al aeropuerto",    "2026-03-07", "Transporte"),
    (450.00,  "Restaurante cumpleaños","2026-03-08", "Alimentación"),
    (90.00,   "Farmacia",              "2026-03-10", "Salud"),
    (380.00,  "Cine + cena",           "2026-03-12", "Entretenimiento"),
    (750.00,  "Luz y agua",            "2026-03-13", "Servicios"),
    (310.00,  "Abarrotes",             "2026-03-14", "Alimentación"),
    (140.00,  "Camión semanal",        "2026-03-15", "Transporte"),
    (500.00,  "Gimnasio mensual",      "2026-03-16", "Salud"),
    (260.00,  "Antojitos",             "2026-03-17", "Alimentación"),
    (980.00,  "Teléfono celular",      "2026-03-18", "Servicios"),
]

with app.app_context():
    # Limpia datos existentes
    Expense.query.delete()
    Category.query.delete()
    db.session.commit()

    # Crea categorías
    cats = {}
    for name in CATEGORIES:
        cat = Category(name=name)
        db.session.add(cat)
        db.session.flush()
        cats[name] = cat.id

    # Crea gastos
    for amount, description, date, cat_name in EXPENSES:
        db.session.add(Expense(
            amount=amount,
            description=description,
            date=date,
            category_id=cats[cat_name],
        ))

    db.session.commit()
    print(f"{len(CATEGORIES)} categorías y {len(EXPENSES)} gastos creados.")

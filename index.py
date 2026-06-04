from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import psycopg2
import psycopg2.extras
from datetime import datetime

app = Flask(__name__)

# URL de tu base de datos en Render
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://vapes_user:Bks8bEN969W1Sg0bYyThhhihy9mEcxyr@dpg-d8gcdojtqb8s73beuabg-a.oregon-postgres.render.com/vapes")

def get_db():
    # Conexión a PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    return conn

PRODUCTOS = [
    {
        "id": 1,
        "nombre": "Neon Mango X",
        "categoria": "Pod System",
        "precio": 250,
        "descripcion": "Mango helado ultra neon explosivo.",
        "imagenes": [
            "https://myvapemx.com/wp-content/uploads/2021/06/11-600x600.png",
            "https://nuubevape.com/cdn/shop/products/I_I___O_1_800x800_crop_center@2x.jpg?v=1681270829",
            "https://maskkingcr.com/wp-content/uploads/2024/11/20mangoice-scaled.jpg",
            "https://yovapeo.com/531-thickbox_default/maskking-high-pro-mango-ice.jpg",
            "https://nuubevape.com/cdn/shop/files/Mangoice_800x800_crop_center@2x.jpg?v=1683473520"
        ]
    },
    {
        "id": 2,
        "nombre": "Cyber Berry",
        "categoria": "Liquid",
        "precio": 350,
        "descripcion": "Berry ice frutal premium.",
        "imagenes": [
            "https://static.wixstatic.com/media/2aec95_3427afd1f0ae4e6d9294ca024bca5741~mv2.jpeg/v1/fit/w_500,h_500,q_90/file.jpg",
            "https://http2.mlstatic.com/D_NQ_NP_787988-MLM47134763687_082021-O.webp",
            "https://maskking.com/cdn/shop/files/maskking-proplus-10pack-blue-raspberry-vapeador-original-mexico..png",
            "https://limberit.cloud/trident/files/image/2024/Apr/Thu/66180ed3e7a2c.png",
            "https://yovapeo.com/532-thickbox_default/maskking-high-pro-mixed-berries.jpg"
        ]
    },
    {
        "id": 3,
        "nombre": "Lime Storm",
        "categoria": "Disposable",
        "precio": 400,
        "descripcion": "Lima ácida explosiva.",
        "imagenes": [
            "https://www.lucky8vapes.com/cdn/shop/files/LemonIceTea_2fd4fa5c-6525-4d47-adf3-5d0d4036ad46_1024x1024.jpg",
            "https://maskking.com/cdn/shop/files/LimePomelo.jpg",
            "https://604smoke.com/cdn/shop/products/LemonLimeStrawberry_700x700_1.jpg",
            "https://static.wixstatic.com/media/d410af_35993e812a464971a96e6816aa1e7b93~mv2.jpg",
            "https://www.royalvapes.co.uk/cdn/shop/files/maskking-sip-lemon-lime-disposable_grande.webp"
        ]
    },
    {
        "id": 4,
        "nombre": "Pink Shock",
        "categoria": "Pod System",
        "precio": 350,
        "descripcion": "Fresa ice neon premium.",
        "imagenes": [
            "https://cdn.shopify.com/s/files/1/0573/8463/2454/files/maskking-high-gt-s-2500-puffs-strawberry-lychee-watermelon-disposable-420.webp",
            "https://nuubevape.com/cdn/shop/products/6_1e614a90-0e0a-410d-a0d7-07526a734d89.jpg",
            "https://goloudevents.com/wp-content/uploads/2025/06/MaskkingHigh2.0PeachIce1000ml-scaled.jpeg",
            "https://yovapeo.com/537/maskking-high-pro-peach-ice.jpg",
            "https://cdn.shopify.com/s/files/1/0573/8463/2454/files/maskking-high-gt-s-2500-puffs-strawberry-lychee-disposable-vape-vapes-947.webp"
        ]
    },
    {
        "id": 5,
        "nombre": "Dragon Frost",
        "categoria": "Liquid",
        "precio": 600,
        "descripcion": "Dragon fruit congelado.",
        "imagenes": [
            "https://masquevapor.com/76273-large_default/vaper-desechable-max-box-dragon-fruit.jpg",
            "https://www.elfbar.de/cdn/shop/files/elfbar-800-dragonfruit-strawberry-2.png",
            "https://fotos.rumardi.com/imagenes/fotos/658433.jpg",
            "https://vapeescapedubai.com/wp-content/uploads/2025/01/3.jpeg",
            "https://www.elfbar.de/cdn/shop/files/elfbar-800-dragonfruit-strawberry-1.png"
        ]
    },
    {
        "id": 6,
        "nombre": "Blue Shock",
        "categoria": "Disposable",
        "precio": 300,
        "descripcion": "Arándano eléctrico neon.",
        "imagenes": [
            "https://www.tucultivo.cl/wp-content/uploads/2023/12/desechable-arandano-1.jpg",
            "https://www.mijovape.co/wp-content/uploads/2023/05/mijo-vape-300-puff-arandano-ice-2.jpg",
            "https://i-vapeshop.com/567-large_default/feelvape-pro-800-arandano-refrescante.jpg",
            "https://cdnx.jumpseller.com/mundotabaco/image/48098571/thumb/1079/1079",
            "https://i-vapeshop.com/563-medium_default/feelvape-pro-800-arandano-refrescante.jpg"
        ]
    }
]

def init_db():
    conn = get_db()
    cur = conn.cursor()
    # En Postgres usamos SERIAL para auto-incrementar
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id SERIAL PRIMARY KEY,
            cliente VARCHAR(255),
            direccion TEXT,
            metodo_pago VARCHAR(50),
            producto VARCHAR(255),
            cantidad INTEGER,
            total REAL,
            fecha TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Inicializar la base de datos al arrancar
init_db()

@app.route("/")
def inicio():
    return render_template("inicio.html", productos=PRODUCTOS)

@app.route("/catalogo")
def catalogo():
    return render_template("catalogo.html", productos=PRODUCTOS)

@app.route("/referencias")
def referencias():
    return render_template("referencias.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/compra_realizada")
def compra_realizada():
    return render_template("compra_realizada.html")

@app.route("/registro_ventas")
def registro_venta():
    conn = get_db()
    # RealDictCursor permite acceder a los datos como diccionarios (igual que sqlite3.Row)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM ventas ORDER BY id DESC")
    ventas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("registro_venta.html", ventas=ventas)

@app.route("/venta", methods=["POST"])
def venta():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cliente = data.get("cliente", "Desconocido")
    direccion = data.get("direccion", "Desconocida")
    pago = data.get("pago", "Efectivo")

    for item in data["carrito"]:
        # En Postgres usamos %s para pasar las variables
        cur.execute("""
            INSERT INTO ventas (cliente, direccion, metodo_pago, producto, cantidad, total, fecha)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            cliente,
            direccion,
            pago,
            item["nombre"],
            item["cantidad"],
            item["precio"] * item["cantidad"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok"})

@app.route("/juego")
def abrir_juego():
    # Ahora renderiza la versión web en lugar de abrir Pygame local
    return render_template("juego.html")

if __name__ == "__main__":
    app.run(debug=True)
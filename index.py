from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import threading
import random
from datetime import datetime
import os
import io
import requests
import pygame

app = Flask(__name__)
DB = "vaporhaus.sqlite"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            direccion TEXT,
            metodo_pago TEXT,
            producto TEXT,
            cantidad INTEGER,
            total REAL,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()

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
    ventas = conn.execute("SELECT * FROM ventas ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("registro_venta.html", ventas=ventas)

@app.route("/venta", methods=["POST"])
def venta():
    data = request.json
    conn = get_db()

    cliente = data.get("cliente", "Desconocido")
    direccion = data.get("direccion", "Desconocida")
    pago = data.get("pago", "Efectivo")

    for item in data["carrito"]:
        conn.execute("""
            INSERT INTO ventas (cliente, direccion, metodo_pago, producto, cantidad, total, fecha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
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
    conn.close()

    return jsonify({"status": "ok"})

def cargar_imagen_url(url, tamano):
    try:
        respuesta = requests.get(url, timeout=5)
        archivo_memoria = io.BytesIO(respuesta.content)
        img = pygame.image.load(archivo_memoria).convert_alpha()
        img = pygame.transform.smoothscale(img, tamano)
        return img
    except Exception as e:
        surf = pygame.Surface(tamano)
        surf.fill((176, 38, 255)) 
        return surf

def iniciar_juego_pygame():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Vaporhaus Arcade")
    clock = pygame.time.Clock()

    # Colores y fuentes
    NEGRO, BLANCO, ROJO, AZUL, VERDE = (10,10,15), (255,255,255), (255,50,50), (0,242,254), (57,255,20)
    fuente = pygame.font.Font(None, 40)
    fuente_big = pygame.font.Font(None, 100)

    # Assets
    fondo_img = cargar_imagen_url("https://static.vecteezy.com/system/resources/previews/003/776/240/non_2x/blurred-colorful-holographic-background-in-neon-colors-trendy-wallpaper-foil-texture-vector.jpg", (ANCHO, ALTO))
    canasta_img = cargar_imagen_url("https://img.magnific.com/psd-gratis/rustic-woven-natural-fiber-basket-with-handles_84443-76208.jpg?semt=ais_hybrid&w=740&q=80", (100, 100))
    URLS_VAPES = [
        "https://myvapemx.com/wp-content/uploads/2021/06/11-600x600.png",
        "https://masquevapor.com/76273-large_default/vaper-desechable-max-box-dragon-fruit.jpg",
        "https://www.elfbar.de/cdn/shop/files/elfbar-800-dragonfruit-strawberry-2.png"
    ]
    vapes_imgs = [cargar_imagen_url(url, (40, 80)) for url in URLS_VAPES]

    # Variables
    jugador_x, jugador_y = ANCHO // 2 - 50, ALTO - 120
    score, vidas, nivel, velocidad_caida = 0, 3, 1, 5
    vapes_cayendo, particulas = [], []
    running, game_over = True, False

    def glow_text(texto, font, color, x, y):
        sombra = font.render(texto, True, (0, 0, 0))
        for i in range(3): pantalla.blit(sombra, (x+i, y+i))
        txt = font.render(texto, True, color)
        pantalla.blit(txt, (x, y))

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            running = False

        if not game_over:
            # Movimiento
            if teclas[pygame.K_LEFT] and jugador_x > 0: jugador_x -= 12
            if teclas[pygame.K_RIGHT] and jugador_x < ANCHO - 100: jugador_x += 12

            # Lógica
            if random.randint(1, max(20, 60 - (nivel * 5))) == 1:
                vapes_cayendo.append([random.randint(20, ANCHO - 60), -80, random.choice(vapes_imgs)])

            pantalla.blit(fondo_img, (0, 0))
            fondo_oscuro = pygame.Surface((ANCHO, ALTO))
            fondo_oscuro.set_alpha(100)
            fondo_oscuro.fill((0, 0, 0))
            pantalla.blit(fondo_oscuro, (0, 0))

            for vape in vapes_cayendo[:]:
                vape[1] += velocidad_caida
                pantalla.blit(vape[2], (vape[0], vape[1]))

                if (jugador_x < vape[0] + 30 and jugador_x + 100 > vape[0] and
                    jugador_y < vape[1] + 70 and jugador_y + 80 > vape[1]):
                    score += 10
                    for _ in range(15): particulas.append([vape[0]+20, vape[1]+40, random.randint(-8,8), random.randint(-8,8), random.randint(15,30), AZUL, random.randint(3,6)])
                    vapes_cayendo.remove(vape)
                    if score % 100 == 0:
                        nivel += 1
                        velocidad_caida += 1
                    continue

                if vape[1] > ALTO:
                    vidas -= 1
                    for _ in range(20): particulas.append([vape[0]+20, ALTO-10, random.randint(-8,8), random.randint(-8,8), random.randint(15,30), ROJO, random.randint(3,6)])
                    vapes_cayendo.remove(vape)
                    if vidas <= 0: game_over = True

            pantalla.blit(canasta_img, (jugador_x, jugador_y))
            
            for p in particulas[:]:
                p[0] += p[2]
                p[1] += p[3]
                p[4] -= 1
                pygame.draw.circle(pantalla, p[5], (int(p[0]), int(p[1])), p[6])
                if p[4] <= 0: particulas.remove(p)

            glow_text(f"PTS: {score}", fuente, VERDE, 20, 20)
            glow_text(f"VIDAS: {vidas}", fuente, ROJO, 20, 60)
            glow_text(f"NIVEL: {nivel}", fuente, AZUL, ANCHO - 150, 20)
        
        else: # GAME OVER SCREEN
            pantalla.fill(NEGRO)
            glow_text("GAME OVER", fuente_big, ROJO, ANCHO//2 - 200, ALTO//2 - 100)
            glow_text(f"PUNTOS: {score}", fuente, BLANCO, ANCHO//2 - 80, ALTO//2 + 20)
            glow_text("ESC PARA SALIR", fuente, AZUL, ANCHO//2 - 110, ALTO//2 + 80)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    return

@app.route("/juego")
def abrir_juego():
    threading.Thread(target=iniciar_juego_pygame, daemon=True).start()
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)
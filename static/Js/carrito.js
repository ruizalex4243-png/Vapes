document.addEventListener("DOMContentLoaded", () => {
    let carrito = JSON.parse(localStorage.getItem("vaporhaus_cart")) || [];

    const contadorBadge = document.getElementById("carrito-contador");
    const contenedorItems = document.getElementById("carrito-items");
    const txtTotal = document.getElementById("carrito-total");
    actualizarInterfaz();
    document.addEventListener("click", (e) => {
        if (e.target && e.target.classList.contains("btn-agregar-carrito")) {
            const boton = e.target;
            
            const producto = {
                id: boton.getAttribute("data-id"),
                nombre: boton.getAttribute("data-nombre"),
                precio: parseFloat(boton.getAttribute("data-precio")),
                imagen: boton.getAttribute("data-imagen"),
                cantidad: 1
            };

            agregarAlCarrito(producto);
            const carritoPanel = new bootstrap.Offcanvas(document.getElementById('carritoPanel'));
            carritoPanel.show();
        }
    });

    function agregarAlCarrito(productoNuevo) {
        const existe = carrito.find(item => item.id === productoNuevo.id);

        if (existe) {
            existe.cantidad++;
        } else {
            carrito.push(productoNuevo);
        }

        guardarYActualizar();
    }
    function guardarYActualizar() {
        localStorage.setItem("vaporhaus_cart", JSON.stringify(carrito));
        actualizarInterfaz();
    }
    function actualizarInterfaz() {
        if (!contenedorItems) return;

        contenedorItems.innerHTML = "";
        let total = 0;
        let cantidadTotal = 0;

        if (carrito.length === 0) {
            contenedorItems.innerHTML = `<p class="text-center text-muted mt-4">Tu carrito está vacío</p>`;
        } else {
            carrito.forEach((item, index) => {
                total += item.precio * item.cantidad;
                cantidadTotal += item.cantidad;

                contenedorItems.innerHTML += `
                    <div class="d-flex align-items-center mb-3 p-2 rounded" style="background: rgba(255,255,255,0.05); border: 1px solid var(--border);">
                        <img src="${item.imagen}" style="width: 50px; height: 50px; object-fit: contain; margin-right: 15px;" alt="${item.nombre}">
                        <div class="flex-grow-1">
                            <h6 class="mb-0 text-white" style="font-size: 0.9rem;">${item.nombre}</h6>
                            <small style="color: var(--lima); font-weight: bold;">$${item.precio}</small>
                        </div>
                        <div class="d-flex align-items-center">
                            <button class="btn btn-sm text-white px-2 py-0" onclick="modificarCantidad(${index}, -1)">➖</button>
                            <span class="mx-2 text-white fw-bold">${item.cantidad}</span>
                            <button class="btn btn-sm text-white px-2 py-0" onclick="modificarCantidad(${index}, 1)">➕</button>
                        </div>
                    </div>
                `;
            });
        }

        if (contadorBadge) contadorBadge.innerText = cantidadTotal;
        if (txtTotal) txtTotal.innerText = total.toFixed(2);
    }
    
    window.modificarCantidad = function(index, cambio) {
        carrito[index].cantidad += cambio;
        if (carrito[index].cantidad <= 0) {
            carrito.splice(index, 1);
        }
        
        guardarYActualizar();
    };

    window.procesarCompra = function() {
        if (carrito.length === 0) {
            alert("¡Tu carrito está vacío! Agrega algo del catálogo primero. 🍓");
            return;
        }
        window.location.href = "/checkout";
    };
});
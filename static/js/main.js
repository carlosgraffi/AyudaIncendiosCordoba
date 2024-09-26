document.addEventListener('DOMContentLoaded', () => {
    fetchBrigades();
});

async function fetchBrigades() {
    try {
        const response = await fetch('/api/brigades');
        const brigades = await response.json();
        displayBrigades(brigades);
    } catch (error) {
        console.error('Error al cargar las brigadas:', error);
    }
}

function displayBrigades(brigades) {
    const container = document.getElementById('brigades-container');
    container.innerHTML = '';

    brigades.forEach(brigade => {
        const brigadeElement = createBrigadeElement(brigade);
        container.appendChild(brigadeElement);
    });
}

function createBrigadeElement(brigade) {
    const element = document.createElement('div');
    element.className = 'brigade-card';
    element.innerHTML = `
        <h2 class="brigade-name">${brigade.nombre}</h2>
        <p class="brigade-info"><strong>Ubicación:</strong> ${brigade.ubicacion}</p>
        <p class="brigade-info"><strong>Contacto principal:</strong> <a href="${brigade.contacto_principal.url}" target="_blank">${brigade.contacto_principal.plataforma}</a></p>
        <div class="donation-info">
            <h3 class="donation-title">Información para donaciones</h3>
            <p class="bank-info"><strong>Banco:</strong> ${brigade.donacion.banco}</p>
            <p class="bank-info"><strong>Tipo de cuenta:</strong> ${brigade.donacion.tipo_cuenta}</p>
            <p class="bank-info"><strong>CBU:</strong> ${brigade.donacion.cbu}</p>
            <p class="bank-info"><strong>Alias:</strong> ${brigade.donacion.alias}</p>
            <p class="bank-info"><strong>CUIT:</strong> ${brigade.donacion.cuit}</p>
        </div>
        <p class="mt-4 text-sm text-gray-600">Última actualización: ${brigade.fecha_actualizacion}</p>
    `;
    return element;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(amount);
}

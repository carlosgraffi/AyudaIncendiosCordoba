document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search');
    const brigadesContainer = document.getElementById('brigades-container');

    searchInput.addEventListener('input', debounce(searchBrigades, 300));
    brigadesContainer.addEventListener('click', handleCopyAlias);

    function searchBrigades() {
        const query = searchInput.value.trim();
        if (query.length === 0) {
            location.reload();
            return;
        }

        fetch(`/search?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                brigadesContainer.innerHTML = '';
                data.forEach(brigade => {
                    brigadesContainer.innerHTML += createBrigadeCard(brigade);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    function createBrigadeCard(brigade) {
        const phoneLink = brigade['Phone Number']
            ? `<a href="https://wa.me/${brigade['Phone Number'].replace(/\s/g, '')}" target="_blank" class="hover:underline">${brigade['Phone Number']}</a>`
            : 'N/A';

        const instagramLink = brigade.Instagram
            ? `<a href="https://www.instagram.com/${brigade.Instagram.replace('@', '')}" target="_blank" class="hover:underline">${brigade.Instagram}</a>`
            : 'N/A';

        return `
            <div class="brigade-card rounded-lg shadow-md p-6 mb-4">
                <h2 class="text-xl font-bold mb-2">
                    <svg class="inline-block w-6 h-6 mr-2 fill-current text-white" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
                        <path d="M336 972.8c-60.8-128-28.8-201.6 19.2-268.8 51.2-76.8 64-150.4 64-150.4s41.6 51.2 25.6 134.4c70.4-80 83.2-208 73.6-256 160 112 230.4 358.4 137.6 537.6 492.8-281.6 121.6-700.8 57.6-745.6 22.4 48 25.6 128-19.2 166.4-73.6-281.6-256-336-256-336 22.4 144-76.8 300.8-172.8 419.2-3.2-57.6-6.4-96-38.4-153.6-6.4 105.6-86.4 188.8-108.8 294.4C89.6 758.4 140.8 860.8 336 972.8L336 972.8z" />
                    </svg>
                    ${brigade.Name}
                </h2>
                <p class="mb-2">
                    Alias: ${brigade.Alias || 'N/A'}
                </p>
                <p class="mb-2">Teléfono: ${phoneLink}</p>
                <p class="mb-2">Instagram: ${instagramLink}</p>
                <p>Facebook: ${brigade.Facebook || 'N/A'}</p>
                <div class="button-container">
                    <button class="mt-4 px-4 py-2 rounded copy-alias copy-alias-btn btn-full-width" data-alias="${brigade.Alias || ''}">Copiar Alias</button>
                </div>
            </div>
        `;
    }

    function handleCopyAlias(event) {
        if (event.target.classList.contains('copy-alias')) {
            const alias = event.target.getAttribute('data-alias');
            navigator.clipboard.writeText(alias).then(() => {
                alert('Alias copiado al portapapeles');
            }).catch(err => {
                console.error('Error al copiar el alias:', err);
            });
        }
    }

    function debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }
});

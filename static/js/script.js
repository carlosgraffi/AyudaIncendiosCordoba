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
        const instagramLink = brigade.Instagram
            ? `<a href="https://www.instagram.com/${brigade.Instagram.replace('@', '')}" target="_blank" class="text-blue-500 hover:underline">${brigade.Instagram}</a>`
            : 'N/A';

        return `
            <div class="brigade-card bg-white rounded-lg shadow-md p-6 mb-4">
                <h2 class="text-xl font-bold mb-2">${brigade.Name}</h2>
                <p class="text-gray-600 mb-2">
                    Alias: ${brigade.Alias || 'N/A'}
                    <button class="ml-2 px-2 py-1 bg-blue-500 text-white rounded copy-alias" data-alias="${brigade.Alias || ''}">Copiar Alias</button>
                </p>
                <p class="text-gray-600 mb-2">Teléfono: ${brigade['Phone Number'] || 'N/A'}</p>
                <p class="text-gray-600 mb-2">Instagram: ${instagramLink}</p>
                <p class="text-gray-600">Facebook: ${brigade.Facebook || 'N/A'}</p>
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

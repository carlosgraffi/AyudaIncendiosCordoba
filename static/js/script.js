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
                <h2 class="text-xl font-bold mb-2">${brigade.Name}</h2>
                <p class="mb-2">
                    Alias: ${brigade.Alias || 'N/A'}
                </p>
                <p class="mb-2">Teléfono: ${phoneLink}</p>
                <p class="mb-2">Instagram: ${instagramLink}</p>
                <p>Facebook: ${brigade.Facebook || 'N/A'}</p>
                <button class="mt-4 px-4 py-2 rounded copy-alias" data-alias="${brigade.Alias || ''}">Copiar Alias</button>
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

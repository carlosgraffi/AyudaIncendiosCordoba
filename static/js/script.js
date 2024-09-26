document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search');
    const brigadesContainer = document.getElementById('brigades-container');

    searchInput.addEventListener('input', debounce(searchBrigades, 300));

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
        return `
            <div class="brigade-card bg-white rounded-lg shadow-md p-6 mb-4">
                <h2 class="text-xl font-bold mb-2">${brigade.Name}</h2>
                <p class="text-gray-600 mb-2">Alias: ${brigade.Alias || 'N/A'}</p>
                <p class="text-gray-600 mb-2">Teléfono: ${brigade['Phone Number'] || 'N/A'}</p>
                <p class="text-gray-600 mb-2">Instagram: ${brigade.Instagram || 'N/A'}</p>
                <p class="text-gray-600">Facebook: ${brigade.Facebook || 'N/A'}</p>
            </div>
        `;
    }

    function debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }
});

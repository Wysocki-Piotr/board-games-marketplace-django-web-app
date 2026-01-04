$(document).ready(function() {
$('#btn-api-search').on('click', function() {
        fetchListings();
    });

    $('#api-search-query').on('keypress', function(e) {
        if(e.which == 13) fetchListings();
    });

    function fetchListings() {
        const query = $('#api-search-query').val();
        const price = $('#api-max-price').val();
        const condition = $('#api-condition').val();

        const params = new URLSearchParams({
            query: query,
            max_price: price,
            condition: condition
        });

        fetch(`/api/search/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                const listings = data;
                const $grid = $('#listings-grid');
                $grid.empty();

                if (listings.length === 0) {
                    $grid.append('<p>Brak wyników spełniających kryteria.</p>');
                    return;
                }

                listings.forEach(item => {

                    let imgHtml = item.image_url
                        ? `<img src="${item.image_url}" alt="${item.title}">`
                        : `<div class="no_photo">Brak zdjęcia</div>`;

                    const cardHtml = `
                        <div class="card">
                            <a href="/listing/${item.id}/" class="card-link-wrapper">
                                ${imgHtml}
                                <h3>${item.title}</h3>
                                <p>${item.category}</p>
                                <p class="price">${item.price} PLN</p>
                                <p>Stan: <strong>${item.condition_display}</strong></p>
                                <small>Sprzedawca: ${item.seller}</small>
                            </a>
                        </div>
                    `;
                    $grid.append(cardHtml);
                });
            })
            .catch(error => console.error('Błąd:', error));
    }
    });
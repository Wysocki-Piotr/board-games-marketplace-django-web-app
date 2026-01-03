$(document).ready(function() {
    $('.select2-game').select2({
        placeholder: "Kliknij i zacznij pisać nazwę gry...",
        allowClear: true,
        language: {
            noResults: function() {
                return "Nie znaleziono takiej gry - wpisz ją poniżej w polu 'Własny tytuł'";
            }
        }
    });

    const $gameSelect = $('#id_game');
    const $customInput = $('#id_custom_title');

    $gameSelect.on('change', function() {
        if ($(this).val()) {
            $customInput.val('').prop('disabled', true);
            $customInput.attr('placeholder', 'Wybrano grę z listy (odznacz X, aby wpisać własną)');
        } else {
            $customInput.prop('disabled', false);
            $customInput.attr('placeholder', 'LUB wpisz własną nazwę (jeśli nie ma na liście)');
        }
    });

    $customInput.on('input', function() {
        if ($(this).val().length > 0) {
            $gameSelect.val(null).trigger('change');
        }
    });

    $gameSelect.trigger('change');

    $('#share-btn').on('click', function() {
    const url = window.location.href;

    navigator.clipboard.writeText(url).then(function() {
        const originalText = $('#share-btn').text();
        $('#share-btn').text('✅ Skopiowano!').css('background', '#27ae60');

        setTimeout(function() {
            $('#share-btn').text(originalText).css('background', 'dodgerblue');
        }, 2000);
    }, function(err) {
        alert('Nie udało się skopiować linku.');
    });
});

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
                const listings = data.listings;
                const $grid = $('#listings-grid');
                $grid.empty();

                if (listings.length === 0) {
                    $grid.append('<p style="text-align:center; width:100%;">Brak wyników spełniających kryteria.</p>');
                    return;
                }

                listings.forEach(item => {

                    let imgHtml = item.image_url
                        ? `<img src="${item.image_url}" alt="${item.title}">`
                        : `<div class="no_photo">Brak zdjęcia</div>`;

                    const cardHtml = `
                        <div class="card">
                            <a href="/market/listing/${item.id}/" class="card-link-wrapper">
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


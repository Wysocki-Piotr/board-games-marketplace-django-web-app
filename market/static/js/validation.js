$(document).ready(function() {
$('#register-form').on('submit', function(e) {
        let isValid = true;

        const username = $('#id_username');
        const email = $('#id_email');

        if (username.length && username.val().trim() === '') {
            showError(username, "Nazwa użytkownika jest wymagana.");
            isValid = false;
        } else {
            clearError(username);
        }

        if (email.length) {
            const emailVal = email.val().trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (emailVal === '') {
                showError(email, "Adres e-mail jest wymagany.");
                isValid = false;
            } else if (!emailRegex.test(emailVal)) {
                showError(email, "Wpisz poprawny adres e-mail.");
                isValid = false;
            } else {
                clearError(email);
            }
        }

        if (!isValid) {
            e.preventDefault();
        }
    });


    $('#listing-form').on('submit', function(e) {
        let isValid = true;

        const gameSelect = $('#id_game');
        const customTitle = $('#id_custom_title');
        const price = $('#id_price');

        const isGameSelected = gameSelect.val() && gameSelect.val() !== '';
        const isCustomTitleFilled = customTitle.val().trim() !== '';

        if (!isGameSelected && !isCustomTitleFilled) {
            showError(customTitle, "Musisz wybrać grę z listy LUB wpisać własny tytuł.");
            isValid = false;
        } else {
            clearError(customTitle);
        }

        const priceVal = parseFloat(price.val());
        if (price.val() === '' || isNaN(priceVal)) {
            showError(price, "Podaj cenę.");
            isValid = false;
        } else if (priceVal <= 0) {
            showError(price, "Cena musi być większa od 0.");
            isValid = false;
        } else {
            clearError(price);
        }

        if (!isValid) {
            e.preventDefault();
            $('html, body').animate({
                scrollTop: $(".js-error-message").first().offset().top - 100
            }, 500);
        }
    });
});
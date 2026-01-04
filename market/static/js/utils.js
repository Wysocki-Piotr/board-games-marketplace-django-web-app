function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

function showError(field, message) {
    const container = $(field).closest('p');

    container.find('.js-error-message').remove();

    $(field).addClass('input-error');

    const errorHtml = `<div class="js-error-message">❌ ${message}</div>`;
    $(field).after(errorHtml);
    }

function clearError(field) {
    const container = $(field).closest('p');
    container.find('.js-error-message').remove();
    $(field).removeClass('input-error');
}

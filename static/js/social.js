/**
 * Social features JavaScript - AJAX interactions
 * Handles favorite toggling, follow toggling, and notification updates
 */

// CSRF token helper for Django
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

const csrftoken = getCookie('csrftoken');

/**
 * Toggle favorite on a hymn (AJAX)
 * @param {string} hymnId - UUID of the hymn
 * @param {HTMLElement} button - The button element that was clicked
 */
function toggleFavorite(hymnId, button) {
    const url = `/hinos/${hymnId}/favoritar/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        // Update button appearance
        if (data.is_favorited) {
            button.innerHTML = '❤️ Favoritado';
            button.classList.add('favorited');
        } else {
            button.innerHTML = '🤍 Favoritar';
            button.classList.remove('favorited');
        }

        // Show message (optional)
        showMessage(data.message, 'success');
    })
    .catch(error => {
        console.error('Error toggling favorite:', error);
        showMessage('Erro ao favoritar. Tente novamente.', 'error');
    });
}

/**
 * Toggle follow on a user (AJAX)
 * @param {string} username - Username to follow/unfollow
 * @param {HTMLElement} button - The button element that was clicked
 */
function toggleFollow(username, button) {
    const url = `/perfil/${username}/seguir/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        // Update button appearance
        if (data.is_following) {
            button.innerHTML = '✓ Seguindo';
            button.classList.add('following');
        } else {
            button.innerHTML = 'Seguir';
            button.classList.remove('following');
        }

        // Show message (optional)
        showMessage(data.message, 'success');
    })
    .catch(error => {
        console.error('Error toggling follow:', error);
        showMessage('Erro ao seguir. Tente novamente.', 'error');
    });
}

/**
 * Update notification count in navbar
 */
function updateNotificationCount() {
    const url = '/notificacoes/nao-lidas/';

    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        const badge = document.getElementById('notification-count');
        if (badge) {
            if (data.count > 0) {
                badge.textContent = data.count;
                badge.style.display = 'inline-block';
            } else {
                badge.style.display = 'none';
            }
        }
    })
    .catch(error => {
        console.error('Error updating notification count:', error);
    });
}

/**
 * Mark notification as read (AJAX)
 * @param {string} notificationId - UUID of the notification
 */
function markNotificationRead(notificationId) {
    const url = `/notificacoes/${notificationId}/marcar-lida/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update UI to show as read
            const notificationElement = document.querySelector(`[data-notification-id="${notificationId}"]`);
            if (notificationElement) {
                notificationElement.classList.add('read');
            }

            // Update count
            updateNotificationCount();
        }
    })
    .catch(error => {
        console.error('Error marking notification as read:', error);
    });
}

/**
 * Submit comment via AJAX (optional enhancement)
 * @param {HTMLFormElement} form - The comment form
 */
function submitComment(form) {
    const formData = new FormData(form);
    const url = form.action;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: formData,
        credentials: 'same-origin',
    })
    .then(response => {
        if (response.ok) {
            // Reload page to show new comment
            window.location.reload();
        } else {
            showMessage('Erro ao enviar comentário. Tente novamente.', 'error');
        }
    })
    .catch(error => {
        console.error('Error submitting comment:', error);
        showMessage('Erro ao enviar comentário. Tente novamente.', 'error');
    });
}

/**
 * Show a temporary message to the user
 * @param {string} message - The message to show
 * @param {string} type - 'success' or 'error'
 */
function showMessage(message, type = 'success') {
    // Remove existing message if any
    const existingMessage = document.getElementById('flash-message');
    if (existingMessage) {
        existingMessage.remove();
    }

    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.id = 'flash-message';
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        background: ${type === 'success' ? '#48bb78' : '#f56565'};
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    messageDiv.textContent = message;

    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);

    document.body.appendChild(messageDiv);

    // Remove after 3 seconds
    setTimeout(() => {
        messageDiv.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => messageDiv.remove(), 300);
    }, 3000);
}

/**
 * Initialize notification count update on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    // Update notification count if user is logged in
    if (document.getElementById('notification-count')) {
        updateNotificationCount();

        // Update every 30 seconds
        setInterval(updateNotificationCount, 30000);
    }

    // Add event listeners to favorite buttons
    document.querySelectorAll('[data-action="toggle-favorite"]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const hymnId = this.dataset.hymnId;
            toggleFavorite(hymnId, this);
        });
    });

    // Add event listeners to follow buttons
    document.querySelectorAll('[data-action="toggle-follow"]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const username = this.dataset.username;
            toggleFollow(username, this);
        });
    });
});

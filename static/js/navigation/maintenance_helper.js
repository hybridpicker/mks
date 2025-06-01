// Notification Helper Function
function showNotification(message, type = 'success') {
    // Erstelle Notification Element
    const notification = document.createElement('div');
    notification.className = `mks-notification ${type}`;
    notification.textContent = message;
    
    // Füge zum Body hinzu
    document.body.appendChild(notification);
    
    // Entferne nach 3 Sekunden
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Füge slideOut Animation hinzu
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

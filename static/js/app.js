// Navigation active state management
document.addEventListener("DOMContentLoaded", () => {
  // Highlight active navigation button based on current page
  const currentPath = window.location.pathname;
  const navButtons = document.querySelectorAll(".nav-btn");

  navButtons.forEach((btn) => {
    const btnPath = btn.getAttribute("href");
    if (currentPath === btnPath || (currentPath === "/" && btnPath === "/")) {
      btn.classList.add("active");
    }
  });
});

// Utility function for API calls
async function apiCall(url, method = "GET", data = null) {
  const options = {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (data && method !== "GET") {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API call failed:", error);
    throw error;
  }
}

// Show notification
function showNotification(message, type = "info") {
  // Create notification element
  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background-color: ${type === "success" ? "#10B981" : type === "error" ? "#EF4444" : "#0EA5E9"};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideInRight 0.3s ease;
    `;

  document.body.appendChild(notification);

  // Remove after 3 seconds
  setTimeout(() => {
    notification.style.animation = "slideOutRight 0.3s ease";
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// Add animation styles
const style = document.createElement("style");
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
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

// Format phone number
function formatPhoneNumber(phone) {
  // Remove all non-digit characters
  const cleaned = phone.replace(/\D/g, "");

  // Format as +221 XX XXX XX XX (Senegal format)
  if (cleaned.startsWith("221")) {
    return `+${cleaned.slice(0, 3)} ${cleaned.slice(3, 5)} ${cleaned.slice(5, 8)} ${cleaned.slice(8, 10)} ${cleaned.slice(10, 12)}`;
  }

  return phone;
}

// Validate phone number
function validatePhoneNumber(phone) {
  const cleaned = phone.replace(/\D/g, "");
  return cleaned.startsWith("221") && cleaned.length === 12;
}

// Export functions for use in templates
window.apiCall = apiCall;
window.showNotification = showNotification;
window.formatPhoneNumber = formatPhoneNumber;
window.validatePhoneNumber = validatePhoneNumber;

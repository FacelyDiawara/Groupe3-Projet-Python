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

// Role-Based Access Control (RBAC) Enforcement
function applyRoleRestrictions() {
  const role = localStorage.getItem("userRole");
  const path = window.location.pathname;

  // 1. Admin bypass: Full rights
  if (role === "Admin") {
    console.log("🔓 Rôle Admin : Accès complet autorisé");
    return;
  }

  console.log(`🔒 Application des restrictions pour le rôle : ${role}`);

  // 2. Chat Mutual Restrictions
  if (path === "/chat") {
    const inputZones = document.querySelectorAll(".input-zone");
    inputZones.forEach((zone) => {
      const isDoctorZone = zone.textContent.includes("Zone Docteur");
      const isPatientZone = zone.textContent.includes("Zone Patient");
      const inputs = zone.querySelectorAll("input, button, .voice-record-btn");

      const shouldRestrict = (role === "Patient" && isDoctorZone) || (role === "Doctor" && isPatientZone);

      if (shouldRestrict) {
        zone.style.opacity = "0.4";
        zone.style.pointerEvents = "none";
        zone.title = "Saisie réservée à l'autre rôle";
        inputs.forEach(input => {
          input.disabled = true;
          input.style.filter = "grayscale(1)";
        });
      } else {
        // Reset if role changed or something
        zone.style.opacity = "1";
        zone.style.pointerEvents = "auto";
        inputs.forEach(input => {
          input.disabled = false;
          input.style.filter = "none";
        });
      }
    });
  }

  // 3. Navbar & Page Access for Patients
  if (role === "Patient") {
    const navButtons = document.querySelectorAll(".nav-btn");
    navButtons.forEach((btn) => {
      const text = btn.textContent.toLowerCase();
      if (
        text.includes("liste") ||
        btn.getAttribute("href") === "/patients_list"
      ) {
        btn.style.display = "none";
      }
    });

    if (path === "/patients_list" || path === "/users") {
      window.location.href = "/";
      alert("Accès refusé : Cette section est réservée au personnel.");
      return;
    }
  }

  // 4. Global Button & Input Restrictions (Doctor & Patient)
  const elements = [
    ...Array.from(document.querySelectorAll("button, .btn, .action-btn")),
    ...Array.from(
      document.querySelectorAll(
        "input:not([type='radio']):not([type='checkbox']), textarea, select",
      ),
    ),
  ];

  const crudKeywords = ["supprimer", "modifier", "ajouter"];
  const patientKeywords = [
    "ordonnance",
    "sms",
    "whatsapp",
    "générer",
    "envoyer",
    "enregistrer",
    "choisir un docteur",
  ];

  elements.forEach((el) => {
    const text = (el.textContent || el.value || "").toLowerCase();
    const id = (el.id || "").toLowerCase();

    // Restricted for BOTH Doctor and Patient
    const isCrud = crudKeywords.some((kw) => text.includes(kw) || id.includes(kw));
    
    // Restricted ONLY for Patient
    const isPatientOnly = role === "Patient" && patientKeywords.some((kw) => text.includes(kw) || id.includes(kw));

    if (isCrud || isPatientOnly) {
      el.classList.add("restricted-feature");
      el.disabled = true;
      el.style.opacity = "0.4";
      el.style.pointerEvents = "none";
      el.style.filter = "grayscale(1)";
      el.style.cursor = "not-allowed";
      el.title = "Action restreinte selon votre rôle";
    }
  });
}

// Export functions for use in templates
window.apiCall = apiCall;
window.showNotification = showNotification;
window.formatPhoneNumber = formatPhoneNumber;
window.validatePhoneNumber = validatePhoneNumber;
window.applyRoleRestrictions = applyRoleRestrictions;

// Check auth status on load (secondary check)
document.addEventListener("DOMContentLoaded", () => {
  const role = localStorage.getItem("userRole");
  const path = window.location.pathname;

  if (!role && path !== "/login") {
    window.location.href = "/login";
  } else {
    applyRoleRestrictions();
    
    // Observer for dynamic content
    const observer = new MutationObserver(() => applyRoleRestrictions());
    observer.observe(document.body, { childList: true, subtree: true });
  }
});

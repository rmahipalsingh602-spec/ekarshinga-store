// ===============================
// Ekarshinga Store - Main JS
// ===============================

console.log("Ekarshinga Store loaded successfully!");

// Glow click animation
document.addEventListener("click", function (e) {
    if (e.target.classList.contains("btn")) {
        e.target.classList.add("clicked");
        setTimeout(() => e.target.classList.remove("clicked"), 200);
    }
});

// Free download confirm
document.addEventListener("click", function (e) {
    if (e.target.classList.contains("free")) {
        alert("Free asset download started ✅");
    }
});

// Buy placeholder (until gateway live)
document.addEventListener("click", function (e) {
    if (e.target.classList.contains("buy-btn")) {
        alert("Redirecting to payment 💳");
    }
});

// Smooth scroll (mobile feel)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute("href")).scrollIntoView({
            behavior: "smooth"
        });
    });
});

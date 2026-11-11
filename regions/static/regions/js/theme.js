
(() => {
    const form = document.getElementById("theme-form");
    const button = document.getElementById("theme-toggle");
    const status = document.getElementById("theme-status");

    if (!form || !button) return;

    function updateTheme(theme) {
        const isDark = theme === "dark";

        document.documentElement.classList.toggle("dark", isDark);

        button.setAttribute(
            "aria-label",
            isDark ? "تفعيل الوضع النهاري" : "تفعيل الوضع الليلي"
        );

        button.title = isDark ? "الوضع النهاري" : "الوضع الليلي";

        if (status) {
            status.textContent = isDark
                ? "تم تفعيل الوضع الليلي"
                : "تم تفعيل الوضع النهاري";
        }
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        if (button.disabled) return;

        button.disabled = true;

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                credentials: "same-origin",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("تعذر حفظ إعداد المظهر");
            }

            const data = await response.json();

            if (data.theme !== "dark" && data.theme !== "light") {
                throw new Error("قيمة المظهر غير صحيحة");
            }

            updateTheme(data.theme);
        } catch (error) {
            if (status) {
                status.textContent =
                    "تعذر تغيير المظهر. حاول مرة أخرى.";
            }

            console.error(error);
        } finally {
            button.disabled = false;
        }
    });
})();

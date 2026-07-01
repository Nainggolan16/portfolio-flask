document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname.replace(/\/$/, "") || "/";

    document.querySelectorAll("[data-nav-link]").forEach((link) => {
        const linkPath = new URL(link.getAttribute("href"), window.location.origin).pathname.replace(/\/$/, "") || "/";
        if (linkPath === currentPath) {
            link.classList.add("is-active");
        }
    });

    const statCards = document.querySelectorAll("[data-dashboard-count]");

    if (!statCards.length) {
        return;
    }

    const countRowsFromPage = async (endpoint) => {
        try {
            const response = await fetch(endpoint, {
                credentials: "same-origin",
            });

            if (!response.ok) {
                return 0;
            }

            const html = await response.text();
            const parser = new DOMParser();
            const documentNode = parser.parseFromString(html, "text/html");
            const tableRows = documentNode.querySelectorAll("table tr");

            return Math.max(tableRows.length - 1, 0);
        } catch (error) {
            return 0;
        }
    };

    statCards.forEach(async (card) => {
        const endpoint = card.dataset.dashboardCount;
        const valueNode = card.querySelector("[data-count-value]");

        if (!endpoint || !valueNode) {
            return;
        }

        const total = await countRowsFromPage(endpoint);
        valueNode.textContent = total.toLocaleString("id-ID");
    });
});
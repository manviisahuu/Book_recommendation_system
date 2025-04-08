document.addEventListener("DOMContentLoaded", function () {
    /** 🔹 FORM HANDLING: Fetch Book Recommendations */
    const form = document.querySelector("form");

    if (form) {
        const resultsContainer = document.createElement("div");
        resultsContainer.id = "results";
        resultsContainer.classList.add("mt-4", "p-4", "rounded", "bg-gray-100", "shadow-md");
        form.parentNode.appendChild(resultsContainer);

        form.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent page reload

            const bookName = form.querySelector("input[name='book_name']").value.trim();
            if (!bookName) {
                resultsContainer.innerHTML = `<p class="text-red-500">Please enter a book name.</p>`;
                return;
            }

            // Show loading message
            resultsContainer.innerHTML = `<p class="text-blue-500">Fetching recommendations...</p>`;

            fetch(`/recommend/?book_title=${encodeURIComponent(bookTitle)}`) // ✅ Corrected API endpoint
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP Error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    resultsContainer.innerHTML = ""; // Clear previous results

                    if (data.error) {
                        resultsContainer.innerHTML = `<p class="text-red-500">${data.error}</p>`;
                        return;
                    }

                    if (!data.recommendations || data.recommendations.length === 0) {
                        resultsContainer.innerHTML = `<p class="text-gray-600">No recommendations found.</p>`;
                        return;
                    }

                    const ul = document.createElement("ul");
                    ul.classList.add("list-disc", "ml-5", "text-gray-800");

                    data.recommendations.forEach(book => {
                        const li = document.createElement("li");
                        li.textContent = `${book.title} by ${book.author} (Similarity: ${book.similarity_score.toFixed(2)})`;
                        li.classList.add("mb-2", "hover:text-blue-500", "cursor-pointer");
                        ul.appendChild(li);
                    });

                    resultsContainer.appendChild(ul);
                })
                .catch(error => {
                    resultsContainer.innerHTML = `<p class="text-red-500">Error fetching recommendations. Please try again.</p>`;
                    console.error("Error:", error);
                });
        });
    }

    /** 🔹 DARK MODE TOGGLE */
    const darkModeToggle = document.getElementById("darkModeToggle");
    const body = document.body;

    if (darkModeToggle) {
        // Retrieve dark mode preference from localStorage
        const isDarkMode = localStorage.getItem("darkMode") === "enabled";

        if (isDarkMode) {
            body.classList.add("dark-mode");
            darkModeToggle.innerText = "Light Mode";
        }

        // Toggle dark mode on button click
        darkModeToggle.addEventListener("click", () => {
            body.classList.toggle("dark-mode");
            const newMode = body.classList.contains("dark-mode") ? "enabled" : "disabled";
            localStorage.setItem("darkMode", newMode);
            darkModeToggle.innerText = newMode === "enabled" ? "Light Mode" : "Dark Mode";
            updateExploreTextColor();
        });

        updateExploreTextColor(); // Ensure correct style on page load
    }

    /** 🔹 UPDATE EXPLORE PAGE VISIBILITY IN DARK MODE */
    function updateExploreTextColor() {
        const exploreText = document.getElementById("explore-text");
        const exploreLine = document.getElementById("explore-line");
        const exploreBtn = document.querySelector(".explore-btn");

        if (body.classList.contains("dark-mode")) {
            if (exploreText) exploreText.style.color = "#ffffff";
            if (exploreLine) exploreLine.style.borderColor = "#ffffff";
            if (exploreBtn) {
                exploreBtn.style.backgroundColor = "#444";
                exploreBtn.style.color = "white";
            }
        } else {
            if (exploreText) exploreText.style.color = "#333";
            if (exploreLine) exploreLine.style.borderColor = "#333";
            if (exploreBtn) {
                exploreBtn.style.backgroundColor = "#222";
                exploreBtn.style.color = "white";
            }
        }
    }  

    /** 🔹 SHOW LOADER ON PAGE LOAD */
    const loader = document.getElementById("loader");
    if (loader) {
        loader.classList.remove("hidden");
        setTimeout(() => {
            loader.classList.add("hidden");
        }, 1200);
    }
});




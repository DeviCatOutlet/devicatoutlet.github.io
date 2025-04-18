document.addEventListener('DOMContentLoaded', () => {
    function setupPagination(galleryContainerId, controlsContainerId, itemsPerPage) {
        console.log(`Attempting to set up pagination for ${galleryContainerId}`);
        const galleryContainer = document.getElementById(galleryContainerId);
        const controlsContainer = document.getElementById(controlsContainerId);

        if (!galleryContainer) {
            console.error(`Gallery container not found: #${galleryContainerId}`);
            return;
        }
        if (!controlsContainer) {
            console.error(`Controls container not found: #${controlsContainerId}`);
            return;
        }

        // Select all <img> tags
        const images = Array.from(galleryContainer.querySelectorAll('img'));
        const totalItems = images.length;

        if (totalItems === 0) {
            console.error(`No <img> tags found in #${galleryContainerId}. Check DOM structure.`);
            console.log(`Gallery container HTML: ${galleryContainer.outerHTML.slice(0, 200)}...`);
            return;
        }

        // Check if images are grouped in a single <p> tag
        const parentParagraphs = Array.from(galleryContainer.querySelectorAll('p'));
        if (parentParagraphs.length === 1 && parentParagraphs[0].querySelectorAll('img').length > 1) {
            console.log(`Found single <p> with ${totalItems} images. Splitting into individual <p> tags.`);
            const singleP = parentParagraphs[0];
            images.forEach(img => {
                const newP = document.createElement('p');
                singleP.parentNode.insertBefore(newP, singleP);
                newP.appendChild(img);
                console.log(`Moved img ${img.src} to new <p>`);
            });
            singleP.remove(); // Remove the original <p> if empty
        } else {
            // Ensure each <img> is wrapped in a <p> tag
            images.forEach(img => {
                if (!img.closest('p')) {
                    const p = document.createElement('p');
                    img.parentNode.insertBefore(p, img);
                    p.appendChild(img);
                    console.log(`Wrapped img in <p> for ${img.src}`);
                }
            });
        }

        // Re-select <p> tags containing images
        const items = Array.from(galleryContainer.querySelectorAll('p')).filter(p => p.querySelector('img'));
        if (items.length === 0) {
            console.error(`No <p> tags with images found after processing in #${galleryContainerId}.`);
            console.log(`Gallery container HTML: ${galleryContainer.outerHTML.slice(0, 200)}...`);
            return;
        }

        const totalPages = Math.ceil(totalItems / itemsPerPage);
        let currentPage = 1;

        function showPage(page) {
            page = Math.max(1, Math.min(page, totalPages));
            currentPage = page;

            const startIndex = (page - 1) * itemsPerPage;
            const endIndex = startIndex + itemsPerPage;

            // Hide all items
            items.forEach(item => item.classList.remove('page-item-visible'));

            // Show items for current page
            items.slice(startIndex, endIndex).forEach(item => item.classList.add('page-item-visible'));

            console.log(`Showing page ${page} for ${galleryContainerId}: items ${startIndex} to ${endIndex}`);

            renderControls();
        }

        function renderControls() {
            controlsContainer.innerHTML = '';

            if (totalPages <= 1) {
                console.log(`Only one page for ${galleryContainerId}, skipping controls`);
                return;
            }

            // Previous Button
            const prevButton = document.createElement('button');
            prevButton.textContent = 'Previous';
            prevButton.disabled = currentPage === 1;
            prevButton.addEventListener('click', () => {
                if (currentPage > 1) showPage(currentPage - 1);
            });
            controlsContainer.appendChild(prevButton);

            // Page Numbers
            for (let i = 1; i <= totalPages; i++) {
                const pageButton = document.createElement('span');
                pageButton.classList.add('page-number');
                pageButton.textContent = i;
                if (i === currentPage) {
                    pageButton.classList.add('active');
                } else {
                    pageButton.style.cursor = 'pointer';
                    pageButton.addEventListener('click', () => showPage(i));
                }
                controlsContainer.appendChild(pageButton);
            }

            // Next Button
            const nextButton = document.createElement('button');
            nextButton.textContent = 'Next';
            nextButton.disabled = currentPage === totalPages;
            nextButton.addEventListener('click', () => {
                if (currentPage < totalPages) showPage(currentPage + 1);
            });
            controlsContainer.appendChild(nextButton);

            console.log(`Rendered pagination controls for ${galleryContainerId}: ${totalPages} pages`);
        }

        console.log(`Setting up pagination for ${galleryContainerId}: ${totalItems} items, ${totalPages} pages`);
        showPage(1);
    }

    // Initialize Pagination
    const ITEMS_PER_PAGE_ART = 12;
    const ITEMS_PER_PAGE_EVENTS = 8;

    setupPagination('art-gallery-items', 'art-pagination-controls', ITEMS_PER_PAGE_ART);
    setupPagination('events-gallery-items', 'events-pagination-controls', ITEMS_PER_PAGE_EVENTS);

    // --- Gallery Popup (Lightbox) Script ---
    window.gallery = window.gallery || {};
    const galleryHeadingSelectors = ["#art", "#events", "#modeling", "#gallery"];

    galleryHeadingSelectors.forEach(headingSelector => {
        const heading = document.querySelector(headingSelector);
        if (heading) {
            let galleryContainer = heading.nextElementSibling;
            while (galleryContainer && (galleryContainer.tagName !== 'DIV' || !galleryContainer.classList.contains('paginated-gallery'))) {
                galleryContainer = galleryContainer.nextElementSibling;
            }

            if (galleryContainer) {
                galleryContainer.addEventListener('click', function(event) {
                    if (event.target.tagName === 'IMG' && event.target.closest('p')) {
                        const img = event.target;
                        const imgHash = "#" + img.src.split('/').pop().split('.')[0].replace(/[^a-zA-Z0-9_-]/g, '');

                        const openPopup = (targetImg) => {
                            document.querySelector('#popup img').src = targetImg.src;
                            document.querySelector('#popup figcaption').textContent = targetImg.alt;
                            document.documentElement.classList.add("show-modal");
                            if (history.replaceState) {
                                try {
                                    history.replaceState(null, "", imgHash);
                                } catch (e) {
                                    console.warn("Could not replace history state with hash:", imgHash, e);
                                }
                            }
                        };

                        window.gallery[imgHash] = () => openPopup(img);
                        openPopup(img);
                        event.stopPropagation();
                    }
                });

                if (window.location.hash) {
                    const potentialHash = window.location.hash;
                    galleryContainer.querySelectorAll('img').forEach(img => {
                        const imgHash = "#" + img.src.split('/').pop().split('.')[0].replace(/[^a-zA-Z0-9_-]/g, '');
                        if (imgHash === potentialHash) {
                            const openPopup = (targetImg) => {
                                document.querySelector('#popup img').src = targetImg.src;
                                document.querySelector('#popup figcaption').textContent = targetImg.alt;
                                document.documentElement.classList.add("show-modal");
                            };
                            openPopup(img);
                        }
                    });
                }
            }
        }
    });

    // --- Other UI Event Listeners ---
    document.querySelectorAll('.nav-dropdown').forEach(dropdownLink => {
        dropdownLink.addEventListener('click', function(ev) {
            document.querySelectorAll('.nav-dropdown').forEach(otherLink => {
                if (otherLink !== this) {
                    otherLink.setAttribute('aria-expanded', 'false');
                }
            });
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !isExpanded);
            ev.preventDefault();
            ev.stopPropagation();
        });
    });

    document.documentElement.addEventListener('click', function(ev) {
        let shouldCloseModal = true;
        if (ev.target.closest('#popup figure')) {
            shouldCloseModal = false;
        }
        if (shouldCloseModal && document.documentElement.classList.contains('show-modal')) {
            document.documentElement.classList.remove("show-modal");
            if (window.location.hash.length > 1 && history.replaceState) {
                try {
                    history.replaceState(null, "", window.location.pathname + window.location.search);
                } catch (e) {
                    console.warn("Could not clear history state hash.", e);
                }
            }
        }
        if (!ev.target.closest('.nav-menucontainer')) {
            document.querySelectorAll('.nav-dropdown').forEach(link => link.setAttribute('aria-expanded', 'false'));
        }
        if (!ev.target.closest("nav")) {
            const navInput = document.querySelector("nav input[type=checkbox]");
            if (navInput) navInput.checked = false;
        }
    });
});
(function () {
    "use strict";

    const navToggle = document.querySelector("[data-nav-toggle]");
    const nav = document.querySelector("[data-nav]");

    if (navToggle && nav) {
        const navLabel = navToggle.querySelector(".sr-only");
        const closeNav = () => {
            nav.classList.remove("is-open");
            navToggle.setAttribute("aria-expanded", "false");
            if (navLabel) {
                navLabel.textContent = "Open menu";
            }
        };

        navToggle.addEventListener("click", () => {
            const open = nav.classList.toggle("is-open");
            navToggle.setAttribute("aria-expanded", open ? "true" : "false");
            if (navLabel) {
                navLabel.textContent = open ? "Close menu" : "Open menu";
            }
        });

        nav.addEventListener("click", (event) => {
            if (event.target.closest("a")) {
                closeNav();
            }
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                closeNav();
            }
        });

        document.addEventListener("click", (event) => {
            if (!nav.contains(event.target) && !navToggle.contains(event.target)) {
                closeNav();
            }
        });
    }

    const fileInput = document.querySelector("[data-file-input]");
    const dropZone = document.querySelector("[data-drop-zone]");
    const preview = document.querySelector("[data-upload-preview]");
    const previewImage = document.querySelector("[data-preview-image]");
    const fileName = document.querySelector("[data-file-name]");
    let previewUrl = null;

    const showFile = (file) => {
        if (!file || !preview || !previewImage || !dropZone) {
            return;
        }
        if (previewUrl) {
            URL.revokeObjectURL(previewUrl);
        }
        previewUrl = URL.createObjectURL(file);
        previewImage.src = previewUrl;
        preview.hidden = false;
        dropZone.classList.add("has-preview");
        if (fileName) {
            fileName.textContent = file.name;
        }
    };

    if (fileInput) {
        fileInput.addEventListener("change", () => {
            const file = fileInput.files && fileInput.files[0];
            showFile(file);
        });
    }

    if (dropZone && fileInput) {
        ["dragenter", "dragover"].forEach((name) => {
            dropZone.addEventListener(name, (event) => {
                event.preventDefault();
                dropZone.classList.add("is-dragging");
            });
        });

        ["dragleave", "dragend"].forEach((name) => {
            dropZone.addEventListener(name, () => {
                dropZone.classList.remove("is-dragging");
            });
        });

        dropZone.addEventListener("drop", (event) => {
            event.preventDefault();
            dropZone.classList.remove("is-dragging");
            const files = event.dataTransfer && event.dataTransfer.files;
            if (!files || !files.length) {
                return;
            }
            try {
                fileInput.files = files;
            } catch (error) {
                return;
            }
            showFile(files[0]);
        });
    }

    const cropSelect = document.querySelector(".js-crop-select");
    const diseaseSelect = document.querySelector(".js-disease-select");

    if (cropSelect && diseaseSelect) {
        const groups = Array.from(diseaseSelect.querySelectorAll("optgroup[data-crop]"));

        const filterDiseases = () => {
            const crop = cropSelect.value;
            groups.forEach((group) => {
                const visible = !crop || group.dataset.crop === crop;
                group.hidden = !visible;
                group.disabled = !visible;
            });

            const selected = diseaseSelect.options[diseaseSelect.selectedIndex];
            if (selected && selected.parentElement && selected.parentElement.tagName === "OPTGROUP") {
                const group = selected.parentElement;
                if (group.hidden) {
                    diseaseSelect.value = "";
                }
            }
        };

        cropSelect.addEventListener("change", filterDiseases);
        filterDiseases();
    }
})();

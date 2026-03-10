/**
 * main.js – Handles form upload, AJAX submission, and result display
 */

document.addEventListener('DOMContentLoaded', () => {

    // --- Element References ---
    const form        = document.getElementById('compare-form');
    const origInput   = document.getElementById('original_form');
    const filledInput = document.getElementById('filled_form');
    const origName    = document.getElementById('original-name');
    const filledName  = document.getElementById('filled-name');
    const compareBtn  = document.getElementById('compare-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const uploadSection  = document.getElementById('upload-section');
    const resultsSection = document.getElementById('results-section');
    const resultImage    = document.getElementById('result-image');
    const summaryCard    = document.getElementById('summary-card');
    const summaryText    = document.getElementById('summary-text');
    const missingList    = document.getElementById('missing-list');
    const resetBtn       = document.getElementById('reset-btn');

    // --- File selection display ---
    origInput.addEventListener('change', () => {
        if (origInput.files.length) {
            origName.textContent = origInput.files[0].name;
            origName.classList.add('selected');
        }
        toggleCompareBtn();
    });

    filledInput.addEventListener('change', () => {
        if (filledInput.files.length) {
            filledName.textContent = filledInput.files[0].name;
            filledName.classList.add('selected');
        }
        toggleCompareBtn();
    });

    function toggleCompareBtn() {
        compareBtn.disabled = !(origInput.files.length && filledInput.files.length);
    }

    // --- Drag & Drop support ---
    ['drop-original', 'drop-filled'].forEach(id => {
        const card = document.getElementById(id);
        const input = id === 'drop-original' ? origInput : filledInput;

        ['dragenter', 'dragover'].forEach(evt => {
            card.addEventListener(evt, e => { e.preventDefault(); card.classList.add('dragover'); });
        });
        ['dragleave', 'drop'].forEach(evt => {
            card.addEventListener(evt, e => { e.preventDefault(); card.classList.remove('dragover'); });
        });

        card.addEventListener('drop', e => {
            const files = e.dataTransfer.files;
            if (files.length && files[0].type === 'application/pdf') {
                input.files = files;
                input.dispatchEvent(new Event('change'));
            }
        });
    });

    // --- Form Submission ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading state
        compareBtn.classList.add('loading');
        compareBtn.disabled = true;
        loadingOverlay.classList.add('active');

        const formData = new FormData();
        formData.append('original_form', origInput.files[0]);
        formData.append('filled_form', filledInput.files[0]);

        try {
            const response = await fetch('/compare', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok || data.error) {
                throw new Error(data.error || 'Server error');
            }

            // Populate results
            resultImage.src = data.result_image + '?t=' + Date.now(); // cache bust
            missingList.innerHTML = '';

            if (data.missing_fields && data.missing_fields.length > 0) {
                summaryCard.className = 'summary-card has-issues';
                summaryText.textContent = `${data.missing_fields.length} missing field(s) detected`;
                data.missing_fields.forEach(f => {
                    const li = document.createElement('li');
                    li.textContent = `Field #${f.id} — Location: (${f.location.x}, ${f.location.y}) — ${f.status}`;
                    missingList.appendChild(li);
                });
            } else {
                summaryCard.className = 'summary-card no-issues';
                summaryText.textContent = 'All required fields are filled!';
            }

            // Show results, hide upload
            uploadSection.style.display = 'none';
            resultsSection.style.display = 'block';

            // Add debug link if session_id available
            const debugLink = document.getElementById('debug-link');
            if (data.session_id && debugLink) {
                debugLink.href = '/debug/' + data.session_id;
                debugLink.style.display = 'inline-block';
            }

        } catch (err) {
            alert('Error: ' + err.message);
        } finally {
            compareBtn.classList.remove('loading');
            compareBtn.disabled = false;
            loadingOverlay.classList.remove('active');
        }
    });

    // --- Reset ---
    resetBtn.addEventListener('click', () => {
        resultsSection.style.display = 'none';
        uploadSection.style.display = 'block';
        form.reset();
        origName.textContent = 'No file selected';
        origName.classList.remove('selected');
        filledName.textContent = 'No file selected';
        filledName.classList.remove('selected');
        compareBtn.disabled = true;
    });
});

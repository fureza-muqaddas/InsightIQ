const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');

if (uploadZone) {
  uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('dragover'); });
  uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
  uploadZone.addEventListener('drop', e => { e.preventDefault(); uploadZone.classList.remove('dragover'); handleFile(e.dataTransfer.files[0]); });
  uploadZone.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', () => handleFile(fileInput.files[0]));
}

function handleFile(file) {
  if (!file) return;
  const progress = document.getElementById('uploadProgress');
  const fill = document.getElementById('progressFill');
  const status = document.getElementById('uploadStatus');
  progress.style.display = 'block';
  fill.style.width = '30%';
  status.textContent = 'Uploading...';

  const formData = new FormData();
  formData.append('file', file);

  fetch('/upload', { method: 'POST', body: formData })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        fill.style.width = '100%';
        status.textContent = `Uploaded! ${data.rows.toLocaleString()} rows, ${data.columns} columns`;
        setTimeout(() => window.location.href = `/analyze/${data.file_id}`, 800);
      } else {
        status.textContent = 'Error: ' + (data.error || 'Upload failed');
        fill.style.background = '#ef4444';
      }
    })
    .catch(() => { status.textContent = 'Upload failed. Try again.'; });
}

function deleteFile(fileId) {
  if (!confirm('Delete this dataset and all its analysis?')) return;
  fetch(`/delete/${fileId}`, { method: 'DELETE' })
    .then(r => r.json())
    .then(() => window.location.reload());
}
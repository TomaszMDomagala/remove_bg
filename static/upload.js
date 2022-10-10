function uploadFile() {
    const file = document.querySelector('input[type=file]').files[0];
    const name = document.querySelector('input[name="file"]').value;
    let formData = new FormData();
    let ext = file['name'].split('.')[1];
    formData.append('file', file);
    formData.set('file', file, `${name}.${ext}`);
    fetch('/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            window.location.reload();
            console.log(response);
        })
        .catch(error => {
            console.error(error);
        });
}

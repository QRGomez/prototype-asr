async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/transcribe', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();

            if (data && data.Transcription !== undefined) {
                // Display the result
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `<p>Transcription: ${data.Transcription}</p>`;
            } else {
                console.error('Unexpected API response format:', data);
            }

        } catch (error) {
            console.error('Error uploading file:', error);
        }
    } else {
        console.error('Please select a file');
    }
}
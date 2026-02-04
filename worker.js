import { pipeline } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers';

let transcriber;

async function init() {
    try {
        transcriber = await pipeline('automatic-speech-recognition', 'Xenova/whisper-tiny', {
            progress_callback: (p) => {
                if (p.status === 'progress') {
                    self.postMessage({ type: 'load', progress: p.progress });
                }
            }
        });
        self.postMessage({ type: 'ready' });
    } catch (err) {
        console.error("Worker Model Loading Error:", err);
    }
}

init();

self.onmessage = async (e) => {
    const { audio, language } = e.data;

    const options = {
        chunk_length_s: 30, // Chia nhỏ để không treo RAM
        stride_length_s: 5,
        task: 'transcribe',
        callback_function: (p) => {
            self.postMessage({ type: 'update', progress: Math.round(p.progress || 0) });
        }
    };

    if (language !== 'auto') options.language = language;

    try {
        const result = await transcriber(audio, options);
        self.postMessage({ type: 'complete', text: result.text.trim() });
    } catch (err) {
        console.error("Transcription Error:", err);
        self.postMessage({ type: 'complete', text: "Lỗi xử lý file âm thanh." });
    }
};

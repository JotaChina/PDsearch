document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('image-container');
    const image = document.getElementById('zoom-image');

    if (!container || !image) {
        console.error('Container or image not found');
        return;
    }

    let isDragging = false;
    let scale = 1;
    let offsetX = 0, offsetY = 0;
    let startX = 0, startY = 0;
    let initialX = 0, initialY = 0;

    // Calcula o fator de zoom inicial para ajustar a imagem ao contêiner
    function calculateInitialZoom() {
        const containerRect = container.getBoundingClientRect();
        const imageRect = image.getBoundingClientRect();
        const scaleX = containerRect.width / imageRect.width;
        const scaleY = containerRect.height / imageRect.height;
        scale = Math.min(scaleX, scaleY);
        updateTransform();
    }

    function updateTransform() {
        image.style.transform = `translate(${initialX}px, ${initialY}px) scale(${scale})`;
    }

    function logImageDimensions() {
        if (image.complete) {
            console.log(`Image dimensions: ${image.naturalWidth}x${image.naturalHeight}`);
            calculateInitialZoom(); // Calcula o zoom inicial depois que a imagem é carregada
        } else {
            image.addEventListener('load', () => {
                console.log(`Image dimensions: ${image.naturalWidth}x${image.naturalHeight}`);
                calculateInitialZoom(); // Calcula o zoom inicial depois que a imagem é carregada
            });
        }
    }

    container.addEventListener('wheel', (event) => {
        event.preventDefault();
        const delta = event.deltaY < 0 ? 1.1 : 0.9; // Inverte a direção do zoom para corresponder ao comportamento esperado
        const rect = container.getBoundingClientRect();
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;
        scale *= delta;
        scale = Math.min(Math.max(1, scale), 10); // Limita o zoom entre 1x e 10x

        // Recalcula a posição para manter o ponto onde o mouse estava
        initialX -= (mouseX - initialX) * (delta - 1);
        initialY -= (mouseY - initialY) * (delta - 1);

        updateTransform();
    });

    container.addEventListener('mousedown', (event) => {
        event.preventDefault();
        if (image) {
            isDragging = true;
            const rect = image.getBoundingClientRect();
            startX = event.clientX;
            startY = event.clientY;
            offsetX = (startX - rect.left - image.clientLeft) / scale;
            offsetY = (startY - rect.top - image.clientTop) / scale;
            container.style.cursor = 'grabbing';
        }
    });

    container.addEventListener('mousemove', (event) => {
        if (isDragging && image) {
            const dx = event.clientX - startX;
            const dy = event.clientY - startY;
            initialX += dx;
            initialY += dy;
            startX = event.clientX;
            startY = event.clientY;
            updateTransform();
        }
    });

    container.addEventListener('mouseup', () => {
        isDragging = false;
        container.style.cursor = 'grab';
    });

    container.addEventListener('mouseleave', () => {
        isDragging = false;
        container.style.cursor = 'grab';
    });

    // Suporte para dispositivos de toque
    container.addEventListener('touchstart', (event) => {
        if (event.touches.length === 1) {
            const touch = event.touches[0];
            isDragging = true;
            const rect = image.getBoundingClientRect();
            startX = touch.clientX;
            startY = touch.clientY;
            offsetX = (startX - rect.left - image.clientLeft) / scale;
            offsetY = (startY - rect.top - image.clientTop) / scale;
            container.style.cursor = 'grabbing';
        }
    }, { passive: false });

    container.addEventListener('touchmove', (event) => {
        if (isDragging && image) {
            const touch = event.touches[0];
            const dx = touch.clientX - startX;
            const dy = touch.clientY - startY;
            initialX += dx;
            initialY += dy;
            startX = touch.clientX;
            startY = touch.clientY;
            updateTransform();
        }
    }, { passive: false });

    container.addEventListener('touchend', () => {
        isDragging = false;
        container.style.cursor = 'grab';
    });

    // Inicializa a transformação e log das dimensões
    logImageDimensions();
});


document.addEventListener('DOMContentLoaded', function () {
    const svgUrl = window.svgUrl; // Obtém a URL do SVG definida no HTML

    function loadSVG(url) {
        return fetch(url)
            .then(response => response.text())
            .then(data => {
                const parser = new DOMParser();
                return parser.parseFromString(data, 'image/svg+xml');
            });
    }

    loadSVG(svgUrl).then(svgDoc => {
        const svgElement = svgDoc.querySelector('svg');
        const svgContainer = document.getElementById('image-container');
        
        // Remove o SVG existente (se houver) antes de adicionar o novo
        const existingSVG = svgContainer.querySelector('svg');
        if (existingSVG) {
            svgContainer.removeChild(existingSVG);
        }

        svgContainer.appendChild(svgElement);

        // Adiciona um evento de clique para as linhas da tabela
        document.querySelectorAll('.clickable-row').forEach(row => {
            row.addEventListener('click', function () {
                const type = this.getAttribute('data-type');
                const x = parseFloat(this.getAttribute('data-x'));
                const y = parseFloat(this.getAttribute('data-y'));

                // Adiciona o círculo vermelho ao SVG
                addRedCircleToSVG(x, y);
            });
        });

        function addRedCircleToSVG(x, y) {
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', x);
            circle.setAttribute('cy', y);
            circle.setAttribute('r', 10); // Tamanho do círculo
            circle.setAttribute('fill', 'red');

            svgElement.appendChild(circle);
        }
    }).catch(error => {
        console.error('Error loading SVG:', error);
    });
});


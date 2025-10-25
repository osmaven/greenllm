document.addEventListener('DOMContentLoaded', () => {
    const iframe = document.getElementById('content-frame');
    const links = document.querySelectorAll('.sidebar a');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const src = e.target.getAttribute('data-src');
            console.log('Link clicked:', src); // Debugging line
            if (src) {
                iframe.src = src;
            }
        });
    });
});

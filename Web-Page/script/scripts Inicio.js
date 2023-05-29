function cambiarPestana(event) {
    event.preventDefault();
    var url = event.target.getAttribute('href');
    window.location.href = url;
  }
  
function abrirNuevaPestana(event) {
    event.preventDefault();
    var url = event.target.getAttribute('href');
    window.open(url, '_blank');
}
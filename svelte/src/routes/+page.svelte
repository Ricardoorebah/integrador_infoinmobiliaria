<script>
  function redirectToFilteredPage() {
    console.log('Redirigiendo a /busqueda');
    window.location.href = '/busqueda';
  }
</script>

<style>
  main {
    text-align: center; /* Alinea el contenido al centro */
    margin-top: 50px;   /* Agrega espacio sobre el botón */
  }

  p {
    font-size: 18px;    /* Ajusta el tamaño del texto de la reseña */
    margin-bottom: 20px; /* Agrega espacio bajo la reseña */
  }

  button {
    padding: 8px 16px;   /* Ajusta el espacio dentro del botón */
    font-size: 14px;     /* Ajusta el tamaño del texto del botón */
    width: 150px;        /* Ajusta el ancho del botón */
    margin: 0 auto;      /* Centra el botón horizontalmente */
  }
</style>

<main>
  <h1>Prototipo Sistema integrador de oferta inmobiliaria para la región de Los Lagos.</h1>
  <p>En este prototipo se presentan propiedades de 3 sitios: Usatusubsidio, Toctoc.com y Toppropiedades.</p>
  <p>Al clickear el botón, se redirecciona al sitio donde se pueden realizar búsquedas de propiedades por filtros.</p>
  <button on:click={redirectToFilteredPage}>Ir a búsqueda por filtros</button>
</main>

<script>
  export let img;
  export let url_origen;
  export let nombre;
  export let valor;
  export let dormitorios;
  export let baños;
  export let superficie;
  export let comuna;
  export let region;
  export let tipoPropiedad;
  export let tipoFinanciamiento;

  // Función para extraer el nombre del dominio
  function getDomainName(url) {
    const match = url.match(/:\/\/(www[0-9]?\.)?(.[^/:]+)/i);
    if (match != null && match.length > 2 && typeof match[2] === 'string' && match[2].length > 0) {
      return match[2];
    } else {
      return null;
    }
  }

  const domainName = getDomainName(url_origen);
</script>

<main class="property">
  <div class="image-container">
    <img src={img} alt="imagen referencial" />
  </div>
  <div class="info-container">
    <h1>{nombre}</h1>
    <p>
      Revisar en sitio de origen: 
      <a href={url_origen} target="_blank" rel="noopener noreferrer">
        {domainName}
      </a>
    </p>
    <p>Valor: {valor} UF</p>
    <p>Número de dormitorios: {dormitorios}</p>
    <p>Número de baños: {baños}</p>
    <p>Superficie: {superficie} m²</p>
    <p>Comuna: {comuna}</p>
    <p>Tipo de propiedad: {tipoPropiedad}</p>
    <p>Tipo de financiamiento: {tipoFinanciamiento}</p>
  </div>
</main>

<style>
  .property {
    display: flex;
    margin: 10px 0;
    border: 1px solid #ffffff; /* Color y grosor del borde */
    padding: 10px; /* Espaciado interno */
  }

  .image-container {
    width: 30%; /* Ajusta el ancho de la imagen */
  }

  .image-container img {
    width: 100%;
    height: auto;
  }

  .info-container {
    flex-grow: 1;
    margin-left: 10px;
    color: #333; 
  }

  p {
    margin: 5px 0;
  }

  h1 {
    margin: 0;
  }

  a {
    color: #f5f5f5; /* Color del enlace */
    text-decoration: underline; /* Subrayado del enlace */
    cursor: pointer;
  }
</style>


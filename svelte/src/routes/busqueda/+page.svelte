<script>
  import { onMount, afterUpdate } from 'svelte';
  import { navigate } from 'svelte-routing';
  import { writable } from 'svelte/store';
  import Property from '../../components/property.svelte';
  import Navbar from '../../components/navbar.svelte';

  const data = writable(null);
  const API_URL = 'http://localhost:8000';

  let selectedMinValor = undefined;
  let selectedMaxValor = undefined;
  let selectedComuna = undefined;
  let selectedDormitorios = undefined;  

  let propertysJson = [];
  let comunas = [
    'Ancud',
    'Castro',
    'Chonchi',
    'Curaco de Vélez',
    'Dalcahue',
    'Puqueldón',
    'Queilén',
    'Quemchi',
    'Quellón',
    'Quinchao',
    'Calbuco',
    'Cochamó',
    'Fresia',
    'Frutillar',
    'Llanquihue',
    'Los Muermos',
    'Maullín',
    'Puerto Montt',
    'Puerto Varas',
    'Osorno',
    'Puerto Octay',
    'Purranque',
    'Puyehue',
    'Río Negro',
    'San Juan de la Costa',
    'San Pablo',
    'Chaitén',
    'Futaleufú',
    'Hualaihué',
    'Palena'
  ];

  let currentPage = 1;
  const propertiesPerPage = 6;

  const minValores = [0, 600, 1100, 1600, 2200];
  const maxValores = [2700, 3200, 3700, 4200, 4700, 5200, 6200];

  const dormitoriosOptions = [1, 2, 3, 4, 5, 6];

  // Función llama a todo de la API
  onMount(async () => {
    const res = await fetch(`${API_URL}/get_all`);
    const apiData = await res.json();
    data.set(apiData);
    propertysJson = apiData;
  });

  let sortOrder = 'asc'; // Valor por defecto: de menor a mayor

  function handleSortOrderChange() {
    getFiltered(); // Llama a getFiltered al cambiar la opción de orden
  }

  function getFiltered() {
    let lista_filtrada = $data.filter(item => (
      (!selectedMinValor || item.valor >= selectedMinValor) &&
      (!selectedMaxValor || item.valor <= selectedMaxValor) &&
      (!selectedDormitorios || item.dormitorios === selectedDormitorios) &&
      (!selectedComuna || item.comuna === selectedComuna)
    ));

    // Ordenar según sortOrder
    lista_filtrada = lista_filtrada.sort((a, b) => {
      if (sortOrder === 'asc') {
        return a.valor - b.valor;
      } else {
        return b.valor - a.valor;
      }
    });
    
    propertysJson = lista_filtrada;
    currentPage = 1; // Reiniciar a la primera página después de aplicar filtros
  }

  function getAll() {
    propertysJson = $data;
    currentPage = 1; // Reiniciar a la primera página al mostrar todos
  }

  // Función para actualizar la URL
  function updateURL() {
    navigate(`${window.location.pathname}?page=${currentPage}`);
  }

  // Llamada inicial para establecer la URL al cargar la página
  onMount(() => {
    updateURL();
  });

  function nextPage() {
    currentPage += 1;
    updateURL();
  }

  function prevPage() {
    currentPage -= 1;
    updateURL();
  }

  afterUpdate(() => {
    // Actualizar la URL después de cambiar de página
    updateURL();
  });

  $: paginatedProperties = propertysJson.slice(
    (currentPage - 1) * propertiesPerPage,
    currentPage * propertiesPerPage
  );

  $: totalPages = Math.ceil(propertysJson.length / propertiesPerPage);
</script>

<Navbar />

<main class="container">
  <h1>Búsqueda Filtrada de Propiedades</h1>
  <div class="filter-bar">
    <label>
      Valor Mínimo UF:
      <select bind:value={selectedMinValor}>
        <option value={undefined}>Seleccionar valor mínimo</option> 
        {#each minValores as valor}
          <option value={valor}>{valor}</option>
        {/each}
      </select>
    </label>
    <label>
      Valor Máximo UF:
      <select bind:value={selectedMaxValor}>
        <option value={undefined}>Seleccionar valor máximo</option> 
        {#each maxValores as valor}
          <option value={valor}>{valor}</option>
        {/each}
      </select>
    </label>
    <label>
      Dormitorios:
      <select bind:value={selectedDormitorios}>
        <option value={undefined}>Seleccionar número de dormitorios</option> 
        {#each dormitoriosOptions as dormitorio}
          <option value={dormitorio}>{dormitorio}</option>
        {/each}
      </select>
    </label>
    <label>
      Comuna:
      <select bind:value={selectedComuna}>
        <option value={undefined}>Seleccionar comuna</option> 
        {#each comunas as comuna (comuna)}
          <option value={comuna}>{comuna}</option>
        {/each}
      </select>
    </label>
    <button on:click={getFiltered}>Buscar</button>
    

    <div class="sort-order">
      <label>
        Ordenar:
        <select bind:value={sortOrder} on:change={handleSortOrderChange}>
          <option value="asc">De menor a mayor</option>
          <option value="desc">De mayor a menor</option>
        </select>
      </label>
    </div>
  </div>

  <div class="flexbox">
    {#each paginatedProperties as el (el._id)}
      <Property
        img={el.img_ref}
        nombre={el.nombre}
        url_origen={el.url_origen}
        valor={el.valor}
        dormitorios={el.dormitorios}
        baños={el.baños}
        superficie={el.superficie}
        comuna={el.comuna}
        region={el.region}
        tipoPropiedad={el.tipo_propiedad}
        tipoFinanciamiento={el.tipo_financiamiento}
      />
    {/each}
  </div>

  <div class="pagination">
    <button on:click={prevPage} disabled={currentPage === 1}>Anterior</button>
    {#if totalPages <= 7}
      {#each Array.from({ length: totalPages }) as _, page}
        <button on:click={() => currentPage = page + 1} class:active={currentPage === page + 1}>{page + 1}</button>
      {/each}
    {:else}
      {#if currentPage <= 4}
        {#each Array.from({ length: 5 }) as _, page}
          <button on:click={() => currentPage = page + 1} class:active={currentPage === page + 1}>{page + 1}</button>
        {/each}
        <span>...</span>
        <button on:click={() => currentPage = totalPages} class:active={currentPage === totalPages}>{totalPages}</button>
      {:else if currentPage >= totalPages - 3}
        <button on:click={() => currentPage = 1} class:active={currentPage === 1}>{1}</button>
        <span>...</span>
        {#each Array.from({ length: 5 }) as _, page}
          <button on:click={() => currentPage = totalPages - 4 + page} class:active={currentPage === totalPages - 4 + page}>{totalPages - 4 + page}</button>
        {/each}
      {:else}
        <button on:click={() => currentPage = 1} class:active={currentPage === 1}>{1}</button>
        <span>...</span>
        {#each Array.from({ length: 3 }) as _, page}
          <button on:click={() => currentPage = currentPage - 1 + page} class:active={currentPage === currentPage - 1 + page}>{currentPage - 1 + page}</button>
        {/each}
        <span>...</span>
        <button on:click={() => currentPage = totalPages} class:active={currentPage === totalPages}>{totalPages}</button>
      {/if}
    {/if}
    <button on:click={nextPage} disabled={currentPage * propertiesPerPage >= propertysJson.length}>Siguiente</button>
  </div>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin:20px;
    margin-left: 100px;
    background-image: url('old-blueprint-background-texture-technical-600nw-284571158.webp'); 
    background-repeat: repeat;
    color: #000000; 
    
  }

  .flexbox {
    display: flex;
    flex-wrap: wrap;
  }

  .container {
    margin: 20px;
  }

  .filter-bar {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
  }

  .filter-bar label {
    display: flex;
    flex-direction: column;
  }

  .filter-bar select,
  .filter-bar button {
    padding: 5px;
    font-size: 16px;
  }

  .filter-bar button {
    max-width: 100px; 
    width: 20; 
  }

  .pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
  }

  .pagination button {
    padding: 5px 10px; 
    font-size: 14px;  
    max-width: 80px;  
    width: auto; 
  }
  .sort-order {
    margin-top: 10px;
  }
</style>

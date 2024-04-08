<script>
    import { Router, Route } from 'svelte-routing';
    import Index from './routes/+page.svelte'; 
    import Filtered from './routes/busqueda/+page.svelte'; 
    import Help from './routes/ayuda/+page.svelte';
    
  </script>
  
  <Router>
    <Route path="/" component={Index} />
    <Route path="/busqueda" component={Filtered} />
    <Route path="/ayuda" component={Help} />

  </Router>
  
  <style>
  
  </style>
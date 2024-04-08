
import App from './App.svelte';
import { createHashHistory } from 'svelte-routing';

const history = createHashHistory();

const app = new App({
  target: document.body,
  props: {
    router: history,
  },
});

export default app;

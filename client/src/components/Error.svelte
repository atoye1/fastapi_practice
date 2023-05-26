<script>
  import { fade } from "svelte/transition";
  export let error;
</script>

{#if typeof error.detail === "string"}
  <div
    in:fade={{ duration: 500 }}
    out:fade={{ duration: 500 }}
    class="alert alert-danger"
    role="alert"
    style="transition: opacity 1s;"
  >
    <ul>
      <li>{error.detail}</li>
    </ul>
  </div>
{:else if typeof error.detail === "object" && error.detail.length > 0}
  <div
    in:fade={{ duration: 500 }}
    out:fade={{ duration: 500 }}
    class="alert alert-danger"
    role="alert"
    style="transition: opacity 1s;"
  >
    {#each error.detail as err, i}
      <div>
        <string>{err.loc[1]}</string>:{err.msg}
      </div>
    {/each}
  </div>
{/if}

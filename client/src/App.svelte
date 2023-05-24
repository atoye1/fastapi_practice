<script>
  async function hello() {
    const res = await fetch("http://127.0.0.1:8000/hello");
    const json = await res.json();

    if (res.ok) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(json.message);
        }, 2000);
      });
    } else {
      alert("error");
    }
  }
  // let message;
  fetch("http://127.0.0.1:8000/hello")
    .then((response) => response.json())
    .then((json) => {
      message = json.message;
    });
  let promise = hello();
</script>

{#await promise}
  <p>...waiting</p>
{:then message}
  <h1>{message}</h1>
{/await}

<script>
  import { push } from "svelte-spa-router";
  import fastapi from "../lib/api";
  import Error from "../components/Error.svelte";
  import { access_token, username, is_login } from "../lib/store";

  let error = { detail: [] };
  let login_username = "";
  let login_password = "";

  async function login(event) {
    event.preventDefault();
    let url = "/api/user/login";
    let params = {
      username: login_username,
      password: login_password,
    };
    try {
      const response = await fastapi("login", url, params);
      const responseBody = await response.json();
      $access_token = responseBody.access_token;
      $username = responseBody.username;
      $is_login = true;
      push("/");
    } catch (err) {
      console.log("error", err.message);
      error = JSON.parse(err.message);
      setTimeout(() => (error = { detail: [] }), 5000);
    }
  }
</script>

<div class="container">
  <h3 class="my-3 border-bottom pb-2">로그인</h3>
  <Error {error} />
  <form method="post">
    <div class="mb-3">
      <label for="username">사용자 이름</label>
      <input
        type="text"
        class="form-control"
        id="username"
        bind:value={login_username}
      />
    </div>
    <div class="mb-3">
      <label for="username">비밀번호</label>
      <input
        type="password"
        class="form-control"
        id="password"
        bind:value={login_password}
      />
    </div>
    <button type="submit" class="btn btn-primary" on:click={login}
      >로그인</button
    >
  </form>
</div>

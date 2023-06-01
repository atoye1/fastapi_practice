<script>
  import { push } from "svelte-spa-router";
  import fastapi from "../lib/api";
  import Error from "../components/Error.svelte";
  let parsedError = { detail: [] };
  let subject = "";
  let content = "";

  async function post_question() {
    let url = "/api/question/create";
    let params = {
      subject: subject,
      content: content,
    };
    try {
      await fastapi("post", url, params);
      push("/");
    } catch (error) {
      console.log("error", error.message);
      parsedError = JSON.parse(error.message);
      setTimeout(() => (parsedError = { detail: [] }), 1000);
    }
  }
</script>

<div class="container">
  <h5 class="my-3 border-bottom pb2">질문등록</h5>
  <Error error={parsedError} />
  <div class="mb-3">
    <label for="subject" class="form-label">제목</label>
    <input type="text" class="form-control" id="subject" bind:value={subject} />
  </div>
  <div class="mb-3">
    <label for="content" class="form-label">내용</label>
    <textarea
      rows="10"
      class="form-control"
      id="content"
      bind:value={content}
    />
  </div>
  <button
    type="button"
    class="btn btn-primary"
    on:click|preventDefault={post_question}>등록하기</button
  >
</div>

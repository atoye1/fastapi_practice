<script>
  import fastapi from "../lib/api";
  import Error from "../components/Error.svelte";

  export let params = {};

  let question_id = params.question_id;
  let question = { answers: [] };
  let content = "";
  let parsedError = { detail: [] };

  async function get_question() {
    const response = await fastapi(
      "get",
      "/api/question/detail/" + question_id
    );
    question = await response.json();
  }
  get_question();

  async function post_answer() {
    let url = "/api/answer/create/" + question_id;
    let params = {
      content: content,
    };
    try {
      await fastapi("post", url, params);
    } catch (error) {
      console.log("error", error.message);
      parsedError = JSON.parse(error.message);
      setTimeout(() => (parsedError = { detail: [] }), 1000);
    }
    await get_question();
    content = "";
  }
</script>

<div class="container my-3">
  <!-- 질문 -->
  <h2 class="border-bottom py-2">{question.subject}</h2>
  <div class="card my-3">
    <div class="card-body">
      <div class="card-text" style="white-space: pre-line;">
        {question.content}
      </div>
      <div class="d-flex justify-content-end">
        <div class="badge bg-light text-dark p-2">
          {question.create_date}
        </div>
      </div>
    </div>
  </div>
  <!-- 답변 목록 -->
  <h5 class="border-bottom my-3 py-2">
    {question.answers.length}개의 답변이 있습니다.
  </h5>
  {#each question.answers as answer}
    <div class="card my-3">
      <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">
          {answer.content}
        </div>
        <div class="d-flex justify-content-end">
          <div class="badge bg-light text-dark p-2">
            {answer.create_date}
          </div>
        </div>
      </div>
    </div>
  {/each}
  <!-- 답변 등록 -->
  <Error error={parsedError} />
  <form method="post" class="my-3">
    <div class="mb-3">
      <textarea rows="10" bind:value={content} class="form-control" />
    </div>
    <input
      type="submit"
      value="답변등록"
      class="btn btn-primary"
      on:click|preventDefault={post_answer}
    />
  </form>
</div>
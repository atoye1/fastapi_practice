<script>
  import fastapi from "../lib/api";
  import Error from "../components/Error.svelte";
  import { push, link } from "svelte-spa-router";
  import moment from "moment/min/moment-with-locales";
  import { is_login, username } from "../lib/store";
  import { marked } from "marked";
  moment.locale("ko");

  export let params = {};

  let question_id = params.question_id;
  let question = { answers: [], voter: [], content: "" };
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
      setTimeout(() => (parsedError = { detail: [] }), 5000);
    }
    await get_question();
    content = "";
  }

  async function delete_question() {
    if (window.confirm("정말로 삭제하시겠습니까?")) {
      let url = "/api/question/delete";
      let params = {
        question_id: question_id,
      };
      try {
        const response = await fastapi("delete", url, params);
        push("/");
      } catch (error) {
        parsedError = JSON.parse(error.message);
        setTimeout(() => (parsedError = { detail: [] }), 5000);
      }
    }
  }

  async function modify_answer(answer) {
    if (answer.modifyMode === undefined || answer.modifyMode === false) {
      answer.modifyMode = true;
      question.answers = [...question.answers];
    } else {
      let url = "/api/answer/update";
      let params = {
        id: answer.id,
        content: answer.content,
      };
      try {
        const response = await fastapi("put", url, params);
      } catch (error) {
        parsedError = JSON.parse(error.message);
        setTimeout(() => (parsedError = { detail: [] }), 5000);
      } finally {
        answer.modifyMode = false;
        question.answers = [...question.answers];
      }
    }
  }

  async function delete_answer(answer) {
    if (window.confirm("정말로 삭제하시겠습니까?")) {
      let url = "/api/answer/delete";
      let params = {
        answer_id: answer.id,
      };
      console.log("params", params);
      try {
        const response = await fastapi("delete", url, params);
        await get_question();
      } catch (error) {
        parsedError = JSON.parse(error.message);
        setTimeout(() => (parsedError = { detail: [] }), 5000);
      }
    }
    return;
  }

  async function vote_question(question_id) {
    if (window.confirm("정말 추천하시겠습니까?")) {
      let url = "/api/question/vote";
      let params = {
        question_id: question_id,
      };
      try {
        const result = await fastapi("post", url, params);
        get_question();
      } catch (error) {
        parsedError = JSON.parse(error.message);
        setTimeout(() => (parsedError = { detail: [] }), 5000);
      }
    }
  }

  async function vote_answer(answer_id) {
    if (window.confirm("정말 추천하시겠습니까?")) {
      let url = "/api/answer/vote";
      let params = {
        answer_id: answer_id,
      };
      try {
        const result = await fastapi("post", url, params);
        get_question();
      } catch (error) {
        parsedError = JSON.parse(error.message);
        setTimeout(() => (parsedError = { detail: [] }), 5000);
      }
    }
  }
</script>

<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css"
/>

<div class="container my-3">
  <!-- 질문 -->
  <h2 class="border-bottom py-2">{question.subject}</h2>
  <div class="card my-3">
    <div class="card-body">
      <div class="card-text" style="white-space: pre-line;">
        {@html marked.parse(question.content)}
      </div>
      <div class="d-flex justify-content-end">
        {#if question.modify_date}
          <div class="badge bg-light text-dark p-2 text-start mx-3">
            <div class="mb-2">modified at</div>
            <div>
              {moment(question.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}
            </div>
          </div>
        {/if}

        <div class="badge bg-light text-dark p-2 text-start">
          <div class="mb-2">
            {question.user ? question.user.username : ""}
          </div>
          <div>
            {moment(question.create_date).format("YYYY-MM-DD hh:mm a")}
          </div>
        </div>
      </div>
      <div class="my-3">
        <button
          class="btn btn-sm btn-outline-primary"
          on:click={() => vote_question(question.id)}
        >
          추천 <span class="badge rounded-pill bg-success"
            >{question.voter.length}</span
          >
        </button>
        {#if question.user && $username === question.user.username}
          <a
            use:link
            href="/question-modify/{question.id}"
            class="btn btn-sm btn-outline-secondary">수정</a
          >
          <button
            class="btn btn-sm btn-outline-danger"
            on:click={delete_question}>삭제</button
          >
        {/if}
      </div>
    </div>
  </div>
  <button
    class="btn btn-secondary"
    on:click={() => {
      push("/");
    }}>목록으로</button
  >
  <!-- 답변 목록 -->
  <h5 class="border-bottom my-3 py-2">
    {question.answers.length}개의 답변이 있습니다.
  </h5>
  {#each question.answers as answer}
    <div class="card my-3">
      <div class="card-body">
        {#if answer.modifyMode}
          <textarea bind:value={answer.content} class="form-control" />
        {:else}
          <div class="card-text" style="white-space: pre-line;">
            {@html marked.parse(answer.content)}
          </div>
        {/if}
        <div class="d-flex justify-content-end">
          {#if answer.modify_date}
            <div class="badge bg-light text-dark p-2 text-start mx-3">
              <div class="mb-2">modified at</div>
              <div>
                {moment(answer.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}
              </div>
            </div>
          {/if}
          <div class="badge bg-light text-dark p-2 text-start">
            <div class="mb-2">
              {answer.user ? answer.user.username : ""}
            </div>
            <div>
              {moment(answer.create_date).format("YYYY-MM-DD hh:mm a")}
            </div>
            <button
              class="btn btn-sm btn-outline-primary"
              on:click={() => {
                vote_answer(answer.id);
              }}
              >추천<span class="badge rounded-pill bg-secondary mx-1"
                >{answer.voter.length}</span
              ></button
            >
            {#if answer.user && $username === answer.user.username}
              <button
                class="btn btn-sm btn-outline-secondary"
                on:click={() => modify_answer(answer)}
              >
                수정
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                on:click={() => delete_answer(answer)}
              >
                삭제
              </button>
            {/if}
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
      class="btn btn-primary {$is_login ? '' : 'disabled'}"
      on:click|preventDefault={post_answer}
    />
  </form>
</div>

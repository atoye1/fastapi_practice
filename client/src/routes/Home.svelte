<script>
  import fastapi from "../lib/api";
  import { link } from "svelte-spa-router";
  import { page, is_login, keyword } from "../lib/store";
  import moment from "moment/min/moment-with-locales";
  moment.locale("ko");

  let question_list = [];
  let size = 10;
  let total = 0;
  let kw = "";

  $: total_page = Math.ceil(total / size);
  $: page_range = $page - ($page % 10);

  async function getQuestionList() {
    let params = {
      page: $page,
      size: size,
      keyword: $keyword,
    };
    const response = await fastapi("get", "/api/question/list", params);
    const responseBody = await response.json();
    question_list = responseBody.question_list;
    total = responseBody.total;
    kw = $keyword;
  }
  $: $page, $keyword, getQuestionList();
</script>

<div class="container my-3">
  <div class="row my-3 justify-content-between">
    <div class="d-flex col-6">
      <div>
        <a
          use:link
          href="/question-create"
          class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a
        >
      </div>
    </div>
    <div class="d-flex col-6 justify-content-between">
      <form
        class="w-75"
        on:submit={() => {
          ($keyword = kw), ($page = 0);
        }}
      >
        <div class="input-group">
          <input type="text" class="form-control" bind:value={kw} />
          <button type="submit" class="btn btn-outline-secondary">찾기</button>
        </div>
      </form>
    </div>
  </div>
  <table class="table">
    <thead>
      <tr class="text-center table-dark">
        <th>번호</th>
        <th style="width:50%">제목</th>
        <th>글쓴이</th>
        <th>작성일시</th>
      </tr>
    </thead>
    <tbody>
      {#each question_list as question, i}
        <tr class="text-center">
          <td>{total - $page * size - i}</td>
          <td class="text-start">
            <a use:link href="/detail/{question.id}">{question.subject}</a>
            {#if question.answers.length > 0}
              <span class="text-danger small mx-2">
                {question.answers.length}
              </span>
            {/if}
          </td>
          <td>{question.user ? question.user.username : ""}</td>
          <td>{moment(question.create_date).format("YYYY-MM-DD hh:mm a")}</td>
        </tr>
      {/each}
    </tbody>
  </table>
  <ul class="pagination justify-content-center">
    <li class="page-item {$page === 0 && 'disabled'}">
      <button class="page-link" on:click={() => getQuestionList(0)}>처음</button
      >
    </li>
    <li class="page-item {$page === 0 && 'disabled'}">
      <button class="page-link" on:click={() => $page--}>이전</button>
    </li>
    {#each Array(total_page) as _, loop_page}
      {#if loop_page >= page_range && loop_page <= page_range + 9}
        <li class="page-item {$page === loop_page && 'active'}">
          <button class="page-link" on:click={() => ($page = loop_page)}
            >{loop_page + 1}</button
          >
        </li>
      {/if}
    {/each}
    <li class="page-item {$page === total_page - 1 && 'disabled'}">
      <button class="page-link" on:click={() => $page++}>다음</button>
    </li>
    <li class="page-item {$page === total_page - 1 && 'disabled'}">
      <button class="page-link" on:click={() => ($page = total_page - 1)}
        >끝</button
      >
    </li>
    <li class="page-item {$page === total_page - 1 && 'disabled'}">
      <input class="page-link" type="number" bind:value={$page} />
    </li>
  </ul>
</div>

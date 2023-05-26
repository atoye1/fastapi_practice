<script>
  import fastapi from "../lib/api";
  import { link } from "svelte-spa-router";
  import { page } from "../lib/store";
  import moment from "moment/min/moment-with-locales";
  moment.locale("ko");

  let question_list = [];
  let size = 10;
  let total = 0;

  $: total_page = Math.ceil(total / size);
  $: page_range = $page - ($page % 10);

  async function getQuestionList(_page) {
    let params = {
      page: _page,
      size: size,
    };
    const response = await fastapi("get", "/api/question/list", params);
    const responseBody = await response.json();
    question_list = responseBody.question_list;
    total = responseBody.total;
    $page = _page;
  }
  getQuestionList($page);
  $: getQuestionList($page);
</script>

<div class="container my-3">
  <table class="table">
    <thead>
      <tr class="table-dark">
        <th>번호</th>
        <th>제목</th>
        <th>작성일시</th>
      </tr>
    </thead>
    <tbody>
      {#each question_list as question, i}
        <tr>
          <td>{total - $page * size - i}</td>
          <td>
            <a use:link href="/detail/{question.id}">{question.subject}</a>
            {#if question.answers.length > 0}
              <span class="text-danger small mx-2">
                {question.answers.length}
              </span>
            {/if}
          </td>
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
      <button class="page-link" on:click={() => getQuestionList($page - 1)}
        >이전</button
      >
    </li>
    {#each Array(total_page) as _, loop_page}
      {#if loop_page >= page_range && loop_page <= page_range + 9}
        <li class="page-item {$page === loop_page && 'active'}">
          <button class="page-link" on:click={() => getQuestionList(loop_page)}
            >{loop_page + 1}</button
          >
        </li>
      {/if}
    {/each}
    <li class="page-item {$page === total_page - 1 && 'disabled'}">
      <button class="page-link" on:click={() => getQuestionList($page + 1)}
        >다음</button
      >
    </li>
    <li class="page-item {$page === total_page - 1 && 'disabled'}">
      <button class="page-link" on:click={() => getQuestionList(total_page - 1)}
        >끝</button
      >
    </li>
    <li class="page-item {$page === total_page - 1 && 'disabled'}">
      <input
        class="page-link"
        type="number"
        bind:value={$page}
        on:change={() => getQuestionList($page - 1)}
      />
    </li>
  </ul>
  <a use:link href="/question-create" class="btn btn-primary">질문 등록하기</a>
</div>

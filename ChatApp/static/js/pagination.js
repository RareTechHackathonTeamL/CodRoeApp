/*
チャンネル一覧ページでレスポンスが返ってきた後、
チャンネル一覧の配列データをもとにページネーションの作成・制御をする
*/

import { initCreateChannelModal } from "/static/js/channels/create-channel.js";
import { initDeleteChannelModal } from "/static/js/channels/delete-channel.js";

const deleteChannelModal = document.getElementById("delete-channel-modal");

/*
ページネーションを作成・制御する関数。
チャンネル名、削除ボタンを作成・制御。
*/
const pagination = () => {
  try {
    let page = 1; // 今何ページ目にいるか
    const STEP = 6; // ステップ数（1ページに表示する項目数）

    // 全ページ数を計算
    // 「チャンネルの総数/(割る)ステップ数」の余りの有無で場合分け
    // 余りがある場合は１ページ余分に追加する
    const TOTAL =
      channels.length % STEP == 0
        ? channels.length / STEP
        : Math.floor(channels.length / STEP) + 1;

    // ページネーションで表示されるページ数部分（< PREV 1 2 3 NEXT >）の要素を作成
    const paginationUl = document.querySelector(".pagination");
    let pageCount = 0;
    while (pageCount < TOTAL) {
      let pageNumber = document.createElement("li");
      pageNumber.dataset.pageNum = pageCount + 1;
      pageNumber.innerText = pageCount + 1;
      paginationUl.appendChild(pageNumber);
      // ページネーションの数字部分が押された時にもページが変わるように処理
      pageNumber.addEventListener("click", (e) => {
        const targetPageNum = e.target.dataset.pageNum;
        page = Number(targetPageNum);
        init(page, STEP);
      });
      pageCount++;
    }

    // 各チャンネル名と削除ボタンの要素を作成
    const createChannelsList = (page, STEP) => {
      const ul = document.querySelector(".channel-box");
      // 一度チャンネルリストを空にする
      ul.innerHTML = "";

      const firstChannelInPage = (page - 1) * STEP + 1;
      const lastChannelInPage = page * STEP;

      // 各チャンネル要素の作成
      channels.forEach((channel, i) => {
        if (i < firstChannelInPage - 1 || i > lastChannelInPage - 1) return;
        const a = document.createElement("a");
        const li = document.createElement("li");
        const channelURL = `/channels/${channel.id}/messages`;
        a.innerText = channel.name;
        a.setAttribute("href", channelURL);
        li.appendChild(a);

        // もしチャンネル作成者uidと自分のuidが同じだった場合は削除ボタンを追加
        if (uid === channel.uid) {
          const deleteButton = document.createElement("button");
          deleteButton.innerHTML =
            '<ion-icon name="trash-bin-outline" style="color: #f57978"></ion-icon>';
          deleteButton.classList.add("delete-button");
          li.appendChild(deleteButton);
          // ゴミ箱ボタンが押された時にdeleteモーダルを表示させる
          deleteButton.addEventListener("click", () => {
            deleteChannelModal.style.display = "flex";

            const deleteChannelForm =
              document.getElementById("deleteChannelForm");

            const endpoint = `/channels/delete/${channel.id}`;
            deleteChannelForm.action = endpoint;
          });
        }

        // もしチャンネルに説明文が登録されていたら吹き出しを作成（hover時に表示される）
        if (channel.abstract) {
          const channelDescriptionTooltip = document.createElement("div");
          channelDescriptionTooltip.style.display = "innerBlock";
          channelDescriptionTooltip.classList.add(
            "channel-description-tooltip"
          );
          channelDescriptionTooltip.appendChild(li);
          const tooltipBody = document.createElement("div");
          tooltipBody.classList.add("tooltip-body");
          tooltipBody.innerHTML = channel.abstract;
          channelDescriptionTooltip.appendChild(tooltipBody);
          ul.appendChild(channelDescriptionTooltip);
        } else {
          // チャンネルに説明文が登録されていない場合はツールチップなしでulにliを追加する
          ul.appendChild(li);
        }
      });
      // チャンネル追加ボタンを付け加える
      const createChannelButton = document.createElement("ion-icon");
      createChannelButton.id = "create-channel-button";
      createChannelButton.name = "add-circle-outline";
      createChannelButton.style = "color: #122543";
      ul.appendChild(createChannelButton);
    };
    // ページネーション内で現在選択されているページの番号に色を付ける
    const colorPaginationNum = () => {
      // ページネーションの数字部分の全要素から"colored"クラスを一旦取り除く
      const paginationArr = [...document.querySelectorAll(".pagination li")];
      paginationArr.forEach((page) => {
        page.classList.remove("colored");
      });
      // 選択されているページにclass="colored"を追加（文字色が変わる）
      paginationArr[page - 1].classList.add("colored");
    };

    const init = (page, STEP) => {
      createChannelsList(page, STEP);
      colorPaginationNum();
      initCreateChannelModal();
      initDeleteChannelModal();
    };
    // 初期動作時に1ページ目を表示
    init(page, STEP);

    // 前ページ遷移
    document.getElementById("prev").addEventListener("click", () => {
      if (page <= 1) return;
      page = page - 1;
      init(page, STEP);
    });

    // 次ページ遷移
    document.getElementById("next").addEventListener("click", () => {
      if (page >= channels.length / STEP) return;
      page = page + 1;
      init(page, STEP);
    });

    return true;
  } catch (error) {
    console.log(`エラー：${error}`);
    return false;
  }
};

// DOMツリーが構築されたらpagination関数を発火（ページネーションを作成し、その後チャンネル追加ボタンを作成・表示）
document.addEventListener("DOMContentLoaded", function () {
  try {
    pagination();
  } catch (error) {
    console.log(`エラー：${error}`);
  }
});

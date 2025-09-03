
// モーダルを表示する関数
function openModal() {
    // id="myModal" の要素を取得して display を "flex" に変更
    // これによりモーダルが画面に表示される
    document.getElementById("myModal").style.display = "flex";
}

// モーダルを非表示にする関数
function closeModal() {
    // id="myModal" の要素を取得して display を "none" に変更
    // これによりモーダルが閉じられる
    document.getElementById("myModal").style.display = "none";
}

// 背景クリックで閉じる
window.onclick = function (event) {
    const modal = document.getElementById("myModal");
    if (event.target === modal) {
        closeModal();
    }
};

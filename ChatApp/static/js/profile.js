
function openModal() {
    document.getElementById("myModal").style.display = "flex";
}
function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

// 背景クリックで閉じる
window.onclick = function (event) {
    const modal = document.getElementById("myModal");
    if (event.target === modal) {
        closeModal();
    }
};

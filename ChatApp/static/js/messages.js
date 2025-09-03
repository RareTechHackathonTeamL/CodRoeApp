

document.addEventListener("DOMContentLoaded", function () {
    const messagesContainer = document.querySelector('main.messages');
    const chatInputForm = document.getElementById('chatInputForm');

    // ------------------------
    // スクロール関数
    // ------------------------
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // 初期表示でスクロール
    scrollToBottom();

    // ------------------------
    // メッセージ時間の変換
    // ------------------------
    function formatMessageTime() {
        document.querySelectorAll('.message-time').forEach(span => {
            const dateStr = span.textContent.trim();
            if (dateStr) {
                const utcStr = dateStr.replace(" ", "T") + "Z";
                const date = new Date(utcStr);
                if (!isNaN(date.getTime())) {
                    const hours = String((date.getUTCHours() + 9) % 24).padStart(2, '0');
                    const minutes = String(date.getUTCMinutes()).padStart(2, '0');
                    span.textContent = `${hours}:${minutes}`;
                }
            }
        });
    }
    formatMessageTime();

    // ------------------------
    // 削除ボタン設定
    // ------------------------
    function setupDeleteButtons() {
        const userMessages = document.querySelectorAll(".message.right");
        userMessages.forEach((msg) => {
            const deleteBtn = msg.querySelector(".slide-delete-btn");
            const deleteForm = msg.querySelector(".delete-form");

            if (!deleteBtn) return;

            msg.addEventListener("click", function (e) {
                e.stopPropagation();
                document.querySelectorAll(".slide-delete-btn").forEach((btn) => {
                    if (btn !== deleteBtn) btn.classList.add("hidden");
                    if (btn !== deleteBtn) btn.parentElement.querySelector(".message-box").style.transform = "translateX(0)";
                });
                deleteBtn.classList.toggle("hidden");
                msg.querySelector(".message-box").style.transform = deleteBtn.classList.contains("hidden") ? "translateX(0)" : "translateX(-50px)";
            });

            deleteBtn.addEventListener("click", function (e) {
                e.stopPropagation();
                fetch(deleteForm.action, { method: "POST", headers: { "X-Requested-With": "XMLHttpRequest" }, body: "" })
                    .then(res => { if (res.ok) msg.remove(); else alert("削除に失敗しました。"); })
                    .catch(err => { console.error(err); alert("削除中にエラーが発生しました。"); });
            });
        });

        document.addEventListener("click", function () {
            userMessages.forEach((msg) => {
                const btn = msg.querySelector(".slide-delete-btn");
                if (btn && !btn.classList.contains("hidden")) {
                    btn.classList.add("hidden");
                    msg.querySelector(".message-box").style.transform = "translateX(0)";
                }
            });
        });
    }
    setupDeleteButtons();

    // ------------------------
    // スタンプ設定
    // ------------------------
    const stampToggle = document.getElementById("stampToggle");
    const stampClose = document.getElementById("stampClose");
    const stampList = document.getElementById("stampList");
    const stamps = document.querySelectorAll(".stamp-item");

    stampToggle.addEventListener("click", (e) => {
        e.stopPropagation();
        stampList.classList.toggle("hidden");
        chatInputForm.style.display = stampList.classList.contains("hidden") ? "flex" : "none";
    });

    stampClose.addEventListener("click", (e) => {
        e.stopPropagation();
        stampList.classList.add("hidden");
        chatInputForm.style.display = "flex";
    });

    stamps.forEach(stamp => {
        stamp.addEventListener("click", (e) => {
            e.stopPropagation();
            document.getElementById('stampInput').value = stamp.dataset.stampId;
            document.getElementById('stampForm').submit();
            stampList.classList.add("hidden");
            chatInputForm.style.display = "flex";
        });
    });

    document.addEventListener("click", (e) => {
        if (!stampList.contains(e.target) && e.target !== stampToggle) {
            stampList.classList.add("hidden");
            chatInputForm.style.display = "flex";
        }
    });

    // ------------------------
    // ページ読み込み後に下スクロール
    // ------------------------
    window.scrollTo(0, messagesContainer.scrollHeight);

});

// ------------------------
// モーダル制御
// ------------------------
function openModal() { document.getElementById("myModal").style.display = "flex"; }
function closeModal() { document.getElementById("myModal").style.display = "none"; }

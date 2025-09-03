const elements = document.getElementsByName("chat_type");
const openForm = document.getElementById("openForm");
const groupForm = document.getElementById("groupForm");
const privateForm = document.getElementById("privateForm");
const openDiv = document.getElementById("open_div");
const groupDiv = document.getElementById("group_div");
const privateDiv = document.getElementById("private_div");

openForm.style.display = "block";
groupForm.style.display = "none";
privateForm.style.display = "none";
openDiv.classList.add("checked");

const checkRadio = () => {
    let checkValue = "";
    for (let i = 0; i < elements.length; i++) {
        if (elements.item(i).checked) {
            checkValue = elements.item(i).value;
        }
    }
    if (checkValue == "open") {
        openForm.style.display = "block";
        groupForm.style.display = "none";
        privateForm.style.display = "none";
        openDiv.classList.add("checked");
        groupDiv.classList.remove("checked");
        privateDiv.classList.remove("checked");
    } else if (checkValue == "group") {
        openForm.style.display = "none";
        groupForm.style.display = "block";
        privateForm.style.display = "none";
        openDiv.classList.remove("checked");
        groupDiv.classList.add("checked");
        privateDiv.classList.remove("checked");
    } else if (checkValue == "private") {
        openForm.style.display = "none";
        groupForm.style.display = "none";
        privateForm.style.display = "block";
        openDiv.classList.remove("checked");
        groupDiv.classList.remove("checked");
        privateDiv.classList.add("checked");
    }
};
const addForm = () => {
    const input_data = document.createElement("input");
    input_data.type = "text";
    input_data.name = "friends_name";
    input_data.classList.add("chat-name");
    input_data.classList.add("member-add-list");
    const parent = document.getElementById("add_member_form");
    parent.appendChild(input_data);
};

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
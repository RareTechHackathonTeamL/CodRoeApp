const addForm = () => {
    const input_data = document.createElement("input");
    input_data.type = "text";
    input_data.name = "friends_name";
    input_data.classList.add("h3-box");
    input_data.classList.add("member-add-list");
    const parent = document.getElementById("add_member_form");
    parent.appendChild(input_data);
};
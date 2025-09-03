
document.getElementById("icon_file").addEventListener("change", function (e) {
    const file = e.target.files[0];
    if (file) {
        document.getElementById("fileName").textContent = file.name;
    } else {
        document.getElementById("fileName").textContent = "";
    }
});

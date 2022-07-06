btn = document.getElementById("btn_search")
tbl = document.getElementById("table")
btn.addEventListener("click", () => {
    fetch(`/students/search/42`).then(data => data.json()).then(data => console.log(data["students"]))
})


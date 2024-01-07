function isCheckboxChecked() {
    // console.log($('div[name="chk"] :checkbox:checked').length >0)
    if ($('div[name="chk"] :checkbox:checked').length >0)
    {
        return true
    }
    else{
        alert("Choose atleast one option.")
        return false
    }
}

function rangeB() {
const value = document.querySelector("#value");
    const input = document.querySelector("#range_bar");
    value.textContent = input.value;
    input.addEventListener("input", (event) => {
      value.textContent = event.target.value;
    });}
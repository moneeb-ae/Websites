// Sidebar toggle
function openNav() {
    document.getElementById("mySidebar").classList.add("open");
    document.getElementById("main").style.marginLeft = "30%";
}

function closeNav() {
    document.getElementById("mySidebar").classList.remove("open");
    document.getElementById("main").style.marginLeft = "0";
}

// Calculator logic
const display = document.getElementById("display");

function appendToDisplay(input) {
    display.value += input;
}

function clearDisplay() {
    display.value = "";
}

function calculate() {
    try {
        display.value = eval(display.value);
    } catch (error) {
        display.value = "Invalid";
    }
}

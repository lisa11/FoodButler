//http://www.randomsnippets.com/2008/02/12/how-to-hide-and-show-your-div/

function toggle() {
    var ele = document.getElementById("toggleText");
    var text = document.getElementById("displayText");
    if(ele.style.display == "block") {
            ele.style.display = "none";
        text.innerHTML = "show ingredients";
    }
    else {
        ele.style.display = "block";
        text.innerHTML = "hide ingredients";
    }
} 

//http://www.w3schools.com/jsref/prop_style_visibility.asp
function hideElem() {
    document.getElementById("myP").style.visibility = "hidden";
}

function showElem() {
    document.getElementById("myP").style.visibility = "visible";
}



function getAnswer(q){

let lang = document.getElementById("lang").value

let semester = new URLSearchParams(window.location.search).get('semester')
let subject = new URLSearchParams(window.location.search).get('subject')
let unit = new URLSearchParams(window.location.search).get('unit')

window.location =
`/answer?q=${q}&semester=${semester}&subject=${subject}&unit=${unit}&lang=${lang}`

}
function reloadAnswer(q){
getAnswer(q)
}

function goBack(){
history.back()
}
function updateSubjects() {

    var semester = document.getElementById("semester").value;
    var subject = document.getElementById("subject");

    subject.innerHTML = "";

    if (semester == "5") {
        subject.innerHTML += "<option>Theory of Computation</option>";
        subject.innerHTML += "<option>Database Management Systems</option>";
        subject.innerHTML += "<option>Pattern Recognition</option>";
        subject.innerHTML += "<option>Internet and Web Technology</option>";
    }

    if (semester == "6") {
        subject.innerHTML += "<option>Machine Learning</option>";
        subject.innerHTML += "<option>Computer Network</option>";
        subject.innerHTML += "<option>Compiler Design</option>";
        subject.innerHTML += "<option>Project Management</option>";
    }
}

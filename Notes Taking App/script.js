var noteTemplate = document.getElementsByClassName("note")[0];
noteTemplate.remove();

var noNotesCreated = true;

function removeTemplateNotesMessage(){ document.getElementsByTagName("h2")[0].remove(); }

function addNote(status, message){
    var clone = noteTemplate.cloneNode(true);
    clone.getElementsByTagName("p")[0].innerText = status;
    clone.getElementsByTagName("pre")[0].innerHTML = message;
    console.log(clone);
    document.getElementById("notes").prepend((clone));
}

function getStatusFromDate(d){
    var time = "";
    if(d.getHours() < 12){
        time += String.prototype.concat(d.getHours(), ":");
        if(d.getMinutes() < 10){
            time += String.prototype.concat("0", d.getMinutes());
        } else {
            time += d.getMinutes();
        }
        time += " am";
    } else {
        time += String.prototype.concat(d.getHours() - 12, ":");
        if(d.getMinutes() < 10){
            time += String.prototype.concat("0", d.getMinutes());
        } else {
            time += d.getMinutes();
        }
        time += " pm";
    }
    return String.prototype.concat("Created at ", time, " on ", d.getDate(), "/", d.getMonth() + 1, "/", d.getFullYear(), ":");
}

function noteSubmitted(){
    var m = document.getElementsByTagName("textarea")[0].value;
    console.log(m);
    if(noNotesCreated){
        document.getElementsByTagName("h2")[0].remove();
        noNotesCreated = false;
    }
    addNote(getStatusFromDate(new Date()), m);
}

var date = new Date();


//addNote(getStatusFromDate(date), "this is a testing of notes");


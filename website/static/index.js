//creating a function to delete notes
function deleteNote(noteId) {
    //creating a request using fetch to delete-note.
    //stringify will convert the coming data from views to string
    fetch('/delete-note', {
        method: 'POST', 
        body: JSON.stringify({ noteId: noteId})
    }).then((_res) => {
        //after deleting notes redirect to home page.
        window.location.href = "/";
    });
}
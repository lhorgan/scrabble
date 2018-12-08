function buildBoard() {
    let elem = "<table>";

    for(let i = 0; i < 15; i++) {
        elem += "<tr>";
        for(let j = 0; j < 15; j++) {
            elem += "<td><input type='text' /></td>";
        }
        elem += "</tr>";
    }
    elem += "</table>";

    return elem;
}
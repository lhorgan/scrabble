function buildBoard() {
    let elem = "<table>";
    let boardValues = getBoardValues();

    for(let i = 0; i < 15; i++) {
        elem += "<tr>";
        for(let j = 0; j < 15; j++) {
            elem += "<td><input type='text' maxlength='1' id='" + ("t-"+i+"-"+j) + "' class='" + boardValues[i][j] + " square'/></td>";
        }
        elem += "</tr>";
    }
    elem += "</table>";

    return elem;
}

function getBoardValues() {
    board =[['TW', 'ST', 'ST', 'DL', 'ST', 'ST', 'ST', 'TW', 'ST', 'ST', 'ST', 'DL', 'ST', 'ST', 'TW'],
            ['ST', 'DW', 'ST', 'ST', 'ST', 'TL', 'ST', 'ST', 'ST', 'TL', 'ST', 'ST', 'ST', 'DW', 'ST'],
            ['ST', 'ST', 'DW', 'ST', 'ST', 'ST', 'DL', 'ST', 'DL', 'ST', 'ST', 'ST', 'DW', 'ST', 'ST'],
            ['DL', 'ST', 'ST', 'DW', 'ST', 'ST', 'ST', 'DL', 'ST', 'ST', 'ST', 'DW', 'ST', 'ST', 'DL'],
            ['ST', 'ST', 'ST', 'ST', 'DW', 'ST', 'ST', 'ST', 'ST', 'ST', 'DW', 'ST', 'ST', 'ST', 'ST'],
            ['ST', 'TL', 'ST', 'ST', 'ST', 'TL', 'ST', 'ST', 'ST', 'TL', 'ST', 'ST', 'ST', 'TL', 'ST'],
            ['ST', 'ST', 'DL', 'ST', 'ST', 'ST', 'DL', 'ST', 'DL', 'ST', 'ST', 'ST', 'DL', 'ST', 'ST'],
            ['TW', 'ST', 'ST', 'DL', 'ST', 'ST', 'ST', 'ST', 'ST', 'ST', 'ST', 'DL', 'ST', 'ST', 'TW'],
            ['ST', 'ST', 'DL', 'ST', 'ST', 'ST', 'DL', 'ST', 'DL', 'ST', 'ST', 'ST', 'DL', 'ST', 'ST'],
            ['ST', 'TL', 'ST', 'ST', 'ST', 'TL', 'ST', 'ST', 'ST', 'TL', 'ST', 'ST', 'ST', 'TL', 'ST'],
            ['ST', 'ST', 'ST', 'ST', 'DW', 'ST', 'ST', 'ST', 'ST', 'ST', 'DW', 'ST', 'ST', 'ST', 'ST'],
            ['DL', 'ST', 'ST', 'DW', 'ST', 'ST', 'ST', 'DL', 'ST', 'ST', 'ST', 'DW', 'ST', 'ST', 'DL'],
            ['ST', 'ST', 'DW', 'ST', 'ST', 'ST', 'DL', 'ST', 'DL', 'ST', 'ST', 'ST', 'DW', 'ST', 'ST'],
            ['ST', 'DW', 'ST', 'ST', 'ST', 'TL', 'ST', 'ST', 'ST', 'TL', 'ST', 'ST', 'ST', 'DW', 'ST'],
            ['TW', 'ST', 'ST', 'DL', 'ST', 'ST', 'ST', 'TW', 'ST', 'ST', 'ST', 'DL', 'ST', 'ST', 'TW']];

    return board;
}

function serializeBoard() {
    board = [];
    for(let i = 0; i < 15; i++) {
        board.push([]);
        for(let j = 0; j < 15; j++) {
            board[i].push("*");
        }
    }

    for(let i = 0; i < 15; i++) {
        for(let j = 0; j < 15; j++) {
            let id = "t-"+i+"-"+j;
            let val = $("#" + id).val();
            if(val != "" && val != " ") {
                board[i][j] = val;
            }
        }
    }

    return board;
}

function requestMove() {
    let data = {"board": serializeBoard(),
                "tiles": $("#tiles").val()};
    console.log(data);
    $.ajax({
        dataType: "json",
        type: "post",
        contentType: 'application/json;charset=UTF-8',
        url: "/requestmove",
        data: JSON.stringify(data),
        success: (res) => {
            console.log(res);
            let word = res["word"];
            let row = res["row"];
            let col= res["col"];
            let horiz = res["horiz"];
            
            for(let i = 0; i < word.length; i++) {
                let cellID = "t-" + row + "-" + col;
                $("#" + cellID).val(word[i]);
                if(horiz) {
                    col++;
                }
                else {
                    row++;
                }
            }
        }
    });
}
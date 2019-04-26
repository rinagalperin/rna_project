function isChecked(element) {
    return document.getElementById(element).checked;
}

function controlOutput(show, area){
    if(show){
        document.getElementById(area).removeAttribute("hidden");
    }
    else{
        document.getElementById(area).setAttribute("hidden", "true");
    }
}

$(document).ready(function () {
   console.log('page is loaded');
   onSeedButtonClick();
   onDwnJsonButtonClick();
   onDwnCsvButtonClick();
   onDwnFastaButtonClick();
   onDwnHtmlButtonClick();
   onDwnTreeButtonClick();
});

function onSeedButtonClick(){
    $('#seed_btn').click(function (event) {
        event.preventDefault();
        let input = $('#seed').val();
        getData(input);
    })
}

function onDwnJsonButtonClick(){
    $('#dwn_json_btn').click(function (event) {
        event.preventDefault();
        let seed = $('#seed').val();
        let json_data = $('#jsonTextArea').val();
        download(json_data, "BioMir_json_"+seed, "txt");
    })
}

function onDwnCsvButtonClick(){
    $('#dwn_csv_btn').click(function (event) {
        event.preventDefault();
        let seed = $('#seed').val();
        let csv_data = $('#csvTextArea').val();
        download(csv_data, "BioMir_"+seed, "csv");
    })
}

function onDwnTreeButtonClick(){
    $('#dwn_tree_btn').click(function (event) {
        event.preventDefault();
        let seed = $('#seed').val();
        let tree_data = $('#treeTextArea').val();
        download(tree_data, "BioMir_"+seed, "PNG");
    })
}

function onDwnHtmlButtonClick(){
    $('#dwn_html_btn').click(function (event) {
        event.preventDefault();
        let seed = $('#seed').val();
        let tree_data = $('#htmlTextArea').html();
        download(tree_data, "BioMir_"+seed, "txt");
    })
}

// TODO: allow downloading the result as image
function onDwnFastaButtonClick(){
    $('#dwn_fasta_btn').click(function (event) {
        event.preventDefault();
        let seed = $('#seed').val();
        let fasta_data = $('#fastaTextArea').val();
        download(fasta_data, "BioMir_fasta_"+seed, "PNG");
    })
}

function getData(input) {
    $.ajax({
        method: "GET",
        url: "get_data/" + input
    }).done(function (data) {
        //$('#graph-pic').attr("src","../static/pics/" + seedInput.url + ".png");
        //$('#graph-pic').attr(seedInput.url);
        //$("#graph-pic").append(document.createTextNode(data));

        if(isChecked("json")){
            // show json text area
            controlOutput(true, "jsonArea");
            // parse json result
            let textedJson = JSON.stringify(JSON.parse(data), undefined, 4);
            // display result in text area
            $('#jsonTextArea').text(textedJson);
        }else{
            controlOutput(false, "jsonArea");
        }
        /*
        if(isChecked("csv")){
            csvOutput(true);
            jsonToCsv(data);
        }else{
            csvOutput(false);
        }
        */

        if(isChecked("fasta")){
            controlOutput(true, "fastaArea");
            jsonToFasta(data)
        }else{
            controlOutput(false, "fastaArea");
        }

        if(isChecked("tree")){
            controlOutput(true, "treeArea");
            jsonToTree(data);
        }else{
            controlOutput(false, "treeArea");
        }

        if(isChecked("html")){
            controlOutput(true, "htmlArea");
            jsonToHtml(data);
        }else{
            controlOutput(false, "htmlArea");
        }
    });
}

function download(data, filename, type) {
    let file = new Blob([data], {type: type});
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        let a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    }
}

function jsonToCsv(json_input){
    $.ajax({
        method: "GET",
        url: "json_to_csv/" + json_input
    }).done(function (result) {
        console.log(result);
        $('#csvTextArea').text(result);
    });
}

function jsonToFasta(json_input){
    $.ajax({
        method: "GET",
        url: "json_to_fasta/" + json_input
    }).done(function (result) {
        $('#fastaTextArea').text(result);
    });
}

function jsonToHtml(json_input){
    $.ajax({
        method: "GET",
        url: "json_to_html/" + json_input
    }).done(function (result) {
        $('#htmlTextArea').html(result);
    });
}

function jsonToTree(json_input){
    $.ajax({
        method: "GET",
        url: "json_to_tree/" + json_input
    }).done(function (result) {
        // result: our tree in newick format (string object)
        // TODO: convert the newick to phyloxml and pass it on instead of 'data' (the uri)
    	let uri = "/static/ViewModel/rina.xml";
    	$.get(uri, function(data) {
            let dataObject = {
                phyloxml: data,     // If using phyloXML, need to tell us - or else we assume it is Newick
                fileSource: true    // Need to indicate that it is from a file for us to process it correctly
            };

            // TODO: not duplicate graph visual on page if clicking "SEARCH" again...
            let phylocanvas = new Smits.PhyloCanvas(
                dataObject,     // Newick or XML string
                'treeTextArea',    // Div Id where to render
                1000, 1000,     // Height, Width in pixels
                'circular'      // Type of tree
            );
        });
    });
}
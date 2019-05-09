let tree_dwn_path = "";
let organism_three_p_five_p_count = {};

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
        download(tree_dwn_path, "BioMir_"+seed, "image/svg+xml;charset=utf-8");
    })
}

function onDwnHtmlButtonClick(){
    $('#dwn_html_btn').click(function (event) {
        event.preventDefault();
        let seed = $('#seed').val();
        let tree_data = $('#htmlTextArea').html();
        download(tree_data, "BioMir_"+seed, "text/html");
    })
}

function onDwnFastaButtonClick(){
    $('#dwn_fasta_btn').click(function (event) {
        event.preventDefault();
        let seed = $('#seed').val();
        let fasta_data = $('#fastaTextArea').val();
        download(fasta_data, "BioMir_fasta_"+seed+'.fa', "text/fa");
    })
}

function getData(input) {
    $.ajax({
        method: "GET",
        url: "get_data/" + input
    }).done(function (data) {
        if(data === '-1'){
            alert("Seed sequence does not exist! \n Please verify you have entered a valid seed or family name \n and try again.")
        }else {
            // construct output page title of seed sequence + family name
            let user_input = $('#seed').val().toLowerCase();
            let other_name = data.split('$')[1];
            let result_title = '';
            if(user_input.includes('-')){
                result_title = 'seed sequence: ' + other_name.toUpperCase() + ', family name: ' + user_input.toLowerCase();
            }else{
                result_title = 'seed sequence: ' + user_input.toUpperCase() + ', family name: ' + other_name.toLowerCase();
            }
            $('#result_title').text(result_title);

            data = data.split('$')[0];

            // ------------------------------------
            // gather 3p/5p count per organism:
            let seed = Object.keys(JSON.parse(data))[0];
            let organisms_json = JSON.parse(data)[seed];
            // iterate over all organisms
            Object.keys(organisms_json).forEach(function(organism) {
                let matures_json = organisms_json[organism];
                let count_of_3p = 0;
                let count_of_5p = 0;
                // iterate over all matures of the organism
                Object.keys(matures_json).forEach(function(mature_key) {
                    //let mature = mature_key;
                    let three_p_five_p = matures_json[mature_key]['mature 3p or 5p'];
                    // increase count of relevant type of mature sequence
                    three_p_five_p === '3p' ? count_of_3p++ : count_of_5p++;
                });

                // result example:
                // Homo sapiens: "2$8"
                // meaning: Homo sapiens organism has 2 matures of type 3p with the given seed,
                // and 8 matures of type 5p with the given seed.
                organism_three_p_five_p_count[organism] = count_of_3p + '$' + count_of_5p;
            });

            // ------------------------------------

            if (isChecked("json")) {
                // show json text area
                controlOutput(true, "jsonArea");
                // parse json result
                let textedJson = JSON.stringify(JSON.parse(data), undefined, 4);

                // display result in text area
                $('#jsonTextArea').text(textedJson);
            } else {
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

            if (isChecked("fasta")) {
                controlOutput(true, "fastaArea");
                jsonToFasta(data)
            } else {
                controlOutput(false, "fastaArea");
            }

            if (isChecked("tree")) {
                $('#treeTextArea').empty(); // avoid multiple graphs (one *below* the other)
                controlOutput(true, "treeArea");
                jsonToTree(data);
            } else {
                controlOutput(false, "treeArea");
            }

            if (isChecked("html")) {
                controlOutput(true, "htmlArea");
                jsonToHtml(data);
            } else {
                controlOutput(false, "htmlArea");
            }
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

// function jsonToCsv(json_input){
//     $.ajax({
//         method: "GET",
//         url: "json_to_csv/" + json_input
//     }).done(function (result) {
//         console.log(result);
//         $('#csvTextArea').text(result);
//     });
// }

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
    }).done(function (relevant_organisms) {
        // result: our tree in newick format (string object)
    	let uri = "/static/ViewModel/evolutionary_tree.xml";
    	$.get(uri, function(data) {
    	    var relevant_organisms_arr = relevant_organisms.split(',');
    	    var temp_xml = edit_graph(data, relevant_organisms_arr);

            let dataObject = {
                phyloxml: temp_xml,     // If using phyloXML, need to tell us - or else we assume it is Newick
                fileSource: false    // Need to indicate that it is from a file for us to process it correctly
            };

            // TODO: not duplicate graph visual on page if clicking "SEARCH" again...
            let phylocanvas = new Smits.PhyloCanvas(
                dataObject,     // Newick or XML string
                'treeTextArea',    // Div Id where to render
                1000, 1000,     // Height, Width in pixels
                'circular'      // Type of tree
            );

            tree_dwn_path = phylocanvas.getSvgSource();  // Put SVG source into the svgSource variable
    	});
    });
}

function edit_graph(xmlFile, relevant_organisms){
    var xmlString = new XMLSerializer().serializeToString(xmlFile);
    var updated_bg_colors = xmlString.replace(
        /<name>/g,
        '<name bgStyle="nonorganisms">').replace(
            /<\/name>/g, '</name><chart><component>other</component><content>0</content></chart>'
    );

    // color all relevant organisms w/ different color & add group mark & bar chart
    for(var i in relevant_organisms){
        var organism_with_count = relevant_organisms[i].replace(',','').replace(' ', '').replace(/'/g, '');
        var count = parseInt(organism_with_count.match(/\d+$/)[0]);

        var organism = organism_with_count.replace(String(count), '');
        var longer_count = count * 10;

        var full_name = getOrganismFullName(organism);

        relevant_organisms[i] = organism;

        var original =
            '<name bgStyle="nonorganisms">' + organism + '</name>' +
            '<chart>' +
            '<component>other</component>' +
            '<content>0</content>' +
            '</chart>';

        var count_of_3p = organism_three_p_five_p_count[full_name].split('$')[0];
        var count_of_5p = organism_three_p_five_p_count[full_name].split('$')[1];

        var full_name_hover =
            '<annotation><desc>' +
            full_name +
            '\n number of matures: ' +
            count +
            '\n #3p: ' +
            count_of_3p +
            '\n #5p: ' +
            count_of_5p +
            '</desc><uri>http://en.wikipedia.org/wiki/' +
            full_name +
            '</uri></annotation>';

        var outer_group_mark = '<chart><component>base</component><content>' + longer_count + '</content></chart>';
        var updated = '<name bgStyle="organisms">' + organism + '</name>' + full_name_hover + outer_group_mark;

        updated_bg_colors = updated_bg_colors.replace(original, updated);
    }

    return updated_bg_colors;
}

function getOrganismFullName(short_name){
    var response = '';
     $.ajax({
        type: "GET",
        url: 'get_organism_full_name/' + short_name,
         async: false,
        success: function(result) {
            response = result;
        },
        error: function() {
            alert('Error occured');
        }
    });

     return response;
}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}
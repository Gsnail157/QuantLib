document.getElementById("add").addEventListener("click", ()=> {
    let rows = document.getElementById("rows");
    let row = document.createElement("div");

    let ticker = document.createElement("label");
    let weight = document.createElement("label");
    let data_source = document.createElement("label");

    let ticker_input = document.createElement("input");
    let weight_input = document.createElement("input");
    let data_source_input = document.createElement("select");

    ticker.textContent = "Ticker: ";
    weight.textContent = " Weight: ";
    data_source.textContent = " Data Source:  ";

    ticker_input.type = "text";
    weight_input.type = "number";

    ticker_input.className = "ticker";
    weight_input.className = "weight";
    data_source_input.className = "optionMenu";

    ticker_input.name = "ticker";
    weight_input.name = "weight";
    data_source_input.name = "optionMenu";

    let sources = ["--Please choose an option--", "Alpha Vantage", "Bloomberg", "Yahoo Finance"]

    for (let source of sources){
        let opt = document.createElement("option");
        opt.value = source;
        opt.textContent = source;
        data_source_input.append(opt);
    }

    // Delete button
    let delete_button = document.createElement("button");
    delete_button.onclick = ()=> {
        row.remove();
    }
    delete_button.textContent = "Delete Row";

    // Putting it together
    ticker.append(ticker_input);
    weight.append(weight_input);
    data_source.append(data_source_input);
    data_source.append(delete_button);

    row.append(ticker);
    row.append(weight);
    row.append(data_source);

    rows.append(row);
});

function delete_row(button) {
    let row = button.parentElement.parentElement;
    row.remove();
};

document.getElementById("calculate").addEventListener("click", ()=> {
    console.log(getRowValues());
});

function getRowValues() {
    let tickers = document.getElementsByClassName("ticker");
    let weights = document.getElementsByClassName("weight");
    let data_sources = document.getElementsByClassName("optionMenu");

    let row_values = [];

    for (let i = 0; i < tickers.length; i++){
        row_values.push({
            ticker: tickers[i].value,
            weight: weights[i].value,
            source: data_sources[i].value
        });
    };
    return row_values;
};
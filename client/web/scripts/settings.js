function openConfig() {
    document.querySelector(
        "section.config"
    ).style.display = "flex";
    document.querySelector(
        "section.overlay"
    ).style.display = "flex";
}
function closeConfig(justConfig = false) {
    document.querySelector(
        "section.config"
    ).style.display = "none";
    if (!justConfig) {
        document.querySelector(
            "section.overlay"
        ).style.display = "none";
    }
}
function setDisplay(query, value) {
    document.querySelector(
        query
    ).style.display = value;
}
function removeAllActiveSettings() {
    document.querySelectorAll(
        "#settings ul.nav a.nav-link"
    ).forEach(li => {
        li.classList.remove("active");
    });
}
function resetShowSettings() {
    setDisplay("#settings #settings-geral", "none");
    setDisplay("#settings #settings-ciclosgale", "none");
    setDisplay("#settings #settings-ciclossoros", "none");
}
function showGeral() {
    removeAllActiveSettings()
    document.querySelector(
        "#settings a#geral"
    ).classList.add("active");

    resetShowSettings()
    setDisplay("#settings #settings-geral", "flex");
}
function showCiclosGales() {
    removeAllActiveSettings()
    document.querySelector(
        "#settings a#gales"
    ).classList.add("active");

    resetShowSettings()
    setDisplay("#settings #settings-ciclosgale", "flex");
}
function showCiclosSoros() {
    removeAllActiveSettings()
    document.querySelector(
        "#settings a#soros"
    ).classList.add("active");

    resetShowSettings()
    setDisplay("#settings #settings-ciclossoros", "flex");
}
function getCiclos(table) {
    let result = [];
    const rows = document.querySelectorAll(table + "tr");
    for (let i = 1; i < rows.length; i++) {
        const columns = rows[i].querySelectorAll("input");
        result.push([]);
        for (let j = 0; j < columns.length; j ++) {
            if (columns[j].value !== "" && columns[j].value !== "0") {
                result[i - 1].push(parseFloat(columns[j].value))
            } else {
                if (j === 0) {
                    result.splice(i - 1, 1);
                }
                break;
            }
        }
        if (result.length < i) {
            break;
        }
    }
    return result;
}
function setCiclos(table, ciclos) {
    const rows = document.querySelectorAll(table + "tr");
    for (let i = 0; i < rows.length; i++) {
        if (i >= ciclos.length) {
            break;
        }
        const columns = rows[i + 1].querySelectorAll("input");
        for (let j = 0; j < columns.length; j ++) {
            if (j >= ciclos[i].length) {
                break;
            }
            columns[j].value = ciclos[i][j]
        }
    }
}

eel.expose(saveChanges)
function saveChanges(config = null) {
    function getValue(query, default_value = "") {
        let result;
        try {
            result = document.querySelector(query).value;
        } catch {
            console.log("Error in", query);
            result = default_value;
        }
        return result;
    }

    if (config == null) {
        config = JSON.parse(localStorage.getItem('config'));

        config.valor = parseFloat(getValue(
            "#valor", config.valor))
        
        config.reverso = getValue(
            "#reverso", config.reverso)
        config.vez_gale = getValue(
            "#vez_gale", config.vez_gale)
        config.tipo_stop = getValue(
            "#tipo_stop", config.tipo_stop)
        config.tipo_gale = getValue(
            "#tipo_gale", config.tipo_gale)
        config.tipo_conta = getValue(
            "#tipo_conta", config.tipo_conta)
        config.tipo_soros = getValue(
            "#tipo_soros", config.tipo_soros)
        config.topranking = getValue(
            "#topranking", config.topranking)
        
        config.delay = parseInt(getValue(
            "#delay", config.delay))
        config.max_gale = parseInt(getValue(
            "#max_gale", config.max_gale))
        config.timeframe = parseInt(getValue(
            "#timeframe", config.timeframe))
        config.max_soros = parseInt(getValue(
            "#max_soros", config.max_soros))
        config.prestopwin = parseInt(getValue(
            "#prestopwin", config.prestopwin))
        config.scalper_win = parseInt(getValue(
            "#scalper_win", config.scalper_win))
        config.tipo_martin = getValue(
            "#tipo_martin", config.tipo_martin)
        config.scalper_loss = parseInt(getValue(
            "#scalper_loss", config.scalper_loss))
        config.stopwin = parseFloat(getValue(
            "#settings #stopwin", config.stopwin))
        config.stoploss = parseFloat(getValue(
            "#settings #stoploss", config.stoploss))

        try {
            config.ciclos_gale = getCiclos("#settings-ciclosgale ")
            config.ciclos_soros = getCiclos("#settings-ciclossoros ")
            config.prestoploss = document.querySelector("#prestoploss").checked
            
            if (!document.querySelector("#delaye").checked) {
                config.delay = false;
            } 
        } catch {}


        localStorage.setItem('config', JSON.stringify(config));
        eel.change_config(config);
        closeConfig()

        document.querySelector(
            ".profile-infos sub"
        ).innerText = `Conta: ${getValue("#tipo_conta").toUpperCase()}`
    } else if (localStorage.getItem('config') == null) {
        localStorage.setItem('config', JSON.stringify(config));
    } else {
        config = JSON.parse(localStorage.getItem('config'));
        eel.change_config(config);
    }
}
eel.expose(loadConfig)
function loadConfig() {
    function setValue(value, query) {
        document.querySelector(query).value = value;
    }
    let config = JSON.parse(localStorage.getItem('config'));
    if (config == null) {
        return
    }
    setValue(config.valor, "#valor")
    setValue(config.stoploss, "#settings #stoploss")
    setValue(config.stopwin, "#settings #stopwin")
    setValue(config.scalper_loss, "#scalper_loss")
    setValue(config.tipo_martin, "#tipo_martin")
    setValue(config.scalper_win, "#scalper_win")
    setValue(config.tipo_conta, "#tipo_conta")
    setValue(config.tipo_soros, "#tipo_soros")
    setValue(config.prestopwin, "#prestopwin")
    setValue(config.tipo_gale, "#tipo_gale")
    setValue(config.tipo_stop, "#tipo_stop")
    setValue(config.max_soros, "#max_soros")
    setValue(config.max_gale, "#max_gale")
    setValue(config.vez_gale, "#vez_gale")
    
    setValue(config.reverso, "#reverso")
    setValue(config.timeframe, "#timeframe")
    setValue(config.topranking, "#topranking")

    if (config['delay'] != false) {
        document.querySelector("#delaye").checked = true;
        setValue(config.delay, "#delay")
    }
    document.querySelector("#prestoploss").checked = config.prestoploss;
    
    setCiclos("#settings-ciclosgale ", config.ciclos_gale) 
    setCiclos("#settings-ciclossoros ", config.ciclos_soros) 
    return config
}
eel.expose(addLog)
function addLog(date, hour, message) {
    let logs = document.querySelector("div.logs ul");
    let newLog = document.createElement("li");
    newLog.innerHTML = `
    <div>
        <p> ${date} </p> <p> ${hour} </p>
    </div> <p> ${message} </p>`
    logs.appendChild(newLog);

    logs.scrollBy(0, 200);
}
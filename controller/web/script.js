let order = {
    title: 'EUR/USD',
    image: "https://static.cdnpub.info/files/storage/public/5b/50/81ba56509.svg",
    option: "Digital",
    timeframe: 60,
    amount: 2
}

const digitalOptions = [
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80fdc4eac.svg", 
        title: "USD/JPY"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/821fcb27e.svg", 
        title: "USD/CAD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80f393d56.svg", 
        title: "GBP/USD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80f283910.svg", 
        title: "GBP/JPY"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80f09f376.svg", 
        title: "GBP/CHF"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80efb5f5f.svg", 
        title: "GBP/AUD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/81ba56509.svg", 
        title: "EUR/USD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80e4a49e3.svg", 
        title: "EUR/JPY"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80eeddd32.svg", 
        title: "EUR/GBP"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80e3c35f5.svg", 
        title: "EUR/CAD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/81324b7c7.svg", 
        title: "AUD/USD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80ee0164c.svg", 
        title: "USD/CHF"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80022b5db.svg", 
        title: "GBP/NZD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80f47589c.svg", 
        title: "GBP/CAD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80e67c8a9.svg", 
        title: "EUR/AUD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/7f1830201.svg", 
        title: "CAD/JPY"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80e2cc14c.svg", 
        title: "AUD/JPY"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/820142ec6.svg", 
        title: "AUD/CAD"}
];
const binaryOptions = [
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/7ea1cbfaf.svg", 
        title: "USD/ZAR"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80f747221.svg", 
        title: "USD/TRY"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/7efab3776.svg", 
        title: "USD/SGD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/81b153506.svg", 
        title: "USD/RUB"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/7f0f95522.svg", 
        title: "USD/PLN"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80d435744.svg", 
        title: "USD/NOK"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/7eabc9598.svg", 
        title: "USD/INR"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/7ef2dcfde.svg", 
        title: "USD/HKD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/7fb941d24.svg", 
        title: "USD/BRL"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80f83efc6.svg", 
        title: "NZD/USD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/80e5913fa.svg", 
        title: "EUR/NZD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/821eb394c.svg", 
        title: "CAD/CHF"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/7f0e8a7f4.svg", 
        title: "AUD/NZD"},
    {image: "https://static.cdnpub.info/files/storage/public/5b/50/7f0179257.svg", 
        title: "AUD/CHF"}
];
const otcOptions = [
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/90f7840641g8f1e1d0.svg", 
        title: "AUD/CAD (OTC)"},
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/918a54c9c8c6a0j2d5.svg", 
        title: "NZD/USD (OTC)"},
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/9115aa2d03b4i8i6e1.svg", 
        title: "EUR/GBP (OTC)"},
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/9160e64818i6j3h5e9.svg", 
        title: "GBP/JPY (OTC)"},
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/914b4b8fd8g9h9i6e0.svg", 
        title: "EUR/USD (OTC)"},
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/9175dbcf21c3d6b9j7.svg", 
        title: "GBP/USD (OTC)"},
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/91ab305396j0j2d9a4.svg", 
        title: "USD/JPY (OTC)"},
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/919a026b05c1i8b2g8.svg", 
        title: "USD/CHF (OTC)"},
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/9125f3bd49c6i0i9e6.svg", 
        title: "EUR/JPY (OTC)"},
]

eel.expose(addCandles)
function addCandles(candles) {
    const tradeMap = document.querySelector(".trade-map");
    tradeMap.innerHTML = "";
    tradeMap.style.top = "25em";
    tradeMap.style.transform = "";
    let local = 0;
    let menor = 0;
    let maior = 0;
    candles.forEach(candle => {
        local -= candle['volume']
        if (local > maior) {
            maior = local;
        } else if (local < menor) {
            menor = local;
        }
    })
    let length = maior - menor;
    local = 0;
    candles.forEach(candle => {
        let realLength = candle['volume'] * 10 / length;
        const span = document.createElement("span");
        span.className = candle['dir']
        span.style.height = `${Math.abs(realLength)}em`
        local -= realLength / 2
        span.style.transform = `translateY(${local}em)`
        local -= realLength / 2
        tradeMap.appendChild(span);
    })
}

function generateAssets(type = "normais") {
    const options = document.querySelectorAll(".option-chooser button");
    options.forEach(option => {
        option.style.backgroundColor = "";
    })
    
    const container = document.querySelector('.others');
    container.innerHTML = "";
    if (type === "normais") {
        digitalOptions.forEach(option => {
            placeAsset(container, option, "Digital")
        })
        binaryOptions.forEach(option => {
            placeAsset(container, option, "Binary")
        })
        options[0].style.backgroundColor = "#373b44"
    } else {
        otcOptions.forEach(option => {
            placeAsset(container, option, "OTC")
        })
        options[1].style.backgroundColor = "#373b44"
    }
}
function placeAsset(container, option, type) {
    const li = document.createElement('li');
    const div = document.createElement('div');
    const h3 = document.createElement('h3');
    const p = document.createElement('p');
    const img = document.createElement('img');
    
    li.addEventListener('click', setAsset);
    h3.textContent = option.title;
    p.textContent = type;
    img.src = option.image;

    container.appendChild(li);
    li.appendChild(img);
    li.appendChild(div);
    div.appendChild(h3);
    div.appendChild(p);
}
function setAsset(evt) {
    let li;
    evt.path.forEach(path => {
        if (path.tagName === "LI") {
            li = path;
        }
    });
    order.image = li.querySelector("img").src;
    order.title = li.querySelector("h3").textContent;
    order.option = li.querySelector("p").textContent;

    const selected = document.querySelector(".asset");
    selected.querySelector("img").src = order.image;
    selected.querySelector("h3").textContent = order.title;
    selected.querySelector("p").textContent = order.option;
    eel.change_asset(order);
}
function showOthers() {
    const selected = document.querySelector("header .asset-chooser");
    if (selected.style.display === "") {
        selected.style.display = "flex";
        generateAssets();
    } else {
        selected.style.display = "";
    }
}

function changeTime(input) {
    let timeframe;
    switch (input.value) {
        case "M1":
            timeframe = 60;
            break;
        case "M5":
            timeframe = 300;
            break;
        default:
            timeframe = 900;
    }
    order.timeframe = timeframe;
    eel.change_asset(order);
}
function changeAmount(input) {
    order.amount = input.value;
    eel.change_asset(order);
}

function placeCall() {
    eel.operate("call");
}
function placePut() {
    eel.operate("put");
}

function captureCandles() {
    eel.start_capture()
}
function stopCandles() {
    eel.stop_capture()
}

function openList() {
    document.querySelector(
        ".listaContainer"
    ).style.display = "flex";
}
async function startList() {
    const texto = document.querySelector(
        ".listaContainer textarea").value;
    const lista = await eel.verificar_lista(texto)();
    document.querySelector(".trade.list").innerHTML = "";
    lista.forEach((item) => {
        const timeframe = (item.timeframe !== 0) ? 
            item.timeframe : order.timeframe / 60;
        const direcao = item.tipo === "lista" ? String(
            item.ordem).toUpperCase() : item.taxa;

        addListItem(item.par, direcao, item.textHour, timeframe)
    })
    eel.seguir_lista(lista)
}
function closeList() {
    document.querySelector(
        ".listaContainer"
    ).style.display = "none";
}
function addListItem(asset, direction, hour, timeframe) {
    const container = document.querySelector(".trade.list");
    const element = document.createElement("span");
    element.innerHTML = `
        <img/> <div>
            <p> ${hour} M${timeframe} </p>
            <p> ${direction} </p>
        </div>
    `
    searchAsset(asset, element);
    container.appendChild(element);
}
function searchAsset(asset, element) {
    function changeSelected(image) {
        element.querySelector("img").src = image;
    }

    if (asset.indexOf("-OTC") !== -1) {
        for (let index = 0; index < otcOptions.length; index++) {
            const element = otcOptions[index];
            const title = element['title'].replace("/", "").replace(" (OTC)", "-OTC");
            if (title == asset) {
                changeSelected(element['image'])
                index = otcOptions.length;
            }
        }
    } else {
        var found = false;
        for (let index = 0; index < binaryOptions.length; index++) {
            const element = binaryOptions[index];
            const title = element['title'].replace("/", "");
            if (title == asset) {
                changeSelected(element['image'])
                index = binaryOptions.length;
                found = true;
            }
        }
        if (found) { return }
        for (let index = 0; index < digitalOptions.length; index++) {
            const element = digitalOptions[index];
            const title = element['title'].replace("/", "");
            if (title == asset) {
                changeSelected(element['image'])
                index = digitalOptions.length;
            }
        }
    }
}
eel.expose(selectItemList)
function selectItemList(index) {
    const container = document.querySelector(".trade.list");
    container.querySelector(
        `span:nth-child(${index + 1})`
    ).id = "call-btn"
}
eel.expose(animatePopUp)
function animatePopUp(img, text) {
    const overlay = document.querySelector(".overlay");
    overlay.querySelector("img").src = `images/${img}`;
    overlay.querySelector("p").innerText = text;
    overlay.id = "animated";
}
function removePopUp() {
    const overlay = document.querySelector(".overlay");
    overlay.removeAttribute("id")
}

eel.expose(createOrder)
function createOrder(asset, order, type, timeframe) {
    function toSeconds(number) {
        const numberStr = String(number);
        return (numberStr.length == 2) ? numberStr : "0" + numberStr
    }
    const local = document.querySelector("header > div");
    const div = document.createElement("div");
    div.className = "asset"
    local.appendChild(div);

    div.innerHTML = `
    <div> <h3> ${asset} </h3> <p> ${type} </p> </div>
    <div> <p> ${order} </p> <p class = "time"> </p> </div>
    `
    
    const time = div.querySelector(".time");
    const atual = new Date().getMinutes();
    const tempo = (timeframe / 60) - (atual % (timeframe / 60))
    var countDownTime = new Date().getTime() + (1000 * tempo * 60);
    var x = setInterval(function () {
        var now = new Date().getTime();

        var distance = countDownTime - now;
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        time.innerHTML = toSeconds(minutes) + ":" + toSeconds(seconds);
        
        if (distance < 0) {
            clearInterval(x);
            local.removeChild(div);
        } 
    }, 1000);
}

async function login(event) {
    event.preventDefault();
    const email = document.querySelector(".login input[type=email]").value
    const password = document.querySelector(".login input[type=password]").value
    const button = document.querySelector(".login button")
    button.innerText = 'Acessando...';
    const result = await eel.login(email, password)();
    if (result) {
        document.querySelectorAll("section.login").forEach(
            element => { element.style.display = "none" }) 
    } else {
        button.innerText = 'Entrar';
    }
    captureCandles();
    generateAssets();
}
eel.expose(changeLicense)
function changeLicense(email, texto) {
    if (texto === "Renove sua licença") {
        document.querySelector(
            ".login button"
        ).disabled = false;
    }
    document.querySelector(
        "sub"
    ).innerText = texto;
    if (email != "") {
        input = document.querySelector(
            "input[type=email]")
        input.value = email;
        input.disabled = true;
    }
}

function searchLicense(input) {
    var reader = new FileReader(); 
    reader.onload = function(){ 
        let textFile = reader.result;
        if (textFile) {
            eel.search_license(textFile);
        }
    } 
    if (input.value !== null) {
      reader.readAsText(input.files[0]); 
    }
}

eel.expose(changeData)
function changeData(data) {
    document.title = data.titulo;
    document.querySelector(
        ".login h2"
    ).innerText = data.login;
    const nome = document.querySelector("header h1")
    if (nome) {
        nome.innerText = data.nome
    }
    if (data.icone !== "") {
        document.querySelector(
            "link[rel~='icon']"
        ).href = data.icone
    }
}
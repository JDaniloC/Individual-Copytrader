let order = {
    title: 'EUR/USD',
    image: "https://static.cdnpub.info/files/storage/public/5b/50/81ba56509.svg",
    option: "Digital",
    timeframe: 60,
    amount: 2
}

eel.expose(addCandles)
function addCandles(candles) {
    const tradeMap = document.querySelector(".trade-map");
    tradeMap.innerHTML = "";
    tradeMap.style.top = "1em";
    tradeMap.style.transform = "";
    let local = 0;
    let menor = 0;
    let maior = 0;
    candles.forEach(candle => {
        const span = document.createElement("span");
        span.className = candle['dir']
        span.style.height = `${Math.abs(candle['volume'])}em`
        local -= candle['volume'] / 2
        span.style.transform = `translateY(${local}em)`
        local -= candle['volume'] / 2
        tradeMap.appendChild(span);
        if (local > maior) {
            maior = local;
        } else if (local < menor) {
            menor = local;
        }
    })
    const soma = Math.abs(maior) + Math.abs(menor);
    const translate = Math.abs(Math.min(maior, menor));
    if (soma > 55) {
        let scale = (50 / soma).toFixed(2);
        tradeMap.style.transform = `scaleY(${scale})`
        tradeMap.style.top = `${Math.abs((Math.abs(menor) * scale) + 1)}em`
    } else if (translate > 0) {
        tradeMap.style.top = `${translate + 1}em`
    }
}

function generateAssets(type = "Digital") {
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
        {image: "https://static.cdnpub.info/files/storage/public/5d/5a/918a54c9c8c6a0j2d5.svg", 
            title: "NZD/USD (OTC)"},
        {image: "https://static.cdnpub.info/files/storage/public/5d/5a/9125f3bd49c6i0i9e6.svg", 
            title: "EUR/JPY (OTC)"},
        {image: "https://static.cdnpub.info/files/storage/public/5d/5a/90f7840641g8f1e1d0.svg", 
            title: "AUD/CAD (OTC)"}
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
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80fdc4eac.svg", 
            title: "USD/JPY"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/7eabc9598.svg", 
            title: "USD/INR"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/7ef2dcfde.svg", 
            title: "USD/HKD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80ee0164c.svg", 
            title: "USD/CHF"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/821fcb27e.svg", 
            title: "USD/CAD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/7fb941d24.svg", 
            title: "USD/BRL"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80f83efc6.svg", 
            title: "NZD/USD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80f393d56.svg", 
            title: "GBP/USD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80f283910.svg", 
            title: "GBP/JPY"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80f09f376.svg", 
            title: "GBP/CHF"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80f47589c.svg", 
            title: "GBP/CAD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80efb5f5f.svg", 
            title: "GBP/AUD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/81ba56509.svg", 
            title: "EUR/USD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80e5913fa.svg", 
            title: "EUR/NZD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80e4a49e3.svg", 
            title: "EUR/JPY"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80eeddd32.svg", 
            title: "EUR/GBP"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80e3c35f5.svg", 
            title: "EUR/CAD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80e67c8a9.svg", 
            title: "EUR/AUD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/821eb394c.svg", 
            title: "CAD/CHF"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/81324b7c7.svg", 
            title: "AUD/USD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/7f0e8a7f4.svg", 
            title: "AUD/NZD"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/80e2cc14c.svg", 
            title: "AUD/JPY"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/7f0179257.svg", 
            title: "AUD/CHF"},
        {image: "https://static.cdnpub.info/files/storage/public/5b/50/820142ec6.svg", 
            title: "AUD/CAD"}
    ];
    const options = document.querySelectorAll(".option-chooser button");
    options.forEach(option => {
        option.style.backgroundColor = "";
    })
    
    const container = document.querySelector('.others');
    container.innerHTML = "";
    if (type === "Digital") {
        digitalOptions.forEach(option => {
            placeAsset(container, option, "Digital")
        })
        options[0].style.backgroundColor = "#373b44"
    } else {
        binaryOptions.forEach(option => {
            placeAsset(container, option, "Binary")
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
            timeframe = 1800;
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
    const local = document.querySelector("header > div");
    const div = document.createElement("div");
    div.className = "asset"
    local.appendChild(div);

    const assetDiv = document.createElement("div")
    const orderDiv = document.createElement("div")
    div.appendChild(assetDiv);
    div.appendChild(orderDiv);

    const h3 = document.createElement("h3");
    const p = document.createElement("p");
    h3.innerText = asset;
    p.innerText = type;
    assetDiv.appendChild(h3);
    assetDiv.appendChild(p);

    const time = document.createElement("p");
    const dir = document.createElement("p");
    dir.innerText = order;
    orderDiv.appendChild(dir);
    orderDiv.appendChild(time);

    const atual = new Date().getMinutes();
    const tempo = (timeframe / 60) - (atual % (timeframe / 60))
    var countDownTime = new Date().getTime() + (1000 * tempo * 60);
    var x = setInterval(function () {
        var now = new Date().getTime();

        var distance = countDownTime - now;
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        time.innerHTML = minutes + ":" + seconds;
        
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
function changeLicense(texto) {
    if (texto === "Renove sua licença") {
        document.querySelector(
            ".login button"
        ).disabled = true;
    }
    document.querySelector(
        "sub"
    ).innerText = texto;
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
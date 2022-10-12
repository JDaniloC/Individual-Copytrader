const assets = [
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
    {image: "https://static.cdnroute.io/files/storage/public/5f/7f/1e2997d0e9c7j7f4g0/USDHKD_OTC.png", 
        title: "USD/HKD (OTC)"},
    {image: "https://static.cdnroute.io/files/storage/public/5f/35/3ae8bf1547c9d7j0f6/USDZAR_OTC.png", 
        title: "USD/ZAR (OTC)"},
    {image: "https://static.cdnroute.io/files/storage/public/5f/7f/1e280cd7d1a7d1b0d6/USDSGD_OTC.png", 
        title: "USD/SGD (OTC)"},
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
        title: "AUD/CHF"},
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
        title: "AUD/CAD"},
    {image: "https://static.cdnroute.io/files/storage/public/5b/50/81e357c97.svg", 
        title: "ETH/USD"},
    {image: "https://static.cdnroute.io/files/storage/public/5b/50/81f9b71a0.svg", 
        title: "BTC/USD"},
    {image: "https://static.cdnroute.io/files/storage/public/5b/50/81b96c88e.svg", 
        title: "XRP/USD"},
    {image: "https://static.cdnroute.io/files/storage/public/5b/50/7f61bcab0.svg", 
        title: "EOS/USD"},
    {image: "https://static.cdnroute.io/files/storage/public/5c/7f/89fa9381e3c5h4e1c5.svg", 
        title: "LTC/USD"},
];

function getImage(asset) {
    for (var i = 0; i < assets.length; i++) {
        const title = assets[i].title.replace("/", "").replace(" (OTC)", "-OTC");
        if (title === asset) {
            return assets[i].image;
        }
    }
}
eel.expose(placeTrade)
function placeTrade(asset, direction, timeframe, value, id) {
    const ul = document.querySelector("main ul");
    const li = document.createElement("li");
    li.innerHTML = `
    <img src="${getImage(asset)}">
    <div>
        <h3> ${asset} </h3>
        <p> ${direction} </p>
    </div>
    <div> 
        <h3 id="id${id}">
            Em andamento
        </h3>
        <p> M${timeframe} R$${value}</p>
    </div>
    `
    ul.appendChild(li);
}

eel.expose(updateInfos)
function updateInfos(gain, stopwin, stoploss) {
    const valores = document.querySelectorAll("footer div p");
    valores[0].innerText = `R$ ${gain.toFixed(2)}`
    valores[1].innerText = `R$ ${stopwin.toFixed(2)}`
    valores[2].innerText = `R$ ${stoploss.toFixed(2)}`
}

eel.expose(setResult)
function setResult(id, result) {
    document.querySelector(`li h3#id${id}`).innerText = result
}

eel.expose(screenAlert)
function screenAlert(message) {
    alert(message);
}

async function login() {
    const email = document.querySelector(".login input[type=email]").value
    const password = document.querySelector(".login input[type=password]").value
    const button = document.querySelector(".login button")
    button.innerText = 'Acessando...';
    button.disabled = true;
    const result = await eel.verify_connection(email, password)();
    button.disabled = false;
    if (result !== null) {
        document.querySelector(
            "section.login"
        ).style.display = "none"; 
        document.querySelector(
            "section.overlay"
        ).style.display = "none"; 
        if (result) {
            localStorage.setItem('account', JSON.stringify({
                email, password
            }))
            loadConfig();
            const status = document.querySelector("header div#status p");
            status.className = "online";
            status.textContent = "Online";
            document.querySelector("header div#status img").style.opacity = 1;
        }
    } else {
        button.innerText = 'Entrar';
    }
    return false;
}

eel.expose(changeData)
function changeData(data) {
    document.title = data.titulo;
    document.querySelector(
        ".login h1"
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

eel.expose(hitStop)
function hitStop() {
    const status = document.querySelector("header #status p");
    status.className = "offline";
    status.textContent = "Bateu em um Stop!";
    document.querySelector("header img").style.opacity = 0;
}

eel.expose(goOnline)
function goOnline() {
    const status = document.querySelector("header #status p");
    status.className = "online";
    status.textContent = "Online";
    document.querySelector("header img").style.opacity = 1;
}
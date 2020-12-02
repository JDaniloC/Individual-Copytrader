const assets = [
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/918a54c9c8c6a0j2d5.svg", 
        title: "NZDUSD-OTC"},
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/9125f3bd49c6i0i9e6.svg", 
        title: "EURJPY-OTC"},
    {image: "https://static.cdnpub.info/files/storage/public/5d/5a/90f7840641g8f1e1d0.svg", 
        title: "AUDCAD-OTC"},
    {title: "USDZAR", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/7ea1cbfaf.svg"},
    {title: "USDTRY", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80f747221.svg"},
    {title: "USDSGD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/7efab3776.svg"},
    {title: "USDRUB", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/81b153506.svg"},
    {title: "USDPLN", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/7f0f95522.svg"},
    {title: "USDNOK", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80d435744.svg"},
    {title: "USDJPY", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80fdc4eac.svg"},
    {title: "USDINR", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/7eabc9598.svg"},
    {title: "USDHKD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/7ef2dcfde.svg"},
    {title: "USDCHF", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80ee0164c.svg"},
    {title: "USDCAD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/821fcb27e.svg"},
    {title: "USDBRL", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/7fb941d24.svg"},
    {title: "NZDUSD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80f83efc6.svg"},
    {title: "GBPUSD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80f393d56.svg"},
    {title: "GBPJPY", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80f283910.svg"},
    {title: "GBPCHF", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80f09f376.svg"},
    {title: "GBPCAD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80f47589c.svg"},
    {title: "GBPAUD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80efb5f5f.svg"},
    {title: "EURUSD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/81ba56509.svg"},
    {title: "EURNZD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80e5913fa.svg"},
    {title: "EURJPY", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80e4a49e3.svg"},
    {title: "EURGBP", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80eeddd32.svg"},
    {title: "EURCAD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80e3c35f5.svg"},
    {title: "EURAUD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80e67c8a9.svg"},
    {title: "CADCHF", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/821eb394c.svg"},
    {title: "AUDUSD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/81324b7c7.svg"},
    {title: "AUDNZD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/7f0e8a7f4.svg"},
    {title: "AUDJPY", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/80e2cc14c.svg"},
    {title: "AUDCHF", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/7f0179257.svg"},
    {title: "AUDCAD", image: 
    "https://static.cdnpub.info/files/storage/public/5b/50/820142ec6.svg"}
];

function getImage(asset) {
    for (var i = 0; i < assets.length; i++) {
        if (assets[i].title === asset) {
            return assets[i].image;
        }
    }
}
eel.expose(placeTrade)
function placeTrade(asset, order, timeframe, id) {
    const ul = document.querySelector("main ul");
    const li = document.createElement("li");
    const img = document.createElement("img");
    img.src = getImage(asset);
    const div1 = document.createElement("div");
    const div2 = document.createElement("div");
    const h31 = document.createElement("h3");
    h31.innerText = asset;
    const h32 = document.createElement("h3");
    h32.innerText = 'Em andamento'
    h32.id = "id" + id;
    const p1 = document.createElement("p");
    p1.innerText = order;
    const p2 = document.createElement("p");
    p2.innerText = "M" + timeframe;
    ul.appendChild(li);
    li.appendChild(img);
    li.appendChild(div1);
    li.appendChild(div2);
    div1.appendChild(h31);
    div1.appendChild(p1);
    div2.appendChild(h32);
    div2.appendChild(p2);
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

eel.verify_connection()((result) => {
    if (result) {
        const status = document.querySelector("header p")
        status.className = "online"
        status.textContent = "Online"
        document.querySelector("header img").style.opacity = 1
    }
});
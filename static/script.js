const navLinks = document.querySelectorAll(".nav-link");
const sections = [
    { id: "anasayfa", element: document.querySelector(".hero") },
    { id: "ceviri", element: document.getElementById("ceviri") },
    { id: "hakkimizda", element: document.getElementById("hakkimizda") },
    { id: "contact", element: document.getElementById("contact") }
];

let isClickScrolling = false;

navLinks.forEach(link => {
    link.addEventListener("click", (e) => {
        const href = link.getAttribute("href");
        if (href.startsWith("#")) {
            // Scroll sırasında aktiflik sabitlensin
            isClickScrolling = true;
            navLinks.forEach(l => l.classList.remove("active"));
            link.classList.add("active");

            // Scroll'un tamamlanma süresi
            setTimeout(() => {
                isClickScrolling = false;
            }, 800);
        }
    });
});

window.addEventListener("scroll", () => {
    if (isClickScrolling) return; // Scroll animasyonu sırasında scroll takibini durdur

    let current = "";

    sections.forEach((section) => {
        const offsetTop = section.element.offsetTop;
        const offsetHeight = section.element.offsetHeight;
        if (pageYOffset >= offsetTop - 150 && pageYOffset < offsetTop + offsetHeight - 150) {
            current = section.id;
        }
    });

    navLinks.forEach((link) => {
        link.classList.remove("active");
        if (link.getAttribute("href") === "#" + current) {
            link.classList.add("active");
        }
    });
});

const nav = document.querySelector(".nav")
const add = 510
window.addEventListener("scroll", () => {
    if (window.scrollY > nav.offsetHeight + add) {
        nav.classList.add("move")
    }
    else {
        nav.classList.remove("move")
    }
})


const observerOptions = {
    root: null,
    rootMargin: '-50% 0px -50% 0px',
    threshold: 0
};

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        const id = entry.target.getAttribute('id');
        const link = document.querySelector(`.nav-link[href="#${id}"]`);

        if (entry.isIntersecting) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}, observerOptions);


sections.forEach(section => {
    if (section.element) { 
        observer.observe(section.element);
    } else {
        console.warn(`Element bulunamadı: ${section.id}`);
    }
});


document.getElementById('translateBtn').addEventListener('click', async () => {
    const direction = document.getElementById('direction').value;
    const text = document.getElementById('inputText').value.trim();

    if (!text) {
        alert('Lütfen çeviri için metin giriniz.');
        return;
    }

    const resultDiv = document.getElementById('result');
    resultDiv.textContent = 'Çeviri yapılıyor...';

    try {
        const response = await fetch('/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ direction, text })
        });

        const data = await response.json();
        if (response.ok) {
            resultDiv.textContent = data.result;
        } else {
            resultDiv.textContent = 'Hata: ' + (data.error || 'Bilinmeyen hata');
        }
    } catch (error) {
        resultDiv.textContent = 'İstek gönderilirken hata oluştu: ' + error.message;
    }
});

document.getElementById('clearBtn').addEventListener('click', () => {
    document.getElementById('inputText').value = '';
    document.getElementById('result').textContent = '';
});



const cevirBtn = document.getElementById('translateBtn');
const temizleBtn = document.getElementById('clearBtn');

function clickEffect(button) {
    button.classList.add('clicked');
    setTimeout(() => {
        button.classList.remove('clicked');
    }, 300);
}

cevirBtn.addEventListener('click', () => {
    clickEffect(cevirBtn);
    
});

temizleBtn.addEventListener('click', () => {
    clickEffect(temizleBtn);
   
});


const resultEl = document.getElementById('result');
const copyBtn = document.getElementById('copyBtn');
const translateBtn = document.getElementById('translateBtn');
const clearBtn = document.getElementById('clearBtn');


function toggleCopyButton() {
    copyBtn.disabled = !resultEl.innerText.trim();
}


translateBtn.addEventListener('click', () => {
    
    toggleCopyButton();
});

clearBtn.addEventListener('click', () => {
    resultEl.innerText = '';
    toggleCopyButton();
});

// Kopyala işlemi
copyBtn.addEventListener('click', () => {
    const textToCopy = resultEl.innerText;

    
    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            copyBtn.textContent = 'Kopyalandı!';
            setTimeout(() => copyBtn.textContent = 'Kopyala', 2000);
        })
        .catch(err => {
            // Fallback yöntemi
            const tmp = document.createElement('textarea');
            tmp.value = textToCopy;
            document.body.appendChild(tmp);
            tmp.select();
            document.execCommand('copy');
            tmp.remove();
        });
});

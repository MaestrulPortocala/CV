
const dateCategorii = [
    {
        titlu: "Steroizi Anabolici",
        desc: "Compuși androgenici pentru studii metabolice și dezvoltare musculară",
    },
    {
        titlu: "SARMS",
        desc: "Modulatori selectivi ai receptorilor androgenici pentru cercetări țintite",
    },
    {
        titlu: "Peptide",
        desc: "Secvențe de aminoacizi pentru studii despre semnalizare celulară",
     
    },
    {
        titlu: "Hormoni de Creștere",
        desc: "Proteine recombinante pentru cercetări avansate despre metabolismul uman",
    }
];
function creazaCarduriCategorii() {
    const div_categorii = document.getElementById('categories-container');
    
    if (!div_categorii) {
        return;
    }
    for (let i = 0; i < dateCategorii.length; i++) {
        const cat = dateCategorii[i];
        const card_nou = document.createElement('div');
        card_nou.className = 'category-card';
        const titluH3 = '<h3>' + cat.titlu + '</h3>';
        const descP = '<p>' + cat.desc + '</p>';
        card_nou.innerHTML = titluH3 + descP;
        div_categorii.appendChild(card_nou);
    }
}
function calculeazaPretCuReducere(cant, pret_unitar) {
    let reducere_aplicata = 0;
    let procent_red = 0;
    if (cant >= 100) {
        procent_red = 25;
    } else if (cant >= 50) {
        procent_red = 20;
    } else if (cant >= 20) {
        procent_red = 15;
    } else if (cant >= 10) {
        procent_red = 10;
    } else if (cant >= 5) {
        procent_red = 5;
    }
    const total_fara_red = cant * pret_unitar;
    reducere_aplicata = (total_fara_red * procent_red) / 100;
    const total_final = total_fara_red - reducere_aplicata;
    const rezultat = {
        subtotal: total_fara_red.toFixed(2),
        discount: reducere_aplicata.toFixed(2),
        discountPercent: procent_red,
        total: total_final.toFixed(2)
    };
    
    return rezultat;
}
function genereazaCalculatorComanda() {
    const container_calc = document.getElementById('order-calculator');
    
    if (!container_calc) {
        return;
    }
    
    let html_calculator = '<div class="calculator-box">';
    html_calculator += '<div class="calc-input-group">';
    html_calculator += '<label for="product-select">Selectează Produsul:</label>';
    html_calculator += '<select id="product-select">';
    html_calculator += '<option value="150">Testosteron Enanthate - 150 EUR/vial</option>';
    html_calculator += '<option value="180">Trenbolon Acetate - 180 EUR/vial</option>';
    html_calculator += '<option value="120">Nandrolon Decanoat - 120 EUR/vial</option>';
    html_calculator += '<option value="200">Oxandrolon - 200 EUR/50 tabs</option>';
    html_calculator += '</select></div>';
    html_calculator += '<div class="calc-input-group">';
    html_calculator += '<label for="quantity-input">Cantitate:</label>';
    html_calculator += '<input type="number" id="quantity-input" min="1" value="1">';
    html_calculator += '</div>';
    html_calculator += '<button id="calculate-btn" class="calc-btn">Calculează Prețul</button>';
    html_calculator += '<div id="result-display" class="calc-result"></div>';
    html_calculator += '</div>';
    
    container_calc.innerHTML = html_calculator;
    const btn_calc = document.getElementById('calculate-btn');
    btn_calc.addEventListener('click', function() {
        const selectie = document.getElementById('product-select');
        const pret = parseFloat(selectie.value);
        const cantitate = parseInt(document.getElementById('quantity-input').value);
        const div_rez = document.getElementById('result-display');
        if (cantitate < 1) {
            alert('Cantitatea trebuie să fie cel puțin 1');
            return;
        }
        const rez = calculeazaPretCuReducere(cantitate, pret);
        let html_rez = '<h3>Rezultatul Comenzii</h3>';
        html_rez += '<p>Subtotal: <strong>' + rez.subtotal + ' EUR</strong></p>';
        
        if (rez.discountPercent > 0) {
            html_rez += '<p>Reducere (' + rez.discountPercent + '%): <strong>-' + rez.discount + ' EUR</strong></p>';
        } else {
            html_rez += '<p>Fără reducere (comandă min. 5 unități pentru discount)</p>';
        }
        
        html_rez += '<p class="result-total">Total: ' + rez.total + ' EUR</p>';
        div_rez.innerHTML = html_rez;
        div_rez.classList.add('show');
    });
}
const listaProduse = [
    { produs: "Testosteron Enanthate 250mg/ml", unitate: "10ml vial", pret: "150.00", puritate: "99.2%" },
    { produs: "Testosteron Cypionate 250mg/ml", unitate: "10ml vial", pret: "155.00", puritate: "99.1%" },
    { produs: "Trenbolon Acetate 100mg/ml", unitate: "10ml vial", pret: "180.00", puritate: "98.9%" },
    { produs: "Nandrolon Decanoat 200mg/ml", unitate: "10ml vial", pret: "120.00", puritate: "99.3%" },
    { produs: "Boldenon Undecylenat 300mg/ml", unitate: "10ml vial", pret: "140.00", puritate: "98.7%" },
    { produs: "Oxandrolon 20mg", unitate: "50 tabs", pret: "200.00", puritate: "99.5%" },
    { produs: "Metandrostenolon 10mg", unitate: "100 tabs", pret: "80.00", puritate: "98.8%" },
    { produs: "Stanozolol 10mg", unitate: "100 tabs", pret: "95.00", puritate: "99.0%" },
    { produs: "Ostarine (MK-2866) 25mg", unitate: "30ml", pret: "85.00", puritate: "99.1%" },
    { produs: "Ligandrol (LGD-4033) 10mg", unitate: "30ml", pret: "90.00", puritate: "98.9%" },
    { produs: "RAD-140 (Testolone) 10mg", unitate: "30ml", pret: "95.00", puritate: "99.2%" },
    { produs: "BPC-157 5mg", unitate: "vial", pret: "45.00", puritate: "99.4%" },
    { produs: "TB-500 5mg", unitate: "vial", pret: "55.00", puritate: "99.3%" },
    { produs: "IGF-1 LR3 1mg", unitate: "vial", pret: "120.00", puritate: "98.8%" },
    { produs: "HGH 100IU", unitate: "kit", pret: "280.00", puritate: "99.5%" }
];
function construiesteTabelPreturi() {
    const loc_tabel = document.getElementById('pricing-table-container');
    
    if (!loc_tabel) {
        return;
    }
    const tabel = document.createElement('table');
    tabel.className = 'pricing-table';
    const thead = document.createElement('thead');
    const rand_header = document.createElement('tr');
    
    const coloane = ['Produs', 'Unitate', 'Puritate', 'Preț (EUR)'];
    for (let j = 0; j < coloane.length; j++) {
        const th = document.createElement('th');
        th.textContent = coloane[j];
        rand_header.appendChild(th);
    }
    thead.appendChild(rand_header);
    tabel.appendChild(thead);
    const tbody = document.createElement('tbody');
    
    for (let k = 0; k < listaProduse.length; k++) {
        const item = listaProduse[k];
        const rand = document.createElement('tr');
        const td1 = document.createElement('td');
        td1.textContent = item.produs;
        rand.appendChild(td1);
        const td2 = document.createElement('td');
        td2.textContent = item.unitate;
        rand.appendChild(td2);
        const td3 = document.createElement('td');
        td3.textContent = item.puritate;
        rand.appendChild(td3);
        const td4 = document.createElement('td');
        td4.className = 'price-highlight';
        td4.textContent = item.pret + ' EUR';
        rand.appendChild(td4);
        
        tbody.appendChild(rand);
    }
    
    tabel.appendChild(tbody);
    loc_tabel.appendChild(tabel);
}
const pachete = [
    {
        nume: "Pachet Începător",
        pret: "450.00",
        economie: "50.00",
        continut: [
            "Testosteron Enanthate 10ml",
            "Oxandrolon 50 tabs",
            "Certificat COA inclus",
            "Ghid de stocare"
        ]
    },
    {
        nume: "Pachet Standard",
        pret: "850.00",
        economie: "120.00",
        continut: [
            "3x Steroizi la alegere",
            "2x SARMS la alegere",
            "Certificate COA incluse",
            "Livrare gratuită",
            "Consultanță tehnică"
        ]
    },
    {
        nume: "Pachet Profesional",
        pret: "1600.00",
        economie: "300.00",
        continut: [
            "5x Steroizi premium",
            "3x SARMS complet ciclu",
            "2x Peptide regenerare",
            "Certificate COA + Rapoarte",
            "Livrare express gratuită",
            "Suport tehnic dedicat"
        ]
    }
];
function afiseazaPachete() {
    const zona_pachete = document.getElementById('research-packages');
    
    if (!zona_pachete) {
        return;
    }
    
    const grid = document.createElement('div');
    grid.className = 'packages-grid';
    for (let m = 0; m < pachete.length; m++) {
        const p = pachete[m];
        const card_pachet = document.createElement('div');
        card_pachet.className = 'package-card';
        const titlu = document.createElement('h3');
        titlu.textContent = p.nume;
        card_pachet.appendChild(titlu);
        const pret_p = document.createElement('p');
        pret_p.className = 'package-price';
        pret_p.textContent = p.pret + ' EUR';
        card_pachet.appendChild(pret_p);
        const econ_p = document.createElement('p');
        econ_p.className = 'package-savings';
        econ_p.textContent = 'Economisești ' + p.economie + ' EUR';
        card_pachet.appendChild(econ_p);
        const ul = document.createElement('ul');
        ul.className = 'package-items';
        
        for (let n = 0; n < p.continut.length; n++) {
            const li = document.createElement('li');
            li.textContent = '✓ ' + p.continut[n];
            ul.appendChild(li);
        }
        
        card_pachet.appendChild(ul);
        grid.appendChild(card_pachet);
    }
    
    zona_pachete.appendChild(grid);
}
function configurareCalculatorBulk() {
    const buton = document.getElementById('calc-button');
    
    if (!buton) {
        return;
    }
    
    buton.addEventListener('click', function() {
        const cant_input = document.getElementById('bulk-quantity');
        const pret_input = document.getElementById('bulk-price');
        const zona_rez = document.getElementById('calc-result');
        const cantitate_bulk = parseInt(cant_input.value);
        const pret_bulk = parseFloat(pret_input.value);
        if (cantitate_bulk < 1 || pret_bulk < 0) {
            alert('Vă rugăm introduceți valori valide');
            return;
        }
        const rezultat_bulk = calculeazaPretCuReducere(cantitate_bulk, pret_bulk);
        let mesaj = '<h3>Rezultatul Calculului</h3>';
        mesaj += '<p><strong>Cantitate:</strong> ' + cantitate_bulk + ' unități</p>';
        mesaj += '<p><strong>Preț unitar:</strong> ' + pret_bulk.toFixed(2) + ' EUR</p>';
        mesaj += '<p><strong>Subtotal:</strong> ' + rezultat_bulk.subtotal + ' EUR</p>';
        
        if (rezultat_bulk.discountPercent > 0) {
            mesaj += '<p><strong>Reducere aplicată:</strong> ' + rezultat_bulk.discountPercent;
            mesaj += '% (-' + rezultat_bulk.discount + ' EUR)</p>';
        } else {
            mesaj += '<p><em>Comandă min. 5 unități pentru discount</em></p>';
        }
        
        mesaj += '<p class="result-total">TOTAL: ' + rezultat_bulk.total + ' EUR</p>';
        mesaj += '<p style="margin-top: 1rem; font-size: 0.9rem; color: #6b7280;">';
        mesaj += '* Reduceri: 5+ (5%), 10+ (10%), 20+ (15%), 50+ (20%), 100+ (25%)</p>';
        
        zona_rez.innerHTML = mesaj;
        zona_rez.classList.add('show');
    });
}
function creeazaFormular() {
    const loc_form = document.getElementById('contact-form');
    
    if (!loc_form) {
        return;
    }
    let html_form = '';
    html_form += '<div class="form-group">';
    html_form += '<label for="name">Nume Complet *</label>';
    html_form += '<input type="text" id="name" name="name" required>';
    html_form += '</div>';
    html_form += '<div class="form-group">';
    html_form += '<label for="institution">Instituție / Universitate *</label>';
    html_form += '<input type="text" id="institution" name="institution" required>';
    html_form += '</div>';
    html_form += '<div class="form-group">';
    html_form += '<label for="email">Email *</label>';
    html_form += '<input type="email" id="email" name="email" required>';
    html_form += '</div>';
    html_form += '<div class="form-group">';
    html_form += '<label for="phone">Telefon</label>';
    html_form += '<input type="tel" id="phone" name="phone">';
    html_form += '</div>';
    html_form += '<div class="form-group">';
    html_form += '<label for="subject">Subiect *</label>';
    html_form += '<select id="subject" name="subject" required>';
    html_form += '<option value="">Selectează subiectul</option>';
    html_form += '<option value="info">Informații generale</option>';
    html_form += '<option value="order">Comandă produse</option>';
    html_form += '<option value="coa">Certificate COA</option>';
    html_form += '<option value="pricing">Ofertă personalizată</option>';
    html_form += '<option value="support">Suport tehnic</option>';
    html_form += '</select></div>';
    html_form += '<div class="form-group">';
    html_form += '<label for="message">Mesaj *</label>';
    html_form += '<textarea id="message" name="message" rows="6" required></textarea>';
    html_form += '</div>';
    html_form += '<button type="button" id="submit-contact" class="submit-btn">Trimite Mesaj</button>';
    html_form += '<div id="form-response" style="margin-top: 1rem; display: none;"></div>';
    
    loc_form.innerHTML = html_form;
    
    
    const btn_submit = document.getElementById('submit-contact');
    btn_submit.addEventListener('click', function() {
     
        const val_nume = document.getElementById('name').value;
        const val_inst = document.getElementById('institution').value;
        const val_email = document.getElementById('email').value;
        const val_subj = document.getElementById('subject').value;
        const val_msg = document.getElementById('message').value;
        const zona_rasp = document.getElementById('form-response');
        
      
        if (!val_nume || !val_inst || !val_email || !val_subj || !val_msg) {
            zona_rasp.style.display = 'block';
            zona_rasp.style.backgroundColor = '#fee';
            zona_rasp.style.padding = '1rem';
            zona_rasp.style.borderRadius = '6px';
            zona_rasp.innerHTML = '<p style="color: #c00; margin: 0;">Vă rugăm completați toate câmpurile obligatorii!</p>';
            return;
        }
        
        zona_rasp.style.display = 'block';
        zona_rasp.style.backgroundColor = '#d1fae5';
        zona_rasp.style.padding = '1rem';
        zona_rasp.style.borderRadius = '6px';
        
        let msg_succes = '<p style="color: #065f46; margin: 0;">';
        msg_succes += '<strong>✓ Mulțumim, ' + val_nume + '!</strong><br>';
        msg_succes += 'Mesajul dvs. a fost trimis cu succes. Vă vom contacta în curând la adresa ' + val_email + '.';
        msg_succes += '</p>';
        
        zona_rasp.innerHTML = msg_succes;
        
        setTimeout(function() {
            document.getElementById('name').value = '';
            document.getElementById('institution').value = '';
            document.getElementById('email').value = '';
            document.getElementById('phone').value = '';
            document.getElementById('subject').value = '';
            document.getElementById('message').value = '';
        }, 500);
    });
}


document.addEventListener('DOMContentLoaded', function() {
    creazaCarduriCategorii();
    genereazaCalculatorComanda();
    construiesteTabelPreturi();
    afiseazaPachete();
    configurareCalculatorBulk();
    creeazaFormular();
});

const currentYear = new Date().getFullYear();
function calculatePrice(unitPrice, quantity, discountPercent = 0) {
    const subtotal = unitPrice * quantity;
    const discount = subtotal * (discountPercent / 100);
    const total = subtotal - discount;
    return total;
}
function formatCurrency(amount) {
    return amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,') + ' EUR';
}
function generateSpecialOffer() {
    const mainElement = document.querySelector('main');
    if (!mainElement) return;
    if (document.querySelector('.special-offer')) return;
    const offerSection = document.createElement('section');
    offerSection.className = 'special-offer';
    offerSection.style.cssText = `
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 40px 0;
        text-align: center;
        margin: 40px 0;
    `;
    const originalPrice = 2499;
    const discountPercent = 20;
    const discountedPrice = calculatePrice(originalPrice, 1, discountPercent);
    offerSection.innerHTML = `
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 15px;">Ofertă Specială - Reducere ${discountPercent}%!</h2>
            <p style="font-size: 1.2rem; margin-bottom: 20px;">
                Pachetul Business la doar <strong>${formatCurrency(discountedPrice)}</strong> 
                <span style="text-decoration: line-through; opacity: 0.7;">${formatCurrency(originalPrice)}</span>
            </p>
            <p style="font-size: 1rem; margin-bottom: 25px;">
                Economisești ${formatCurrency(originalPrice - discountedPrice)}! Ofertă valabilă până la sfârșitul lunii.
            </p>
            <a href="contact.html" class="btn-primary">Profită Acum!</a>
        </div>
    `;
    const heroSection = document.querySelector('.hero');
    if (heroSection && heroSection.nextElementSibling) {
        heroSection.parentNode.insertBefore(offerSection, heroSection.nextElementSibling);
    } else {
        mainElement.insertBefore(offerSection, mainElement.firstChild);
    }
}
function generateServiceCards() {
    const servicesContainer = document.getElementById('dynamic-services');
    if (!servicesContainer) return;
    const services = [
        {
            title: 'Web Development',
            description: 'Site-uri moderne și responsive',
            basePrice: 1200,
            features: ['Design responsive', 'Optimizare SEO', 'CMS Integration']
        },
        {
            title: 'Mobile Apps',
            description: 'Aplicații iOS și Android',
            basePrice: 5000,
            features: ['Native & Cross-platform', 'UI/UX Design', 'App Store Publishing']
        },
        {
            title: 'Consultanță IT',
            description: 'Strategie și optimizare',
            basePrice: 100,
            features: ['Audit tehnologic', 'Cloud migration', 'Security consulting']
        },
        {
            title: 'Mentenanță',
            description: 'Suport tehnic continuu',
            basePrice: 300,
            features: ['Backup zilnic', 'Actualizări', 'Monitoring 24/7']
        }
    ];
    const cardsWrapper = document.createElement('div');
    cardsWrapper.style.cssText = `
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
        margin-top: 30px;
    `;
    services.forEach(service => {
        const card = document.createElement('div');
        card.style.cssText = `
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        `;
        
        card.innerHTML = `
            <div style="font-size: 3rem; margin-bottom: 15px;">${service.icon}</div>
            <h3 style="color: #667eea; font-size: 1.5rem; margin-bottom: 10px;">${service.title}</h3>
            <p style="margin-bottom: 15px; color: #666;">${service.description}</p>
            <p style="font-size: 1.5rem; font-weight: bold; color: #764ba2; margin-bottom: 15px;">
                de la ${formatCurrency(service.basePrice)}
            </p>
            <ul style="list-style: none; padding: 0; margin-bottom: 20px; text-align: left;">
                ${service.features.map(feature => 
                    `<li style="padding: 5px 0; border-bottom: 1px solid #e0e0e0;">
                        <span style="color: #4caf50; margin-right: 8px;">✓</span>${feature}
                    </li>`
                ).join('')}
            </ul>
            <a href="servicii.html" style="
                display: inline-block;
                background-color: #667eea;
                color: white;
                padding: 10px 25px;
                border-radius: 5px;
                text-decoration: none;
                transition: background-color 0.3s ease;
            ">Află mai mult</a>
        `;
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        });
        
        cardsWrapper.appendChild(card);
    });

    servicesContainer.appendChild(cardsWrapper);
}
function generatePricingCalculator() {
    const calculatorContainer = document.getElementById('pricing-calculator');
    if (!calculatorContainer) return;

    const calculator = document.createElement('div');
    calculator.style.cssText = `
        background: white;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        max-width: 600px;
        margin: 40px auto;
    `;

    calculator.innerHTML = `
        <h3 style="color: #667eea; font-size: 2rem; margin-bottom: 30px; text-align: center;">
            Calculator Preț Personalizat
        </h3>
        
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 600;">Selectează Serviciul:</label>
            <select id="serviceType" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 5px; font-size: 1rem;">
                <option value="500">Site Prezentare Simple - 500 EUR</option>
                <option value="1500">Site Prezentare Complex - 1500 EUR</option>
                <option value="3000">Site E-commerce - 3000 EUR</option>
                <option value="5000">Aplicație Mobile - 5000 EUR</option>
                <option value="100">Consultanță IT (pe oră) - 100 EUR</option>
            </select>
        </div>

        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 600;">
                Cantitate/Ore: <span id="quantityValue">1</span>
            </label>
            <input type="range" id="quantity" min="1" max="10" value="1" 
                style="width: 100%; height: 8px; border-radius: 5px; background: #e0e0e0;">
        </div>

        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 600;">Tip Client:</label>
            <select id="clientType" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 5px; font-size: 1rem;">
                <option value="0">Client Nou (0% reducere)</option>
                <option value="10">Client Recurent (10% reducere)</option>
                <option value="15">Contract Anual (15% reducere)</option>
                <option value="20">Partnership (20% reducere)</option>
            </select>
        </div>

        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 30px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600;">Subtotal:</span>
                <span id="subtotal">500.00 EUR</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px; color: #4caf50;">
                <span style="font-weight: 600;">Reducere:</span>
                <span id="discount">0.00 EUR</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 1.5rem; font-weight: bold; color: #667eea; padding-top: 15px; border-top: 2px solid #e0e0e0;">
                <span>Total:</span>
                <span id="total">500.00 EUR</span>
            </div>
        </div>

        <p style="margin-top: 20px; text-align: center; color: #666; font-size: 0.9rem;">
            * Prețurile sunt estimate și nu includ TVA (19%)
        </p>
    `;

    calculatorContainer.appendChild(calculator);
    const serviceType = calculator.querySelector('#serviceType');
    const quantity = calculator.querySelector('#quantity');
    const quantityValue = calculator.querySelector('#quantityValue');
    const clientType = calculator.querySelector('#clientType');

    function updatePrice() {
        const unitPrice = parseFloat(serviceType.value);
        const qty = parseInt(quantity.value);
        const discount = parseFloat(clientType.value);

        quantityValue.textContent = qty;

        const subtotal = unitPrice * qty;
        const discountAmount = subtotal * (discount / 100);
        const total = calculatePrice(unitPrice, qty, discount);

        calculator.querySelector('#subtotal').textContent = formatCurrency(subtotal);
        calculator.querySelector('#discount').textContent = '-' + formatCurrency(discountAmount);
        calculator.querySelector('#total').textContent = formatCurrency(total);
    }

    serviceType.addEventListener('change', updatePrice);
    quantity.addEventListener('input', updatePrice);
    clientType.addEventListener('change', updatePrice);
}
function handleContactForm() {
    const form = document.getElementById('contactForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            company: document.getElementById('company').value,
            service: document.getElementById('service').value,
            budget: document.getElementById('budget').value,
            message: document.getElementById('message').value
        };
        alert(`Mulțumim, ${formData.name}!\n\nMesajul tău a fost trimis cu succes. Îți vom răspunde în maxim 24 de ore la adresa ${formData.email}.\n\nDetalii:\n- Serviciu: ${formData.service}\n- Buget: ${formData.budget}`);
        form.reset();
    });
}
function updateCopyrightYear() {
    const footerBottom = document.querySelector('.footer-bottom p');
    if (footerBottom) {
        footerBottom.textContent = `© ${currentYear} TechSolutions. Toate drepturile rezervate.`;
    }
}
function enableSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    updateCopyrightYear();
    generateSpecialOffer();
    generateServiceCards();
    generatePricingCalculator();
    handleContactForm();
    enableSmoothScrolling();
    
    console.log('TechSolutions website initialized successfully!');
    console.log(`Current year: ${currentYear}`);
});

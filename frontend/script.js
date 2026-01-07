// AI Website Generator - Frontend JavaScript

const API_URL = '/api';

// Éléments du DOM
const form = document.getElementById('websiteForm');
const loadingContainer = document.getElementById('loadingContainer');
const resultContainer = document.getElementById('resultContainer');
const generateBtn = document.getElementById('generateBtn');

// Gestion du formulaire
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Récupérer les données du formulaire
    const formData = new FormData(form);
    const pages = Array.from(form.querySelectorAll('input[name="pages"]:checked'))
        .map(cb => cb.value);

    const saveAsBlueprint = formData.get('saveAsBlueprint') === 'on';

    const requestData = {
        business_name: formData.get('businessName'),
        business_description: formData.get('businessDescription'),
        industry: formData.get('industry') || null,
        target_audience: formData.get('targetAudience') || null,
        language: formData.get('language'),
        pages: pages.length > 0 ? pages : null,
        save_as_blueprint: saveAsBlueprint,
        blueprint_name: saveAsBlueprint ? formData.get('businessName') : null
    };

    // Afficher le loading
    form.style.display = 'none';
    loadingContainer.style.display = 'block';

    // Animation des étapes
    animateSteps();

    try {
        // Appel à l'API
        const response = await fetch(`${API_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            throw new Error('Erreur lors de la génération du site');
        }

        const result = await response.json();

        // Afficher les résultats
        showResults(result);

    } catch (error) {
        console.error('Erreur:', error);
        alert('Une erreur est survenue lors de la génération du site. Veuillez réessayer.');

        // Réinitialiser l'affichage
        loadingContainer.style.display = 'none';
        form.style.display = 'block';
    }
});

// Animation des étapes de chargement
function animateSteps() {
    const steps = document.querySelectorAll('.step');
    let currentStep = 0;

    const interval = setInterval(() => {
        if (currentStep > 0) {
            steps[currentStep - 1].classList.remove('active');
        }

        if (currentStep < steps.length) {
            steps[currentStep].classList.add('active');
            currentStep++;
        } else {
            clearInterval(interval);
        }
    }, 2000);
}

// Afficher les résultats
function showResults(result) {
    loadingContainer.style.display = 'none';
    resultContainer.style.display = 'block';

    // Message
    let message = result.message;
    if (result.blueprint_id) {
        message += ` (Blueprint sauvegardé: ${result.blueprint_id})`;
    }
    document.getElementById('resultMessage').textContent = message;

    // Lien de téléchargement
    document.getElementById('downloadLink').href = result.download_url;

    // Liste des pages
    const pagesList = document.getElementById('pagesList');
    pagesList.innerHTML = '';

    result.pages.forEach(page => {
        const li = document.createElement('li');
        li.textContent = page;
        pagesList.appendChild(li);
    });

    // Scroll vers les résultats
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

// Animation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    // Ajouter une animation aux features
    const features = document.querySelectorAll('.feature');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.animation = `fadeInUp 0.6s ease forwards`;
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    features.forEach(feature => {
        feature.style.opacity = '0';
        observer.observe(feature);
    });
});

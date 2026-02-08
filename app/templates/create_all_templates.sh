#!/bin/bash

# Index.html avec animations premium
cat > index.html << 'EOFINDEX'
{% extends "base.html" %}
{% block title %}Dashboard{% endblock %}

{% block content %}
<style>
.hero-gradient {
    background: var(--gradient-1);
    min-height: 500px;
    display: flex;
    align-items: center;
    border-radius: 30px;
    margin-bottom: 4rem;
    position: relative;
    overflow: hidden;
}

.hero-gradient::before {
    content: '';
    position: absolute;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.metric-card-premium {
    background: var(--bg-primary);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: var(--shadow);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: 1px solid var(--border-color);
}

.metric-card-premium:hover {
    transform: translateY(-10px);
    box-shadow: var(--shadow-lg);
}

.metric-icon-premium {
    width: 70px;
    height: 70px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: white;
    margin-bottom: 1.5rem;
}

.metric-value-premium {
    font-size: 3rem;
    font-weight: 800;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.feature-card-premium {
    background: var(--bg-primary);
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: var(--shadow);
    transition: all 0.3s ease;
    border: 1px solid var(--border-color);
    height: 100%;
}

.feature-card-premium:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.feature-icon-premium {
    width: 80px;
    height: 80px;
    border-radius: 20px;
    background: var(--gradient-1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    color: white;
    margin-bottom: 1.5rem;
}

.btn-premium {
    padding: 0.875rem 2rem;
    border-radius: 12px;
    font-weight: 600;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
}

.btn-primary-premium {
    background: var(--gradient-1);
    color: white;
}

.btn-primary-premium:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    margin-bottom: 4rem;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
}
</style>

<div class="container">
    <!-- Hero Section -->
    <div class="hero-gradient" data-aos="fade-up">
        <div style="position: relative; z-index: 1; padding: 4rem; color: white;">
            <h1 style="font-size: 3.5rem; margin-bottom: 1.5rem; font-weight: 800;">
                Intelligence Artificielle<br>Sécurité Biométrique
            </h1>
            <p style="font-size: 1.3rem; opacity: 0.95; margin-bottom: 2rem; max-width: 600px;">
                Plateforme avancée de classification avec protection contre les attaques adversariales
            </p>
            {% if not session.user %}
            <a href="{{ url_for('main.login') }}" class="btn-premium btn-primary-premium">
                <i class="fas fa-rocket"></i> Commencer maintenant
            </a>
            {% endif %}
        </div>
    </div>
    
    <!-- Metrics -->
    <div class="stats-grid">
        <div class="metric-card-premium" data-aos="fade-up" data-aos-delay="100">
            <div class="metric-icon-premium" style="background: linear-gradient(135deg, #667eea, #764ba2);">
                <i class="fas fa-brain"></i>
            </div>
            <h3 class="metric-value-premium">92.3%</h3>
            <p style="color: var(--text-secondary); font-weight: 500; margin: 0;">Accuracy Baseline</p>
        </div>
        
        <div class="metric-card-premium" data-aos="fade-up" data-aos-delay="200">
            <div class="metric-icon-premium" style="background: linear-gradient(135deg, #f093fb, #f5576c);">
                <i class="fas fa-shield-alt"></i>
            </div>
            <h3 class="metric-value-premium">91.2%</h3>
            <p style="color: var(--text-secondary); font-weight: 500; margin: 0;">Modèle Robuste</p>
        </div>
        
        <div class="metric-card-premium" data-aos="fade-up" data-aos-delay="300">
            <div class="metric-icon-premium" style="background: linear-gradient(135deg, #4facfe, #00f2fe);">
                <i class="fas fa-shield-virus"></i>
            </div>
            <h3 class="metric-value-premium">83.4%</h3>
            <p style="color: var(--text-secondary); font-weight: 500; margin: 0;">Robustesse FGSM</p>
        </div>
        
        <div class="metric-card-premium" data-aos="fade-up" data-aos-delay="400">
            <div class="metric-icon-premium" style="background: linear-gradient(135deg, #fa709a, #fee140);">
                <i class="fas fa-layer-group"></i>
            </div>
            <h3 class="metric-value-premium">3</h3>
            <p style="color: var(--text-secondary); font-weight: 500; margin: 0;">Modèles Disponibles</p>
        </div>
    </div>
    
    <!-- Features -->
    <h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 3rem;" data-aos="fade-up">
        <i class="fas fa-star" style="color: #fbbf24;"></i> Fonctionnalités
    </h2>
    
    <div class="features-grid">
        <div class="feature-card-premium" data-aos="fade-up" data-aos-delay="100">
            <div class="feature-icon-premium">
                <i class="fas fa-vial"></i>
            </div>
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">Test de Modèles</h3>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                Testez vos images sur les 3 modèles : Baseline, Empoisonné et Robuste
            </p>
            {% if session.user %}
            <a href="{{ url_for('main.test') }}" class="btn-premium btn-primary-premium">
                Essayer <i class="fas fa-arrow-right"></i>
            </a>
            {% endif %}
        </div>
        
        <div class="feature-card-premium" data-aos="fade-up" data-aos-delay="200">
            <div class="feature-icon-premium" style="background: linear-gradient(135deg, #f093fb, #f5576c);">
                <i class="fas fa-code-compare"></i>
            </div>
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">Comparaison</h3>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                Comparez les performances des modèles côte à côte
            </p>
            {% if session.user %}
            <a href="{{ url_for('main.compare') }}" class="btn-premium" style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white;">
                Comparer <i class="fas fa-arrow-right"></i>
            </a>
            {% endif %}
        </div>
        
        <div class="feature-card-premium" data-aos="fade-up" data-aos-delay="300">
            <div class="feature-icon-premium" style="background: linear-gradient(135deg, #4facfe, #00f2fe);">
                <i class="fas fa-bug-slash"></i>
            </div>
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">Attaques Adversariales</h3>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                Générez des attaques FGSM, PGD et Data Poisoning
            </p>
            {% if session.user %}
            <a href="{{ url_for('main.attacks') }}" class="btn-premium" style="background: linear-gradient(135deg, #4facfe, #00f2fe); color: white;">
                Tester <i class="fas fa-arrow-right"></i>
            </a>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
EOFINDEX

echo "✅ index.html créé"


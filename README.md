# 📎 PDF Fusion Tool

Un outil open source **moderne** et **intuitif** pour fusionner jusqu’à 150 fichiers PDF en ligne, avec tri intelligent par date extraite du nom, renommage dynamique, et gestion de très gros volumes (jusqu’à 1 Go d’upload).

---

## 🚀 Fonctionnalités principales

- **Fusion de 2 à 150 fichiers PDF** en un clic, sans perte de qualité
- **Tri automatique** des fichiers avant fusion  
  - Par date détectée dans le nom (`jour-mois-année`, `mois-année`, etc.)
  - Sinon, tri alphabétique
  - Affichage explicite de l’ordre de fusion
- **Renommage du fichier fusionné** avant téléchargement
- **Affichage dynamique** du nombre et du poids total des fichiers uploadés
- **Réinitialisation complète** du formulaire en un clic
- **Compatible gros volumes** : jusqu’à 1 Go de fichiers PDF (si machine adaptée)
- **Interface moderne, responsive, facilement personnalisable (CSS/Tailwind)**

---

## 🏗️ Architecture et conception

```bash
pdf_merge_app/
├── fusion/
│   ├── __init__.py                # Marqueur de module Python
│   └── fusion.py                  # Logique de fusion PDF
├── streamlit_app.py               # Application principale Streamlit (UI/UX & orchestration)
├── requirements.txt               # Dépendances Python
├── static/                        # (optionnel) Feuilles de style CSS custom
├── .streamlit/
│   └── config.toml                # Configuration avancée Streamlit (limite upload, etc.)
└── README.md                      # Documentation du projet

```

### Points clés de conception

- Separation of concerns : la logique de fusion est indépendante de la couche UI (peut être réutilisée dans d’autres projets, CLI, API…)

- Session state Streamlit : pour gérer l’état entre uploads, reset et téléchargements

- Tri des fichiers : tout upload est analysé et ordonné avant écriture sur disque/temp

- Robustesse : gestion des erreurs d’upload, poids, nombre de fichiers, etc.

- Extensible : support d’autres modes de tri, d’autres backends, etc.

## ⚙️ Installation & lancement

### 1. Cloner le repo

```bash
git clone https://github.com/votre-pseudo/pdf_merge_app.git
cd pdf_merge_app

```

### 2. Créer un environnement virtuel (optionnel mais recommandé)

```bash
python3 -m venv venv
source venv/bin/activate   # sous Windows : venv\Scripts\activate

```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt

```

### 4. Configurer la limite d’upload (facultatif, recommandé pour gros volumes)

Crée un fichier ```.streamlit/config.toml``` avec :

```bash
[server]
maxUploadSize = 1000

```

Ou lance l’application avec l’option CLI :

```bash
streamlit run streamlit_app.py --server.maxUploadSize=1000

```

### 5. Lancer l’application

```bash
streamlit run streamlit_app.py

```

Ouvre ```http://localhost:8501``` dans ton navigateur.

## 🖥️ Utilisation

1. Glisse-dépose ou sélectionne jusqu’à 150 fichiers PDF (poids total ≤ 1 Go)

2. Visualise le nombre et le poids des fichiers uploadés

3. Clique sur Fusionner les PDF

4. L’ordre de fusion s’affiche (par date détectée ou alphabétique)

5. Nomme le fichier fusionné selon ton besoin

6. Télécharge le PDF fusionné !

7. Clique sur Réinitialiser pour recommencer

## 🧠 Tri automatique et formats reconnus

Le projet essaie de détecter la date dans les noms de fichiers :

Formats : depot-12_06_2025.pdf, facture-06_2025.pdf, note-2025-06-12.pdf, etc.

S’il ne trouve pas de date, il trie par nom.

Le tri est extensible à d’autres patterns : personnalisez extract_date() dans streamlit_app.py !

## 🚫 Limites connues

Upload total limité à 1 Go (Streamlit)

Impossible de drag & drop manuellement l’ordre des fichiers en pur Streamlit natif (sauf composant custom ou JS)

Les fichiers sont gardés temporairement en mémoire/disque pendant la session : nécessite une machine avec RAM/espace adaptés si gros volumes

Pas de preview des PDF ni édition avancée (rotation, extraction de pages…) — ce projet est spécialisé sur la fusion rapide et fiable

## 🛣️ Roadmap & idées de contribution

Ajout d’un composant drag & drop de tri manuel (ex : streamlit-sortables)

Compression optionnelle du PDF final

Historique des fusions pour utilisateurs identifiés

API REST pour intégration à d’autres outils

Contributions bienvenues !
Ouvre une issue ou une PR avec tes idées.

## Auteurs et crédits

Idée, conception, dev : Ton nom ou pseudo

Basé sur Streamlit et PyPDF2

## Licence

Projet sous licence MIT — libre à l’usage, à la modification et à la redistribution.

```bash 
Besoin d’aide ?
Contact : ton.email@email.com

```
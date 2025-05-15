# API Génération PDF Pro - Ferraillage

Cette API accepte un appel POST avec les données d'une structure béton (poutre, dalle, poteau, semelle).
Elle génère un PDF professionnel avec plan, coupes, tableau d’armatures.

## Exemple de JSON

{
  "structure": "poutre",
  "dimensions": { "longueur": 5000, "largeur": 300, "hauteur": 500 },
  "ferraillage": { "ha": "HA12", "nb_barres": 4, "etrs": "8@20" }
}

## Résultat
→ Un PDF complet est généré dans /output/ et renvoyé immédiatement.
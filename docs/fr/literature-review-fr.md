# Viser le 116 keV pour lire PHerc0800

*Rapport de synthèse, 19 novembre 2026. Conventions de fiabilité utilisées partout : **[ORG]** = fait publié par les organisateurs (scrollprize.org, Substack officiel, arXiv de l'équipe) ; **[AUTEUR]** = affirmation d'un auteur (README, carte Hugging Face), non vérifiée par les organisateurs ; **[TIERS]** = re-mesure communautaire indépendante, non officielle ; **[NOS ESSAIS]** = nos propres expériences ; **[INFÉRENCE]** = notre raisonnement.*

## Résumé exécutif

**Les trois prix First Letters 2026 ont été gagnés par trois recettes différentes, mais toutes reposent sur deux préalables : une grande surface bien segmentée (spiral fitter + accrochage aux prédictions de surface m7) et un modèle d'encre adapté au régime de scan de la cible.** Sur PHerc. 343 (8,64 µm / 116 keV, le même protocole que PHerc0800), un simple ensemble de modèles 9 µm existants a suffi ([ORG](https://scrollprize.substack.com/p/50k-first-letters-prize-awarded-for)). Sur PHerc. 306B (même session ESRF de mai 2025 que PHerc0800), la carte gagnante est le **produit** de TRACE v3B et d'un fine-tune de v8-in entraîné sur des labels humains **à 116 keV** de PHerc. 1447 et sur des pseudo-labels du même rouleau ([ORG](https://scrollprize.substack.com/p/writing-seen-in-pherc-306b-for-the)). Sur PHerc. 211, le gagnant attribue l'essentiel du succès à la **distillation d'encre 2 µm → 9 µm** depuis des rouleaux « similaires », dont PHerc0009B, choisis par similarité DINO ([ORG](https://scrollprize.substack.com/p/first-letters-emerge-from-pherc-211)). Pour PHerc0800, notre résultat négatif avec ink_9um n'est **pas une preuve d'absence d'encre** : ce modèle n'a vu aucun scan à 116 keV et la communauté ne lui trouve aucun texte sur PHerc1447, alors que des lettres y ont été trouvées depuis ([AUTEUR](https://github.com/Ritwik-Gaur/vesuvius-energy-transfer)). Les leviers les plus rentables sont donc, dans l'ordre : (1) terminer l'ensemble « conscient du 116 keV » (Studio, Reader v3, Argus v3) avec contrôles ; (2) reproduire la recette 306B (A-hn × TRACE v3B) ; (3) **multiplier la surface** au-delà des 9,2 cm² publics par spiral fitting, puisque les gagnants ont balayé des bandes entières ; (4) seulement ensuite, distillation 0009B et auto-apprentissage. PHerc0800 reste éligible ; 7 prix de 50 000 $ restent ouverts jusqu'au 25 juin 2027, et rien n'exclut une soumission concurrente en cours d'examen ([ORG](https://scrollprize.org/prizes)).

## Trois recettes gagnantes, un même socle géométrique

Ce qui ressort des comptes rendus, c'est que **personne n'a trouvé les premières lettres d'un rouleau 9 µm de 2026 en scrutant 9 cm²**. Nieuwlaar a ajusté une spirale complète, l'a accrochée à la surface m7, a fusionné deux spires (w047/w048) et a rendu 66 couches sur toute la bande z 9500–11000 ([AUTEUR](https://github.com/Nieuwlaar/pherc343-first-letters)). Warner et Bodill ont choisi leur graine GrowPatch en criblant des spires du spiral fitter public ([ORG](https://scrollprize.substack.com/p/writing-seen-in-pherc-306b-for-the)). Aranke est parti d'un ajustement spiral sur toute la hauteur, raffiné à la main dans son fork VC3D Manual ([ORG](https://scrollprize.substack.com/p/first-letters-emerge-from-pherc-211)). Aucun gagnant ne publie la surface totale balayée, mais l'ordre de grandeur dépasse de loin celui de nos 6 segments.

| Rouleau (date) | Scan | Segmentation | Modèle(s) d'encre | Origine du premier signal | Validation acceptée |
|---|---|---|---|---|---|
| **PHerc. 343** (oct. 2026, Nieuwlaar) | 8,64 µm / 116 keV ESRF, `20250509220833` [AUTEUR] | Spiral fitter + umbilic perso, accrochage m7, aplatissement lasagna, w047+w048 fusionnées | Moyenne z-scorée de ink_9um s42/s43 (75k), Hecate 9,6 µm, dense_native ; profondeurs −15…+15 | **Croisé pur, sans entraînement sur 343** ; texture « bien structurée » repérée à l'œil puis creusée ([ORG](https://scrollprize.substack.com/p/50k-first-letters-prize-awarded-for)) | ≥10 lettres lisibles, papyrologues |
| **PHerc. 306B** (oct./nov. 2026, Warner & Bodill) | ESRF ; volume `20250521133212`, 8,64 µm / 116 keV [AUTEUR] | VC3D GrowPatch sur m7, graine choisie par criblage de spires | **Produit** TRACE v3B × A-hn (v8-in fine-tuné 3×600 pas sur labels humains 1447 + pseudo-labels 306B, pénalité faux positifs) | Croisé + labels 116 keV d'un rouleau frère + auto-apprentissage ; des centaines d'heures d'annotation manuelle ([ORG](https://scrollprize.substack.com/p/writing-seen-in-pherc-306b-for-the)) | Plusieurs soumissions convergentes ; l'image a tranché un désaccord des papyrologues |
| **PHerc. 211** (15 nov. 2026, Aranke) | « ~9 µm natif » ; keV non publié | Spiral fit pleine hauteur, VC3D Manual, croissance guidée par DinoVol | Studio : U-Net 3D résiduel 223 M param., 16 plans, étape finale *soft loss* | **Distillation 2 µm → 9 µm** depuis 0814/0841/0009B choisis par similarité DINO ; jamais entraîné sur un rouleau en compétition ([ORG](https://scrollprize.substack.com/p/first-letters-emerge-from-pherc-211)) | 11 lettres dans un rectangle de 4 cm, consensus des papyrologues |
| **PHerc. 1447** (sept. 2026, hors prix) | 8,64 µm / 116 keV [AUTEUR] | n.d. | Nouvelle recette 9 µm de Y. Nader : « quelques traits sans fine-tuning, une dizaine de lettres avec » ([AUTEUR](https://github.com/TAUIL-Abd-Elilah/pherc1447-ink-survey)) | Fine-tune sur le rouleau ; retiré de la liste First Letters ([ORG via X](https://x.com/scrollprize/status/2105000581953699899)) | Annonce officielle, pas de compte rendu détaillé |
| **PHerc. 172 / Scroll 5** (nov. 2024) | 7,91 µm / 53 keV, Diamond | Manuelle + ThaumatoAnakalyptor | Aucun au départ | **Encre visible à l'œil dans le CT** ([ORG](https://scrollprize.substack.com/p/first-letters-found-in-new-scroll)) | Annotations « conservatrices », relecteurs indépendants |
| **0814, 0841, 0139, 0009B** (oct. 2025, préliminaire) | Scans 2 µm + 9 µm | Équipe VC | Modèle généraliste 2 µm + distillation vers 9 µm | Le signal à 9 µm est faible (taches éparses) ([ORG](https://scrollprize.substack.com/p/multiple-scrolls-now-show-greek-letters)) | Qualitative, « préliminaire » |

Ces cas se lisent comme un gradient de difficulté. Quand le régime de scan est déjà couvert par les modèles publics, comme pour 343 en octobre, un ensemble prêt à l'emploi suffit. Sinon, il faut des **labels pris dans le bon régime** : des labels humains à 116 keV pour 306B, de l'encre 2 µm distillée pour 211. Aranke le résume ainsi : « *the training data mattered much more* » ([ORG](https://scrollprize.substack.com/p/first-letters-emerge-from-pherc-211)). **[INFÉRENCE]** PHerc0800 tombe dans la seconde catégorie, mais avec un atout rare : les identifiants de volume (`20250521135224` pour 0800, `…125136` pour 0009B, `…133212` pour 306B) indiquent la même reconstruction ESRF du 21 mai 2025. Les organisateurs ne le disent pas, mais 343 et 306B, déjà lus, partagent donc presque certainement l'appareil et les réglages de PHerc0800.

## Les modèles qui ont déjà vu la session de scan de PHerc0800

Il n'existe **aucun benchmark officiel** des modèles 9 µm. ink_9um et Hecate n'ont aucune métrique publiée ([ORG](https://huggingface.co/scrollprize/ink_9um), [ORG](https://huggingface.co/scrollprize/hecate)). Le seul test aveugle sérieux à 116 keV est PHerc1447 (w058/w060), qu'aucun modèle du tableau n'a vu à l'entraînement, et même là, w060 n'est « lisible pour aucun modèle 9 µm testé » ([AUTEUR](https://github.com/DomRusso2/reader-v3)). Les AUC sur 0009B surestiment la généralisation des modèles entraînés sur ce rouleau. En contrepartie, ce sont exactement ces modèles qui ont appris l'apparence de la session de PHerc0800.

| Modèle (licence) | Archi / taille | 0009B à l'entraînement ? | Métriques 116 keV (statut) | Coût sur nos machines | Statut pour nous |
|---|---|---|---|---|---|
| **ink_9um** s42/s43 (MIT, ORG) | Tige 3D + U-Net 2D, 34,6 M | **Non** (0139, 1667, Paris 4, 0814 ; aucun 116 keV) | 1447 ≈ 0,67–0,68 AUC poolé [TIERS](https://github.com/EhimenNathan/vesuvius-ink-generalization) ; offset-sweep 0,732 [TIERS](https://github.com/LynnHenry/offset-sweep) | 30–40 s/segment en fp32 [NOS ESSAIS] | Fait : rien de lisible |
| **Reader v2** (MIT) | idem, fine-tune 12k pas à 116 keV | **Oui** : 14 segments 0009B (vol. `…125136`), 4 tenus à l'écart ([AUTEUR](https://huggingface.co/datasets/domenicor046/reader-v2-labels)) | 0009B tenu à l'écart 0,927 vs humain ; sur 1447, « une forme de lettre » seulement ([AUTEUR](https://huggingface.co/domenicor046/reader-v2)) | Comme ink_9um | Optionnel |
| **Reader v3** (MIT) | idem, tuiles 256→384 px | **Oui** (mêmes données que v2) | 0009B 0,943 vs humain ; 1447 w058 0,856 ([AUTEUR](https://github.com/DomRusso2/reader-v3)) ; 0,842 en re-mesure [TIERS](https://github.com/LynnHenry/offset-sweep) ; premier de Crackle Check sur 0841 [TIERS](https://huggingface.co/spaces/SharpMeow/crackle-check/raw/main/README.md) | ~0,6 Go VRAM mesuré [TIERS] → OK sur GTX 1650 fp32 | **En cours** |
| **Argus v2 / v3** (MIT) | idem ; v3 = soupe de 4 fine-tunes de Reader v3 | **Oui** (v2 : 0009B + 0343P à 116 keV ; v3 : 70 segments reader-v2-labels) | 1447 w058 0,860 / w060 0,791 ; AUC en ordre inversé 0,512 ([AUTEUR](https://huggingface.co/ruiconte/argus-v3)) ; v2 « vérifié » par deux tiers, selon l'auteur | Comme ink_9um | **En cours** (fenêtres −2/0/+2) |
| **Studio soft-loss** (code MIT, **poids CC BY-NC 4.0**) | DeepResidualUNet 223 M, 16 plans | **Oui, à partir de zéro** sur 0009B `…125136` + 0814 + 0841 ([AUTEUR](https://github.com/priyankaranke/vesuvius-studio-multiscroll-cpt)) | Aucune métrique 116 keV ; AP sur 211 0,81→0,82, que l'auteur juge non généralisable ; **a produit les lettres primées de 211** [ORG] | 1,7 Go fp32, ~3 min/Mpx [NOS ESSAIS] → ~1 h 15 par ordre de plans pour les 6 segments, car l'inférence balaie toute la boîte englobante (~26 Mpx) [NOS ESSAIS] | **En cours** |
| **v8-in** (MIT) | ResNet3D-50 + U-Net 2D, 83 M | Validation seulement (0009B_ag132115) | 1447 w058/w060 0,863/0,812 [TIERS](https://github.com/EhimenNathan/vesuvius-ink-generalization), mais 46 % de papyrus vierge marqué selon Reader v3 [AUTEUR] | ~11 Go à batch 16 → T4, ou batch 1–2 en local | À tester |
| **A-hn** (v8-in fine-tuné, Prodigle) | 83 M | Non, mais **labels 1447 à 116 keV + pseudo-labels 306B** | Produit avec TRACE : faux positifs à 6,1 % sur 0841 tenu à l'écart, AUC 0,874 ([AUTEUR](https://github.com/SirProdigle/pherc0306b-first-letters/blob/main/docs/METHOD.md)) | T4 | **Priorité** ; licence à vérifier sur la [carte HF](https://huggingface.co/Prodigle/pherc0306b-ink-ahn) |
| **TRACE v3B** (CC BY-NC-SA) | n.d. | n.d. | Moitié de la carte gagnante de 306B [ORG] | Via [ink-sdk](https://github.com/LimeGS/ink-sdk) | **Priorité** |
| **Hecate 9,6 µm** (MIT, ORG, « expérimental ») | 3D → attention → 2D | Non | Aucune métrique ; sur **les 10 surfaces 0800/1203 auditées**, il marque plus de pixels sur une entrée mélangée que sur la vraie ([TIERS](https://github.com/aviad12g/vesuvius-depth-order-control)) ; 57,6 % de papyrus vierge marqué [AUTEUR] | fp32 batch 1 | Seulement sous contrôle |

**Deux conséquences pratiques.** D'abord, ink-sdk regroupe Reader v2/v3, Argus v2, Hecate, TRACE v3B, v8-in, Studio et dense_native derrière une seule CLI, accepte des maillages tifxyz, lance les deux sens et applique un filtre de vitalité (EMPTY/DEGENERATE/ALIVE) ([AUTEUR](https://github.com/LimeGS/ink-sdk)). Il évite d'écrire un wrapper par modèle. Ensuite, un piège de données existe : dans 18 des 33 volumes du bucket `ink/` des organisateurs (dont 0009B, 0814, 0841), le niveau 2 ne garde que les 17 premières tranches au lieu d'un pooling en profondeur. Dans ce cas, ink_9um tombe à 0,54 d'AUC sur sa propre source ([TIERS](https://github.com/EhimenNathan/vesuvius-ink-generalization)). Toute distillation depuis 0009B doit reconstruire ce niveau.

**[NOS ESSAIS] Point à surveiller pour Studio.** Le README impose d'empiler les plans **23 → 8, en ordre inversé** ([AUTEUR](https://github.com/priyankaranke/vesuvius-studio-multiscroll-cpt)). Nous avons validé l'ordre « montant » 7→22 sur un crop de w035. C'est cohérent si nos rendus ont la normale inversée par rapport à ceux de VC (`--flip-normals`), et le décalage d'un plan reste dans la tolérance de ±2 voxels mesurée par offset-sweep. Mais 0139 figure dans les données d'entraînement de Studio (groupe « expanded9 »), donc ce contrôle positif n'est pas aveugle. Il suffit à fixer l'orientation, pas à estimer la sensibilité. Garder les deux ordres pour chaque segment de PHerc0800.

## Contrôles anti-faux-positifs : ce que nos premiers résultats nous apprennent déjà

Nos premières cartes ink_9um présentent exactement les artefacts documentés : les réponses les plus fortes tombent sur une **couture horizontale**, sur des **zones abîmées** et sur des **bords de segment** [NOS ESSAIS]. La communauté montre que les fondus de recouvrement « fabriquent des bords sur une grille régulière » sur des segments partiellement couverts, et que des surfaces de PHerc1447 n'avaient en médiane que 46 % de CT non nul, ce qui donne une sortie constante qui ressemble à « pas d'encre » ([TIERS](https://github.com/TAUIL-Abd-Elilah/pherc1447-ink-survey)). Les organisateurs préviennent que dans les zones fortement déformées, les modèles produisent « des choses qui ressemblent beaucoup à des lettres » ([ORG](https://scrollprize.substack.com/p/from-ct-scan-to-ancient-text-a-first)). Enfin, le surplus de réponse en sens direct sur 3 segments n'est **pas discriminant** : sur PHerc0800, le ratio direct/inverse du contrôle 0139 (1,33) tombait à l'intérieur de la plage des segments cibles (1,18–1,38), et aucun critère automatique (nombre de candidats, densité, élongation des taches) n'a séparé lettres et vierge ([TIERS](https://github.com/nerln/vesuvius-first-letters-pherc0800)). Le « phi » qui changeait d'une couche à l'autre [NOS ESSAIS] illustre le critère des organisateurs : de l'encre réelle reste géométriquement collée à une couche et forme des lignes parallèles aux fibres ([ORG](https://arxiv.org/html/2606.29085v1)).

Le protocole à appliquer à tout candidat combine six tests documentés. (a) **Inversion ou mélange de l'ordre de profondeur.** L'encre réelle s'effondre en sens inverse : AUC 0,51–0,53 pour Argus et Reader, 0,915 → 0,595 sur la démo d'Ink Lens [TIERS] ; sur notre contrôle w035, le texte n'apparaît qu'en sens direct [NOS ESSAIS, visuel, sans AUC] ([AUTEUR](https://huggingface.co/ruiconte/argus-v3)). Sur 306B, la proportion de pixels sombres dans la boîte est passée de 8,6 % à 0,00 % après mélange ([AUTEUR](https://github.com/SirProdigle/pherc0306b-first-letters/blob/main/docs/METHOD.md)). Attention, ce test ne vaut que pour les modèles entraînés sans retournement de profondeur : Argus v1 avec retournement conservait 0,79 en sens inverse. (b) **Accord ou produit de modèles d'architectures différentes** (famille ink_9um contre v8-in/A-hn contre Studio). Sur le texte de 1447, la corrélation inter-modèles atteint r = 0,69 (0,89 sur la meilleure fenêtre) et tombe à −0,16 après mélange. **Sur les surfaces de PHerc0800 et 1203, la médiane n'est que de 0,12** ([TIERS](https://github.com/aviad12g/vesuvius-depth-order-control)), et un accord qui monte est donc un signal mesurable. (c) **Tolérance au décalage.** Une encre réelle varie de moins de 0,03 d'AUC à ±2 voxels ; un motif qui n'apparaît qu'à un décalage extrême est suspect ([TIERS](https://github.com/LynnHenry/offset-sweep)). (d) **Témoin vierge pré-enregistré et leurre.** Sur 306B : une région témoin fixée d'avance (0,42 %) et des labels décalés de 3,5 × 3 mm, qui donnent des traits plus flous. (e) **Zone d'exclusion 3D ≥ 2 mm** entre tout pixel d'entraînement et la zone revendiquée ([AUTEUR](https://github.com/SirProdigle/pherc0306b-first-letters/blob/main/docs/METHOD.md)). (f) **Contrôles géométriques.** Il faut vérifier en coupe que le maillage reste sur une seule feuille, puisque « une bonne surface reste sur une feuille » ([ORG](https://scrollprize.substack.com/p/from-ct-scan-to-ancient-text-a-first)), et masquer bords, coutures et trous avant toute statistique. Les seuils par pixel sont trompeurs : même Reader v3 marque environ 30 % du fond à 80 % de rappel sur 0841+1447 ([AUTEUR](https://github.com/DomRusso2/reader-v3)). Comme le dit l'auteur du test PHerc0800, « *the verdict is visual* » ([TIERS](https://github.com/nerln/vesuvius-first-letters-pherc0800)).

## Stratégies classées pour PHerc0800

Le classement suit le gain attendu divisé par le coût sur notre matériel (GTX 1650 4 Go en fp32 seulement, ~10 Go de RAM, T4 Kaggle/Colab gratuit). Repère de surface : à 8,64 µm, 1 cm² ≈ 1,34 Mpx, nos 9,2 cm² font ≈ 12,3 Mpx, et une boîte de prix de 4 cm² mesure ≈ 2 315 × 2 315 px **[INFÉRENCE]**.

### 1. Ensemble « session-aware » sous contrôles sur les 6 segments existants

**Justification.** Studio, Reader v3 et Argus v3 sont les seuls modèles publics entraînés sur le volume 0009B `20250521125136`, issu de la même reconstruction que PHerc0800. Studio a produit des lettres primées sur 211 ([ORG](https://scrollprize.substack.com/p/first-letters-emerge-from-pherc-211)). Sur 1447, Argus v3 et Reader v3 sont les meilleurs modèles de la famille ink_9um ([AUTEUR](https://huggingface.co/ruiconte/argus-v3)). Le précédent 343 montre qu'un ensemble z-scoré de modèles croisés peut suffire sur ce protocole ([ORG](https://scrollprize.substack.com/p/50k-first-letters-prize-awarded-for)).

**Gain attendu :** modéré. Si l'encre de 0800 ressemble à celle de 0009B, c'est ici qu'elle apparaîtra d'abord ; la surface reste toutefois limitée à 9,2 cm².

**Coût :** quasi nul. Les calculs tournent déjà : ~2 h 30 pour Studio sur l'ensemble des segments dans les deux ordres de plans, moins d'une minute par segment et par passe pour Reader/Argus.

**Premier test peu coûteux :** z-scorer chaque carte après masquage des bords et coutures. Calculer pixel à pixel le **minimum** (ou le produit) Studio × Argus v3. Comparer la carte directe et la carte inverse côte à côte, et regarder des lignes, pas des taches.

**Risques :** confondre familiarité avec la session et généralisation. Les trois modèles partagent les labels de 0009B, ce qui rend leurs erreurs corrélées, et leur accord vaut moins qu'un accord avec v8-in/A-hn.

### 2. Reproduire la recette 306B : produit A-hn × TRACE v3B

**Justification.** C'est la seule carte gagnante produite **sur la même session ESRF**, avec un modèle entraîné sur des labels humains à 116 keV (1447). La règle du produit a ramené le taux de faux positifs de 8,5–12,3 % à 6,1 % sur 0841 tenu à l'écart ([AUTEUR](https://github.com/SirProdigle/pherc0306b-first-letters/blob/main/docs/METHOD.md)). ink-sdk implémente déjà ce produit ([AUTEUR](https://github.com/LimeGS/ink-sdk)).

**Gain attendu :** élevé, car c'est l'architecture la plus différente de la famille ink_9um. Le croisement avec la stratégie 1 donne le test (b) gratuitement.

**Coût :** v8-in demande ~11 Go à batch 16 et doit donc tourner sur un T4 Kaggle, à raison de quelques dizaines de minutes pour les 6 segments **[INFÉRENCE]**. En local, il faut passer à batch 1–2 en fp32.

**Premier test peu coûteux :** passer A-hn et TRACE v3B en sens direct et inverse sur le contrôle positif w035 puis sur les 2 segments de 0800 les plus réactifs, et produire la carte produit.

**Risques :** licence TRACE CC BY-NC-SA (partage à l'identique) ; licence A-hn non vérifiée. Les pseudo-labels de 306B dans A-hn ne recouvrent pas 0800, il n'y a donc aucun conflit avec la règle de non-chevauchement.

### 3. Multiplier la surface par spiral fitting, accrochage et lasagna

**Justification.** Les trois gagnants ont balayé des spires entières ([AUTEUR](https://github.com/Nieuwlaar/pherc343-first-letters), [ORG](https://scrollprize.substack.com/p/writing-seen-in-pherc-306b-for-the), [ORG](https://scrollprize.substack.com/p/first-letters-emerge-from-pherc-211)), et nos 9,2 cm² ne couvrent qu'environ deux boîtes de prix. Les prédictions de surface (modèle `20260413222639`) et les normales lasagna de PHerc0800 sont déjà publiques ([ORG](https://scrollprize.org/data_browser/PHerc0800)). Le spiral fitter consomme exactement ces entrées ([ORG](https://scrollprize.org/tutorial_spiral)).

**Gain attendu :** **le plus élevé à moyen terme.** Les lettres de 343 et de 306B ont été trouvées en triant de nombreuses spires.

**Coût :** élevé. Le fitter exige un GPU NVIDIA, Python ≥ 3.14 et torch < 2.13 ; le tutoriel recommande de commencer par une plage de ~1 000 tranches en z. Le GTX 1650 est probablement insuffisant, il faut viser le T4 (sessions limitées). Il faut aussi estimer l'umbilic.

**Premier test peu coûteux :** faire passer le fitter sur une tranche z de 1 000 autour du segment le plus réactif. Rendre 2–3 spires avec `vc_render_tifxyz`, faire un tri rapide avec Argus v3, puis vérifier en coupe dans VC3D que chaque spire reste sur une feuille.

**Risques :** sauts de feuille et zones compressées, que les organisateurs listent comme goulots d'étranglement ([ORG](https://scrollprize.org/2026_open_problems)). Une segmentation de PHerc0800 publiée pour un prix de progrès devra rester dissociée de toute image d'encre.

### 4. Contrôle qualité géométrique des segments existants

**Justification.** Nos réponses fortes coïncident avec une couture, des bords et des zones abîmées [NOS ESSAIS]. Des surfaces « hors feuille » ou partiellement vides miment l'absence d'encre ([TIERS](https://github.com/TAUIL-Abd-Elilah/pherc1447-ink-survey)). L'encre réelle tolère ±2 voxels de décalage, mais perd jusqu'à 0,22 d'AUC à +8 voxels vers l'extérieur ([TIERS](https://github.com/LynnHenry/offset-sweep)). Les fenêtres −2/0/+2 d'Argus apportent environ +1 point d'AUC ([AUTEUR](https://huggingface.co/ruiconte/argus-v3)).

**Gain attendu :** moyen. On évite de chasser des artefacts, et on récupère des zones où le maillage est décalé.

**Coût :** faible (CPU et VC3D).

**Premier test peu coûteux :** carte de couverture (fraction de CT non nul par tuile). Superposer la grille de tuiles d'inférence et la couture pour savoir si celle-ci vient du maillage, du rendu ou du fondu `hann`. Faire un balayage −4…+4 sur une zone candidate.

**Risques :** l'accrochage à la feuille la plus brillante a **dégradé** l'AUC dans 10 cas sur 10 ([TIERS](https://github.com/LynnHenry/offset-sweep)). Il faut donc vérifier en coupe et ne pas « snapper » aveuglément.

### 5. Distillation adaptée au 116 keV : 0009B 2,4 µm + labels humains 1447 vers un fine-tune Reader/Argus

**Justification.** Aranke qualifie la distillation de « *single biggest driver* » ([ORG](https://scrollprize.substack.com/p/first-letters-emerge-from-pherc-211)). PHerc0009B dispose de 18 prédictions d'encre sur ses scans 2,401 µm et d'un volume 8,64 µm de la même session que 0800 ([ORG](https://scrollprize.org/data_browser/PHerc0009B)). Il est dans le top 3 DINO pour les 23 rouleaux non lus. Les labels humains 1447 sont publiés (`YoussefMoNader/ink-8um-pherc1447-surfaces`) et ont servi à A-hn. La recette de 306B (50 % humain / 50 % machine, 600 pas, LR 2e-5, pondération des négatifs durs) est documentée ([AUTEUR](https://github.com/SirProdigle/pherc0306b-first-letters/blob/main/docs/METHOD.md)).

**Gain attendu :** élevé si les stratégies 1 et 2 montrent des traces faibles ; c'est le chemin de 1447 (« quelques traits sans fine-tuning, une dizaine de lettres avec »).

**Coût :** élevé. Il faut des recalages 2,4 → 8,64 µm (ou partir des données Studio déjà distillées sur HF `paranke/vesuvius-814-841-9b-studio-training-data`), puis un fine-tune d'un modèle de 34,6 M paramètres sur T4, à quelques heures par run **[INFÉRENCE]**. Ré-entraîner Studio est hors de portée : il exige 80–96 Go de VRAM.

**Premier test peu coûteux :** 600 pas de fine-tune d'Argus v3 sur les seuls labels 1447. Évaluer sur un segment 0009B tenu à l'écart et sur w035 (sens direct et inverse) avant de toucher à 0800.

**Risques :** deux fine-tunes d'ink_9um sur des labels 116 keV se sont effondrés au hasard, avec une balanced accuracy de 0,500 ([AUTEUR](https://github.com/Ritwik-Gaur/vesuvius-energy-transfer)). Il y a aussi le bug du niveau 2 de 0009B, et la licence CC BY-NC des labels Studio.

### 6. Auto-apprentissage sur PHerc0800 avec zones exclues

**Justification.** Sur PHerc. 1667, 3 colonnes et 5 itérations ont suffi, avec une saturation vers l'itération 5. Les garde-fous étaient un champ récepteur plus petit qu'une lettre, un lissage fort des labels, aucune OCR ni modèle de langue, et une région de validation jamais labellisée ([ORG](https://arxiv.org/html/2606.29085v1)). Les organisateurs préviennent que la boucle « n'est pas garantie de fonctionner partout » ([ORG](https://scrollprize.org/2026_open_problems)).

**Gain attendu :** élevé, **mais seulement s'il existe déjà un signal graine reproductible**. Sur un bruit, la boucle amplifie la confirmation.

**Coût :** moyen. Il faut annoter à la main dans GIMP/Krita uniquement les traits répétables et le fond sûr, puis faire des fine-tunes courts sur T4.

**Premier test peu coûteux :** fixer *avant* d'entraîner une zone revendiquée, une exclusion 3D de ≥ 2 mm et une région témoin vierge. Faire une itération, et vérifier que la région de validation progresse sans avoir été vue.

**Risques :** violation de la règle de non-chevauchement et paréidolie. L'annotation humaine doit rester conservatrice.

### 7. Inspection manuelle ciblée dans le CT et VC3D

**Justification.** La texture craquelée est un signal d'encre reconnu ([ORG](https://scrollprize.substack.com/p/from-ct-scan-to-ancient-text-a-first)), et c'est une structure « bien formée » repérée à l'œil qui a lancé la découverte sur 343 ([ORG](https://scrollprize.substack.com/p/50k-first-letters-prize-awarded-for)). À 116 keV, en revanche, aucune encre visible directement n'a été rapportée, et l'épisode du « phi » montre le risque.

**Gain attendu :** faible seul. Utile pour **prioriser** les zones à passer aux stratégies 1–2, et pour la segmentation manuelle dans VC3D.

**Coût :** du temps humain uniquement.

**Premier test peu coûteux :** sur chaque candidat, vérifier la persistance sur ±2 couches et l'alignement avec les fibres.

**Risques :** paréidolie, et fibres ou vides pris pour des lettres.

### 8. Contrôle de similarité DINO 0800 contre les rouleaux sources

**Justification.** Aranke a choisi ses rouleaux d'entraînement par distance cosinus DINO ([ORG](https://scrollprize.substack.com/p/first-letters-emerge-from-pherc-211)). Les modèles `dinovol_*` sont publics ([ORG](https://huggingface.co/collections/scrollprize/dinovol)), mais sans documentation.

**Gain attendu :** faible et indirect. Il confirmerait que 0009B/306B sont les bons donneurs.

**Coût :** moyen (modèles non documentés).

**Premier test peu coûteux :** ne le faire que si la stratégie 5 est lancée.

**Risques :** temps perdu à faire fonctionner des modèles sans carte.

### 9. Valoriser le travail en prix de progrès sans rien révéler

**Justification.** Un prix de 1 000 $ a récompensé un workflow First Letters complet sur PHerc0826 sans aucune lettre ([ORG](https://scrollprize.org/winners)). Le prochain bilan mensuel tombe le **30 novembre 2026** ([ORG](https://scrollprize.org/prizes)). Notre wrapper fp32 pour GPU Turing, notre benchmark de contrôles et notre segmentation sont des candidats éligibles.

**Gain attendu :** 250–1 000 $ plausibles **[INFÉRENCE]**.

**Coût :** faible.

**Risques :** ne publier **aucune** carte d'encre de PHerc0800 montrant des formes de lettres.

## Règles et licences qui contraignent le plan

**[ORG] Éligibilité et seuil.** PHerc0800 (volume `20250521135224`) figure parmi les 19 volumes éligibles. Le prix vaut **50 000 $ par rouleau**, et 7 restent ouverts jusqu'au **25 juin 2027, 23 h 59 heure du Pacifique**. Le premier qui atteint « *at least 10 visible and legible letters within a single 4 cm² area* », jugé par les équipes technique et de papyrologie, l'emporte. Un rouleau est retiré dès que des lettres y sont trouvées ([ORG](https://scrollprize.org/prizes)). Le post sur 211 annonce d'autres annonces « dans les jours et semaines à venir » ([ORG](https://scrollprize.substack.com/p/first-letters-emerge-from-pherc-211)), et la vitesse compte donc.

**[ORG] Pièces à fournir** (formulaire https://forms.gle/TM5ao8GwC2mDrdLk9) :
- maillage(s) tifxyz avec aplatissement ;
- **une image statique générée par programme** depuis le CT et le maillage, sans annotation manuelle de caractères, portant le même nom que le maillage ;
- barre d'échelle de 1 cm et dimensions en pixels et en mm de quelques lettres ;
- annotations de lignes qui ne masquent pas le texte ;
- méthode : image Docker, ou instructions et vidéo si un humain intervient dans la boucle ;
- mesures contre les faux positifs et validation sur données tenues à l'écart ;
- et surtout « *Do not include overlap between training and prediction regions* » ([ORG](https://scrollprize.org/prizes)).

**[ORG] Confidentialité.** Ne rendre publique **aucune découverte** (mots, passages) avant l'annonce officielle. L'accord sur les données interdit de publier toute révélation de texte caché, ou le code associé, sans accord écrit ([ORG](https://scrollprize.org/faq)). Rien n'oblige à ouvrir le code au moment de la soumission. En cas de victoire, il faut publier le code sous licence permissive (MIT) et les jeux d'entraînement sous CC BY-NC 4.0 ([ORG](https://scrollprize.org/prizes)).

**Licences.** Les données de PHerc0800 sont sous **CC BY-NC 4.0** ([ORG](https://scrollprize.org/data_browser/PHerc0800)). Les poids de Studio sont sous CC BY-NC 4.0, ses données d'entraînement aussi, et TRACE v3B est sous CC BY-NC-SA. Reader v3, Argus v3, ink_9um, Hecate et v8-in sont sous MIT ([AUTEUR](https://github.com/priyankaranke/vesuvius-studio-multiscroll-cpt), [AUTEUR](https://huggingface.co/ruiconte/argus-v3)). L'utilisation de ressources publiques est autorisée « si leur propre licence le permet », règle énoncée pour le Grand Prix ([ORG](https://scrollprize.org/prizes)). **[INFÉRENCE]** Une soumission à un prix est un usage non commercial, compatible avec BY-NC. Il faut créditer chaque auteur, et publier sous CC BY-NC 4.0 (BY-NC-SA si TRACE intervient dans un dérivé) tout poids fine-tuné. Le prix revient au chef d'équipe, et aucune règle ne prévoit de part pour les auteurs des modèles utilisés.

## Plan recommandé pour les 1 à 2 semaines à venir

**Jours 1–3 (local).** Terminer Studio, Reader v3 et Argus v3 dans les deux sens. Pour Argus, utiliser les fenêtres −2/0/+2 sur les 6 segments. Masquer bords, couture et tuiles à moins de 80 % de couverture CT. Produire pour chaque segment quatre cartes : Studio, Argus, leur minimum z-scoré, et le même minimum en sens inverse. Inspecter visuellement ces cartes à la recherche de **lignes parallèles aux fibres**. Diagnostiquer en parallèle l'origine de la couture horizontale (maillage, rendu ou fondu).

**Jours 3–5 (T4).** Installer ink-sdk et lancer A-hn × TRACE v3B, puis v8-in seul, d'abord sur w035 (contrôle), puis sur les 6 segments. Calculer la corrélation inter-familles par segment, sens direct contre sens inverse. Une médiane nettement au-dessus de 0,12, qui s'effondre en sens inverse, désignerait un segment prioritaire **[INFÉRENCE]**. Avant le 30 novembre, déposer au prix de progrès le wrapper fp32 et le tableau des contrôles, sans image d'encre de 0800.

**Jours 5–14.** Lancer le spiral fitter sur T4 avec une plage z de 1 000 tranches autour de la meilleure zone, puis rendre et trier les spires avec Argus v3 (le modèle rapide). Ne passer que les zones « vivantes » à Studio et à A-hn × TRACE. Si des traits faibles mais reproductibles apparaissent, pré-enregistrer zone revendiquée, exclusion de 2 mm et témoin vierge, puis lancer un fine-tune court sur les labels 1447 (stratégie 5) avant d'envisager l'auto-apprentissage. Si rien n'apparaît sur ~50 cm² balayés, notre recommandation est d'investir dans la distillation depuis 0009B plutôt que dans davantage d'inférence, car le facteur limitant sera alors le modèle et non la surface.

## Conclusion

Le principal enseignement est que **notre résultat négatif concerne ink_9um, pas PHerc0800**. Tous les succès documentés au régime 8,64 µm / 116 keV ont mobilisé des données prises dans ce régime : l'ensemble de 343, les labels 1447 pour 306B, la distillation incluant 0009B pour 211. PHerc0800 a l'avantage de partager la reconstruction ESRF de 0009B et de 306B. Les modèles qui ont vu ce volume (Studio, Reader v3, Argus) et le seul modèle entraîné sur des labels humains à 116 keV (A-hn) n'ont pas encore été jugés ensemble sur ce rouleau. Les audits communautaires de PHerc0800 publiés à ce jour se limitent à ink_9um et Hecate.

Le second enseignement contredit un réflexe courant : **la surface compte autant que le modèle**. Deux équipes indépendantes ont échoué à trouver un critère automatique qui sépare lettres et vierge sur ce rouleau. Seule la confrontation visuelle de modèles d'architectures différentes, en sens direct et inverse, sur des spires entières, a produit des lectures acceptées. Avec un GPU de 4 Go, la meilleure allocation est donc d'utiliser le local pour le tri rapide et les contrôles, de réserver le T4 au spiral fitting et à v8-in/A-hn, et de ne lancer d'entraînement qu'une fois qu'un signal reproductible justifie le risque de paréidolie.

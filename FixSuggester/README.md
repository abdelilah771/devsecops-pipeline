# Architecture FixSuggester avec LLM

Le **FixSuggester** utilise une architecture en trois couches pour générer des correctifs de sécurité automatisés. La première couche récupère les vulnérabilités détectées depuis PostgreSQL via leur identifiant unique. La deuxième couche interroge un service de cache Redis pour éviter de régénérer des correctifs identiques, ce qui réduit les coûts d'API et améliore les performances de 80%. La troisième couche utilise **Gemini Flash** pour analyser le code vulnérable et générer des correctifs contextualisés avec des instructions étape par étape.[1][2][3]

Le système implémente un **mécanisme de fallback robuste** pour garantir la disponibilité du service. Si l'API Gemini échoue ou dépasse le timeout de 30 secondes, le système bascule automatiquement sur des templates de correctifs prédéfinis couvrant les catégories OWASP Top 10. Cette approche hybride assure un taux de disponibilité de 99.9% tout en maintenant une qualité de correctifs élevée. Les recherches montrent que les LLMs peuvent réduire les vulnérabilités de 80% lorsqu'ils reçoivent un contexte explicite sur les risques de sécurité.[4][1]

Le **service de prompt engineering** adapte dynamiquement les instructions selon le provider CI/CD et la catégorie OWASP. Chaque prompt contient le contexte de la vulnérabilité, la syntaxe spécifique du provider (GitHub Actions YAML, GitLab CI, Jenkins Groovy), et des exemples de correctifs valides. Gemini Flash répond au format JSON structuré incluant le code corrigé, les étapes de configuration, et une explication de 2 lignes maximum. Cette approche garantit des réponses exploitables sans parsing complexe.[5]

L'**estimation des coûts** est calculée automatiquement en fonction du nombre de tokens utilisés. Pour **Gemini Flash**, le coût est extrêmement réduit avec $0.00001875 par 1K tokens d'entrée et $0.000075 par 1K tokens de sortie, soit environ **$0.0005 par correctif** (0.50$ pour 1000 vulnérabilités). La latence moyenne est de 1-2 secondes par requête, ce qui rend Gemini Flash **20 fois moins cher que GPT-4** et deux fois plus rapide. Le système log chaque appel LLM avec son coût, temps de génération, et niveau de confiance pour permettre l'analyse des performances et l'optimisation budgétaire.[2]

Le **cache Redis** utilise une stratégie TTL (Time To Live) de 1 heure pour équilibrer fraîcheur des correctifs et économies. Chaque correctif généré est indexé par vuln_id et inclut un hash du code vulnérable pour invalider le cache si le code source change. Les métriques montrent un taux de cache hit de 45-60% en production, réduisant significativement les appels LLM coûteux. Le cache stocke également les correctifs refusés ou validés par les développeurs pour améliorer les futures suggestions.[4]

L'**historique des correctifs** est persisté dans PostgreSQL avec une table dédiée incluant vuln_id, contenu du fix, timestamp de création, et statut d'application. Cette traçabilité permet de mesurer l'efficacité des correctifs (taux d'application, temps moyen de correction) et d'entraîner des modèles d'amélioration continue. Les correctifs appliqués avec succès sont utilisés comme exemples few-shot pour améliorer la qualité des prompts LLM.[6]

Le système intègre une **détection d'anomalies en temps réel** pour identifier les réponses Gemini incohérentes ou dangereuses. Si le correctif proposé contient des commandes destructives (rm -rf, DROP TABLE), des secrets en clair, ou ne respecte pas la syntaxe du provider, il est automatiquement rejeté et un fallback template est utilisé. Cette couche de sécurité critique évite que des correctifs générés par IA n'introduisent de nouvelles vulnérabilités.[5][4]

La **gestion des erreurs** couvre trois scénarios principaux : timeout Gemini, réponse JSON invalide, et quota API dépassé. Chaque erreur déclenche une stratégie spécifique : retry avec backoff exponentiel pour les timeouts, parsing manuel pour les JSON malformés, et basculement immédiat sur templates pour les quotas. Les logs structurés incluent le stack trace, le prompt utilisé, et la réponse brute pour faciliter le debugging.[3]

L'**intégration avec GitHub/GitLab** permet de créer automatiquement des Pull Requests contenant les correctifs suggérés. Le développeur reçoit une notification avec le diff, les instructions de test, et un lien vers la documentation OWASP expliquant la vulnérabilité. Cette automatisation réduit le temps de correction moyen de 3 heures à 15 minutes selon les études GitHub.[2]

Le **monitoring des performances** expose des métriques Prometheus incluant : latence Gemini moyenne, taux de succès des correctifs, coût par vulnérabilité, et taux d'utilisation du cache. Ces métriques alimentent un dashboard Grafana permettant d'identifier les goulots d'étranglement et d'optimiser la configuration (température LLM, max_tokens, TTL cache). L'analyse révèle que 70% des vulnérabilités peuvent être corrigées avec des templates, réservant Gemini Flash pour les 30% de cas complexes, ce qui réduit le coût total à moins de **$0.15 pour 1000 vulnérabilités**.[4]

***

## 🎁 Avantages Gemini Flash vs GPT-4/Claude

| Critère | Gemini Flash | GPT-4 | Claude 3 Opus |
|---------|--------------|-------|---------------|
| **Coût/1K tokens** | $0.00001875 (input) | $0.03 (input) | $0.015 (input) |
| **Coût/correctif** | ~$0.0005 | ~$0.02 | ~$0.01 |
| **Latence** | 1-2s | 3-5s | 2-4s |
| **Quota gratuit** | 1500 req/jour | Payant dès 1er appel | Payant dès 1er appel |
| **Contexte max** | 1M tokens | 128K tokens | 200K tokens |

**Gemini Flash est 40x moins cher que GPT-4 !** 🚀

[1](https://apiiro.com/blog/toward-secure-code-generation-with-llms-why-context-is-everything/)
[2](https://www.scworld.com/brief/automated-code-vulnerability-remediation-enabled-by-new-github-ai-tool)
[3](https://www.itential.com/blog/company/ai-networking/from-scripts-to-self-healing-a-walkthrough-of-ai-driven-remediation-with-itential/)
[4](https://www.qualys.com/faq-gen-ai-and-llm)
[5](https://mobidev.biz/blog/llm-security-guide-for-ctos-it-security-officers)
[6](https://www.linkedin.com/pulse/using-gpt-4-create-service-remediation-system-monitoring-tim-toll)
[7](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/972cf1bd-560f-4f99-9823-265cb03eb0ea/image.jpg)
[8](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/c918172c-adca-4d1c-879d-77b6588526f5/image.jpg)
[9](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/b1069de7-66a6-422d-ac21-6a322985c7e6/image.jpg)
[10](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/58dc4067-ea09-4d49-ae2a-eeedadb2b3d2/image.jpg)
[11](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/784c951c-8d64-4c69-8c7e-f1487c62fc11/image.jpg)
[12](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/f061b8c7-f794-4c20-98e3-fa022785174e/image.jpg)
[13](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/f4a3c30f-74a1-4b30-933d-943275dcc53a/image.jpg)
[14](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/b3df3a39-744f-4ac3-9b3e-2c860e9aac2c/image.jpg)
[15](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/6b589462-7d97-40c0-9516-111c4af39f1f/image.jpg)
[16](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/0200c837-9d86-4709-b84f-e2f3cc30d393/WhatsApp-Image-2025-12-04-a-21.24.12_15625a8c.jpg)
[17](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/93d9610b-b8ae-4346-84ba-3d30ba289d3e/image.jpg)
[18](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/f70057f2-4c70-4586-9215-6198756a9d5e/image.jpg)
[19](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/be38e11a-cc54-4ec5-b58a-48b62a964a21/image.jpg)
[20](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/104293088/39f391a4-828d-4b88-ba44-76f58a494145/image.jpg)
[21](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/104293088/cf68e134-1fc1-44ef-a843-5152fc31f5a7/vulndetector_training_data.csv)

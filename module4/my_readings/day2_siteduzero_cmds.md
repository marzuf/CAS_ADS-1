##############################
### configuration générale
##############################

# activer la couleur dans git (aide la visibilité des messages dans la console)
git config --global color.diff auto
git config --global color.status auto
git config --global color.branch auto


# configuration globale
git config --global user.name "marzuf"
git config --global user.email 'zuffereymarie0@gmail.com'

# éditer le fichier de configuration
vim ~/.gitconfig

##############################
### créer un nouveau projet
##############################
mkdir plusoumoins
cd plusoumoins
# initialiser dépôt git
git init

##############################
### clôner un dépôt existant (récupérer tous les fichiers et leur historique)
##############################
git clone <...>.git

# le dossier .git créé contient l'historique des modifications des fichiers et la configuration git pour ce projet
# au final la racine du dossier d'un projet contient la dernière version des fichiers du projet + le dossier .git où sont stockés l'historique et les fichiers de configuration

##############################
### mettre en place un serveur
##############################
# utiliser l'option --bare dans git clone ou git init
# -> ne créer qu'un fichier .git (sans les fichiers source, puisque ceux-ci ne sont pas modifiés sur le serveur)

##############################
### divers
##############################

# pour indiquer les fichiers récemment modifiés:
git status 

# cycle "normal" de travail: modifier le code source -> tester les modifications -> valider les modifications avec un commit -> modifier le code source -> ...

# les commits sont là pour valider l'avancement d'un projet

# pour voir ce qui a changé dans un fichier depuis le dernier commit:
git diff
# -> les lignes ajoutées sont précédées d'un "+"; celles supprimées précédées d'un "-"
# affiche les modifications de tous les fichiers
# pour voir les modifications d'un fichier en particulier:
git diff <nom_du_fichier>

##############################
### effectuer un commit
##############################
# il faut explicitement préciser les fichiers à "commiter"; 3 façons de le faire

# 1) ajouter les fichiers à commiter puis commiter
git add <nom_du_fichier1> <nom_du_fichier2>
git commit
# -> est indispensable pour commiter des fichiers nouvellement créés
# 2) commiter tous les fichiers listés dans git status
git commit -a 
# -> utile pour commiter tous les fichiers d'un coup
# 3) indiquer lors du commit les fichiers à commiter
git commit nom_du_fichier1 nom_du_fichier2
# -> utile pour commiter spécifiquement certains fichiers

# après git commit -> l'éditeur s'ouvre et il faut saisir dans l'éditeur un message de commit
# le commit est local; l'envoi sur le serveur se fait séparément



##############################
### les logs
##############################
# => ce sont l'historique des commits
# lorsqu'un commit a été effectué, se voit dans
git log
# chaque commit est numéroté avec un long chiffre hexadécimal permettant de l'identifier

# pour voir le détail des lignes ajoutées/retirées à chaque commit:
git log -p

# pour un résumé plus court des commits
git log --stat

##############################
### corriger une erreur
##############################

# pour modifier le dernier message de commit (par ex. à cause d'une faut d'orthographe)
git commit --amend
# l'éditeur s'ouvre et le message peut être modifié
# ! ne peut pas être modifié si le commit a été transmis à d'autres personnes 

# pour annuer le dernier commit (soft)
git reset HEAD^
# -> annule le dernier commit et revient à l'avant-dernier
# -> seul le commit est retiré de git; les fichiers restent modifiés !
# pour indiquer à quel commit revenir:
# - HEAD: dernier commit
# - HEAD^: avant-dernier commit
# - HEAD^^ ou HEAD~2: avant-avant-dernier commit
# - <long chiffre hexadécimal>: pour indiquer un commit précis auquel revenir
# - <premiers chiffres/lettres d'un long chiffre hexadécimal>: les premiers caractères suffisent tant qu'aucun autre commit ne commence par les mêmes caractères

# pour annuler le dernier commit (hard)
# -> annule le commit !et! les changements dans les fichiers:
git reset --hard HEAD^
# -> annule le commit ET perd tous les changements !

# pour annuler les modifications d'un fichier avant un commit
# (si plusieurs fichiers ont été modifiés mais que le commit n'a pas encore été envoyé,
# pour restaurer un fichier tel qu'il était au dernier commit):
git checkout <nomfichier>
# -> le fichier revient le même tel qu'il était lors du dernier commit

# annuler/supprimer un fichier avant un commit
# (par ex. un fichier ajouter avec git add, mais qu'on se rend compte qu'il ne faut pas le commiter,
# donc pour annuler le git add):
# git reset HEAD -- <nom_du_fichier_a_supprimer>
# -> retire le fichier qui avait été ajouté pour être commité


##############################
### télécharger les nouveautés depuis le serveur
##############################

# télécharger les modifications effectuées par d'autres personnes
git pull
# 2 cas de figure:
# 1) si aucune modification n'a été effectuée en local depuis le dernier pull, la mise à jour est simple (fast-forward)
# 2) si on a fait des commits en même temps, les changements sont fusionnés aux nôtres automatiquement
# si la même zone de code a été modifiée en même temps, git indique qu'il y a un conflit; git indique les noms des fichiers;
# il faut rechercher les lignes contenant les symboles "<<<<<<<<<<<<<<<<" qui délimitent nos changements et ceux des autres personnes
# et garder uniquement les changements nécessaires; puis faire un commit pour enregistrer tout cela.


##############################
### envoyer les nouveautés au serveur
##############################

# recommandé de consulter le log local afin de vérifier ce qu'on s'apprête à envoyer
git log -p
# pour passer à l'envoi
git push
# le changement vers le serveur doit être de type fast-forward car le serveur ne peut pas gérer les conflits
# -> personne ne doit avoir fait un push avant nous depuis notre dernier pull (le mieux est de s'assurer d'être à jour
# en faisant un pull avant le push)

# il est recommandé de faire des commits régulièrement mais pas des push (pas plus d'1x/jour en général)
# éviter de faire des push après chaque commit: on perd la facilité à annuler/modifier un commit

# ! un push est irréversible ! 


##############################
### annuler un commit publié
##############################

# un commit erroné envoyé sur le serveur peut être annulé en créant un nouveau commit qui effectue l'inverse
# des modifications (un commit envoyé ne peut pas être supprimé, on ne peut que créer des nouveaux !)
# les lignes ajoutées seront supprimées et inversément

git revert <chiffre_hexa>
# -> va annuler le commit avec l'ID <chiffre_hexa> (les premiers caractères suffisent) en créant un commit inverse
# ouvre un éditeur pour saisir un message de commit; le commit d'annulation est ainsi créé et peut être publié avec git push

##############################
### les branches
##############################

# moyens de travailler en parallèle sur d'autres fonctionnalités
# (par ex. tester une copie du code source avec les idées plus folles et vérifier si cela fonctionne avant
# de les intégrer au véritable code source)

# dans git, toutes les modifications faites au fil du temps par défaut considérées comme appartenant à la 
# branche principale appelée "master"

# si on veut tester quelque chose de spécial qu'on est pas sûr que cela va marcher et qu'on ne veut pas que 
# le projet intègre ces changements dans l'immédiat -> créer une branche pour y travailler en parallèle

# on peut faire des commits sur cette branche en particulier, cela n'empêche pas de continuer à travailler
# et faire des commits sur la branche master

# si l'idée s'avère concluante à la fin, on peut fusionner tous les commits de la branche créée à la branche principale

# git est unique dans sa capacité à gérer les branches (sans copies de fichiers); crée une branche virtuelle dans laquelle
# il retient tous les changements en parallèle; au moment de fusionner avec la branche master, vérifie que les modifications
# n'entrent pas en conflits avec les commits effectués en parallèle

# gestion facilitée des branches par git encourage à créer des branches pour toutes les modifications qui pourraient prendre 
# du temps avant d'être terminées

# des sous-branches peuvent être créées à partir d'une branche

# si les changements testés ne s'avèrent pas concluants par exemple, une (sous-)branche peut être supprimée sans qu'aucun commit
# intermédiaire ne soit finalement incorporé à la branche principale

# pour voir toutes les branches:
git branch
# l'étoile indique sur quelle branche on se trouve actuellement

# question à se poser pour savoir si créer une branche: ma modification sera-t-elle rapide ? simple ? en combien de commits ? 
# -> créer une branche pour chaque modification qui risque d'être un peu longue
# (au pire, on crée une branche "pour pas grand-chose"


##############################
### créer et se déplacer sur une branche 
##############################

# créer une nouvelle branche ma_nouvelle_branche
git branch ma_nouvelle_branche
# (pour le moment la branche est locale, non publiée)

# pour voir la branche
git branch
# pour le moment, on est toujours sur la branche master

# pour aller sur la nouvelle branche:
git checkout ma_nouvelle_branche

# ! checkout a donc un double usage: i) pour restaurer un fichier tel qu'il était lors du dernier commit; ii) pour changer de branche

# lors d'un changement de branche, on ne change pas de dossier sur le disque dur, mais git change les fichiers pour qu'ils reflètent 
# l'état de la branche dans laquelle on se rend (les branches de git sont comme des dossiers virtuels)
# (on reste dans le même dossier, mais git modifie les fichiers qui ont changé entre la branche où l'on était et celle où on se rend)
# ainsi, si on fait un git log sur la branche ma_nouvelle_branche, les commits faits sur la branche master n'apparaissent pas

# pour revenir sur la branche master
git checkout master

##############################
### fusion d'une autre branche avec la branche principale 
##############################

# à la fin, on voudra sûrement fusionner une branche sur laquelle on a travaillé avec la master
# avec git, on peut fusionner n'importe quelle branche avec n'importe quelle autre branche
# (le plus courant reste de fusionner une branche de test dans une branche master)
# se rendre dans la branche maste, puis intégrer le travail fait dans l'autre branche
git checkout master
git merge ma_nouvelle_branche
# (tous les commits faits dans ma_nouvelle_branche se retrouve maintenant dans la branche master)
# (on a pu travailler en parallèle, et maintenant seulement le travail s'applique sur la branche master)

##############################
### suppression d'une branche 
##############################

# la branche ne servant plus à rien, on peut la supprimer
git branch -d ma_nouvelle_branche
# git vérifie que le travail dans ma_nouvelle_branche a bien été fusionné dans master; sinon il avertit et interdit la suppression

# pour supprimer une branche même si elle contient des changements non fusionnés
# ! attention: tout le travail sera perdu
git branch -D ma_nouvelle_branche


##############################
### commit et changement de branche (mettre de côté une branche)
##############################

# avant de pouvoir changer de branche, il faut effectuer un commit de tous les changements
# (i.e. un git status doit afficher qu'aucun fichier est en cours de modification)
# si on a des changements non commités et qu'on change de branche, les fichiers modifiés restent
# comme ils étaient dans la nouvelle branche
# pour éviter d'avoir à faire un commit au milieu d'un travail en cours:
git stash
# -> les fichiers modifiés sont sauvegardés et mis de côté
# git status n'affiche plus aucun fichier (le working directory est propre)
# on peut alors changer de branche, faire des modifications, commiter, et revenir sur la branche
git stash
git checkout master
[modifier des fichiers]
git commit -a
git checkout mabranche
# pour récupérer les changements mis de côté
git stash apply
# (les fichiers sont restaurés et retrouvent l'état dans lequel ils étaient avant git stash)

##############################
### branches partagées
##############################

# il est possible de travailler à plusieurs sur une branche (comme pour master)
# pour lister toutes les branches que le serveur connait:
git branch -r
# origin/HEAD
# origin/master

# origin = nom du serveur depuis lequel le dépôt a été cloné
# (en théorie on peut suivre directement les branches de plusieurs personnes ; git étant un peu comme le peer-to-peer;
# mais on travaille plutôt avec des serveurs pour suivre les changements)
# HEAD est un peu particulier
# master indique la branche principale

# si le serveur possède une autre branche, e.g. origin/une_branche et qu'on veut travailler dessus,
# il faut créer une copie de la branche sur notre ordinateur pour suivre (tracker) les changements 
# sur le serveur
git branch --track <branchelocale> origin/<brancheserveur>
# e.g.
git branch --track une_branche origin/une_branche

# lorsqu'on fera un pull depuis la branche une_branche, les changements seront fusionnés dans la branche une_branche locale
# ! important de savoir depuis où on fait un pull !
# un pull depuis la branche master met à jour notre branche master locale en fonction de ce qui a changé sur le serveur,
# il en va de même pour n'importe quelle autre branche

# pour ajouter une branche sur le serveur pour y travailler à plusieurs:
git push origin origin:refs/heads/nom_nouvelle_branche
# on peut ensuite créer une branche locale qui suit la branche serveur comme vu précédemment avec git branch --track

# l'inverse est également possible: on peut créer une branche locale puis la copier sur le serveur
# pour ce faire:
# - créer la branche sur le serveur avec git push ...
# - et modifier le fichier git/config comme ceci:
#     -> copier le bloc [branch "master"];
#     -> remplacer les occurences de master par le nom de la branche
#     -> enregistrer les modifications
# - faire git pull et git push

# pour supprimer une branche sur le serveur:
git push origin :heads/nom_branche_a_supprimer

# les "remote tracking branches" (celles qui apparaissent lorsqu'on fait git branch -r) ne seront pas 
# automatiquement supprimés chez les autres clients; il faut les supprimer manuellement avec la commande
git branch -r -d origin/nom_branche_a_supprimer 

##############################
### tagger une version
##############################

# donner un alias à un commit précis pour le référencer sous ce nom
git tag NOMTAG IDCOMMIT 
# e.g.
git tag v1.3 34j332209e
# (permet à d'autres personnes de récupérer une version plus facilement)

# un tag n'est pas envoyé lors d'un push, il faut préciser l'option -tags:
git push -tags
# ainsi tout le monde peut se référencer à ce commit par le nom de tag plutôt que le numéro id

# pour supprimer un tag créé:
git tag -d NOMTAG

##############################
### recherche dans fichiers source
##############################

# git connait tous les fichiers source d'un projet; il est facile de faire une recherche à l'intérieur
# e.g. trouver tous les noms de fichiers qui contiennent le mot "TODO" dedans:
git grep "TODO"
# (possible d'utiliser les expressions régulières)

# pour connaitre les numéros de ligne qui contiennent le mot recherché
git grep -n "TODO"


##############################
### demander à git d'ignorer des fichiers (.gitignore)
##############################

# pour ignorer un fichier: créer un fichier .gitignore à la racine et indiquer le nom du fichier
# (en entrant un nom de fichier par ligne)
# aucun de ces fichiers n'apparaitra dans git status, même s'il est modifié, et n'apparait pas dans les commits
# (utile e.g. pour les fichiers temporaires qui n'ont rien à faire dans git)
# (dans les noms de fichier on peut utiliser "*" comme joker, e.g. "*.tmp" pour ignorer tous les fichiers temporaires)


##############################
cf. le cours Pro Git
https://git-scm.com/book/en/v2


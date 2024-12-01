---

Est-ce que ce document correspond à vos attentes ? 😊



---

# 🚀 Guide d'Utilisation pour le Projet [Sixteen-Soldiers]  

Bienvenue dans le projet **Sixteen-Soldiers** ! Ce document vous expliquera toutes les étapes pour :  
- Créer un compte GitHub  
- Installer Git sur votre machine  
- Accéder à la **GitHub Classroom** et rejoindre une équipe  
- Cloner le projet  
- Travailler sur le projet et pousser vos modifications sur le dépôt  
- Découvrir quelques ressources utiles.  

---

## ✍️ 1. Créer un Compte GitHub  

Si vous n’avez pas encore de compte GitHub, suivez ces étapes :  
1. Rendez-vous sur [github.com](https://github.com).  
2. Cliquez sur **Sign up**.  
3. Remplissez les champs demandés (email, mot de passe, etc.).  
4. Vérifiez votre email et confirmez votre inscription.  

#### Astuce : 
Utilisez un mot de passe fort et facile à retenir, et activez l’authentification à deux facteurs pour sécuriser votre compte.  

---

## 🛠️ 2. Installer Git  

### a) Windows  
1. Téléchargez le programme d'installation depuis le site officiel : [git-scm.com](https://git-scm.com).  
2. Lancez l'installation en suivant les étapes par défaut.  

### b) macOS  
1. Installez Git via **Homebrew** (si installé) :  
   ```bash  
   brew install git  
   ```  
2. Sinon, téléchargez Git directement depuis [git-scm.com](https://git-scm.com).  

### c) Linux  
1. Utilisez votre gestionnaire de paquets préféré (par exemple, pour Ubuntu) :  
   ```bash  
   sudo apt update  
   sudo apt install git  
   ```  

### Vérifiez l'installation :  
Dans votre terminal, tapez :  
```bash  
git --version  
```  

---


## 👥 3. Rejoindre la GitHub Classroom  

1. Cliquez sur le lien d'invitation que vous avez reçu par email pour accéder à la **GitHub Classroom**.  
2. Connectez-vous à votre compte GitHub (ou créez-en un si ce n'est pas encore fait).  
3. Suivez les instructions pour :  
   - **Créer une équipe** si vous êtes désigné comme **capitaine**.  
   - **Rejoindre une équipe existante** si vous faites partie d'un groupe.  

### Points Importants :  

- **Pour les capitaines d'équipe :**  
    Vous êtes responsables de créer l’équipe via le lien de la GitHub Classroom. Assurez-vous que le nom que vous fournissez à votre équipe soit le même que celui fourni lors du formulaire *(au risque que votre repôt ne sois pas prise en compte)*

- **Pour les autres membres de l'équipe :**  
    Une fois l'équipe créée par le capitaine, retrouvez-la dans la liste des équipes disponibles sur la GitHub Classroom et rejoignez-la directement via le même lien.  


**Rappel :** Tous les membres doivent être assignés à une équipe via la plateforme pour que vos contributions soient bien suivies.  



---

## 💻 4. Cloner le Projet  

Une fois que vous êtes dans la GitHub Classroom et que vous avez rejoins une équipe, vous tomberez sur une fenêtre du genre : 

![alt text](/assets/images/docs/doc_github.png)

En cliquant sur le lien qui vous y est présenté (varie en fonction de chaque équipe), vous serez rediriger vers le repository github qui vous est associé. 

### Clone du repot github :
Maintenant, vous pouvez cloner le code et le récupérer en local. Pour cela : 

1. Rendez-vous sur le dépôt GitHub du projet.

2. Copiez l’URL du dépôt en cliquant sur le bouton **Code** > **HTTPS**.  

3. Ouvrez votre terminal et tapez la commande suivante pour cloner le projet sur votre machine : 

   ```bash  
   git clone [URL du dépôt]  
   ```  
   Remplacez `[URL du dépôt]` par l’URL que vous avez copiée.  

---

## 🔨 5. Travailler sur le Projet  

### a) Modifier des fichiers  
- Ajoutez ou modifiez des fichiers localement en utilisant un éditeur de texte comme VS Code, Pycharm, Spyder, etc.  

### b) Commandes utiles pour Git  
- **Vérifier l'état des modifications** :  
   ```bash  
   git status  
   ```  
- **Ajouter un fichier spécifique** :  
   ```bash  
   git add nom_du_fichier.txt  
   ```  
- **Ajouter tous les fichiers modifiés** :  
   ```bash  
   git add .  
   ```  

### c) Enregistrer vos modifications avec un commit  
Après avoir ajouté vos fichiers, enregistrez les modifications avec :  
```bash  
git commit -m "Message expliquant vos modifications"  
```  

### d) Envoyer vos modifications sur GitHub  
1. Si vous travaillez sur la branche principale :  
   ```bash  
   git push  
   ```  
2. Si vous avez créer une branche ou travaillez sur différentes branches :  
   ```bash  
   git push origin nom_de_votre_branche  
   ```  


Important :

Après avoir récupérer le code, et ajouté votre IA, vous devez suivre successivement (à chaque fois que vous voudrez pousser vos modifications) les étapes présentées par les commandes en b).

*Nous ne pourrons récupérer votre code que si vous faites un "push" de vos modifications. Toute équipe n'ayant pas pousser son code via les commandes sus-mentionnés ne verra d'office pas son code prise en compte et donc sera automatiquement recalée.*

Nous vous encourageons donc pour cela à *pousser régulièrement vos modifications* sur votre repository Github.

---

## 🌟 6. Quelques Ressources Utiles  

- **Documentation officielle GitHub** : [https://docs.github.com](https://docs.github.com)  
- **Formation interactive GitHub** : [GitHub Learning Lab](https://lab.github.com/)  
- **Comprendre le flux GitHub** : [Introduction to GitHub Flow](https://guides.github.com/introduction/flow/)  
- **Vidéos courtes sur Git/GitHub** : [GitHub YouTube Channel](https://www.youtube.com/github)  

---

Avec ce guide, vous avez tout ce qu’il faut pour participer efficacement au projet Sixteen-Soldiers. Si vous avez des questions ou des problèmes, n’hésitez pas à demander de l’aide dans le canal dédié.  

**Bon codage et amusez-vous bien !** 🎉  
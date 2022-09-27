from re import T
from sqlite3 import Date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    # return HttpResponse("Page dashboard !")
    template = loader.get_template('dashboard_accueil.html')
    return HttpResponse(template.render())

def releve(request):
    import datetime
    import requests
    from urllib.parse import urlparse
    from urllib.parse import urlunparse
    from bs4 import BeautifulSoup
    import csv 
    from cleantext import clean
    
    from dashboard.models import Threads
    from dashboard.models import Comments
    from dashboard.models import Projet
    from dashboard.models import Histo

    
    id_de_thread_a_traitee = 1678
    

    def getSoupObject(domain, url_path): # Va sur la page et renvoie son contenu
        thread_url = urlunparse(('https', domain, url_path, "", "", "")) # construct the url to access the posts for each thread
        page = requests.get(thread_url)
        soup = BeautifulSoup(page.content, "html.parser")

        return soup

    def getPostsFromPage(soup, posts_content):# Renvoi le contenu des comm (même un peu plus...)
        thread_results = soup.find_all("div", class_="lia-message-body-content") #Recup des contenu des comm du threads

        for page_posts_content in thread_results:
            body_content = page_posts_content.get_text()   
            #Entrée bdd table Comments
            entreComment = Comments(comment = body_content, threadId_id = der_id_de_thread )
            entreComment.save()
            posts_content.append(body_content)
        return posts_content

    def getNextPageUrl(soup): # Passe à la page de commentaire suivant dans un thread
        # get to next page 
        all_next_page_link_components = soup.find_all("li", class_="lia-paging-page-next")
        if len(all_next_page_link_components) < 2: # case where the thread just have one page to navigate
            return None
        
        next_page_link_component = all_next_page_link_components[1] # second child makes reference to the url we need
        
        if not next_page_link_component: #case where there is just one navigation page
            return None
        
        link = next_page_link_component.find("a")
        if not link: #case were we checked all the navigation pages
            return None
        else:
            next_page_url = link["href"] # get the url for the next page 
        return next_page_url

    def getLienPageSuivante(soup):
        lienPageSuivante = soup.find("li", class_="lia-paging-page-next")
        lienPageSuivante = lienPageSuivante.find("a")
        lienPageSuivante = lienPageSuivante["href"]

        return lienPageSuivante

    def recupInfoThreads(results,threads):
        for thread_title in results:
            first_element = thread_title.find("div") # get first children - the div
            link = first_element.find("a")
            
            title = link["title"] # get the title and save it 
            url = link["href"] # get the link towards the post of the thread 
            threads.append((title, url))
        return threads

    def donnerDate():
        dateLogs = datetime.datetime.now()
        dateLogsDay = dateLogs.strftime('%d')
        dateLogsMonth = dateLogs.strftime('%b')
        dateLogsYear = dateLogs.strftime('%Y')
        dateLogsHour = dateLogs.strftime('%H')
        dateLogsMinute = dateLogs.strftime('%M')
        dateLogsSecond = dateLogs.strftime('%S')
        dateLogsMicrosecond = dateLogs.strftime('%f')

        dateDebut = str(dateLogsDay) + "_" + str(dateLogsMonth) + "_" + str(dateLogsYear) + "_" + str(dateLogsHour) + "_" + str(dateLogsMinute) + "_" + str(dateLogsSecond) + "_" + str(dateLogsMicrosecond)
        return dateDebut


    nbRelThreads = 0


    #Création fichiers logs.txt
    dateDebut = donnerDate()
    logs = open(dateDebut + ".txt", "x")

    #Url de la page en cours de scraping
    URL = "https://community.o2.co.uk/t5/Discussions-Feedback/bd-p/4"

    logTotalPosts = 0

    # Permet threads épinglés scrappé que une fois
    threadsEpinglés = 0 

    der_id_de_thread = (Threads.objects.last()).idThread
    der_id_de_thread = der_id_de_thread + 1
    print(der_id_de_thread)

    x = 0
    derPage = 2 # Valeur 2 permet seulement d'entrer dans la boucle, modifié systematiquement à la suite
    while x < 2 : #Déterminer le nombre de pages à scrapper manuellement #ici derPage à mettre!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        x += 1

        #Aller sur la page -----------------------
        logPageTraitee = "URL de la page qui va être traitée: " + URL
        print(logPageTraitee)

        log = open(dateDebut + ".txt", "a") #Entrée dans le log
        log.write(logPageTraitee + "\n")
        #pas .close tte suite...ou si plus simple non ?

        domain = urlparse(URL).netloc
        page = requests.get(URL)

        #Récup contenu de la page-----------------
        soup = BeautifulSoup(page.content, "html.parser")
        
        li_last_page = soup.find_all("li", class_="lia-paging-page-last")[0].find("a").string
        derPage = int(li_last_page)

        #Récup contenu infos des threads (titre, date, lien,...)
        if threadsEpinglés == 0:
            threadsEpinglés +=1
            results = soup.find_all("article", class_="custom-message-tile") #correspond à touts les posts
        else:
            results = soup.find_all("article", class_="custom-message-tile custom-thread-unread") #correspond seulements aux posts non-épinglé 

        
        #results = soup.find_all("article", class_="custom-message-tile custom-thread-unread")
        
        #Récup des infos threads-------------------------
        threads = [] #Contiendra (title, url) de chaque threads

        # get all threads titles and urls
        threads = recupInfoThreads(results,threads)
        
        #icicicicicicicicicicicicicicicicicciciicciiciiiiiiiiiiiiiiiiccccccccccccccccciiiiiiiiiiiiiiii Entrée BDD Table Threads
        
        
        

        for elt in threads:
            entreeThreads = Threads(nomThread = elt[0], projetId_id = 1 ) #projetId_id ? #ajouter dynamisme id projet non fixe
            entreeThreads.save()

        #Emoji à enlever
        
        
        #Récup de la liste des articles en .txt => variable threads mit dans un .txt
        #liste_des_art = open("liste_des_articles.txt","a") #Attention pas créer seulement ouverts, ajouter create if not exist ?
        #liste_des_art.write(str(threads))
        #liste_des_art.close()

        # get all post content for each thread
        all_thread_posts = [] # Contient tout les threads (et comm?)
        for thread in threads:
            thread_posts = []
            thread_url_path = thread[1]
            soupObject = getSoupObject(domain, thread_url_path) # Va sur la page du thread  et renvoie le contenu de la page 

            thread_posts = getPostsFromPage(soupObject, thread_posts) # Renvoi le contenu des comm (même un peu plus...)

            next_page_url = getNextPageUrl(soupObject) # Passe à la page de commentaire suivant dans un thread

            #Récup de tout les comm d'un thread
            while next_page_url:
                # get all posts for given a page
                next_page_url_path = urlparse(next_page_url).path
                soupObject = getSoupObject(domain, next_page_url_path)
                thread_posts = getPostsFromPage(soupObject, thread_posts)
                next_page_url = getNextPageUrl(soupObject)
            
            id_de_thread_a_traitee += 1

            
            der_id_de_thread += 1

            logNbPosts = f'Nombre de post extrait du thread "{thread[0]}": {len(thread_posts)}' # Logs
            all_thread_posts.append((thread[0], thread_posts)) # adding tuples with the title of a thread and the array containing all the posts content of a thread, pas compris
            
            logTotalPosts += len(thread_posts)

            #logs
            sansEmoji = clean(logNbPosts, no_emoji=True) #Enleve les emoji pour eviter les erreurs
            log.write(sansEmoji + '\n')
            print(sansEmoji)
            
            #Extraction des posts vers un csv
            contenu_des_posts = open("contenu_des_posts.csv","w",encoding="utf-8")
            writer = csv.writer(contenu_des_posts)
            for elements in all_thread_posts:
                writer.writerow(elements)
            contenu_des_posts.close()

            #Extraction vers BDD
        
        logNbThreads = "Nombre de threads scrappé:" + str(len(all_thread_posts))
        nbRelThreads += len(all_thread_posts)
        print(logNbThreads)


        
        #logs
        log.write(logNbThreads + '\n')

        URL = getLienPageSuivante(soup) #Lien vers la page suivante

    dateFin = donnerDate()

    logFin = "Fin" + '\n' + 'Scrapping terminé à ' + dateFin  #Afficher le nb de thread et commentaire récoltés

    #logs
    log.write('Total posts scrappé: ' + str(logTotalPosts))
    log.write(logFin)
    print(logFin)
    #fermer logs !!
    
    dateRelev = datetime.datetime.now()
    nbRelCom = str(logTotalPosts)
    
    entreeHisto = Histo(dateRel = dateRelev, nbThreadsRel = nbRelThreads, nbCommRel = nbRelCom, projetId_id = 1, status = True )
    entreeHisto.save()
    
    # template = loader.get_template('dashboard_accueil.html')
    # return HttpResponse(template.render())
    
    
    
    
    
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard_accueil.html')

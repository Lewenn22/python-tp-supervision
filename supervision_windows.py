import os
import subprocess
from time import sleep

# taux de rafraichissement
refresh_rate = int(input("Entrez le taux de rafraichissement en secondes : "))

# limite de % de RAM utilisé 
ram_limite = int(input("Entrez le taux de RAM maximal acceptable en pourcentage : "))
# limite de % de CPU utilisé
cpu_limite = int(input("Entrez le taux de CPU maximal acceptable en pourcentage : "))

# création du répertoire 'Supervision' s'il n'existe pas
if not os.path.exists("C:/Supervision"):
    os.mkdir("C:/Supervision")
else:
    print("Le dossier Supervision existe déjà")

# on se place dans le dossier Supervision
workdir = os.chdir("C:/Supervision")

# boucle principale jusqua CTRL+C
while True:
    os.system("cls")

    # récupère les infos de la RAM et du CPU
    free_physical_memory = int(subprocess.check_output("wmic OS get FreePhysicalMemory").decode().split("\n")[1])
    total_visible_memory_size = int(subprocess.check_output("wmic OS get TotalVisibleMemorySize").decode().split("\n")[1])
    real_memory_used = total_visible_memory_size - free_physical_memory
    # convertir le résultat en % de RAM utilisé
    real_memory_used_percentage = (real_memory_used / total_visible_memory_size) * 100

    # récupère les infos du CPU
    charge_cpu = int(subprocess.check_output("wmic cpu get loadpercentage").decode().split("\n")[1])

    # affichage des infos
    print(charge_cpu, "% de CPU sont utilisés")
    print(real_memory_used_percentage, "% de RAM sont utilisés sur", total_visible_memory_size / 1024 / 1024, "Go au total")

    # écriture des infos dans le fichier Supervision.txt
    with open("Supervision.txt", "a") as file:
        file.write(str(charge_cpu) + " % de CPU sont utilisés\n")
        file.write(str(real_memory_used_percentage) + " % de RAM sont utilisés sur " + str(total_visible_memory_size / 1024 / 1024) + " Go au total\n")

    # détection du seuil de RAM utilisé défini
    if real_memory_used_percentage > ram_limite:
        print(f"la RAM est utilisée à plus de {ram_limite}%")
        with open("Supervision.txt", "a") as file:
            file.write(f"la RAM est utilisée à plus de {ram_limite}%\n")
        os.system(f"PowerShell -Command \"Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('la RAM est utilisée à plus de {ram_limite}%')\"")

    # detection du seuil de CPU utilisé défini
    if charge_cpu > cpu_limite:
        print(f"le CPU est utilisé à plus de {cpu_limite}%")
        with open("Supervision.txt", "a") as file:
            file.write(f"le CPU est utilisé à plus de {cpu_limite}%\n")
        os.system(f"PowerShell -Command \"Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('le CPU est utilisé à plus de {cpu_limite}%')\"")
   
    # rafraichissement 
    sleep(refresh_rate)
